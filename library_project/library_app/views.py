from django.http import Http404
from django.views import generic
from library_app import forms
from library_app import models
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import get_user_model
User = get_user_model()


class BookListView(generic.ListView):
    model = models.Book
    context_object_name = "book_list" #human-understandable name of variable to access from templates
    paginate_by = 10
    queryset = models.Book.objects.all()  # Default: Model.objects.all()

    #do listy ksiazek dodaj kontekst z egzemplarzami ksiazki
    # def get_context_data(self, **kwargs):
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     context['bookcopys'] = models.BookCopy.objects.all
    #     return context

class BookDetailView(generic.DetailView):
    model = models.Book

class CreateBookView(LoginRequiredMixin, generic.CreateView):
    login_url = reverse_lazy('login')

    form_class = forms.BookForm
    model = models.Book

    def form_valid(self, form):
        self.object = form.save(commit=True) #zapisz egzemplarz ksiazki w bazie
        book_instance = self.object   #wez zapisany egzemplarz

        #dla kazdej nowo utworzonej ksiazki stworz jej egzemplarz
        models.BookCopy.objects.create(book=book_instance)
        return HttpResponseRedirect(self.get_success_url())
    
      
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
    success_url = reverse_lazy("library_app:book_list")
    

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
    #queryset = models.Borrow.objects.all()  # Default: Model.objects.all()

    def get_queryset(self):
        if self.request.user.is_superuser:
            # queryset = models.Borrow.objects.filter(book_copy_id__is_borrowed=True)
            queryset = models.Borrow.objects.all()
        else:
            queryset = models.Borrow.objects.filter(user=self.request.user).filter(book_copy_id__is_borrowed=True)
        return queryset 

class BorrowDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = reverse_lazy('login')
    model = models.Borrow

class CreateBorrowView(LoginRequiredMixin, generic.CreateView):
    login_url = reverse_lazy('login')

    form_class = forms.BorrowForm
    model = models.Borrow
    success_url = reverse_lazy("library_app:borrow_list")

    #przed dodaniem wypożyczenia trzeba zmienic w egzemplarzu ksiazki ze jest wypozyczony
    def form_valid(self, form):
        self.object = form.save(commit=False) #wez z formularza stworzony obiekt wypozyczenia
        bookcopy = self.object.book_copy_id   # w obiekcie wypozyczenia jest obiekt egzemplarza ksiazki
        bookcopy.is_borrowed = True           #zmien w obiekcie egzemplarza "wypozyczony" na true
        bookcopy.save()                       #zapisz obiekt egzemplarza

        self.object.borrow_librarian = User.objects.get(id=self.request.user.id) # zapisz jako wypozyczajacego zalogowanego usera (wypozyczac moze tylko bibliotekarz)
        self.object.save()                    #wszystko zmienione, mozna zapisac wypozyczenie
        return HttpResponseRedirect(self.get_success_url())
    
    

class UpdateBorrowView(LoginRequiredMixin, generic.UpdateView):
    login_url = reverse_lazy('login')

    fields = ('is_borrowed',)
    model = models.BookCopy

    template_name_suffix = '_update_form'

class DeleteBorrowView(LoginRequiredMixin, generic.DeleteView):
    login_url = reverse_lazy('login')

    model = models.Borrow
    success_url = reverse_lazy("library_app:borrow_list")

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        bookcopy = self.object.book_copy_id   # w obiekcie wypozyczenia jest obiekt egzemplarza ksiazki
        bookcopy.is_borrowed = False           #zmien w obiekcie egzemplarza "wypozyczony" na false
        bookcopy.save()                       #zapisz obiekt egzemplarza        
       
        self.object.receive_librarian = User.objects.get(id=self.request.user.id)
       
        self.object.delete()                 #usun wypozyczenie z bazy
        return HttpResponseRedirect(self.get_success_url())



