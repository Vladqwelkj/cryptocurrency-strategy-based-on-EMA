from matplotlib import pylab
import matplotlib.pyplot as plt
import ta_indicators


_, ax = plt.subplots()
def addPoint(pose=None, index=None, price=None, chart_on=True):
	return
	if chart_on:
		if pose=='Long':
			ax.scatter([index], [price], s = 50, color = 'green', alpha = 0.5)
		if pose=='Short':
			ax.scatter([index], [price], s = 50, color = 'red', alpha = 0.5)
		if pose=='Stop':
			ax.scatter([index], [price], s = 50, color = 'black', alpha = 0.5)
		if pose=='Take':
			ax.scatter([index], [price], s = 50, color = 'yellow', alpha = 0.8)


def backtest(H,L,C,
			src_enter_long, src_enter_short,
			src_sma,
			sma_n, atr_n, confirm_n, atr_stop_x,
			parts_exit,
			fee_limit=-0.00025, fee_market=0.00075, slip=3.0,
			chart_on=True, procent_one_deal=1):

	sma = ta_indicators.SMA(src_sma, sma_n)
	atr = ta_indicators.ATR(atr_n, H, L)

	balance = 1000
	losses, profits = 0, 0

	fee_limit *= procent_one_deal
	fee_market *= procent_one_deal

	max_papers_profits = []
	tmp_max_paper_profits = []
	balance_changes = []
	sum_parts = sum(parts_exit.values())
	position = {'amount': 0, 'first': True, 'is_long': None}#enter, takes[], stop, is_finished

	for i, close in enumerate(C):
		if not (sma[i] and atr[i]):
			continue
		if not sma[i-confirm_n]:
			continue

		if not position['amount']==0: # если есть незаврешенная позиция 
			result = False
########
			if position['is_long']:
				tmp_max_paper_profits.append(H[i]/position['enter']-1)

				if L[i] < position['stop']: #STOP trigger
					addPoint(pose='Stop', index=i, price=position['stop'], chart_on=chart_on)
					result = (((position['stop']) / (position['enter']))
						- (fee_market+fee_limit)/100) * position['amount'] - position['amount']
					position['amount'] = 0

				position['stop'] = close-atr[i]*atr_stop_x
########
				for take in position['takes']:
					if H[i] > take['price'] and not take['is_filled']:
						addPoint(pose='Take', index=i, price=take['price'], chart_on=chart_on)
						result = ((take['price'] / (position['enter']))
							- fee_limit/100*2) * take['amount'] - take['amount']
						position['amount'] = position['amount'] - take['amount']
						take['is_filled'] = True
						if result > 0:
							profits += result
						else:
							losses += result
						balance += result
						#balance_changes.append(balance)
						result = False
########
			if not position['is_long']: #if short

				tmp_max_paper_profits.append(position['enter']/L[i]-1)

				if H[i] > position['stop']: #STOP trigger
					addPoint(pose='Stop', index=i, price=position['stop'], chart_on=chart_on)
					result = (((position['enter']) / (position['stop']))
						- (fee_market+fee_limit)/100) * position['amount'] - position['amount']
					position['amount'] = 0

				position['stop'] = close+atr[i]*atr_stop_x
########
				for take in position['takes']:
					if L[i] < take['price']  and not take['is_filled']:
						addPoint(pose='Take', index=i, price=take['price'], chart_on=chart_on)
						result = (position['enter'] / take['price']
							- fee_limit/100*2) * take['amount'] - take['amount']
						position['amount'] = position['amount'] - take['amount']
						take['is_filled'] = True
						if result > 0:
							profits += result
						else:
							losses += result
						balance += result
						#balance_changes.append(balance)
						result = False
			if result:
				if result > 0:
					profits += result
				else:
					losses += result
				balance += result
				balance_changes.append(balance)
				result = False
########
		is_long = True
		is_short = True
		for n in range(0, confirm_n):
			if src_enter_long[i-n] > sma[i-n]:
				is_short = False
			if src_enter_short[i-n] < sma[i-n]:
				is_long = False

########
		if is_long and (position['first'] or not position['is_long']):
			try:
				position['enter'] #если первый ордер - на этом этапе вылетит исключение
				result = ((position['enter']) / (close) - fee_limit/100*2) * position['amount'] - position['amount']
				if result > 0:
					profits += result
				else:
					losses += result
				balance += result
				balance_changes.append(balance)
				max_papers_profits.append(max(tmp_max_paper_profits))
				tmp_max_paper_profits = []
			except:
				pass
			addPoint(pose='Long', index=i, price=close, chart_on=chart_on)
			position = {'is_long': True, 'enter': close-slip, 'takes':[], 'stop':close-atr[i]*atr_stop_x, 'amount': balance*procent_one_deal, 'first': False}

			for proc in parts_exit.keys():
				position['takes'].append({'price': close*(1+proc/100),
										 'amount': parts_exit[proc]/sum_parts *balance*procent_one_deal,
										 'is_filled': False})



########
		if is_short and (position['first'] or position['is_long']):
			try:
				position['enter'] #если первый ордер - на этом этапе вылетит исключение
				result = ((close + slip) / (position['enter']) - fee_limit/100*2) * position['amount'] - position['amount']
				if result > 0:
					profits += result
				else:
					losses += result
				balance += result
				balance_changes.append(balance)
				max_papers_profits.append(max(tmp_max_paper_profits))
				tmp_max_paper_profits = []
			except:
				pass
			addPoint(pose='Short', index=i, price=close, chart_on=chart_on)
			position = {'is_long': False, 'enter': close+slip, 'takes':[], 'stop':close+atr[i]*atr_stop_x, 'amount': balance*procent_one_deal, 'first': False}

			for proc in parts_exit.keys():
				position['takes'].append({'price': close*(1-proc/100),
										 'amount': parts_exit[proc]/sum_parts *balance*procent_one_deal,
										 'is_filled': False})


	if chart_on:
		for src in [H, L, C, sma]:
			pylab.plot(src, alpha=0.3)
		f = open('balance.txt', 'w')
		for b in balance_changes:
			f.write(str(b)+'\n')
		pylab.show()
		pylab.plot(balance_changes)
		pylab.show()
		pylab.plot(sorted(max_papers_profits))
		pylab.show()

	return {'balance': balance, 'factor': profits/-losses}