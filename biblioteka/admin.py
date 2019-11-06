from django.contrib import admin
from biblioteka.models import Author, Book, Library

# Register your models here.
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Library)