from get_data import get_data
from logic import backtest

parts_exit = {# proc_exit, part_of_position

	0.4: 1,
	0.5: 1,
	0.8: 1,
	1.2: 1,
	1.5: 1,
	#2.5: 1,
	#3: 1
#10: 1

	}
'''


0.3: 10,
0.5: 1,
1: 1,
1.5: 1,
2: 1,
2.5: 1,
3: 1,
3.5: 1,
5: 1,
7: 1,
10: 1,
'''
OHLC = get_data(59000, 62000, 'txt.txt')
result = backtest(H=OHLC['high'], L=OHLC['low'], C=OHLC['close'],
			src_enter_long=OHLC['close'], src_enter_short=OHLC['close'],
			src_sma=OHLC['close'],

			sma_n=20,
			atr_n=30,
			confirm_n=2,
			atr_stop_x=5,
			atr_stop_after_take=5,
			parts_exit=parts_exit,
			stop_without_loss_after_take= False,
			fee_limit=-0.023, fee_market=0.077, slip=-1.5*10000,
			chart_on=True, procent_one_deal =2)

print(result)