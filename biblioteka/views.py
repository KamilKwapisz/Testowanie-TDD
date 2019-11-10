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


def index(request):
    return HttpResponse("Hello, world!")


class BookDetailView(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BookCreateView(CreateView):
    model = Book
    fields = ['title', 'genre', 'author', 'library']
    template_name = "create/createBook.html"
    success_message = "Książka została utworzona."
    success_url = reverse_lazy('biblioteka:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BookEditView(UpdateView):
    model = Book
    fields = ['title', 'genre', 'author', 'library']
    template_name = "edit/editAuthor.html"
    success_message = "Książka została zedytowana."
    success_url = reverse_lazy('biblioteka:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BookDeleteView(DeleteView):
    model = Book
    fields = ['title', 'genre', 'author', 'library']
    template_name = "delete/deleteAuthor.html"
    success_message = "Książka została usunięta."
    success_url = reverse_lazy('biblioteka:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BookListView(ListView):
    model = Book
    fields = ['title', 'genre', 'author', 'library']
    template_name = "books.html"
    success_url = reverse_lazy('biblioteka:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def index(self):
        data = Book.objects.all()
        return render(self.request, self.template_name, {'books': data})

    def booksInLibrary(self):
        libId = self.request.GET["id"]
        data = Book.objects.all().filter((Book.library.id == libId))
        return render(self.request, self.template_name, {'books': data})

    def authorBooks(self):
        authorId = self.request.GET["id"]
        data = Book.objects.all().filter((Book.author.id == authorId))
        return render(self.request, self.template_name, {'books': data})


class AuthorCreateView(CreateView):
    model = Author
    fields = ['name', 'books']
    template_name = "create/createAuthor.html"
    success_message = "Autor został utworzony."
    success_url = reverse_lazy('biblioteka:index')

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
    success_url = reverse_lazy('biblioteka:index')

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
    success_url = reverse_lazy('biblioteka:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AuthorListView(ListView):
    model = Author
    fields = ['name']
    template_name = "authors.html"
    success_url = reverse_lazy('biblioteka:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def index(self):
        data = Author.objects.all()
        return render(self.request, self.template_name, {'authors': data})


class LibraryCreateView(CreateView):
    model = Library
    fields = ['location', 'books']
    template_name = "create/createLibrary.html"
    success_message = "Biblioteka została dodana."
    success_url = reverse_lazy('biblioteka:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LibraryEditView(UpdateView):
    model = Library
    fields = ['location', 'books']
    template_name = "edit/editLibrary.html"
    success_message = "Biblioteka została zedytowana."
    success_url = reverse_lazy('biblioteka:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LibraryDeleteView(DeleteView):
    model = Library
    fields = ['location', 'books']
    template_name = "delete/deleteLibrary.html"
    success_message = "Biblioteka została usunięa."
    success_url = reverse_lazy('biblioteka:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LibraryListView(ListView):
    model = Library
    fields = ['location', 'books']
    template_name = "libraries.html"
    success_url = reverse_lazy('biblioteka:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def index(self):
        data = Library.objects.all()
        return render(self.request, self.template_name, {'libraries': data})

    def libraryWithBook(self):
        bookId = self.request.GET["id"]
        book = Book.objects.get(id == bookId)
        data = Library.objects.all().filter((Library.books.get(book).id == bookId))
        return render(self.request, self.template_name, {'libraries': data})


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