from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views.decorators.debug import sensitive_variables, sensitive_post_parameters
from django.shortcuts import render, redirect

from biblioteka.models import Book, Author, Library


def index(request):
    return HttpResponse("Hello, world!")


class BookDetailView(DetailView):

    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AuthorDetailView(DetailView):

    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LibraryDetailView(DetailView):

    model = Library

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Register(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    context = dict(username=request.user.username)
    return render(request, 'profile.html', context)
