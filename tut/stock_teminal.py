'''
Build up a stock terminal that can retrive company's infomation
such as company profle, historical stock prices, income statement, balance sheet
'''

import pandas as pd
import matplotlib.pyplot as plt
import requests
from pandas_datareader import DataReader as web
from datetime import datetime as dt

api_token = 'Tsk_5458757fdaf14aa782ec34ee1692ee20'



def income_statement(ticker):
    '''
    Return I/S for selected stock, either annually or quarterly.
    Note it is only available for US symbols
    '''
    while True:
        a_or_q = input("Would you like a quaterly or annually data? Please enter 'a' for annual data, 'q' for quarter data ").strip()
       
        if a_or_q == 'a':
            period = 'annual'
            break
        elif a_or_q == 'q':
            period = 'quarter'
            break
        else:
            print('Cannot identify. Please re-enter')
            continue

    api_url = f'https://sandbox.iexapis.com/stable/stock/{ticker}/income?period={period}&token={api_token}'
    IS = requests.get(api_url).json()
    IS = pd.DataFrame.from_dict(IS['income']).T
    IS.append(pd.Series({'symbol': ticker}), ignore_index=True)

    print(IS)

    save_csv = input('Would you like to store the data in a .csv file? \ny or n? ').strip()
    if save_csv == 'y':
        IS.to_csv('IS.csv')


def historical_stock_price(ticker, start_date, end_date):
    '''
    Return a .csv file which contains historical daily stock prices 
    from start date to end date for the selected stock.
    ==========
    Paramters:
    - ticker -> string: listed stock symbol
    - start_date -> string: YY-MM-DD
    - end_date -> string: YY-MM-DD
    '''

    start = start_date
    end = end_date

    df = web(ticker, 'yahoo', start, end)

    df.to_csv(f'{ticker}_histoical_stock_price.csv')

historical_stock_price('AAPL', '2019-01-01', '2020-02-01')

# income_statement('AAPL')
