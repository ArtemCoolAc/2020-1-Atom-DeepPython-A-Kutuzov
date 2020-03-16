import requests
import time
import json

usd_rates = dict()
rates = dict()
names_currencies = dict()


class ExchangeRate:
    """Класс для взятия из API курсов валют"""
    class Config:
        API_URL = 'https://openexchangerates.org/api'
        CURRENCY_LIST = '/currencies.json'
        RATE = '/latest.json'
        APP_ID = '?app_id=de82935e1deb403e9cfadf9d38585e85'
        GET_CURRENCIES_URL = f'{API_URL}{CURRENCY_LIST}{APP_ID}'
        GET_BASE_RATE_URL = f'{API_URL}{RATE}{APP_ID}'

    def __init__(self, read_rate_from_file=False):
        """
        Инициализатор класса взятия курсов валют, используется идея взятия только курса доллара, так как остальные курсы
        можно вычислить. По итогу обращение к API производится 2 раза - берется список всех валют с их расшифровкой и
        курс USD/...
        @param read_rate_from_file: для ограничения запросов к API в целях отладки после обращение к API данные
        записываются в файл и если необходимо считать данные с файла, ставится True, если посмотреть котировки посвежее
        ставится False
        """
        global rates
        global usd_rates
        global names_currencies
        if read_rate_from_file:
            file = open('USD_rates.txt', 'r')
            file2 = open('Names_of_currencies.txt', 'r')
            usd_rates = json.load(file)
            names_currencies = json.load(file2)
            file.close()
            file2.close()
        else:
            names_currencies = requests.get(self.Config.GET_CURRENCIES_URL).json()
            self.base_rate_json = requests.get(self.Config.GET_BASE_RATE_URL).json()
            self.time = time.ctime(self.base_rate_json['timestamp'])
            usd_rates = self.base_rate_json['rates']
            file = open('USD_rates.txt', 'w')
            file2 = open('Names_of_currencies.txt', 'w')
            json.dump(usd_rates, file)
            json.dump(names_currencies, file2)
            file.close()
            file2.close()
        for first_key, first_value in usd_rates.items():
            if first_key not in rates:
                rates[first_key] = dict()
            for second_key, second_value in usd_rates.items():
                if second_key not in rates[first_key]:
                    rates[first_key][second_key] = second_value / first_value

    @staticmethod
    def get_rate(first_currency, second_currency):
        return rates[first_currency.upper()][second_currency.upper()]


class Currency:
    """Класс, описывающий поведение валюты"""
    EPSILON = 0.0001

    def __init__(self, value, currency=None):
        """
        Инициализатор класса валюты, имеет параметры значение и тип валюты
        @param value: числовое значение валюты
        @param currency: строковое представление валюты в международном формате
        """
        self.value = value
        self.currency = currency
        if currency is not None:
            self.currency = currency.upper()

    def __add__(self, other):
        if type(other) == int or type(other) == float:
            return Currency(self.value + other, self.currency)
        elif type(self) == int or type(self) == float:
            return Currency(self + other.value, other.currency)
        elif self.currency is None and other.currency is None:
            raise AttributeError("Отсутствует валюта")
        elif self.currency is not None and other.currency is None:
            return Currency(self.value + other.value, self.currency)
        elif self.currency is None and other.currency is not None:
            return Currency(self.value + other.value, other.currency)
        elif self.currency is not None and other.currency is not None:
            exchange_rate = ExchangeRate.get_rate(other.currency, self.currency)
            return Currency(self.value + other.value * exchange_rate, self.currency)

    def __sub__(self, other):
        if type(other) == int or type(other) == float:
            return Currency(self.value - other, self.currency)
        elif type(self) == int or type(self) == float:
            return Currency(self - other.value, other.currency)
        elif self.currency is None and other.currency is None:
            raise AttributeError("Отсутствует валюта")
        elif self.currency is not None and other.currency is None:
            return Currency(self.value - other.value, self.currency)
        elif self.currency is None and other.currency is not None:
            return Currency(self.value - other.value, other.currency)
        elif self.currency is not None and other.currency is not None:
            exchange_rate = ExchangeRate.get_rate(other.currency, self.currency)
            return Currency(self.value - other.value * exchange_rate, self.currency)

    def __iadd__(self, other):
        self = self + other
        return self

    def __isub__(self, other):
        self = self - other
        return self

    def __eq__(self, other):
        if self.currency is None and other.currency is None:
            raise AttributeError("Неизвестные валюты")
        elif not (self.currency is not None and other.currency is not None):
            return self.value == other.value
        else:
            return abs(self.value - other.value * rates[other.currency][self.currency]) <= self.EPSILON

    def __ne__(self, other):
        if self.currency is None and other.currency is None:
            raise AttributeError("Неизвестные валюты")
        elif not (self.currency is not None and other.currency is not None):
            return self.value != other.value
        else:
            return abs(self.value - other.value * rates[other.currency][self.currency]) > self.EPSILON

    def __gt__(self, other):
        if self.currency is None and other.currency is None:
            raise AttributeError("Неизвестные валюты")
        elif not (self.currency is not None and other.currency is not None):
            return self.value > other.value
        else:
            return (self.value - other.value * rates[other.currency][self.currency]) > self.EPSILON

    def __ge__(self, other):
        if self.currency is None and other.currency is None:
            raise AttributeError("Неизвестные валюты")
        elif not (self.currency is not None and other.currency is not None):
            return self.value >= other.value
        else:
            return (self.value - other.value * rates[other.currency][self.currency]) > -self.EPSILON

    def __lt__(self, other):
        if self.currency is None and other.currency is None:
            raise AttributeError("Неизвестные валюты")
        elif not (self.currency is not None and other.currency is not None):
            return self.value < other.value
        else:
            return -(self.value - other.value * rates[other.currency][self.currency]) > self.EPSILON

    def __le__(self, other):
        if self.currency is None and other.currency is None:
            raise AttributeError("Неизвестные валюты")
        elif not (self.currency is not None and other.currency is not None):
            return self.value >= other.value
        else:
            return -(self.value - other.value * rates[other.currency][self.currency]) > -self.EPSILON

    def __repr__(self):
        if self.currency is None:
            return f'{str(self.value)} НЕТ ВАЛЮТЫ'
        return f'{str(self.value)} {self.currency} ({names_currencies[self.currency.upper()]})'

    def __str__(self):
        if self.currency is None:
            return f'{str(str(round(self.value, 4)))}'
        return f'{str(round(self.value, 4))} {self.currency}'


if __name__ == '__main__':
    try:
        A = ExchangeRate(True)
        print(A.get_rate('eur', 'rub'))
        a = Currency(2, 'eur')
        b = Currency(30, 'rub')
        c = a + b
        print(repr(c))
        print(str(c))
        f = Currency(0.23, 'btc')
        print(repr(f))
        g = Currency(47, 'usd')
        e = g + f
        print(e)
        aa = Currency(10)
        bb = Currency(20)
        cc = aa + Currency(3, 'rub')
        dd = Currency(2.5, 'eur') + bb
        dd = dd + 6
        dd += 100
        dd += Currency(16, 'rub')
        print(dd)
        print(cc)
        print(repr(cc))
        print(str(cc))
    except Exception as e:
        print(e)


