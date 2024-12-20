import pandas as pd # for typing
from .constants import NOTEBOOK_RUNCONFIG as cfg 

def number_to_emoji(number: int):
    # Utilitary function to transform any number into a sequence of digit emojis
    # Used for artistic purposes only
    return ''.join([f'{chr(ord("0") + int(digit))}\uFE0F\u20E3' for digit in str(number)])

def all_valid(*args):
    # Asserts all function arguments are valid
    assert all(arg is not None for arg in args), f"Some arguments are None!"


# Mathy helpers 

def normalize_sa(value):
    # Used to normalize the sentiment analysis values obtained
    return (value + 1) / 2

def zscore(series: pd.Series) -> pd.Series:
    # generic function to compute the zscore of a series
    mean = series.mean()
    std_dev = series.std()
    return (series - mean) / std_dev

def display_all_plotly_figures(fig_lst: list,i):
    if not cfg.USE_MATPLOTLIB:
        for f in fig_lst:
            #f.show()
            f.write_html(f"{i}.html", include_plotlyjs='cdn')
            i+=1
    return i
