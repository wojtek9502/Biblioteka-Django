from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse

# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=400)

    def __str__(self):
        return self.name
    

class Author(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    biography = models.TextField(default='', blank=True, null=True)
    birth_place = models.CharField(max_length=200, default='', blank=True, null=True)
    image_url = models.URLField(default='', blank=True, null=True)
    years_of_life = models.CharField(max_length=10, default='', blank=True, null=True)


    def __str__(self):
        return self.last_name + " " + self.first_name
    

class PublishingHouse(models.Model):
    name = models.CharField(max_length=400)
    city = models.CharField(max_length=300)
    street = models.CharField(max_length=300)
    house_number = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=9)

    def __str__(self):
        return self.name
    

class Book(models.Model):
    authors = models.ManyToManyField(Author, related_name='book_authors')
    category = models.ForeignKey(Category, related_name='book_categories')
    publishing_house = models.ForeignKey(PublishingHouse, related_name='publishing_houses')
    isbn = models.CharField(max_length=30, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    publish_date = models.DateField(auto_now=False)
    edition = models.IntegerField(default=1)
    image_url = models.URLField(default='', blank=True, null=True)
    is_borrowed = models.BooleanField(default=False)
    slug = models.SlugField(allow_unicode=True, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_single', kwargs={"slug": self.slug})

class BookCopy(models.Model):
    book = models.ForeignKey(Book)
   
    def __str__(self):
        return self.book.title + ' copy_nr= ' + str(self.id)
    

class Borrow(models.Model):
    user = models.ForeignKey(User)
    book_copy_id = models.ForeignKey(BookCopy)
    borrow_date = models.DateField(auto_now=True)
    receive_date = models.DateField(auto_now=False, blank=True, null=True )

    def __str__(self):
        return "user=" + self.user.username + " book= " + str(self.book_copy_id) 

    