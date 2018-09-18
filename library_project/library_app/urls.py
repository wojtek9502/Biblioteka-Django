from django.conf.urls import url
from library_app import views

app_name = 'library_app' #uzywane w navbar w base.html
urlpatterns = [
    url(r'^book_list/$',views.BookListView.as_view(),name='book_list'),
    url(r'^book_list/book_detail/(?P<pk>\d+)/$', views.BookDetailView.as_view(), name='book_detail'),
    url(r'^new_book/$', views.CreateBookView.as_view(), name='book_create'),
    url(r'^authors/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author_detail'),
    url(r'^new_author/$', views.CreateAuthorView.as_view(), name='author_create'),

]