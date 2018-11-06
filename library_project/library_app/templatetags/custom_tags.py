from django import template
from library_app import models

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
