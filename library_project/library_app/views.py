from django.http import Http404
from django.views import generic
from library_app import forms
from library_app import models
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from datetime import datetime, timedelta, date
from django.db import transaction
from chartjs.views.lines import BaseLineChartView
import json

 
from braces.views import SuperuserRequiredMixin, LoginRequiredMixin

from django.contrib.auth import get_user_model
User = get_user_model()

BORROW_LIMIT = 5
PROLONG_DAYS = 30
EXCEEDED_DATE_COST_PER_DAY = 0.50 #koszt za przekroczenie daty oddania (zł/dzien)

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #w context['author'] jest przechowywany aktualnie przegladany
        context["author_books"] = models.Book.objects.all().filter(authors=context['author'])
        return context

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #w context['publishinghouse'] jest przechowywane aktualnie przegladane wydawnictwo
        context["publishing_house_books"] = models.Book.objects.all().filter(publishing_house=context['publishinghouse'])
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #w context['category_books'] jest przechowywany aktualnie przegladana kategoria
        context["category_books"] = models.Book.objects.all().filter(category=context['category'])
        return context


class CreateCategoryView(LoginRequiredMixin, SuperuserRequiredMixin, generic.CreateView):
    login_url = reverse_lazy('no_permission')

    form_class = forms.CategoryForm
    model = models.Category
    

class UpdateCategoryView(LoginRequiredMixin, SuperuserRequiredMixin, generic.UpdateView):
    login_url = reverse_lazy('no_permission')

    model = models.Category
    form_class = forms.CategoryForm
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
        query_result = None
        if search_query is not None:
            if search_type == "title":
                query_result = models.Borrow.objects.all().filter(book_copy_id__book__title__icontains=search_query)
            elif search_type == "author":
                authors_result = models.Borrow.objects.all().filter(book_copy_id__book__authors__first_name__icontains=search_query) | models.Borrow.objects.all().filter(book_copy_id__book__authors__last_name__icontains=search_query)
                query_result = authors_result
            elif search_type == "bookcopy_nr":
                query_result = models.Borrow.objects.all().filter(book_copy_id__id__icontains=search_query)
            elif search_type == "borrow_by_user":
                borrow_by_result = models.Borrow.objects.all().filter(user__first_name__contains=search_query) | models.Borrow.objects.all().filter(user__last_name__contains=search_query)
                query_result = borrow_by_result
            elif search_type == "borrow_by_librarian":
                borrow_by_result = models.Borrow.objects.all().filter(borrow_librarian__first_name__contains=search_query) | models.Borrow.objects.all().filter(borrow_librarian__last_name__contains=search_query)
                query_result = borrow_by_result
            return query_result.order_by("receive_date")
        else:
            return models.Borrow.objects.all().order_by("receive_date")


class BorrowDetailView(LoginRequiredMixin, SuperuserRequiredMixin, generic.DetailView):
    login_url = reverse_lazy('no_permission')
    model = models.Borrow


class CreateBorrowView(LoginRequiredMixin, SuperuserRequiredMixin, generic.CreateView):
    login_url = reverse_lazy('no_permission')

    form_class = forms.BorrowForm
    model = models.Borrow
    success_url = reverse_lazy("library_app:borrow_list")

    #przed dodaniem wypożyczenia trzeba zmienic w egzemplarzu ksiazki ze jest wypozyczony
    @transaction.atomic
    def form_valid(self, form):
        self.object = form.save(commit=False) #wez z formularza stworzony obiekt wypozyczenia
        bookcopy = self.object.book_copy_id   # w obiekcie wypozyczenia jest obiekt egzemplarza ksiazki
        bookcopy.is_borrowed = True           #zmien w obiekcie egzemplarza "wypozyczony" na true
        bookcopy.save()                       #zapisz obiekt egzemplarza

        #jesli user osiagnal limit wypozyczen to w userProfileInfo.can_borrow ustaw na False
        user_curr_borrow_count = models.Borrow.objects.filter(user=self.object.user.id).count()
        user_curr_borrow_count = user_curr_borrow_count + 1
        if(user_curr_borrow_count==BORROW_LIMIT): #jesli liczba wypozyczen == limit
            userProfileInfoObj =  models.UserProfileInfo.objects.get(user=self.object.user.id)
            userProfileInfoObj.can_borrow = False
            userProfileInfoObj.save()


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

    @transaction.atomic
    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        bookcopy = self.object.book_copy_id   # w obiekcie wypozyczenia jest obiekt egzemplarza ksiazki
        bookcopy.is_borrowed = False           #zmien w obiekcie egzemplarza "wypozyczony" na false
        bookcopy.save()                       #zapisz obiekt egzemplarza        
       
        self.object.receive_librarian = User.objects.get(id=self.request.user.id) #ustaw bibliotekarza ktory przyjal ksiazke
        self.object.receive_date = datetime.now()                                 #ustaw date oddania na aktualna

        #przy oddaniu ksiązki ustaw UserProfileInfo.can_borrow na true, moze teraz wypożyczać
        userProfileInfoObj = models.UserProfileInfo.objects.get(user=self.object.user.id)
        userProfileInfoObj.can_borrow = True
        userProfileInfoObj.save()

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


class BorrowProlongDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = reverse_lazy('login')
    model = models.Borrow
    context_object_name = "borrow" #w templatce
    template_name = 'library_app/borrow_confirm_prolong.html'

    def get(self, request, pk):
        borrowObj = models.Borrow.objects.get(id=pk)

        #jesli user wejdzie za pomoca linku do nie swojego wypozyczenia to wróci do listy wypożyczeń
        if borrowObj.user.id is not self.request.user.id:
            return redirect('library_app:my_borrow_list')
        else:
            context = {
                'borrow': borrowObj
            }
            return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, pk):
        borrowObj = models.Borrow.objects.get(id=pk)
        borrowObj.receive_date = borrowObj.receive_date + timedelta(days=PROLONG_DAYS)
        borrowObj.is_prolong=True
        borrowObj.save()  # zapisz wypożyczenie ze zmienioną datą
        return redirect('library_app:my_borrow_list')

########### HISTORIA WYPOŻYCZEŃ WIDOK ADMIN
class BorrowHistoryListView(LoginRequiredMixin, SuperuserRequiredMixin, generic.ListView):
    login_url = reverse_lazy('no_permission')
    model = models.BorrowHistory
    context_object_name = "borrow_history_list" 
    paginate_by = 10

    def get_queryset(self):
        search_query = self.request.GET.get("search_query")
        search_type = self.request.GET.get("search_type")
        if search_query is not None:
            if search_type == "title":
                return models.BorrowHistory.objects.filter(book_copy_id__book__title__icontains=search_query)
            elif search_type == "author":
                authors_result = models.BorrowHistory.objects.filter(book_copy_id__book__authors__first_name__icontains=search_query) | models.BorrowHistory.objects.filter(book_copy_id__book__authors__last_name__icontains=search_query)
                return authors_result
            elif search_type == "bookcopy_nr":
                return models.BorrowHistory.objects.filter(book_copy_id__id__icontains=search_query)
            elif search_type == "borrow_by_user":
                borrow_by_result = models.BorrowHistory.objects.filter(user__first_name__contains=search_query) | models.BorrowHistory.objects.filter(user__last_name__contains=search_query)
                return borrow_by_result
            elif search_type == "borrow_by_librarian":
                borrow_by_result = models.BorrowHistory.objects.filter(borrow_librarian__first_name__contains=search_query) | models.BorrowHistory.objects.filter(borrow_librarian__last_name__contains=search_query)
                return borrow_by_result
            elif search_type == "receive_by_librarian":
                borrow_by_result = models.BorrowHistory.objects.filter(receive_librarian__first_name__contains=search_query) | models.BorrowHistory.objects.filter(receive_librarian__last_name__contains=search_query)
                return borrow_by_result
        else:
            return models.BorrowHistory.objects.all()


