import bitmex, datetime
import time
from dateutil.tz import tzutc

client = bitmex.bitmex(
	test=False,)

startTime = datetime.datetime(2019, 6, 1,   00,00, tzinfo=tzutc())
stop = datetime.datetime(2019, 10, 1, 
							7,40,  tzinfo=tzutc())

def GetPrices(startTime):
	prices = client.Trade.Trade_getBucketed(

            binSize = '5m',

            symbol = 'XBTUSD',

            count = 750,

            reverse = False,
            startTime = startTime

        ).result()[0]
	return prices


prices = []
cnt = 1
firstTime = True
while True:
	if firstTime:
		for val in GetPrices(startTime):
			prices.append(val)

		firstTime = False
		time.sleep(2.0)
		print('first')
		continue

	if prices[-1]['timestamp'] >= stop:
		break	
	for val in GetPrices(prices[-1]['timestamp']):
		prices.append(val)

	print(cnt)
	cnt += 1
	time.sleep(2.01)

factor = 3 #30 min / 5min = 6
candles = []
for n in range(factor, len(prices), factor):
	openPrice = prices[n-factor : n][0]['open']
	closePrice = prices[n-factor : n][-1]['close']
	lowTmp = []
	highTmp = []
	for val in prices[n-factor : n]:
		highTmp.append(val['high'])
		lowTmp.append(val['low'])
	candles.append({'open':openPrice, 'high':max(highTmp), 'low':min(lowTmp), 'close':closePrice})
prices = candles

open('15min.txt', 'w')
#prices.reverse()

for price in prices:

	open('txt.txt', 'a').write('%r %r %r %r\n' % 
		tuple([int(price[val]) if (price[val]/0.5)%2==0 else round(price[val], 15) for val in ('open', 'high', 'low', 'close')])
		)

print(len(prices))