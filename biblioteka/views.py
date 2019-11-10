from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import ListView

from biblioteka.models import Book, Author, Library
from biblioteka.utils import *


def index(request):
    return redirect('biblioteka:profile')


class BookDetailView(DetailView):
    model = Book
    template_name = "detail/detailBook.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BookCreateView(CreateView):
    model = Book
    fields = ['title', 'genre']
    template_name = "create/createBook.html"
    success_message = "Książka została utworzona."
    success_url = reverse_lazy('biblioteka:book-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        if form.is_valid():
            book = form.save(commit=False)
            title = self.request.POST.get("title", None)
            genre = self.request.POST.get("genre", None)
            author_pk = self.kwargs['author_pk']
            author = Author.objects.get(pk=author_pk)
            print(title, genre, author.name)
            book.title = title
            book.genre = title
            book.author = author
            book.save()
            return super(BookCreateView, self).form_valid(form)
        else:
            return super(BookCreateView, self).form_invalid(form)


class BookEditView(UpdateView):
    model = Book
    fields = ['title', 'genre', 'author', 'library']
    template_name = "edit/editAuthor.html"
    success_message = "Książka została zedytowana."
    success_url = reverse_lazy('biblioteka:book-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BookDeleteView(DeleteView):
    model = Book
    fields = ['title', 'genre', 'author', 'library']
    template_name = "delete/deleteAuthor.html"
    success_message = "Książka została usunięta."
    success_url = reverse_lazy('biblioteka:book-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def books_list(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, "list/books.html", context)


class AuthorDetailView(DetailView):
    model = Author
    template_name = "detail/detailAuthor.html"

    def get_context_data(self, **kwargs):
        author_books = view_books_by_author(self.get_object())
        context = super().get_context_data(**kwargs)
        context['author_books'] = author_books
        return context

class AuthorCreateView(CreateView):
    model = Author
    fields = ['name', 'books']
    template_name = "create/createAuthor.html"
    success_message = "Autor został utworzony."
    success_url = reverse_lazy('biblioteka:author-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        if form.is_valid():
            author = form.save(commit=False)
            first_name = self.request.POST.get("name", None)
            surname = self.request.POST.get("surname", None)
            if first_name:
                name = f"{first_name.strip()} {surname.strip()}"
                if Author.objects.filter(name=name):
                    return super(AuthorCreateView, self).form_invalid(form)
                author.name = name
                author.save()
                return super(AuthorCreateView, self).form_valid(form)
            else:
                return super(AuthorCreateView, self).form_invalid(form)                
        else:
            return super(AuthorCreateView, self).form_invalid(form)


class AuthorEditView(UpdateView):
    model = Author
    fields = ['name', 'books']
    template_name = "create/createAuthor.html"
    success_message = "Autor został zmieniony."
    success_url = reverse_lazy('biblioteka:author-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        if form.is_valid():
            author = form.save(commit=False)
            first_name = self.request.POST.get("name", None)
            surname = self.request.POST.get("surname", None)
            if first_name:
                name = f"{first_name.strip()} {surname.strip()}"
                if Author.objects.filter(name=name):
                    return super(AuthorEditView, self).form_invalid(form)
                author.name = name
                author.save()
                return super(AuthorEditView, self).form_valid(form)
            else:
                return super(AuthorEditView, self).form_invalid(form)
        else:
            return super(AuthorEditView, self).form_invalid(form)


class AuthorDeleteView(DeleteView):
    model = Author
    fields = ['name']
    template_name = "delete/deleteAuthor.html"
    success_message = "Autor został usunięty."
    success_url = reverse_lazy('biblioteka:author-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def authors_list(request):
    authors = Author.objects.all()
    context = {'authors': authors}
    return render(request, "list/authors.html", context)


class LibraryDetailView(DetailView):
    model = Library
    template_name = "detail/detailLibrary.html"

    def get_context_data(self, **kwargs):
        titles = count_titles(self.get_object())
        books = view_books_in_library(self.get_object())
        context = super().get_context_data(**kwargs)
        context['titles'] = titles
        context['books'] = books
        return context


class LibraryCreateView(CreateView):
    model = Library
    fields = ['location']
    template_name = "create/createLibrary.html"
    success_message = "Biblioteka została dodana."
    success_url = reverse_lazy('biblioteka:library-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        if form.is_valid():
            lib = form.save(commit=False)
            location = self.request.POST.get("location", None)
            lib.location = location
            lib.save()
            return super(LibraryCreateView, self).form_valid(form)
        else:
            return super(LibraryCreateView, self).form_invalid(form)


class LibraryEditView(UpdateView):
    model = Library
    fields = ['location', 'books']
    template_name = "edit/editLibrary.html"
    success_message = "Biblioteka została zedytowana."
    success_url = reverse_lazy('biblioteka:library-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LibraryDeleteView(DeleteView):
    model = Library
    fields = ['location', 'books']
    template_name = "delete/deleteLibrary.html"
    success_message = "Biblioteka została usunięa."
    success_url = reverse_lazy('biblioteka:library-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def libraries_list(request):
    libraries = Library.objects.all()
    context = {'libraries': libraries}
    return render(request, "list/libraries.html", context)


class Register(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


@login_required(login_url='/login/')
def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    context = dict(username=request.user.username)
    return render(request, 'profile.html', context)