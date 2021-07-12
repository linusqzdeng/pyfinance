import pandas as pd
import numpy as np
import pickle
from collections import Counter

df = pd.read_csv('S&P_500_3m_adjClose.csv', index_col=0)

def processing_data_labels(ticker):
    hm_day = 5
    tickers = df.columns.values
    df.fillna(0, inplace=True)

    for i in range(1, hm_day+1):
        df[f'{ticker}_{i}d'] = np.log10(df[ticker]).shift(-i) - np.log10(df[ticker])

    df.fillna(0, inplace=True)

    return tickers, df, hm_day

def buy_sell_hold(*args):
    cols = [c for c in args]
    requirement = 0.02
    for col in cols:
        if col > requirement:
            return 1
        elif col < requirement:
            return -1
    return 0 

def extract_featuresets(ticker):
    tickers, df, hm_day = processing_data_labels(ticker)

    df[f'{ticker}_target'] = list(map(buy_sell_hold, 
                            *[df[f'{ticker}_{i}d'] for i in range(1, hm_day+1)]))

    vals = df[f'{ticker}_target'].values
    str_vals = [str(i) for i in vals]
    print('Data spread:', Counter(str_vals))

    df.fillna(0, inplace=True)
    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace=True)