########### WYPOŻYCZENIA WIDOK UŻYTKOWNIKA
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
        borrows_with_exceeded_date = self.get_borrows_with_exceeded_date()

        context["current_borrow_list"] = models.Borrow.objects.filter(user=self.request.user).order_by("receive_date")
        context['borrows_with_exceeded_date'] = borrows_with_exceeded_date
        context['EXCEEDED_DATE_COST_PER_DAY'] = EXCEEDED_DATE_COST_PER_DAY
        context['receivables_cost'] = self.calc_receivables_for_borrows_with_exceeded_date(borrows_with_exceeded_date)
        return context
    
    def get_borrows_with_exceeded_date(self):
        return models.Borrow.objects.filter(user=self.request.user).filter(is_date_exceeded=True).order_by("receive_date")

    def get_days_between_borrow_date_and_today(self, borrow_date_param):
        borrow_date = datetime.strptime(str(borrow_date_param), "%Y-%m-%d")
        today_date = datetime.strptime(str(date.today()), "%Y-%m-%d")
        return abs((borrow_date - today_date).days)

    def calc_receivables_for_borrows_with_exceeded_date(self, borrows):
        result = 0.0
        for borrow in borrows:
            days = self.get_days_between_borrow_date_and_today(borrow.receive_date)
            result += days * EXCEEDED_DATE_COST_PER_DAY
        return result            


############ UŻYTKOWNIK - WIDOKI DLA BIBLIOTEKARZA
class UsersListView(LoginRequiredMixin, SuperuserRequiredMixin, generic.ListView):
    login_url = reverse_lazy('no_permission')
    model = models.UserProfileInfo
    paginate_by = 10
    context_object_name = "users_profile_list" #w templatce teraz user_list zamiast user_list_set
    template_name = 'library_app/users_list.html'


class UpdateUserProfileView(LoginRequiredMixin, generic.UpdateView):
    login_url = reverse_lazy('login')

    model = models.UserProfileInfo
    form_class = forms.UserProfileInfoForm
    template_name = 'library_app/user_update_form.html'

    def get_success_url(self):
            return reverse_lazy('index')

    

class UserDetailView(LoginRequiredMixin, SuperuserRequiredMixin, generic.DetailView):
    login_url = reverse_lazy('no_permission')
    model = models.UserProfileInfo
    context_object_name = "user_profile" #w templatce teraz user_profile zamiast user_profile_set
    template_name = 'library_app/user_detail.html'

class UserBorrowsList(LoginRequiredMixin, SuperuserRequiredMixin, generic.ListView):
    login_url = reverse_lazy('no_permission')
    model = models.BorrowHistory
    context_object_name = "history_borrow_list"
    paginate_by = 10
    template_name = "library_app/user_borrows.html"

    def get_queryset(self):
        queryset = models.BorrowHistory.objects.filter(user=self.request.user)
        return queryset 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id_from_url = str(self.request.path).split('/')[3]
        user_obj = User.objects.get(id=user_id_from_url)

        borrows_with_exceeded_date = self.get_borrows_with_exceeded_date(user_obj.id)

        context['user_full_name'] = user_obj.get_full_name()
        context["current_borrow_list"] = models.Borrow.objects.filter(user__id=user_obj.id).order_by("receive_date")
        context['borrows_with_exceeded_date'] = borrows_with_exceeded_date
        context['EXCEEDED_DATE_COST_PER_DAY'] = EXCEEDED_DATE_COST_PER_DAY
        context['receivables_cost'] = self.calc_receivables_for_borrows_with_exceeded_date(borrows_with_exceeded_date)
        return context
    
    def get_borrows_with_exceeded_date(self, user_id):
        return models.Borrow.objects.filter(user__id=user_id).filter(is_date_exceeded=True).order_by("receive_date")

    def get_days_between_borrow_date_and_today(self, borrow_date_param):
        borrow_date = datetime.strptime(str(borrow_date_param), "%Y-%m-%d")
        today_date = datetime.strptime(str(date.today()), "%Y-%m-%d")
        return abs((borrow_date - today_date).days)

    def calc_receivables_for_borrows_with_exceeded_date(self, borrows):
        result = 0.0
        for borrow in borrows:
            days = self.get_days_between_borrow_date_and_today(borrow.receive_date)
            result += days * EXCEEDED_DATE_COST_PER_DAY
        return result 

