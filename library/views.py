from django.shortcuts import render ,redirect
from .models import  Book,Member,BookInteraction
from django.apps import apps
from django.http import HttpResponse
from .forms import BookForm,MemberForm,BookInteractionForm
from django.shortcuts import get_object_or_404, redirect
from .models import DynamicCategory, DynamicData
from .forms import CategoryForm
from django import forms
from django.urls import reverse


# View for creating a new table/category
def add_table(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_tables')  # Adjust to the correct URL path
    else:
        form = CategoryForm()
    return render(request, 'add_table.html', {'form': form})

# View for adding data to a specific category
def add_data(request, category_id):
    category = get_object_or_404(DynamicCategory, id=category_id)
    fields = category.fields.split(',')  # Get the comma-separated fields
    
    # Dynamically generate the form class based on the category fields
    class DynamicDataForm(forms.Form):
        # Create form fields dynamically based on category's fields
        for field in fields:
            locals()[field.strip()] = forms.CharField(max_length=255, required=True)
        del field

    if request.method == "POST":
        form = DynamicDataForm(request.POST)
        if form.is_valid():
            # Save the data dynamically as JSON
            data = DynamicData(category=category, data=form.cleaned_data)
            data.save()
            return redirect('manage_tables')  # Adjust to the correct URL path
    else:
        form = DynamicDataForm()

    return render(request, 'add_data.html', {'form': form, 'category': category})


def manage_tables(request):
    categories = DynamicCategory.objects.all()
    return render(request, 'manage_tables.html', {'categories': categories})

# View to display data for a specific category
def view_table_data(request, category_id):
    category = DynamicCategory.objects.get(id=category_id)
    fields = category.fields.split(',')
    data_entries = DynamicData.objects.filter(category=category)

    # Prepare data entries as a list of dictionaries
    data_list = []
    for entry in data_entries:
        row = {field: entry.data.get(field) for field in fields}
        data_list.append(row)

    return render(request, 'view_table_data.html', {
        'category': category,
        'fields': fields,
        'data_entries': data_list,  # Pass the pre-processed data
    })

    
def delete_table(request, category_id):
   category = get_object_or_404(DynamicCategory, id=category_id)
   category.delete()  # Deletes the selected table
   return redirect(reverse('manage_tables'))  # Redirect back to manage tables page

# Edit Book View
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('books')
    else:
        form = BookForm(instance=book)
    return render(request, 'edit_book.html', {'form': form, 'book': book})

# Delete Book View
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.delete()
        return redirect('books')
    return render(request, 'confirm_delete.html', {'book': book})

def dashboard(request):
    books = Book.objects.all()  # Get all books from the database
    return render(request, 'dashboard.html', {'books': books})

def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books')
    else:
        form = BookForm()

    return render(request, 'add_book.html', {'form': form})

def books(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(author__icontains=query) | Book.objects.filter(isbn__icontains=query)
    else:
        books = Book.objects.all()
    return render(request, 'books.html', {'books': books})

def members(request):
    query = request.GET.get('q')
    if query:
        members = Member.objects.filter(first_name__icontains=query) | Member.objects.filter(last_name__icontains=query)
    else:
        members = Member.objects.all()
    return render(request, 'members.html', {'members': members})

def add_member(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('members')
    else:
        form = MemberForm()
    return render(request, 'add_member.html', {'form': form})

def edit_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == "POST":
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('members')
    else:
        form = MemberForm(instance=member)
    return render(request, 'edit_member.html', {'form': form, 'member': member})

def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == "POST":
        member.delete()
        return redirect('members')
    return render(request, 'confirm_delete_member.html', {'member': member})
    
def member_detail(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    interactions = member.interactions.select_related('book').order_by('-date')

    if request.method == 'POST':
        interaction_form = BookInteractionForm(request.POST)
        if interaction_form.is_valid():
            interaction = interaction_form.save(commit=False)
            interaction.member = member
            interaction.save()

            # Update book stock based on interaction status
            if interaction.status == 'borrowed' and interaction.book.stock > 0:
                interaction.book.stock -= 1
            elif interaction.status == 'returned':
                interaction.book.stock += 1
            # ... handle other statuses if needed ...
            interaction.book.save()

            return redirect('member_detail', member_id=member.id)
    else:
        interaction_form = BookInteractionForm()

    return render(request, 'member_detail.html', {
        'member': member,
        'interactions': interactions,
        'interaction_form': interaction_form,
    })



