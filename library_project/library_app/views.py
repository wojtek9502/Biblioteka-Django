from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.views import generic

from . import models

from django.contrib.auth import get_user_model
User = get_user_model()


class BookListView(generic.ListView):
    model = models.Book

class BookDetailView(generic.DetailView):
    model = models.Book

class AuthorDetailView(generic.DetailView):
    model = models.Author