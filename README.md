## Principle of operation:
![Explanation of the strategy](https://gitlab.com/vladqwelkj/fixing-over-the-sma-strategy_backtest/raw/master/explanation.png)

The backtester is in the repository. Also there is an unfinished bot for the Bitmex.

### Result for 5 month:
![Result for 5 month](https://gitlab.com/vladqwelkj/fixing-over-the-sma-strategy_backtest/raw/master/result_5month.png)
config:

```
EMA_VALUE = 20
NUM_OF_AMOUNT_CLOSES_UNDER_EMA_FOR_OPEN = 2
ATR_VALUE = 30
ATR_STOP_COEFFICIENT = 5

PROCENT_ON_ONE_DEAL = 100.0
FEE_LIMIT = -0.023
FEE_MARKET = 0.077


PARTS_EXIT = {
	0.4: 1,
	0.5: 1,
	0.8: 1,
	1.2: 1,
	1.5: 1,
	}
```