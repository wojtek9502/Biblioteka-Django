from django.http import Http404
from django.views import generic
from library_app import forms
from library_app import models
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import get_user_model
User = get_user_model()


class BookListView(generic.ListView):
    model = models.Book
    context_object_name = "book_list" #human-understandable name of variable to access from templates
    paginate_by = 10
    queryset = models.Book.objects.all()  # Default: Model.objects.all()

class BookDetailView(generic.DetailView):
    model = models.Book

class CreateBookView(LoginRequiredMixin, generic.CreateView):
    login_url = reverse_lazy('login')

    form_class = forms.BookForm
    model = models.Book

class UpdateBookView(LoginRequiredMixin, generic.UpdateView):
    login_url = reverse_lazy('login')

    fields = ('title','authors','description','isbn','category','edition','publishing_house','publish_date','image_url')
    model = models.Book
    template_name_suffix = '_update_form' #czyli templatka = book_update_form.html

class DeleteBookView(LoginRequiredMixin, generic.DeleteView):
    login_url = reverse_lazy('login')

    model = models.Book
    success_url = reverse_lazy("library_app:book_list")

############################ Egzemplarz książki
class BookCopyListView(generic.ListView):
    model = models.BookCopy


class BookCopyDetailView(generic.DetailView):
    model = models.BookCopy


class CreateBookCopyView(LoginRequiredMixin, generic.CreateView):
    login_url = reverse_lazy('login')

    form_class = forms.BookCopyForm
    model = models.BookCopy


class UpdateBookCopyView(LoginRequiredMixin, generic.UpdateView):
    login_url = reverse_lazy('login')

    fields = ('book', 'is_borrowed')
    model = models.BookCopy
    template_name_suffix = '_update_form'  # czyli templatka = book_update_form.html


class DeleteBookCopyView(LoginRequiredMixin, generic.DeleteView):
    login_url = reverse_lazy('login')

    model = models.BookCopy
    success_url = reverse_lazy("library_app:bookcopy_list")


############################   AUTOR
class AuthorDetailView(generic.DetailView):
    model = models.Author

class CreateAuthorView(LoginRequiredMixin,generic.CreateView):
    login_url = reverse_lazy('login')

    form_class = forms.AuthorForm
    model = models.Author

class UpdateAuthorView(LoginRequiredMixin, generic.UpdateView):
    login_url = reverse_lazy('login')

    fields = ('first_name', 'last_name', 'country', 'biography', 'birth_place', 'image_url', 'years_of_life')
    model = models.Author
    template_name_suffix = '_update_form' #czyli templatka = author_update_form.html

class DeleteAuthorView(LoginRequiredMixin, generic.DeleteView):
    login_url = reverse_lazy('login')

    model = models.Author
    success_url = reverse_lazy("library_app:book_list")


##########################      Wydawnictwo
class PublishingHouseDetailView(generic.DetailView):
    model = models.PublishingHouse

class CreatePublishingHouseView(LoginRequiredMixin,generic.CreateView):
    login_url = reverse_lazy('login')

    form_class = forms.PublishingHouseForm
    model = models.PublishingHouse
    success_url = reverse_lazy("library_app:book_create")
    

class DeletePublishingHouseView(LoginRequiredMixin, generic.DeleteView):
    login_url = reverse_lazy('login')

    model = models.PublishingHouse
    success_url = reverse_lazy("library_app:book_list")

class UpdatePublishingHouseView(LoginRequiredMixin, generic.UpdateView):
    login_url = reverse_lazy('login')

    fields = ('name', 'city', 'street', 'house_number', 'postal_code')
    model = models.PublishingHouse

    template_name_suffix = '_update_form'


#################### Kategoria
class CategoryDetailView(generic.DetailView):
    model = models.Category

class CreateCategoryView(LoginRequiredMixin,generic.CreateView):
    login_url = reverse_lazy('login')

    form_class = forms.CategoryForm
    model = models.Category
    

class UpdateCategoryView(LoginRequiredMixin, generic.UpdateView):
    login_url = reverse_lazy('login')

    fields = ('category_name',)
    model = models.Category
    template_name_suffix = '_update_form' 

class DeleteCategoryView(LoginRequiredMixin, generic.DeleteView):
    login_url = reverse_lazy('login')

    model = models.Category
    success_url = reverse_lazy("library_app:book_list")

########################## Wypozyczenia
class BorrowListView(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('login')
    model = models.Borrow
    context_object_name = "borrow_list" #human-understandable name of variable to access from templates
    paginate_by = 10
    queryset = models.Borrow.objects.all()  # Default: Model.objects.all()

class BorrowDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = reverse_lazy('login')
    model = models.Borrow

class CreateBorrowView(LoginRequiredMixin, generic.CreateView):
    login_url = reverse_lazy('login')

    form_class = forms.BorrowForm
    model = models.Borrow
    success_url = reverse_lazy("library_app:borrow_list")

class DeleteBorrowView(LoginRequiredMixin, generic.DeleteView):
    login_url = reverse_lazy('login')

    model = models.Borrow
    success_url = reverse_lazy("library_app:borrow_list")
