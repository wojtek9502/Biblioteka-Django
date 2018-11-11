from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta

# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()

class Category(models.Model):
    category_name = models.CharField(max_length=400, unique=True, verbose_name='Nazwa kategorii')

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse('library_app:category_detail', kwargs={"pk": str(self.pk)})
    

class Author(models.Model):
    first_name = models.CharField(max_length=200, verbose_name='Imię')
    last_name = models.CharField(max_length=200, verbose_name='Nazwisko')
    country = models.CharField(max_length=200, verbose_name='Kraj')
    biography = models.TextField(default='', blank=True, null=True, verbose_name='Biografia')
    birth_place = models.CharField(max_length=200, default='', blank=True, null=True, verbose_name='Miejsce urodzenia')
    image_url = models.URLField(default='', blank=True, null=True, verbose_name='Adres url portretu, zakończony rozszerzeniem')
    years_of_life = models.CharField(max_length=10, default='', blank=True, null=True, verbose_name='Lata życia')

    def get_absolute_url(self):
        return reverse('library_app:author_detail', kwargs={"pk": str(self.pk)})

    def __str__(self):
        return self.last_name + " " + self.first_name
    

class PublishingHouse(models.Model):
    name = models.CharField(max_length=400, unique=True, verbose_name='Nazwa')
    city = models.CharField(max_length=300, verbose_name='Miasto')
    street = models.CharField(max_length=300, verbose_name='Ulica')
    house_number = models.CharField(max_length=20, verbose_name='Numer domu')
    postal_code = models.CharField(max_length=9, verbose_name='Kod pocztowy')

    def get_absolute_url(self):
        return reverse('library_app:publishinghouse_detail', kwargs={"pk": str(self.pk)})

    def __str__(self):
        return self.name
    

class Book(models.Model):
    authors = models.ManyToManyField(Author, related_name='book_authors', verbose_name='Autorzy')
    category = models.ForeignKey(Category, related_name='book_categories', verbose_name='Kategoria')
    publishing_house = models.ForeignKey(PublishingHouse, related_name='publishing_houses', verbose_name='Wydawnictwo')
    isbn = models.CharField(max_length=30, unique=True, verbose_name='Numer ISBN')
    title = models.CharField(max_length=200, verbose_name='Tytuł')
    description = models.TextField(blank=True, default='', verbose_name='Opis')
    publish_date = models.DateField(default=datetime.now, blank=True, verbose_name='Data publikacji')
    edition = models.PositiveIntegerField(default=1, verbose_name='Numer wydania')
    image_url = models.URLField(default='', blank=True, null=True, verbose_name='Adres url okładki zakończony rozszerzeniem obrazu')
    add_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(allow_unicode=True, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.isbn)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('library_app:book_detail', kwargs={"pk": str(self.pk)})

class BookCopy(models.Model):
    book = models.ForeignKey(Book, related_name="bookcopies", verbose_name='Wybierz książkę') #teraz w templatce mozemy z poziomu klasy book odnosic sie do obiektow bookcopy, np {{book.bookcopies.count}} da liczbe kopii ksiazek ktore maja w polu book id danej ksiazki
    is_borrowed = models.BooleanField(default=False)

   
    def __str__(self):
        return self.book.title + ', ISBN: ' + str(self.book.isbn) + ', nr egzemplarza: ' + str(self.id)
    
    def get_absolute_url(self):
        return reverse('library_app:bookcopy_detail', kwargs={"pk": str(self.pk)})
    

class Borrow(models.Model):
    user = models.ForeignKey(User, verbose_name='Wypożycz dla')
    borrow_librarian = models.ForeignKey(User, related_name="borrow_librarian", verbose_name='Bibliotekarz wypożyczający')
    receive_librarian = models.ForeignKey(User, related_name="receive_librarian", null=True, blank=True, verbose_name='Bibliotekarz odbierający')
    book_copy_id = models.ForeignKey(BookCopy, related_name="borrow_bookcopy", verbose_name='Egzemplarz ksiązki')
    borrow_date = models.DateField(auto_now=True, verbose_name='Data wypożyczenia')
    receive_date = models.DateField(default=datetime.now()+timedelta(days=60), verbose_name='Data oddania')
    is_prolong = models.BooleanField(default=False)
    is_date_exceeded = models.BooleanField(default=False)

    def __str__(self):
        return "user=" + self.user.username + " book= " + str(self.book_copy_id) 

class BorrowHistory(models.Model):
    user = models.ForeignKey(User, related_name="history_user")
    borrow_librarian = models.ForeignKey(User, related_name="history_borrow_librarian")
    receive_librarian = models.ForeignKey(User, related_name="history_receive_librarian", null=True, blank=True)
    book_copy_id = models.ForeignKey(BookCopy)
    borrow_date = models.DateField()
    receive_date = models.DateField()
    
    def __str__(self):
        return "history_borrow user=" + self.user.username + " book= " + str(self.book_copy_id) 

    
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,verbose_name='Użytkownik', related_name='user_profile')
    pesel = models.CharField(max_length=11, verbose_name='PESEL')
    street = models.CharField(max_length=200, verbose_name='Ulica')
    city = models.CharField(max_length=200, verbose_name='Miasto')
    phone = models.CharField(max_length=20, verbose_name='Telefon')
    post_code = models.CharField(max_length=6, verbose_name='Kod pocztowy')
    house_number = models.CharField(max_length=20, verbose_name='Numer domu')
    can_borrow = models.BooleanField(default=True, verbose_name='Czy może wypożyczać?')

    def __str__(self):
        return self.user.get_full_name() + ',  PESEL: ' + self.pesel
