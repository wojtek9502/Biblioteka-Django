from django import forms

from library_app import models

class BookForm(forms.ModelForm):
    class Meta:
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
        model = models.Book


class AuthorForm(forms.ModelForm):
    class Meta:
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
        model = models.Author