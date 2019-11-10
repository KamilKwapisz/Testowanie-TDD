from django.urls import include, path

from .views import *

app_name = 'biblioteka'

urlpatterns = [
    path('', index, name='index'),
    path('author/create/', AuthorCreateView.as_view(), name='author-create'),
    path('author/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
    path('author/edit/<int:pk>/', AuthorEditView.as_view(), name='author-edit'),
    path('author/delete/<int:pk>/', AuthorDeleteView.as_view(), name='author-delete'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('book/create/<int:author_pk>', BookCreateView.as_view(), name='book-create'),
    path('book/edit/<int:pk>/', BookEditView.as_view(), name='book-edit'),
    path('book/delete/<int:pk>/', BookDeleteView.as_view(), name='book-delete'),
    path('library/create/', LibraryCreateView.as_view(), name='library-create'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
    path('library/edit/<int:pk>/', LibraryEditView.as_view(), name='library-edit'),
    path('library/delete/<int:pk>/', LibraryDeleteView.as_view(), name='library-delete'),
    path('libraries/', libraries_list, name='library-list'),
    path('books/', books_list, name='book-list'),
    path('authors/', authors_list, name='author-list'),
    path('register/', Register.as_view(), name="register"),
    path('profile/', profile, name="profile"),
]