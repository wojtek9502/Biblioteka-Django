from django import template
from library_app import models
from datetime import datetime, date

register = template.Library()


@register.simple_tag(name='free_bookcopies_counter_tag')
def free_bookcopies_counter(bookcopies_obj):
    return bookcopies_obj.filter(is_borrowed=False).count()

#zwraca obiekt wypozyczenia dla danej kopii
@register.simple_tag(name='get_bookcopy_borrow')
def get_bookcopy_borrow(p_book_copy_id):
    borrows = models.Borrow.objects.all().filter(book_copy_id=p_book_copy_id)
    if(borrows.count() == 1):
        return borrows[0]
    else:
        return None

# zwraca liczbe wypozyczonych przez usera kopii
@register.simple_tag(name='get_borrow_by_user_count')
def get_borrow_by_user_count(user_obj):
    return models.Borrow.objects.filter(user=user_obj).count()

# zwraca wypozyczone przez usera ksiazki
@register.simple_tag(name='get_borrow_by_user')
def get_borrow_by_user(user_obj):
    return models.Borrow.objects.filter(user=user_obj)

# zwraca id_profilu usera na podstawie obietu usera
@register.simple_tag(name='get_user_profile')
def get_user_profile(user_obj):
    return models.UserProfileInfo.objects.get(user=user_obj)

# zwraca kwote do zapłaty za nieoddaną książkę
# calc_receivable_for_bookcopy
@register.simple_tag(name='calc_receivable_for_bookcopy')
def calc_receivable_for_bookcopy(bookcopy_obj, cost_per_day):
    days_delta = get_days_between_borrow_date_and_today(bookcopy_obj.receive_date)
    return days_delta * cost_per_day


def get_days_between_borrow_date_and_today(borrow_date_param):
    borrow_date = datetime.strptime(str(borrow_date_param), "%Y-%m-%d")
    today_date = datetime.strptime(str(date.today()), "%Y-%m-%d")
    return abs((borrow_date - today_date).days)

# zwraca liczbe dni spóżnienia w oddaniu książki
@register.simple_tag(name='calc_bookcopy_receive_delay')
def calc_bookcopy_receive_delay(bookcopy_obj):
    return get_days_between_borrow_date_and_today(bookcopy_obj.receive_date)


#zwraca czy użytkownik ma jakieś wypożyczenia nie oddane w terminie
@register.simple_tag(name='have_any_borrows_with_exceeded_receive_date')
def have_any_borrows_with_exceeded_receive_date(user_obj):
    for borrow in models.Borrow.objects.filter(user=user_obj):
        if borrow.is_date_exceeded:
            return True
    return False


#zwraca liczbe książek autora
@register.simple_tag(name='get_authors_book_count')
def get_authors_book_count(author_obj):
      return models.Book.objects.filter(authors=author_obj).count()


#zwraca liczbe ksiazek w danej kategorii
@register.simple_tag(name='get_categories_book_count')
def get_categories_book_count(category_obj):
      return models.Book.objects.filter(category=category_obj).count()

#zwraca liczbe ksiażek danego wydawnictwa
@register.simple_tag(name='get_publishing_house_book_count')
def get_publishing_house_book_count(publishing_house_obj):
      return models.Book.objects.filter(publishing_house=publishing_house_obj).count()

