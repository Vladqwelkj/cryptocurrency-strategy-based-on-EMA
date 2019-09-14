from get_data import get_data
from logic import backtest

parts_exit = {# proc_exit, part_of_position
	0.5: 100,
1.0: 2,
1.5: 1,
2.0: 1,
2.5: 1,
3.0: 1,
3.5: 1,
#90:  500
	}
'''

'''
OHLC = get_data(3, 30000, 'PriceData/15min.txt')
result = backtest(H=OHLC['high'], L=OHLC['low'], C=OHLC['close'],
			src_enter_long=OHLC['close'], src_enter_short=OHLC['close'],
			src_sma=OHLC['close'],

			sma_n=31,
			atr_n=35,
			confirm_n=3,
			atr_stop_x=5,

			parts_exit=parts_exit,
			fee_limit=-0.025, fee_market=0.075, slip=300.0,
			chart_on=True, one_deal =15000)

print(result)