import requests
from bs4 import BeautifulSoup
import json
import time
import random
import numpy as np
import re

with open('hotel_ids.json', 'r') as f:
    hotel_ids = json.load(f)

start = '(?:Rate|Price).*?'
end = '.*?^(?:From )?([a-z]+)\s*([\d.,]+)'

def get_hotel_price(text):
    price = 0
    prices = re.findall(start + r'breakfast and dinner' + end, text,
                        re.MULTILINE | re.IGNORECASE | re.DOTALL | re.UNICODE)
    if prices:
        currency, prices = zip(*prices)
        print(currency, prices)
        prices = [price.replace(',', '.') for price in prices]
        prices = np.array(prices, dtype=float)
        price = min(price for price in prices)
    # Extracting meal prices
    else:
        breakfast_prices = re.findall(start + r'breakfast' + end, text,
                                      re.MULTILINE | re.IGNORECASE | re.DOTALL | re.UNICODE)
        dinner_prices = re.findall(start + r'(?:menu|dinner|evening meal)' + end, text,
                                   re.MULTILINE | re.IGNORECASE | re.DOTALL | re.UNICODE)

        if len(breakfast_prices) == 0 and len(dinner_prices) == 0:
            prices = re.findall(end, text, re.MULTILINE | re.IGNORECASE | re.DOTALL | re.UNICODE)
            currency, prices = zip(*prices)
            if len(prices) == 0:
                print('No prices found')
                return 0
            if len(prices) > 1:
                print('Many weird prices found')
            prices = [price.replace(',', '.') for price in prices]
            prices = np.array(prices, dtype=float)
            price = min(price for price in prices)
            return price

        currency1, breakfast_prices = zip(*breakfast_prices)

        if len(breakfast_prices) == 0 or len(dinner_prices) == 0:
            print(breakfast_prices)
            price = min(np.array(breakfast_prices, dtype=float))
            return price

        breakfast_prices = [price.replace(',', '.') for price in breakfast_prices]
        breakfast_price = min(np.array(breakfast_prices, dtype=float))
        currency2, dinner_prices = zip(*dinner_prices)

        if currency1 != currency2:
            print('Different currencies for breakfast and dinner')
        # to int
        dinner_prices = [price.replace(',', '.') for price in dinner_prices]
        dinner_price = min(np.array(dinner_prices, dtype=float))
        print(currency1, breakfast_prices, dinner_prices)

        price = breakfast_price + dinner_price

    return price


i = 0
for hotel in hotel_ids:
    if i % 10 == 0:
        print(i / len(hotel_ids) * 100, '%')
    i += 1
    if 'text' not in hotel.keys():
        hotel['cost'] = -1
        print(hotel)
    else:
        # print(hotel['text'])
        cost = get_hotel_price(hotel['text'])
        if cost == 0:
            print(hotel['text'])
            print('PANIK')
        hotel['cost'] = cost
