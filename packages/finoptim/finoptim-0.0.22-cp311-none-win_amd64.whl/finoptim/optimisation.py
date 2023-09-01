import numpy as np
import pandas as pd
import finoptim.rust_as_backend as rs

from typing import Optional, Callable, Union, Dict

from finoptim.final_results import FinalResults
from finoptim.validations import __validate__prices__, __find_period__


def optimise(usage: pd.DataFrame,
             prices: Union[Dict, pd.DataFrame, Callable],
             convergence_detail: Optional[bool] = None,
             n_jobs=2) -> FinalResults:
     
    """Optimise the levels of reservations and savings plans according to the usage to minimize the cost.
    It is important prices of reservations are always inferior to savings plans prices. Otherwise the problem
    is not convex anymore and there is a risk of not reaching a global minimum.

    Args:
        usage (pd.DataFrame): The usage in hours or days of cloud compute
        prices (Union[Dict, pd.DataFrame, Callable]): A `DataFrame` of prices

            Columns must be the same as usage, and index must be pricing models names in:
            `{'OD'|'RI1Y'|'SP1Y'|'RI3Y'|'SP3Y'}`
   
        convergence_detail (Optional[bool], optional): If `True` return convergence details of the optimisation algorithm,
        such as cost and coverage at every iterations. Defaults to None.
        n_job (int, optional): Number of initialisation for the inertial optimiser. This is also the number of threads used,
         every initialisation running in its own thread. Defaults to 2.
    Raises:
        TypeError: If the entry is not a DataFrame
        Exception: If the time period can't be infered

    Returns:
        FinalResults: The optimal commitments on the time period given in a `FinalResult` object
    """

    if not isinstance(usage, pd.DataFrame):
        raise TypeError("You need to provide a time series DataFrame with a time index")
    
    prices = __validate__prices__(prices)

    sps = set([c for c in prices.index if c[:2] == 'SP'])
    if sps:
        correct_order = prices.loc[sps.pop()].div(prices.loc['OD'])
        correct_order = np.argsort(correct_order.values)
        usage = usage.reindex(columns=usage.columns[correct_order])
        prices = prices.reindex(columns=prices.columns[correct_order])

    X = usage.values.astype(float)

    period = __find_period__(usage)
    if period not in {'D', 'H'}:
        raise Exception("Can't infer time_period, please provide period={'days'|'hours'}")
        
    usage.index = pd.to_datetime(usage.index).to_pydatetime()

    timespan, n = usage.shape
    order = {"RI1Y" : 3, "RI3Y" : 4, "SP1Y" : 1, "SP3Y" : 2, "OD" : 0}
    horizon = set([p[-2:] for p in prices.index if p != 'OD'])
    if len(horizon) == 1:
        # use simplified optimisation to go faster
        print("simple optimisation")
        # here sort the prices accordingly
        prices.sort_index(axis='index', inplace=True, key=lambda x: x.map(order))
        if (np.diff(prices.values, axis=0) > 0).any():
            raise Exception("Prices do not follow the correct order for every instance, optimisation will fail")
        res = rs.simple_optimisation(X, prices.values, period, convergence_detail, step=10)
    else:
        print("complex optimisation")
        parameters = prices.index.map({"RI1Y" : n, "RI3Y" : n, "SP1Y" : 1, "SP3Y" : 1, "OD" : 0}).values.sum()
        current_levels = np.zeros((timespan, parameters))
        res = rs.general_optimisation(X, prices.values, current_levels, list(prices.index), period, n_jobs, convergence_detail)

    
    arangment = pd.DataFrame(res.commitments, index=["savings plans"] + list(usage.columns))


    if len(arangment.columns) == 1:
        horizon = horizon.pop()
        arangment.columns = ("three_years_commitments" if horizon == '3Y' else 'one_year_commitments', )

    p = np.zeros(len(usage.columns) + 1)
    for price in prices.index:
        # print(price[2:])
        if price[:2] == "OD":
            continue
        horizon = 'three_years_commitments' if price[2:] == '3Y' else "one_year_commitments"
        p += np.append(1, prices.loc[price] * (23 * (period == "D") + 1)) * arangment[horizon]

    arangment[f"price_per_{period}"] = p

    fres = FinalResults(
        optimal_arangment=arangment,
        minimum=res.minimum,
        coverage=0,
        n_iter=res.n_iter,
        convergence=res.convergence
    )
    return fres




def optimise_prediction(prediction: np.ndarray,
                        current_prices: Union[Dict, pd.DataFrame, Callable[[str], dict]],
                        current_levels: Union[None, Dict, pd.DataFrame] = None) -> FinalResults:
    """optimise for the preditions of usage

    Args:
        prediction (np.ndarray): a three dimensionnal array.
        The first dimension is assumed to be predictions, and the last one time ?

        current_prices (Union[Dict, pd.DataFrame, Callable[[str], dict]]): A `DataFrame` of prices

            Columns must be the same as usage, and index must be pricing models names in:
            `{'OD'|'RI1Y'|'SP1Y'|'RI3Y'|'SP3Y'}`

        current_levels (Union[None, Dict, pd.DataFrame], optional): A `DataFrame` of commitment levels

                For every reservations, you must indicate the index of ? and the type of reservations ?
                    `{'RI1Y'|'SP1Y'|'RI3Y'|'SP3Y'}`
        Defaults to None.

    Returns:
        FinalResults: still not sure
    """


     
    prices = __validate__prices__(current_prices)

    sps = set([c for c in prices.index if c[:2] == 'SP'])
    if sps:
        correct_order = prices.loc[sps.pop()].div(prices.loc['OD'])
        correct_order = np.argsort(correct_order.values)
        usage = usage.reindex(columns=usage.columns[correct_order])
        prices = prices.reindex(columns=prices.columns[correct_order])

    # here substract the current commitment to the usage and save the associated cost somewhere
    # or no ? because SP and RI can interact ? should add it everytime to the proposed commitments ?

    if prices.any():
        return True
    return False
