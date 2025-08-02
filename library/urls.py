from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add_book/', views.add_book, name='add_book'),
    path('books/', views.books, name='books'),
    path('edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('members/', views.members, name='members'),
    path('members/add/', views.add_member, name='add_member'),
    path('members/edit/<int:member_id>/', views.edit_member, name='edit_member'),
    path('members/delete/<int:member_id>/', views.delete_member, name='delete_member'),
    path('members/<int:member_id>/', views.member_detail, name='member_detail'),
    #path('book/<int:pk>/', views.book_detail, name='book_detail'),
    
    
    
    path('manage-tables/', views.manage_tables, name='manage_tables'),  # List all tables
    path('table/<int:category_id>/', views.view_table_data, name='view_table_data'),  # View table data
    path('add-table/', views.add_table, name='add_table'),
    path('add-data/<int:category_id>/', views.add_data, name='add_data'),
 
    path('delete_table/<int:category_id>/', views.delete_table, name='delete_table'),
    
]

    
    
    
    
    
   
