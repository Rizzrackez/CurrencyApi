import xml.etree.ElementTree as ET
import requests
import time

from . import _currency_data


def _get_currency_by_date(date, char_code):
    """
    Принимает символьный код валюты (USD) и дату в формате (DD/MM/YYYY).
    Возвращает курс валюты относительно рубля на указанную дату.
    """
    url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}"
    r = requests.get(url)

    currency_tree = ET.fromstring(r.text)

    value_of_currency = [currency.findtext('Value') for currency in currency_tree if currency.findtext('CharCode') == char_code]

    if value_of_currency:
        value_of_currency = float(value_of_currency[0].replace(',', '.'))

    return value_of_currency


def get_all_currencies():
    """Возвращает список всех валют в формате ({"character_code": символьный код ISO, "name": Название валюты})"""
    all_currencies = _currency_data.CURRENCIES_LIST
    return all_currencies


def get_difference_between_currencies(char_code, first_date, second_date):
    """
        Принимает символьный код валюты (USD) и 2 даты в формате (YYYY-MM-DD).
        Возвращает курс валюты относительно рубля на указанные даты и разницу между ними в единицах и процентах.
    """
    difference_between_currencies, difference_between_currencies_in_percentages = None, None

    try:
        date_1, date_2 = "/".join(first_date.split('-')[::-1]), "/".join(second_date.split('-')[::-1])
        time.strptime(date_1, '%m/%d/%Y')
        time.strptime(date_2, '%m/%d/%Y')

    except ValueError:
        date_1, date_2 = None, None

    if date_1 is not None and char_code in _currency_data.CURRENCIES_CHAR_CODES:
        first_currency_by_date, second_currency_by_date = _get_currency_by_date(date_1, char_code), _get_currency_by_date(date_2, char_code)
        difference_between_currencies = abs(float("%.2f" % (first_currency_by_date - second_currency_by_date)))
        difference_between_currencies_in_percentages = abs(float("%.1f" % (100 * (second_currency_by_date - first_currency_by_date) / first_currency_by_date)))

    else:
        first_currency_by_date, second_currency_by_date = None, None

    currency = {f"currency_for_first_date": first_currency_by_date,
                f"currency_for_second_date": second_currency_by_date,
                "difference": difference_between_currencies,
                "difference_in_percentage": difference_between_currencies_in_percentages}

    return currency
