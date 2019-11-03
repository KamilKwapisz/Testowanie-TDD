from django.urls import include, path

from .views import *

app_name = 'biblioteka'

urlpatterns = [
    path('', index, name='index'),
    path('author/<int:id>/', AuthorDetailView.as_view(), name='author-detail'),
    path('book/<int:id>/', BookDetailView.as_view(), name='book-detail'),
    path('library/<int:id>/', LibraryDetailView.as_view(), name='library-detail'),
    path('register/', Register.as_view(), name="register"),
    path('profile/', profile, name="profile"),
]