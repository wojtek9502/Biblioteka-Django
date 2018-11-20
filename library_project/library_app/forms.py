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

        
        #stworz liste id userów którzy maja w UserProfileInfo.can_borrow = True
        borrow_allowed_users_ids = []
        for user_obj in User.objects.all():
            userProfileObj = models.UserProfileInfo.objects.get(user=user_obj.id)
            if(userProfileObj.can_borrow == True):
                borrow_allowed_users_ids.append(user_obj.id)

        users = User.objects.filter(pk__in=borrow_allowed_users_ids)  # wez userow których id znajduje się w borrow_allowed_users_ids
        self.fields['user'].choices = [(user.pk, get_user_info_for_field(user)) for user in users]

    class Meta:
        model = models.Borrow
        fields = ('user', 'book_copy_id', 'receive_date')


def get_user_info_for_field(user_obj):
    userProfileObj = models.UserProfileInfo.objects.get(user=user_obj.id)
    return user_obj.get_full_name() + ', PESEL: ' + userProfileObj.pesel
