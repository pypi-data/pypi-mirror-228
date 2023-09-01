import warnings

import numpy as np
import pandas as pd

# import the contents of the Rust library into the Python extension
# optional: include the documentation from the Rust module
# __all__ = __all__ + ["PythonClass"]


def add_one(x: int) -> int:
    """see if documentation works

    Args:
        x (int): your number

    Returns:
        int: numnber +1
    """
    return x + 1



def __validate__prices__(prices):

    if isinstance(prices, pd.DataFrame):
        assert(set(prices.index).issubset({'OD', 'RI1Y', 'SP1Y', 'RI3Y', 'SP3Y'}))

    if isinstance(prices, dict):
        prices = pd.DataFrame(prices)
        assert(set(prices.index).issubset({'OD', 'RI1Y', 'SP1Y', 'RI3Y', 'SP3Y'}))

    if callable(prices):
        raise NotImplemented("Not Implemented Yet")

    return prices

def __find_period__(df: pd.DataFrame) -> str:
        dates = pd.to_datetime(df.index)
        periods = np.diff(dates, 1)
        if periods.min() != periods.max():
            warnings.warn("Careful, you have missing datas in your usage")
        return dates.inferred_freq

