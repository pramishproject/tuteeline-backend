import requests
from tkinter import *
import tkinter as tk
from tkinter import ttk

from config.settings.base import env

class RealTimeCurrencyConverter():
    def __init__(self):
        URL = env("CURRENCY_URL")
        self.data= requests.get(URL).json()
        self.currencies = self.data['rates']
    def convert(self, from_currency, to_currency, amount): 
        initial_amount = amount 
        #first convert it into USD if it is not in USD.
        # because our base currency is USD
        if from_currency != 'USD' : 
            amount = amount / self.currencies[from_currency] 
        
        # limiting the precision to 4 decimal places 
        amount = round(amount * self.currencies[to_currency], 4) 
        return amount

    def CurrencyName(self):
        currencyName =[]
        for i in self.data['rates'].keys():
            tpl = (i, i)
            currencyName.append(tpl)
        
        return tuple(currencyName)

# url = 'https://api.exchangerate-api.com/v4/latest/USD'
# converter = RealTimeCurrencyConverter()
# print(converter.convert('INR','USD',100))
# converter.CurrencyName()