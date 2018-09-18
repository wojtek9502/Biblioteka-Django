from django.http import Http404
from django.views import generic
from library_app import forms
from library_app import models
from django.core.urlresolvers import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import get_user_model
User = get_user_model()


class BookListView(generic.ListView):
    model = models.Book

class BookDetailView(generic.DetailView):
    model = models.Book

class CreateBookView(LoginRequiredMixin,generic.CreateView):
    login_url = reverse_lazy('login')

    form_class = forms.BookForm
    model = models.Book

class AuthorDetailView(generic.DetailView):
    model = models.Author

class CreateAuthorView(LoginRequiredMixin,generic.CreateView):
    login_url = reverse_lazy('login')

    form_class = forms.AuthorForm
    model = models.Author