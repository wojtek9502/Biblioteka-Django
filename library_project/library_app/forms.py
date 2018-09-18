from django import forms

from library_app import models

class BookForm(forms.ModelForm):
    class Meta:
        fields = ('authors', 'category', 'publishing_house', 'isbn', 'title', 'description',
                  'publish_date', 'edition', 'image_url')
        model = models.Book


class AuthorForm(forms.ModelForm):
    class Meta:
        fields = ('first_name', 'last_name', 'country', 'biography', 'birth_place', 'image_url',
                  'years_of_life')
        model = models.Author