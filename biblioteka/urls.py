from django.urls import include, path

from .views import *

app_name = 'biblioteka'

urlpatterns = [
    path('', index, name='index'),
    path('author/<int:id>/', AuthorDetailView.as_view(), name='author-detail'),
    path('author/create/', AuthorCreateView.as_view(), name='author-create'),
    path('book/<int:id>/', BookDetailView.as_view(), name='book-detail'),
    path('book/create/', BookCreateView.as_view(), name='book-create'),
    path('library/<int:id>/', LibraryDetailView.as_view(), name='library-detail'),
    path('library/create/', LibraryCreateView.as_view(), name='library-create'),
    path('register/', Register.as_view(), name="register"),
    path('profile/', profile, name="profile"),
]