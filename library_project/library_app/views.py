from django.http import Http404
from django.views import generic
from library_app import forms
from library_app import models
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from datetime import datetime
 
from braces.views import SuperuserRequiredMixin, LoginRequiredMixin

from django.contrib.auth import get_user_model
User = get_user_model()


class BookListView(generic.ListView):
    model = models.Book
    context_object_name = "book_list" #human-understandable name of variable to access from templates
    paginate_by = 10
    queryset = models.Book.objects.all()  # Default: Model.objects.all()

    def get_queryset(self):
        search_query = self.request.GET.get("search_query")
        search_type = self.request.GET.get("search_type")
        if search_query is not None:
            if search_type == "title":
                return models.Book.objects.all().filter(title__icontains=search_query)
            elif search_type == "author":
                authors_result = models.Book.objects.all().filter(authors__first_name__icontains=search_query) | models.Book.objects.all().filter(authors__last_name__icontains=search_query)
                return authors_result
            elif search_type == "category":
                return models.Book.objects.all().filter(category__category_name__icontains=search_query)
            elif search_type == "publishing-house":
                return models.Book.objects.all().filter(publishing_house__name__icontains=search_query)
        else:
            return models.Book.objects.all()

       

class BookDetailView(generic.DetailView):
    model = models.Book

class CreateBookView(LoginRequiredMixin, SuperuserRequiredMixin, generic.CreateView):
    login_url = reverse_lazy('no_permission')

    form_class = forms.BookForm
    model = models.Book

    def form_valid(self, form):
        self.object = form.save(commit=True) #zapisz egzemplarz ksiazki w bazie
        book_instance = self.object   #wez zapisany egzemplarz

        #dla kazdej nowo utworzonej ksiazki stworz jej egzemplarz
        models.BookCopy.objects.create(book=book_instance)
        return HttpResponseRedirect(self.get_success_url())
    
      
class UpdateBookView(LoginRequiredMixin, SuperuserRequiredMixin, generic.UpdateView):
    login_url = reverse_lazy('no_permission')

    fields = ('title','authors','description','isbn','category','edition','publishing_house','publish_date','image_url')
    model = models.Book
    template_name_suffix = '_update_form' #czyli templatka = book_update_form.html


class DeleteBookView(LoginRequiredMixin, SuperuserRequiredMixin, generic.DeleteView):
    login_url = reverse_lazy('no_permission')

    model = models.Book
    success_url = reverse_lazy("library_app:book_list")

############################ Egzemplarz książki


class BookCopyListView(generic.ListView):
    model = models.BookCopy
    paginate_by = 10

    def get_queryset(self):
        search_query = self.request.GET.get("search_query")
        search_type = self.request.GET.get("search_type")
        if search_query is not None:
            if search_type == "title":
                return models.BookCopy.objects.all().filter(book__title__icontains=search_query)
            elif search_type == "author":
                authors_result = models.BookCopy.objects.all().filter(book__authors__first_name__icontains=search_query) | models.BookCopy.objects.all().filter(book__authors__last_name__icontains=search_query)
                return authors_result
            elif search_type == "bookcopy_nr":
                return models.BookCopy.objects.all().filter(id__icontains=search_query)
            elif search_type == "isbn":
                return models.BookCopy.objects.all().filter(book__isbn__icontains=search_query)
        else:
            return models.BookCopy.objects.all()



class BookCopyDetailView(generic.DetailView):
    model = models.BookCopy


class CreateBookCopyView(LoginRequiredMixin, SuperuserRequiredMixin, generic.CreateView):
    login_url = reverse_lazy('no_permission')

    form_class = forms.BookCopyForm
    model = models.BookCopy


class UpdateBookCopyView(LoginRequiredMixin, SuperuserRequiredMixin, generic.UpdateView):
    login_url = reverse_lazy('no_permission')

    fields = ('book', 'is_borrowed')
    model = models.BookCopy
    template_name_suffix = '_update_form'  # czyli templatka = book_update_form.html


class DeleteBookCopyView(LoginRequiredMixin, SuperuserRequiredMixin, generic.DeleteView):
    login_url = reverse_lazy('no_permission')

    model = models.BookCopy
    success_url = reverse_lazy("library_app:bookcopy_list")


############################   AUTOR
class AuthorDetailView(generic.DetailView):
    model = models.Author


class CreateAuthorView(LoginRequiredMixin, SuperuserRequiredMixin, generic.CreateView):
    login_url = reverse_lazy('no_permission')

    form_class = forms.AuthorForm
    model = models.Author


class UpdateAuthorView(LoginRequiredMixin, SuperuserRequiredMixin, generic.UpdateView):
    login_url = reverse_lazy('no_permission')
    
    model = models.Author
    form_class = forms.AuthorForm
    template_name_suffix = '_update_form' #czyli templatka = author_update_form.html


class DeleteAuthorView(LoginRequiredMixin, SuperuserRequiredMixin, generic.DeleteView):
    login_url = reverse_lazy('no_permission')

    model = models.Author
    success_url = reverse_lazy("library_app:book_list")


##########################      Wydawnictwo
class PublishingHouseDetailView(generic.DetailView):
    model = models.PublishingHouse


class CreatePublishingHouseView(LoginRequiredMixin, SuperuserRequiredMixin, generic.CreateView):
    login_url = reverse_lazy('no_permission')

    form_class = forms.PublishingHouseForm
    model = models.PublishingHouse
    success_url = reverse_lazy("library_app:book_list")
    

