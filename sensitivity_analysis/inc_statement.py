# Apply the sensiticity analysis on apple's income statement

import requests
import pandas as pd
from secret import IEX_CLOUD_API_SANDBOX


symbol = 'AAPL'

url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/income?token={IEX_CLOUD_API_SANDBOX}'

fetch = requests.get(url).json()

print(fetch)

growth = 0.03
negative_growth = 0.1       # set up the sensitivity
