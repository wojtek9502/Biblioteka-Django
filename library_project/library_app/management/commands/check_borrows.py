#Skrypt sprawdza wszystkie wypożyczenia
#jesli data oddania wypożyczenia > data obecna skrypt oznacza wypożyczenie jako 
# spóżnione, a użytkownikowi blokuje możliwość wypożyczania

from django.core.management.base import BaseCommand, CommandError
from library_app import models
from datetime import datetime, date

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
            try:
                print("Sprawdzam daty wypozyczen")
                for borrow in models.Borrow.objects.all():
                
                    if borrow.is_date_exceeded == False:
                        userProfileInfo = models.UserProfileInfo.objects.get(user=borrow.user)
                        
                        if is_bookcopy_receive_date_exceeded(borrow):
                            mark_bookcopy_as_exceeded(self, borrow)
                            change_user_can_borrow(self, userProfileInfo)
                print("Gotowe")
                        
            except Exception as e:
                raise CommandError(repr(e))


#sprawdza czy data oddania egzemplarza > dzisiejsza data
def is_bookcopy_receive_date_exceeded(borrow):
    borrow_date = datetime.strptime(str(borrow.receive_date), "%Y-%m-%d")
    today_date = datetime.strptime(str(date.today()), "%Y-%m-%d")
    date_delta = (borrow_date - today_date).days

    if date_delta >= 0:
        return False
    else:
        return True


#oznacza wypożyczenie jako przekroczone
def mark_bookcopy_as_exceeded(command_obj, borrow):
    borrow.is_date_exceeded = True
    borrow.save()
    command_obj.stdout.write("Egzemplarz nr %s oznaczony jako nieoddany w terminie" %
                      str(borrow.book_copy_id.id))

#oznacza w profilu użytkownika flage 'can_borrow'
def change_user_can_borrow(command_obj, userProfileInfo):
    userProfileInfo.can_borrow = False  # ustaw flage
    userProfileInfo.save()
    command_obj.stdout.write("Uzytkownik %s posiada książki nie oddane w terminie, nie moze wypożyczać" %
                             str(userProfileInfo.user.get_full_name()) )
