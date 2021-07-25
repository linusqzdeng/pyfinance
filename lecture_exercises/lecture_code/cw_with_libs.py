import pandas as pd
import numpy as np

def load_file(filename: str):
    """Load the .xls file and return as a dataframe object."""
    df = pd.read_csv(filename, delimiter='\t')

    return df

data = load_file('outputs.xls')
print(data.info())
