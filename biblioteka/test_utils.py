from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.db.utils import IntegrityError
from django.urls import reverse

from biblioteka.models import Author, Book, Library
from biblioteka.utils import *

class UtilsTestCase(TestCase):

    def test_add_author_with_name_only(self):
        # Given
        name = "Orwell"
        add_author(name)

        # When
        author = Author.objects.get(name=name)

        # Then
        self.assertIsNotNone(author)
        self.assertEqual(author.name, name)

    def test_add_library_with_location_only(self):
        # Given
        location = "Narutowicza 15"
        add_library(location)

        # When
        library = Library.objects.get(location=location)

        # Then
        self.assertIsNotNone(library)
        self.assertEqual(library.location, location)

    def test_add_book(self):
        # Given
        title = "Jak zdobyć bogactwo"
        genre = "biznes"
        author_name = "Felix Dennis"
        author = Author.objects.create(name=author_name)
        add_book(
            title=title,
            genre=genre,
            author=author
        )

        # When
        book = Book.objects.get(title=title)

        # Then
        self.assertIsNotNone(book)
        self.assertEqual(type(book), Book)
        self.assertEqual(book.title, title)
        self.assertEqual(book.genre, genre)
        self.assertEqual(book.author, author)

    def test_add_book_with_wrong_autor_object(self):
        # Given
        title = "Jak zdobyć bogactwo"
        genre = "biznes"
        author_name = "Felix Dennis"

        with self.assertRaises(ValueError):
            add_book(title, genre, author_name)
            
    def test_add_book_with_wrong_title(self):
        # Given
        title = 4.3241
        genre = "biznes"
        author_name = "Felix Dennis"
        author = Author.objects.create(name=author_name)

        with self.assertRaises(ValueError):
            add_book(title, genre, author_name)
            

    def test_add_book_with_bad_autor_object(self):
        # Given
        title = "Jak zdobyć bogactwo"
        genre = True
        author_name = "Felix Dennis"
        author = Author.objects.create(name=author_name)

        with self.assertRaises(ValueError):
            add_book(title, genre, author_name)
            
    def test_view_books_by_author(self):
        # Given
        author = add_author(name="Tim Ferriss")
        book1 = add_book(
            title="4h workweek",
            genre="biznes",
            author=author
        )
        book2 = add_book(
            title="Narzędzia tytanów",
            genre="biznes",
            author=author
        )
        author.publish_books([book1, book2])

        # When
        books = view_books_by_author(author=author)

        # Then
        self.assertEqual(type(books), list)
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0], book1)
        self.assertEqual(books[1], book2)

    def test_view_books_by_author_with_wrong_name(self):
        self.name = "Null Pointer"
        with self.assertRaises(ValueError):
            view_books_by_author(self.name)
            

    def test_view_books_in_library_with_wrong_location_type(self):
        self.name = 3.14
        with self.assertRaises(ValueError):
            view_books_by_author(self.name)
            
    
    def test_view_books_in_library(self):
        # Given
        author = add_author(name="Tim Ferriss")
        library = add_library("Plac politechniki 1")
        book1 = add_book(
            title="4h workweek",
            genre="biznes",
            author=author,
            library=library,
        )
        book2 = add_book(
            title="Narzędzia tytanów",
            genre="biznes",
            author=author,
            library=library,
        )

        # When
        books = view_books_in_library(library=library)

        # Then
        self.assertEqual(type(books), list)
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0], book1)
        self.assertEqual(books[1], book2)

    def test_view_books_in_library_with_wrong_location(self):
        self.location = "Null Pointer 00"
        with self.assertRaises(ValueError):
            view_books_in_library(self.location)

    def test_view_books_in_library_with_wrong_location_type(self):
        self.location = 3.14
        with self.assertRaises(ValueError):
            view_books_in_library(self.location)

    def test_count_titles(self):
        # Given
        author1 = add_author(name="Tim Ferriss")
        title1 = "4h workweek"
        counter1 = 5
        author2 = add_author(name="GaryVee")
        title2 = "Przebij się!"
        counter2 = 3
        library = add_library("Plac politechniki 1")
        for _ in range(counter1):
            add_book(
                title=title1,
                genre="biznes",
                author=author1,
                library=library,
            )
        for _ in range(counter2):
            add_book(
                title=title2,
                genre="biznes",
                author=author2,
                library=library,
            )
        
        # When
        titles = count_titles(library=library)

        # Then
        self.assertEqual(type(titles), dict)
        self.assertEqual(len(titles), 2)
        self.assertEqual(titles[title1], counter1)
        self.assertEqual(titles[title2], counter2)

    def test_titles_by_author(self):
        # Given
        author = add_author(name="Tim Ferriss")
        title1 = "4h workweek"
        title2 = "Narzędzia tytanów"
        book1 = add_book(
            title=title1,
            genre="biznes",
            author=author
        )
        book2 = add_book(
            title=title2,
            genre="biznes",
            author=author
        )
        author.publish_books([book1, book2])

        # When
        titles = view_titles_by_author(author)

        # Then
        self.assertEqual(type(titles), list)
        self.assertEqual(len(titles), 2)
        self.assertEqual(titles[0], title1)
        self.assertEqual(titles[1], title2)
    
    def test_view_titles_by_author_with_wrong_name(self):
        self.name = "Null Pointer"
        with self.assertRaises(ValueError):
            view_titles_by_author(self.name)
            

    def test_titles_by_author_with_wrong_name_type(self):
        self.name = 3.14
        with self.assertRaises(ValueError):
            view_titles_by_author(self.name)
            

    def test_find_libraries_with_book(self):
        # Given
        author = add_author(name="Tim Ferriss")
        library1 = add_library("Plac Narutowicza")
        library2 = add_library("Marszałkowska")
        library3 = add_library("Złota 44")
        title = "4h workweek"
        book = add_book(
            title=title,
            genre="biznes",
            author=author
        )
        library1.add_book(book)
        library2.add_book(book)
        library3.add_book(book)

        # When
        libraries_with_book = find_libraries_with_book(book)

        # Then
        self.assertEqual(type(libraries_with_book), list)
        self.assertEqual(len(libraries_with_book), 3)
        self.assertEqual(libraries_with_book[0], library1)
        self.assertEqual(libraries_with_book[1], library2)
        self.assertEqual(libraries_with_book[2], library3)

    def test_find_libraries_with_book_with_wrong_name_type(self):
        self.book = 3.14
        with self.assertRaises(ValueError):
            find_libraries_with_book(self.book)