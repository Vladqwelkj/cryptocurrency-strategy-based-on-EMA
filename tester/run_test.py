from get_data import get_data
from logic import backtest
import config


OHLC = get_data(0, 99999, 'data/15min_candles.txt')
result = backtest(H=OHLC['high'], L=OHLC['low'], C=OHLC['close'],
			src_enter_long=OHLC['close'], src_enter_short=OHLC['close'],
			src_sma=OHLC['close'],

			sma_n=config.EMA_VALUE,
			atr_n=config.ATR_VALUE,
			confirm_n=config.NUM_OF_AMOUNT_CLOSES_UNDER_EMA_FOR_OPEN,
			atr_stop_x=config.ATR_STOP_COEFFICIENT,
			atr_stop_after_take=5,
			parts_exit=config.PARTS_EXIT,
			stop_without_loss_after_take= False,
			fee_limit=config.FEE_LIMIT, fee_market=config.FEE_MARKET, slip=0*10000,
			chart_on=True, procent_one_deal =config.PROCENT_ON_ONE_DEAL/100)

print(result)