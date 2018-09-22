from django.conf.urls import url
from library_app import views

app_name = 'library_app' #uzywane w navbar w base.html
urlpatterns = [
    url(r'^book_list/$',views.BookListView.as_view(),name='book_list'),
    url(r'^book_list/book_detail/(?P<pk>\d+)/$', views.BookDetailView.as_view(), name='book_detail'),
    url(r'^new_book/$', views.CreateBookView.as_view(), name='book_create'),
    url(r'^update_book/(?P<pk>\d+)/$', views.UpdateBookView.as_view(), name='book_update'),
    url(r'^delete_book/(?P<pk>\d+)/$', views.DeleteBookView.as_view(), name='book_delete'),

    url(r'^authors/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author_detail'),
    url(r'^new_author/$', views.CreateAuthorView.as_view(), name='author_create'),
    url(r'^update_author/(?P<pk>\d+)/$', views.UpdateAuthorView.as_view(), name='author_update'),
    url(r'^delete_author/(?P<pk>\d+)/$', views.DeleteAuthorView.as_view(), name='author_delete'),

    url(r'^publishing_house/(?P<pk>\d+)$', views.PublishingHouseDetailView.as_view(), name='publishinghouse_detail'),
    url(r'^publishing_house/$', views.CreatePublishingHouseView.as_view(), name='publishinghouse_create'),
    url(r'^delete_publishing_house/(?P<pk>\d+)/$', views.DeletePublishingHouseView.as_view(), name='publishinghouse_delete'),
    url(r'^update_publishing_house/(?P<pk>\d+)/$', views.UpdatePublishingHouseView.as_view(), name='publishinghouse_update'),
]