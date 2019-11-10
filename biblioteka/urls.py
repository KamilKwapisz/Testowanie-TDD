from django.urls import include, path

from .views import *

app_name = 'biblioteka'

urlpatterns = [
    path('', index, name='index'),
    path('author/create/', AuthorCreateView.as_view(), name='author-create'),
    path('author/edit/<int:id>/', AuthorEditView.as_view(), name='author-edit'),
    path('author/delete/<int:id>/', AuthorDeleteView.as_view(), name='author-delete'),
    path('book/<int:id>/', BookDetailView.as_view(), name='book-detail'),
    path('book/create/', BookCreateView.as_view(), name='book-create'),
    path('book/edit/<int:id>/', BookEditView.as_view(), name='book-edit'),
    path('book/delete/<int:id>/', BookDeleteView.as_view(), name='book-delete'),
    path('library/create/', LibraryCreateView.as_view(), name='library-create'),
    path('library/edit/<int:id>/', LibraryEditView.as_view(), name='library-edit'),
    path('library/delete/<int:id>/', LibraryDeleteView.as_view(), name='library-delete'),
    path('libraries/', LibraryListView.as_view(), name='library-list'),
    path('books/', BookListView.as_view(), name='book-list'),
    path('authors/', AuthorListView.index, name='author-list'),
    path('register/', Register.as_view(), name="register"),
    path('profile/', profile, name="profile"),
    path('books/<int:id>/', LibraryListView.libraryWithBook, name="find-libraries-with-book"),
    path('authors/<int:id>/', BookListView.authorBooks, name="books-by-author"),
    path('libraries/<int:id>/', BookListView.booksInLibrary, name="books-in-library")
]