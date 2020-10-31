from django.urls import path
from backend.views import CurrenciesList, GetCurrency

urlpatterns = [
    path('currencies_list', CurrenciesList.as_view()),
    path('currency=<str:currency>&date1=<str:date1>&date2=<str:date2>', GetCurrency.as_view()),
]
