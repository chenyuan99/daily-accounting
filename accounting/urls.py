from django.urls import path, include
from django.conf.urls import url

from .views import TransferRecordViewSet, UserViewSet, GroupViewSet, PhotoViewSet, AccountViewSet, CurrencyViewSet
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'photos', PhotoViewSet)
router.register(r'transferrecords', TransferRecordViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'currencys', CurrencyViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('retrieve_category/', views.retrieve_category, name='retrieve_category'),
    path('retrieve_subcategory/', views.retrieve_subcategory, name='retrieve_subcategory'),
    path('record_income_expense/', views.record_income_expense, name='record_income_expense'),
    path('retrieve_current_month_income_expense/', views.retrieve_current_month_income_expense,
         name='retrieve_current_month_income_expense'),
    path('retrieve_current_year_income_expense/', views.retrieve_current_year_income_expense,
         name='retrieve_current_year_income_expense'),
    path('retrieve_year_has_data/', views.retrieve_year_has_data, name='retrieve_year_has_data'),
    path('retrieve_month_has_data/', views.retrieve_month_has_data, name='retrieve_month_has_data'),
    path('search_record/', views.search_record, name='search_record'),
    path('filter_record_by_date/', views.filter_record_by_date, name='filter_record_by_date'),
    path('transfer-between-accounts/', views.transfer_between_accounts, name='transfer_between_accounts'),

    # Dashboard

    path('pc/dashboard', views.page_demo, name='pc/dashboard'),
    path('pc/dashboard/categoryList', views.display_categoryList, name='pc/dashboard/categoryList'),
    path('pc/dashboard/accountList', views.display_accountList, name='pc/dashboard/accountList'),
    path('pc/dashboard/billList', views.page_demo, name='pc/dashboard/billList'),
    url(r'^page_demo/', views.page_demo),
    path("register/", views.register, name="register"),
    # logitistics
    path("legacy", views.legacy, name="legacy"),
    path("about", views.about, name="about"),
    path("faq", views.faq, name="faq"),
    path("privacy-policy", views.privacy, name="privacy-policy"),

    # api
    path('api/', include(router.urls)),
]
