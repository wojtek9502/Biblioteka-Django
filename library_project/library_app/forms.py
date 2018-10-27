from django import forms
from library_app import models
from django.contrib.auth.models import User

class BookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = ('authors', 'category', 'publishing_house', 'isbn', 'title', 'description',
                  'publish_date', 'edition', 'image_url')
        labels = {
            'authors': 'Autorzy',
            'category':'Kategoria',
            'publishing_house':'Wydawnictwo',
            'title':'Tytuł',
            'description':'Opis',
            'isbn':'ISBN',
            'publish_date':'Data publikacji (DD.MM.YYYY)',
            'edition':'Wydanie',
            'image_url':'Adres url okładki',
        }


class BookCopyForm(forms.ModelForm):
    class Meta:
        model = models.BookCopy
        fields = ('book','is_borrowed')
        labels = {
            'book': 'Książka',
            'is_borrowed': 'Czy wypożyczona?'
        }
        


class AuthorForm(forms.ModelForm):
    class Meta:
        model = models.Author
        fields = ('first_name', 'last_name', 'country', 'biography', 'birth_place', 'image_url',
                  'years_of_life')

        labels = {
            'first_name':'Imię',
            'last_name':'Nazwisko',
            'country':'Narodowość',
            'biography':'Biografia',
            'birth_place':'Miejsce urodzenia',
            'image_url':'Adres url portretu autora',
            'years_of_life':'Lata życia',
        }
        

class PublishingHouseForm(forms.ModelForm):
    class Meta:
        model = models.PublishingHouse
        fields = ('name', 'city', 'street', 'house_number', 'postal_code')

        labels = {
            'name':'Nazwa',
            'city':'Miasto',
            'street':'Ulica',
            'house_number':'Nr domu',
            'postal_code':'Kod pocztowy',
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ('category_name',)

        labels = {
            'category_name':'Kategoria',
        }


class BorrowForm(forms.ModelForm):
    ## w formularzu daj do wyboru tylko niewypozyczone egzemplarze
    def __init__(self, *args, **kwargs):
        super(BorrowForm, self).__init__(*args, **kwargs)  # wywolaj formularz najpierw żeby ustawić mu pola fields
        self.fields['book_copy_id'].queryset = models.BookCopy.objects.filter(is_borrowed=False)
        
        #wyswietl w polu user formularza, jego imie i nazwisko zamiast loginu
        users = User.objects.all()
        self.fields['user'].choices = [(user.pk, user.get_full_name()) for user in users]

    class Meta:
        model = models.Borrow
        fields = ('user', 'book_copy_id', 'receive_date')
        

        labels = {
            'user': 'Wypożycz dla',
            'book_copy_id': 'Kopia książki',
            'receive_date': 'Data oddania',
        }

