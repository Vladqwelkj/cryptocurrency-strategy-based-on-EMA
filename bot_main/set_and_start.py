from get_data import get_data
from logic import backtest

parts_exit = {# proc_exit, part_of_position
	0.5: 5,
0.8: 4,
1.4: 3,
1.9: 2,
2.5: 1,
3: 5,
5: 5,
10:10

	}

OHLC = get_data(3, 300000, 'txt.txt')
result = backtest(H=OHLC['high'], L=OHLC['low'], C=OHLC['close'],
			src_enter_long=OHLC['close'], src_enter_short=OHLC['close'],
			src_sma=OHLC['close'],

			sma_n=31,
			atr_n=35,
			confirm_n=2,
			atr_stop_x=5,

			parts_exit=parts_exit,
			fee_limit=-0.015, fee_market=0.08, slip=-0*10000,
			chart_on=True, procent_one_deal =1)

print(result)