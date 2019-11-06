from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.db.utils import IntegrityError
from django.urls import reverse

from biblioteka.models import Author, Book, Library
from biblioteka.utils import *


class BookTestCase(TestCase):
    def setUp(self):
        self.title = "4-hour workweek"
        self.genre = "business"
        self.author = Author.objects.create(name="Tim Ferriss")
        Book.objects.create(
            title=self.title, 
            genre=self.genre, 
            author=self.author
        )

    def test_created_book_exists_by_title(self):
        # When
        book = Book.objects.get(title=self.title)

        # Then
        self.assertIsNotNone(book)
        self.assertEqual(book.genre, self.genre)

    def test_creating_more_books_with_same_title_and_genre_count(self):
        # Given
        new_author_name = "Fakeman"
        new_author = Author.objects.create(name=new_author_name)
        Book.objects.create(
            title=self.title, 
            genre=self.genre,
            author=new_author
        )

        # When
        books = Book.objects.filter(title=self.title)
        
        # Then
        self.assertEqual(books.count(), 2)
    
    def test_creating_more_books_with_same_title_and_genre(self):
        # Given
        new_author_name = "Fakeman"
        new_author = Author.objects.create(name=new_author_name)
        Book.objects.create(
            title=self.title, 
            genre=self.genre,
            author=new_author
        )

        # When
        books = Book.objects.filter(title=self.title)
        author1 = books[0].author.name
        author2 = books[1].author.name
        genre1 = books[0].genre
        genre2 = books[1].genre
        
        # Then
        self.assertNotEqual(author1, author2)
        self.assertEqual(genre1, genre2)


    def test_creating_new_book(self):
        # Given
        new_title = "Rich dad, poor dad"
        new_genre = "finance"
        new_author_name = "Robert Kiyosaki"
        new_author = Author.objects.create(name=new_author_name)
        Book.objects.create(
            title=new_title, 
            genre=new_genre,
            author=new_author
        )

        # When
        book = Book.objects.get(title=new_title)

        # Then
        self.assertIsNotNone(book)
        self.assertEqual(book.genre, new_genre)
        self.assertEqual(book.author, new_author)

    def test_deleting_book(self):
        # Given
        Book.objects.filter(title=self.title).delete()

        # When
        book = Book.objects.filter(title=self.title)

        # Then
        result = bool(book)
        self.assertFalse(result)
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(title=self.title).pk


class LibraryTestCase(TestCase):
    def setUp(self):
        self.address = "Plac Politechniki 1"
        self.library = Library.objects.create(location=self.address)

    def test_created_library_exists(self):
        # When
        library = Library.objects.get(location=self.address)

        # Then
        self.assertIsNotNone(library)
        self.assertEqual(library.location, self.address)

    def test_creating_more_libraries_with_same_location(self):
        with self.assertRaises(IntegrityError):
            Library.objects.create(location=self.address)

    def test_creating_new_library(self):
        # Given
        new_address = "Złota 44"
        Library.objects.create(location=new_address)

        # When
        lib = Library.objects.get(location=new_address)

        # Then
        self.assertIsNotNone(lib)
        self.assertEqual(lib.location, new_address)

    def test_deleting_library(self):
        # Given
        Library.objects.filter(location=self.address).delete()

        # When
        library = Library.objects.filter(location=self.address)

        # Then
        result = bool(library)
        self.assertFalse(result)
        with self.assertRaises(Library.DoesNotExist):
            Library.objects.get(location=self.address).pk

    def test_adding_books_to_library_object(self):
        # Given
        title1 = "Krew elfów"
        genre1 = "fantasy"
        author1_name = "Sapkowski"
        author1 = Author.objects.create(name=author1_name)
        book1 = Book.objects.create(
            title=title1, 
            genre=genre1, 
            author=author1
        )
        title2 = "Zaczynaj od dlaczego"
        genre2 = "biznes"
        author2_name = "Sinek"
        author2 = Author.objects.create(name=author2_name)
        book2 = Book.objects.create(
            title=title2, 
            genre=genre2, 
            author=author2
        )
        self.library.books.add(book1)
        self.library.books.add(book2)
        self.library.save()

        # When
        library = Library.objects.get(location=self.address)
        books = library.books.all()

        # Then
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0].title, title1)
        self.assertEqual(books[1].title, title2)
        self.assertEqual(books[0].author, author1)
        self.assertEqual(books[1].author, author2) 

    
