from biblioteka.models import Author, Book, Library

def add_author(name):
    author = Author.objects.create(name=name)
    return author


def add_library(location):
    library = Library.objects.create(location=location)
    return library


def add_book(title, genre, author, library=None):
    if not type(author) == Author:
        raise ValueError("Author should be a DB object")
    if type(genre) != str or type(title) != str:
        raise ValueError("Title and genre have to be strings!")
    
    book = Book.objects.create(
        title=title,
        genre=genre,
        author=author,
        library=library
    )

    return book


def view_books_by_author(author):
    if type(author) == str:
        try:
            author = Author.objects.get(name=author)
        except Exception:
            raise ValueError("Wrong author name!")
    elif type(author) != Author:
        raise ValueError("Parameter should be author name or object!")
    
    books = list(Book.objects.filter(author=author))
    return books


def view_books_in_library(library):
    if type(library) == str:
        try:
            library = Library.objects.get(location=location)
        except Exception:
            raise ValueError("Wrong library location!")
    elif type(library) != Library:
        raise ValueError("Parameter should be library location or object!")
    
    books = list(Book.objects.filter(library=library))
    return books


def count_titles(library):
    if type(library) == str:
        try:
            library = Library.objects.get(location=location)
        except Exception:
            raise ValueError("Wrong library location!")
    elif type(library) != Library:
        raise ValueError("Parameter should be library location or object!")
    
    titles = dict()
    books = Book.objects.filter(library=library)
    for book in books:
        if book.title in titles:
            titles[book.title] += 1
        else:
            titles[book.title] = 1
    
    return titles


def view_titles_by_author(author):
    if type(author) == str:
        try:
            author = Author.objects.get(name=author)
        except Exception:
            raise ValueError("Wrong author name!")
    elif type(author) != Author:
        raise ValueError("Parameter should be author name or object!")
    
    titles = []
    books = Book.objects.filter(author=author)
    for book in books:
        if book.title not in titles:
            titles.append(book.title)

    return titles

def find_libraries_with_book(book):
    if type(book) != Book:
        raise ValueError("Parameter should be a Book object!")

    libraries = list(Library.objects.filter(books__in=[book]).distinct())
    return libraries