class UserGrantDetailView(LoginRequiredMixin, SuperuserRequiredMixin, generic.DetailView):
    login_url = reverse_lazy('no_permission')
    model = models.UserProfileInfo
    context_object_name = "user_profile" #w templatce teraz user_profile zamiast user_profile_set
    template_name = 'library_app/user_grant.html'

    #gdy dajemy post w formularzu (klikniecie w nadaj) to nadaj userowi, superuser
    def post(self, request, pk):
        userProfileInfoObj = models.UserProfileInfo.objects.get(id=pk)
        userProfileInfoObj.user.is_superuser = True
        userProfileInfoObj.user.save() #zapisz usera
        return redirect('library_app:users_list')


class UserGetRightsDetailView(LoginRequiredMixin, SuperuserRequiredMixin, generic.DetailView):
    login_url = reverse_lazy('no_permission')
    model = models.UserProfileInfo
    # w templatce teraz user_profile zamiast user_profile_set
    context_object_name = "user_profile"
    template_name = 'library_app/user_get_rights.html'

    #gdy dajemy post w formularzu (klikniecie w nadaj) to nadaj userowi, superuser
    def post(self, request, pk):
        userProfileInfoObj = models.UserProfileInfo.objects.get(id=pk)
        userProfileInfoObj.user.is_superuser = False
        userProfileInfoObj.user.save()  # zapisz usera
        return redirect('library_app:users_list')

class UserActivateDetailView(LoginRequiredMixin, SuperuserRequiredMixin, generic.DetailView):
    login_url = reverse_lazy('no_permission')
    model = models.UserProfileInfo
    # w templatce teraz user_profile zamiast user_profile_set
    context_object_name = "user_profile"
    template_name = 'library_app/user_activate.html'

    #gdy dajemy post w formularzu (klikniecie w nadaj) to nadaj userowi, superuser
    def post(self, request, pk):
        userProfileInfoObj = models.UserProfileInfo.objects.get(id=pk)
        userProfileInfoObj.user.is_active = True
        userProfileInfoObj.user.save()  # zapisz usera
        return redirect('library_app:users_list')


class UserDeactivateDetailView(LoginRequiredMixin, SuperuserRequiredMixin, generic.DetailView):
    login_url = reverse_lazy('no_permission')
    model = models.UserProfileInfo
    # w templatce teraz user_profile zamiast user_profile_set
    context_object_name = "user_profile"
    template_name = 'library_app/user_deactivate.html'

    #gdy dajemy post w formularzu (klikniecie w nadaj) to nadaj userowi, superuser
    def post(self, request, pk):
        userProfileInfoObj = models.UserProfileInfo.objects.get(id=pk)
        userProfileInfoObj.user.is_active = False
        userProfileInfoObj.user.save()  # zapisz usera
        return redirect('library_app:users_list')



############# PROFIL USERA
class UpdateMyProfileView(LoginRequiredMixin, generic.UpdateView):
    login_url = reverse_lazy('login')

    model = models.UserProfileInfo
    form_class = forms.UserProfileInfoForm
    template_name = 'library_app/my_profile_update_form.html'

    def get_success_url(self):
            return reverse('index')


class MyProfileTemplateView(LoginRequiredMixin, generic.TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'library_app/my_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_profile"] = models.UserProfileInfo.objects.get(user=self.request.user)
        return context


class MyProfileStatisticsTemplateView(LoginRequiredMixin, generic.TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'library_app/my_statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        borrowHistoryObj = models.BorrowHistory.objects.filter(user=self.request.user)

        context["borrows_per_month_chart_data"] = self.get_borrows_per_months_data(borrowHistoryObj)
        return context

    def get_borrows_per_months_data(self, borrow_history_obj):
        months_counter = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for borrow in borrow_history_obj:
            if(str(borrow.receive_date).split('-')[0] == str(datetime.now().year)): #tylko z biezacego roku
                months_counter_index = int(str(borrow.receive_date).split('-')[1].strip('0'))-1
                months_counter[months_counter_index] +=1
        
        return months_counter





    
