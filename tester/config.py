EMA_VALUE = 20
NUM_OF_AMOUNT_CLOSES_UNDER_EMA_FOR_OPEN = 2
ATR_VALUE = 30
ATR_STOP_COEFFICIENT = 5

PROCENT_ON_ONE_DEAL = 200.0 # 200 = X2 от баланса при каждой сделке
FEE_LIMIT = -0.023
FEE_MARKET = 0.077


PARTS_EXIT = {# настройка частичного выхода. %Процент%: %часть от сделки%
	0.4: 1,
	0.5: 1,
	0.8: 1,
	1.2: 1,
	1.5: 1,
	}

FILENAME = 'data/15min_candles.txt'
