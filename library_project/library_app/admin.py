from django.contrib import admin
from library_app import models

# Register your models here.
# class BookAdmin(admin.ModelAdmin):
#     list_display = ('title','show_authors','slug','isbn','category','edition','publishing_house','publish_date',)
#     search_fields = ('title', 'authors')
#     raw_id_fields = ('authors', 'category', 'publishing_house')
#     prepopulated_fields = {"slug": ("title",)}

#     def show_authors(self, obj):
#         return ", ".join([author_entry.last_name for author_entry in obj.authors.all()]) #zwroc , <nazwisko autora> dla kazdego autora w ksiazce
#     show_authors.short_description = 'Authors'

# admin.site.register(models.Book, BookAdmin)
# admin.site.register(models.BookCopy)
# admin.site.register(models.Author)
# admin.site.register(models.Category)
# admin.site.register(models.PublishingHouse)
# admin.site.register(models.Borrow)
# admin.site.register(models.BorrowHistory)


class UserProfileInfoAdmin(admin.ModelAdmin):
    exclude = ('user', 'pesel')

admin.site.register(models.UserProfileInfo, UserProfileInfoAdmin)
