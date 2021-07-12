import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as web
from datetime import date

start = date(2020, 4, 30)
end = date(2021, 2, 1)


def obtain_data(stock, start, end) -> str:
    '''
    return a dataframe that contains the open, high. low, volume and clost price
    of a listed stock.
    ===============================
    parameters:
    stock: str. symbol or ticker of a listed stock
    start: str. start trading date (format: "YY-MM-DD")
    end: str. end trading date (format:"YY-MM-DD")
    '''

    start_date = start
    end_date = end

    df = pd.DataFrame()
    df = web.DataReader(stock, data_source='yahoo',
                        start=start_date, end=end_date)

    return df

def visualisation(data) -> pd.DataFrame:

    plt.style.use('fivethirtyeight')
    plt.figure(figsize=(12, 8))

    plt.plot(data['Close'])
    plt.xticks(rotation=30)
    plt.title('Uber\'s closing prices')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')

    return plt.show()


df = obtain_data('UBER', '2021-01-01', '2021-01-31')
print(df)
visualisation(df)
