import xml.etree.ElementTree as ET
import requests
import time


def _get_currency_tree():
    """Возвращает список всех валют со всей их информацией"""
    r = requests.get('http://www.cbr.ru/scripts/XML_valFull.asp')
    currency_tree = ET.fromstring(r.text)

    all_currencies = [({"Name": item.findtext('Name'),
                      "Nominal": item.findtext('Nominal'),
                      "ParentCode": item.findtext('ParentCode').replace(' ', ''),
                      "ISO_Num_Code": item.findtext('ISO_Num_Code'),
                      "ISO_Char_Code": item.findtext('ISO_Char_Code')}) for item in currency_tree if item.findtext('ISO_Char_Code')]

    return all_currencies


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
    currency_tree = _get_currency_tree()
    all_currency = [{"character_code": currency["ISO_Char_Code"], "name": currency["Name"]} for currency in currency_tree]

    return all_currency


def get_difference_between_currencies(char_code, first_date, second_date):
    """
        Принимает символьный код валюты (USD) и 2 даты в формате (YYYY-MM-DD).
        Возвращает курс валюты относительно рубля на указанные даты и разницу между ними в единицах и процентах.
    """
    difference_between_currencies, difference_between_currencies_in_percentages = None, None
    date_1, date_2 = "/".join(first_date.split('-')[::-1]), "/".join(second_date.split('-')[::-1])

    try:
        time.strptime(date_1, '%m/%d/%Y')
        time.strptime(date_2, '%m/%d/%Y')

    except ValueError:
        pass

    first_currency_by_date, second_currency_by_date = _get_currency_by_date(date_1, char_code), _get_currency_by_date(date_2, char_code)

    if first_currency_by_date and second_currency_by_date:

        difference_between_currencies = abs(float("%.2f" % (first_currency_by_date - second_currency_by_date)))
        difference_between_currencies_in_percentages = abs(float("%.1f" % (100 * (second_currency_by_date - first_currency_by_date) / first_currency_by_date)))

    currency = {f"currency_for_first_date": first_currency_by_date,
                f"currency_for_second_date": second_currency_by_date,
                "difference": difference_between_currencies,
                "difference_in_percentage": difference_between_currencies_in_percentages}

    return currency


get_difference_between_currencies("USD", "2019-02-15", "2020-01-22")


if __name__ == '__main__':
    USD_currency = get_difference_between_currencies("USD", "2006-08-22", "2019-05-01")
    print(USD_currency)