class DeletePublishingHouseView(LoginRequiredMixin, SuperuserRequiredMixin, generic.DeleteView):
    login_url = reverse_lazy('no_permission')

    model = models.PublishingHouse
    success_url = reverse_lazy("library_app:book_list")


class UpdatePublishingHouseView(LoginRequiredMixin, SuperuserRequiredMixin, generic.UpdateView):
    login_url = reverse_lazy('no_permission')

    fields = ('name', 'city', 'street', 'house_number', 'postal_code')
    model = models.PublishingHouse

    template_name_suffix = '_update_form'


#################### Kategoria
class CategoryDetailView(generic.DetailView):
    model = models.Category


class CreateCategoryView(LoginRequiredMixin, SuperuserRequiredMixin, generic.CreateView):
    login_url = reverse_lazy('no_permission')

    form_class = forms.CategoryForm
    model = models.Category
    

class UpdateCategoryView(LoginRequiredMixin, SuperuserRequiredMixin, generic.UpdateView):
    login_url = reverse_lazy('no_permission')

    fields = ('category_name',)
    model = models.Category
    template_name_suffix = '_update_form' 


class DeleteCategoryView(LoginRequiredMixin, SuperuserRequiredMixin, generic.DeleteView):
    login_url = reverse_lazy('no_permission')

    model = models.Category
    success_url = reverse_lazy("library_app:book_list")

########################## Wypozyczenia


class BorrowListView(LoginRequiredMixin, SuperuserRequiredMixin, generic.ListView):
    login_url = reverse_lazy('no_permission')
    model = models.Borrow
    context_object_name = "borrow_list" #human-understandable name of variable to access from templates
    paginate_by = 10
    #queryset = models.Borrow.objects.all()  # Default: Model.objects.all()

    def get_queryset(self):
        search_query = self.request.GET.get("search_query")
        search_type = self.request.GET.get("search_type")
        if search_query is not None:
            if search_type == "title":
                return models.Borrow.objects.all().filter(book_copy_id__book__title__icontains=search_query)
            elif search_type == "author":
                authors_result = models.Borrow.objects.all().filter(book_copy_id__book__authors__first_name__icontains=search_query) | models.Borrow.objects.all().filter(book_copy_id__book__authors__last_name__icontains=search_query)
                return authors_result
            elif search_type == "bookcopy_nr":
                return models.Borrow.objects.all().filter(book_copy_id__id__icontains=search_query)
            elif search_type == "borrow_by_user":
                borrow_by_result = models.Borrow.objects.all().filter(user__first_name__contains=search_query) | models.Borrow.objects.all().filter(user__last_name__contains=search_query)
                return borrow_by_result
            elif search_type == "borrow_by_librarian":
                borrow_by_result = models.Borrow.objects.all().filter(borrow_librarian__first_name__contains=search_query) | models.Borrow.objects.all().filter(borrow_librarian__last_name__contains=search_query)
                return borrow_by_result
        else:
            return models.Borrow.objects.all()


class BorrowDetailView(LoginRequiredMixin, SuperuserRequiredMixin, generic.DetailView):
    login_url = reverse_lazy('no_permission')
    model = models.Borrow


class CreateBorrowView(LoginRequiredMixin, SuperuserRequiredMixin, generic.CreateView):
    login_url = reverse_lazy('no_permission')

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
    
    
class UpdateBorrowView(LoginRequiredMixin, SuperuserRequiredMixin, generic.UpdateView):
    login_url = reverse_lazy('no_permission')

    fields = ('is_borrowed',)
    model = models.BookCopy

    template_name_suffix = '_update_form'


class DeleteBorrowView(LoginRequiredMixin, SuperuserRequiredMixin, generic.DeleteView):
    login_url = reverse_lazy('no_permission')

    model = models.Borrow
    success_url = reverse_lazy("library_app:borrow_list")

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        bookcopy = self.object.book_copy_id   # w obiekcie wypozyczenia jest obiekt egzemplarza ksiazki
        bookcopy.is_borrowed = False           #zmien w obiekcie egzemplarza "wypozyczony" na false
        bookcopy.save()                       #zapisz obiekt egzemplarza        
       
        self.object.receive_librarian = User.objects.get(id=self.request.user.id) #ustaw bibliotekarza ktory przyjal ksiazke
        self.object.receive_date = datetime.now()                                 #ustaw date oddania na aktualna

        #zapisanie obiektu borrow jako obiekt borrowHistory przed usunieciem obiektu Borrow
        models.BorrowHistory.objects.create(
            user=self.object.user, 
            borrow_librarian=self.object.borrow_librarian,
            receive_librarian=self.object.receive_librarian,
            book_copy_id=self.object.book_copy_id,
            borrow_date=self.object.borrow_date,
            receive_date=self.object.receive_date
        )

        self.object.delete()                 #usun wypozyczenie z bazy
        return HttpResponseRedirect(self.get_success_url())

########### WYPOŻYCZENIA UŻYTKOWNIKA
class MyBorrowListView(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('login')
    model = models.BorrowHistory
    context_object_name = "history_borrow_list" #human-understandable name of variable to access from templates
    paginate_by = 5
    template_name = "library_app/myborrowlist.html"
    #queryset = models.Borrow.objects.all()  # Default: Model.objects.all()

    def get_queryset(self):
        queryset = models.BorrowHistory.objects.filter(user=self.request.user)
        return queryset 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_borrow_list"] = models.Borrow.objects.filter(user=self.request.user)
        return context
    