class AuthorTestCase(TestCase):
    def setUp(self):
        self.name = "Andrzej Sapkowski"
        self.author = Author.objects.create(name=self.name)

    def test_created_author_exists(self):
        # When
        author = Author.objects.get(name=self.name)

        # Then
        self.assertIsNotNone(author)
        self.assertEqual(author.name, self.name)

    def test_creating_more_authors_with_same_name(self):
        with self.assertRaises(IntegrityError):
            Author.objects.create(name=self.name)

    def test_creating_new_author(self):
        # Given
        name = "Stephen King"
        Author.objects.create(name=name)

        # When
        author = Author.objects.get(name=name)

        # Then
        self.assertIsNotNone(author)
        self.assertEqual(author.name, name)

    def test_deleting_author(self):
        # Given
        Author.objects.filter(name=self.name).delete()

        # When
        author = Author.objects.filter(name=self.name)

        # Then
        result = bool(author)
        self.assertFalse(result)
        with self.assertRaises(Author.DoesNotExist):
            Author.objects.get(name=self.name).pk

    def test_publish_book(self):
        # Given
        title = "Krew elfów"
        genre = "fantasy"
        book = Book.objects.create(
            title=title, 
            genre=genre, 
            author=self.author
        )
        self.author.publish_book(book)

        # When
        author = Author.objects.get(name=self.name)
        books = author.books.all()

        # Then
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, title)
        self.assertEqual(books[0].genre, genre)
    
    def test_publish_book_with_invalid_arg_string(self):
        with self.assertRaises(ValueError):
            self.author.publish_book("Sezon burz")

    def test_publish_book_with_invalid_arg_id(self):
        with self.assertRaises(ValueError):
            self.author.publish_book(1)

    def test_publish_books_with_list(self):
        # Given
        title1 = "Krew elfów"
        genre1 = "fantasy"
        book1 = Book.objects.create(
            title=title1, 
            genre=genre1, 
            author=self.author
        )
        title2 = "Jak nie sprzedawać praw do dzieła, czyli jaki stracić miliony"
        genre2 = "byznes"
        book2 = Book.objects.create(
            title=title2, 
            genre=genre2, 
            author=self.author
        )
        books_list = [book1, book2]
        self.author.publish_books(books_list)

        # When
        author = Author.objects.get(name=self.name)
        books = author.books.all()

        # Then
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0].title, title1)
        self.assertEqual(books[1].title, title2)

    def test_publish_books_with_tuple(self):
        # Given
        title1 = "Krew elfów"
        genre1 = "fantasy"
        book1 = Book.objects.create(
            title=title1, 
            genre=genre1, 
            author=self.author
        )
        title2 = "Jak nie sprzedawać praw do dzieła, czyli jaki stracić miliony"
        genre2 = "byznes"
        book2 = Book.objects.create(
            title=title2, 
            genre=genre2, 
            author=self.author
        )
        books_list = (book1, book2)
        self.author.publish_books(books_list)

        # When
        author = Author.objects.get(name=self.name)
        books = author.books.all()

        # Then
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0].title, title1)
        self.assertEqual(books[1].title, title2)

    def test_publish_books_with_bad_argument(self):
        title = "Jak nie sprzedawać praw do dzieła, czyli jaki stracić miliony"
        genre = "byznes"
        book = Book.objects.create(
            title=title, 
            genre=genre, 
            author=self.author
        )
        books_list = [book, "Jakiś tam tytuł"]
        with self.assertRaises(ValueError):
            self.author.publish_books(books_list)
        

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
            

    # def test_add_book_to_author(self):
    #     # Given
    #     title = "Jak zdobyć bogactwo"
    #     genre = "biznes"
    #     author_name = "Felix Dennis"
    #     author = add_author(author_name)
    #     book = add_book(
    #         title=title,
    #         genre=genre,
    #         author=author
    #     )

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
            

class LoginTestCase(TestCase):
    def setUp(self):
        self.username = "test"
        self.password = 'pass@123#'
        self.email = "test@test.com"
        self.user = User.objects.create(username=self.username, password=self.password, email=self.email)
        self.client = Client()

    def test_profile_view_with_logged_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('biblioteka:profile'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_profile_view_without_logged_user(self):
        response = self.client.get('/profile/', follow=False)
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/profile/', follow=True)
        self.assertEqual(len(response.redirect_chain), 1)
