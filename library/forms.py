from django import forms
from .models import Book,Member,BookInteraction
from .models import DynamicCategory, DynamicData

class CategoryForm(forms.ModelForm):
    class Meta:
        model = DynamicCategory
        fields = ['name', 'fields']

class DynamicDataForm(forms.Form):
    # This will be generated dynamically based on category fields
    pass

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'publisher', 'page', 'stock']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full border rounded p-2 mb-2'}),
            'author': forms.TextInput(attrs={'class': 'w-full border rounded p-2 mb-2'}),
            'isbn': forms.TextInput(attrs={'class': 'w-full border rounded p-2 mb-2'}),
            'publisher': forms.TextInput(attrs={'class': 'w-full border rounded p-2 mb-2'}),
            'page': forms.TextInput(attrs={'class': 'w-full border rounded p-2 mb-2'}),
            'stock': forms.TextInput(attrs={'class': 'w-full border rounded p-2 mb-2'}),
        }
class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']
        
class BookInteractionForm(forms.ModelForm):
    class Meta:
        model = BookInteraction
        fields = ['book', 'status', 'notes']
        widgets = {
            'status': forms.Select(choices=BookInteraction.STATUS_CHOICES),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(BookInteractionForm, self).__init__(*args, **kwargs)
        # Only show books with stock greater than 0
        self.fields['book'].queryset = Book.objects.filter(stock__gt=0)