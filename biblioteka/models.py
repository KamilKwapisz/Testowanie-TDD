from django.db import models
from django.urls import reverse


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(
        "Author",
        on_delete=models.CASCADE,
        verbose_name="author",
        related_name='+',
    )
    genre = models.CharField(max_length=25)
    library = models.ForeignKey(
        "Library",
        on_delete=models.CASCADE,
        verbose_name="library",
        related_name='+',
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(f"{self.author} - {self.title}")

    def get_absolute_url(self):
        return reverse('biblioteka:book-detail', kwargs={'id': self.pk})


class Author(models.Model):
    name = models.CharField(max_length=50, unique=True)
    books = models.ManyToManyField(
        "Book",
        verbose_name="books",
        related_name='+',
        blank=True,
    )

    def publish_book(self, book):
        if type(book) != Book:
            raise ValueError("Given argument is not a Book object")
        self.books.add(book)
        self.save()
    
    def publish_books(self, books):
        for book in books:
            self.publish_book(book)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('biblioteka:author-detail', kwargs={'id': self.pk})


class Library(models.Model):
    location = models.CharField(max_length=100, blank=True, null=True, unique=True)
    books = models.ManyToManyField(
        Book,
        verbose_name="books",
        related_name='+',
        blank=True,
    )

    def add_book(self, book):
        if type(book) != Book:
            raise ValueError("Given argument is not a Book object")
        self.books.add(book)
        self.save()
    
    def add_books(self, books):
        for book in books:
            self.publish_book(book)

    def __str__(self):
        return str(self.location)

    def get_absolute_url(self):
        return reverse('biblioteka:library-detail', kwargs={'id': self.pk})
