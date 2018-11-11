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
                for borrow in models.Borrow.objects.all():
                    userProfileInfo = models.UserProfileInfo.objects.get(user=borrow.user)

                    if is_bookcopy_receive_date_exceeded(borrow):
                        if borrow.is_date_exceeded == False:
                            mark_bookcopy_as_exceeded(borrow)
                            self.stdout.write("Egzemplarz nr %s oznaczony jako nieoddany w terminie" %
                                              str(borrow.book_copy_id.id) )

                    if userProfileInfo.can_borrow == True:
                        change_user_can_borrow(userProfileInfo)
                        self.stdout.write("Użytkownik %s stacił prawa do wypożyczania" % borrow.user.get_full_name())
            except Exception as e:
                raise CommandError(repr(e))


#sprawdza czy data oddania egzemplarza > dzisiejsza data
def is_bookcopy_receive_date_exceeded(borrow):
    borrow_date = datetime.strptime(str(borrow.receive_date), "%Y-%m-%d")
    today_date = datetime.strptime(str(date.today()), "%Y-%m-%d")
    if borrow_date > today_date:
        return False
    else:
        return True


#oznacza wypożyczenie jako przekroczone
def mark_bookcopy_as_exceeded(borrow):
    borrow.is_date_exceeded = True
    borrow.save()

#oznacza w profilu użytkownika flage 'can_borrow'
def change_user_can_borrow(userProfileInfo):
    userProfileInfo.can_borrow = False  # ustaw flage
    userProfileInfo.save()
