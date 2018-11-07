from django import forms
from library_app import models
from django.contrib.auth.models import User

class BookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = ('authors', 'category', 'publishing_house', 'isbn', 'title', 'description',
                  'publish_date', 'edition', 'image_url')
        error_messages = {
            'isbn': {
                'unique': ("Istnieje już książka o takim numerze ISBN"),
            },
        }
        


class BookCopyForm(forms.ModelForm):
    class Meta:
        model = models.BookCopy
        fields = ('book',)
        


class AuthorForm(forms.ModelForm):
    class Meta:
        model = models.Author
        fields = ('first_name', 'last_name', 'country', 'biography', 'birth_place', 'image_url',
                  'years_of_life')
        

class PublishingHouseForm(forms.ModelForm):
    class Meta:
        model = models.PublishingHouse
        fields = ('name', 'city', 'street', 'house_number', 'postal_code')
        error_messages = {
            'name': {
                'unique': ("Istnieje już wydawnictwo o takiej nazwie"),
            },
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ('category_name',)
        error_messages = {
            'category_name': {
                'unique': ("Istnieje już kategoria o takiej nazwie"),
            },
        }


class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = models.UserProfileInfo
        fields = ('street', 'house_number', 'post_code', 'city', 'phone')


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

