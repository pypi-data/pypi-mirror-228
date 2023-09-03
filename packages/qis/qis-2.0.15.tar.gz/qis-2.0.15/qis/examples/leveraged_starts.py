

"""
performance report for a universe of several assets
with comparison to 1-2 benchmarks
output is one-page figure with key numbers
"""

# packages
import matplotlib.pyplot as plt
from enum import Enum

import pandas as pd
import yfinance as yf
import qis

from qis.portfolio.reports.config import PERF_PARAMS, REGIME_PARAMS
from qis.portfolio.reports.multi_assets_factsheet import generate_multi_asset_factsheet
from qis.portfolio.reports.config import fetch_default_report_kwargs

# select tickers
benchmark = 'SPY'
tickers = [benchmark, 'SSO', 'IEF']

prices = yf.download(tickers=tickers, start=None, end=None, ignore_tz=True)['Adj Close'][tickers]
prices = prices.asfreq('B', method='ffill').dropna()  # make B frequency

leveraged_portfolio = qis.backtest_model_portfolio(prices=prices[['SSO', 'IEF']],
                                                   weights={'SSO': 0.5, 'IEF': 0.5},
                                                   rebalance_freq='B',
                                                   rebalancing_costs=0.0010,  # 10bp
                                                   ticker='50/50 SSO/IEF')

prices = pd.concat([prices, leveraged_portfolio], axis=1)

# generate report since SSO launch
time_period = qis.TimePeriod('21Jun2006', '01Sep2023')
fig = generate_multi_asset_factsheet(prices=prices,
                                     benchmark=benchmark,
                                     time_period=time_period,
                                     **fetch_default_report_kwargs(time_period=time_period))

qis.save_fig(fig=fig, file_name=f"leveraged_fund_analysis", local_path=qis.local_path.get_output_path())

qis.save_figs_to_pdf(figs=[fig],
                     file_name=f"leveraged_fund_analysis", orientation='landscape',
                     local_path=qis.local_path.get_output_path())

plt.show()

"""


class UnitTests(Enum):
    CORE_ETFS = 1
    BTC_SQQQ = 2


def run_unit_test(unit_test: UnitTests):

    if unit_test == UnitTests.CORE_ETFS:



    elif unit_test == UnitTests.BTC_SQQQ:
        benchmark = 'QQQ'
        tickers = [benchmark, 'BTC-USD', 'TQQQ', 'SQQQ']
        time_period = qis.TimePeriod('31Dec2019', '01Sep2023')

    else:
        raise NotImplementedError

    prices = yf.download(tickers=tickers, start=None, end=None, ignore_tz=True)['Adj Close'][tickers]
    prices = prices.asfreq('B', method='ffill')  # make B frequency
    fig = generate_multi_asset_factsheet(prices=prices,
                                         benchmark=benchmark,
                                         time_period=time_period,
                                         **fetch_default_report_kwargs(time_period=time_period))
    qis.save_figs_to_pdf(figs=[fig],
                         file_name=f"multiasset_report", orientation='landscape',
                         local_path=qis.local_path.get_output_path())
    qis.save_fig(fig=fig, file_name=f"multiassets", local_path=qis.local_path.get_output_path())

    plt.show()


if __name__ == '__main__':

    unit_test = UnitTests.BTC_SQQQ

    is_run_all_tests = False
    if is_run_all_tests:
        for unit_test in UnitTests:
            run_unit_test(unit_test=unit_test)
    else:
        run_unit_test(unit_test=unit_test)
"""