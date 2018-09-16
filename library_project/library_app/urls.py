from django.conf.urls import url
from library_app import views

app_name = 'library_app' #uzywane w navbar w base.html
urlpatterns = [
    url(r'^book_list/$',views.BookListView.as_view(),name='book_list'),
    url(r'^book_list/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book_detail'),
]