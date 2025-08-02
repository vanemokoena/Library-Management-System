from django.contrib import admin
from .models import Book, DynamicCategory, DynamicData, Member, BookInteraction

# Customizing the Book admin interface
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'publisher', 'page', 'stock', 'availability_status')
    list_filter = ('availability_status', 'author', 'publisher')
    search_fields = ('title', 'author', 'isbn')
    ordering = ('title',)

# Customizing the Member admin interface
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('last_name',)

# Customizing the BookInteraction admin interface
@admin.register(BookInteraction)
class BookInteractionAdmin(admin.ModelAdmin):
    list_display = ('member', 'book', 'status', 'date')
    list_filter = ('status', 'date')
    search_fields = ('member__first_name', 'member__last_name', 'book__title', 'status')
    ordering = ('-date',)

# Registering DynamicCategory and DynamicData in the admin
@admin.register(DynamicCategory)
class DynamicCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(DynamicData)
class DynamicDataAdmin(admin.ModelAdmin):
    list_display = ('category', 'data')
    search_fields = ('category__name',)