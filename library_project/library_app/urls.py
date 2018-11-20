from django.conf.urls import url
from library_app import views

app_name = 'library_app' #uzywane w navbar w base.html
urlpatterns = [
    url(r'^book_list/$',views.BookListView.as_view(),name='book_list'),
    url(r'^book_detail/(?P<pk>\d+)/$', views.BookDetailView.as_view(), name='book_detail'),
    url(r'^new_book/$', views.CreateBookView.as_view(), name='book_create'),
    url(r'^update_book/(?P<pk>\d+)/$', views.UpdateBookView.as_view(), name='book_update'),
    url(r'^delete_book/(?P<pk>\d+)/$', views.DeleteBookView.as_view(), name='book_delete'),

    url(r'^book_copy_list/$', views.BookCopyListView.as_view(), name='bookcopy_list'),
    url(r'^bookcopy_detail/(?P<pk>\d+)/$', views.BookCopyDetailView.as_view(), name='bookcopy_detail'),
    url(r'^new_bookcopy/$', views.CreateBookCopyView.as_view(), name='bookcopy_create'),
    url(r'^update_bookcopy/(?P<pk>\d+)/$', views.UpdateBookCopyView.as_view(), name='bookcopy_update'),
    url(r'^delete_bookcopy/(?P<pk>\d+)/$', views.DeleteBookCopyView.as_view(), name='bookcopy_delete'),


    url(r'^authors/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author_detail'),
    url(r'^new_author/$', views.CreateAuthorView.as_view(), name='author_create'),
    url(r'^update_author/(?P<pk>\d+)/$', views.UpdateAuthorView.as_view(), name='author_update'),
    url(r'^delete_author/(?P<pk>\d+)/$', views.DeleteAuthorView.as_view(), name='author_delete'),

    url(r'^publishing_house/(?P<pk>\d+)$', views.PublishingHouseDetailView.as_view(), name='publishinghouse_detail'),
    url(r'^new_publishing_house/$', views.CreatePublishingHouseView.as_view(), name='publishinghouse_create'),
    url(r'^delete_publishing_house/(?P<pk>\d+)/$', views.DeletePublishingHouseView.as_view(), name='publishinghouse_delete'),
    url(r'^update_publishing_house/(?P<pk>\d+)/$', views.UpdatePublishingHouseView.as_view(), name='publishinghouse_update'),

    url(r'^category/(?P<pk>\d+)$', views.CategoryDetailView.as_view(), name='category_detail'),
    url(r'^new_category/$', views.CreateCategoryView.as_view(), name='category_create'),
    url(r'^delete_category/(?P<pk>\d+)/$', views.DeleteCategoryView.as_view(), name='category_delete'),
    url(r'^update_category/(?P<pk>\d+)/$', views.UpdateCategoryView.as_view(), name='category_update'),

    url(r'^borrow_list/$', views.BorrowListView.as_view(), name='borrow_list'),
    url(r'^borrow/(?P<pk>\d+)/$', views.BorrowDetailView.as_view(), name='borrow_detail'),
    url(r'^delete_borrow/(?P<pk>\d+)/$', views.DeleteBorrowView.as_view(), name='borrow_delete'),
    url(r'^update_borrow/(?P<pk>\d+)/$', views.UpdateBorrowView.as_view(), name='borrow_update'),
    url(r'^borrow_prolong/(?P<pk>\d+)/$', views.BorrowProlongDetailView.as_view(), name='borrow_prolong'),
    
    url(r'^new_borrow_search_bookcopy/$', views.BorrowBookCopySearchBookCopy.as_view(), name='borrow_create_search_bookcopy'),
    url(r'^new_borrow/$', views.CreateBorrowView.as_view(), name='borrow_create'),

    url(r'^borrow_history_list/$', views.BorrowHistoryListView.as_view(), name='borrow_history_list'),

    url(r'^my_borrow_list/$', views.MyBorrowListView.as_view(), name='my_borrow_list'),
    url(r'^my_profile_update/(?P<pk>\d+)/$', views.UpdateMyProfileView.as_view(), name='my_profile_update'),
    url(r'^my_profile/', views.MyProfileTemplateView.as_view(), name='my_profile'),
    url(r'^my_statistics/', views.MyProfileStatisticsTemplateView.as_view(), name='my_statistics'),

    url(r'^users_list/$', views.UsersListView.as_view(), name='users_list'),
    url(r'^user_profile/(?P<pk>\d+)/$', views.UserDetailView.as_view(), name='user_profile'),
    url(r'^user_grant/(?P<pk>\d+)/$', views.UserGrantDetailView.as_view(), name='user_grant'),
    url(r'^user_activate/(?P<pk>\d+)/$', views.UserActivateDetailView.as_view(), name='user_activate'),
    url(r'^user_deactivate/(?P<pk>\d+)/$', views.UserDeactivateDetailView.as_view(), name='user_deactivate'),
    url(r'^get_rights/(?P<pk>\d+)/$', views.UserGetRightsDetailView.as_view(), name='get_rights'),
    url(r'^user_borrows/(?P<pk>\d+)/$', views.UserBorrowsList.as_view(), name='user_borrows'),


]
