from rest_framework.views import APIView
from rest_framework.response import Response
from backend.currency_functions import get_all_currencies, get_difference_between_currencies


class CurrenciesList(APIView):
    """Получение всех валют в формате ("character_code": символьный код валюты, "name": название валюты)"""
    def get(self, request):
        currency_list = get_all_currencies()
        return Response(currency_list)


class GetCurrency(APIView):
    """
        Получения курса валюты относительно рубля в формате ("currency_for_first_date": курс за первую дату,
        "currency_for_second_date": курс за вторую дату, "difference": разницу в единицах,
        "difference_in_percentage": разницу в процентах)
    """
    def get(self, request, currency, date1, date2):
        currency = get_difference_between_currencies(char_code=currency, first_date=date1, second_date=date2)
        return Response(currency)
