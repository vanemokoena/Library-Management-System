from django.db import models
from django.utils import timezone


# DynamicCategory model to store table names and fields
class DynamicCategory(models.Model):
    name = models.CharField(max_length=255)  # The name of the dynamic table (category)
    fields = models.CharField(max_length=500)  # Fields as a comma-separated string

    def __str__(self):
        return self.name

# DynamicData model to store data for each category
class DynamicData(models.Model):
    category = models.ForeignKey(DynamicCategory, on_delete=models.CASCADE)
    data = models.JSONField()  # Store the actual data in a JSON format

    def __str__(self):
        return f"Data for {self.category.name}"

class Book(models.Model):
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('reserved', 'Reserved'),
        ('lost', 'Lost/Damaged'),
    ]
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    publisher = models.CharField(max_length=200)
    page = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)
    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='available')
    
    def is_available(self):
        return self.stock > 0  # Book is available if stock is greater than 0
    def __str__(self):
        return self.title
    

class Member(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
class BookInteraction(models.Model):
    STATUS_CHOICES = [
        ('borrowed', 'Book Borrowed'),
        ('overdue', 'Overdue Book'),
        ('reserved', 'Book Reserved'),
        ('returned', 'Book Returned'),
        ('ready', 'Reservation Ready for Pickup'),
        ('fines', 'Fines/Fees'),
        ('lost', 'Lost/Damaged Book'),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='interactions')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.member} - {self.book} - {self.get_status_display()}"
    
