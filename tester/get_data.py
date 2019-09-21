
def get_data(start, end, filename='1h.txt'):
	pricesListOpen = []
	pricesList = []
	pricesListHigh= []
	pricesListLow = []
	f = open(filename, 'r')
	cnt = 0
	factor = 10000
	for line in f:
		cnt += 1
		if cnt < start:
			continue
		if cnt > end:
			break
		line = line.split()
		pricesList.append(float(line[3])*factor)
		pricesListHigh.append(float(line[1])*factor)
		pricesListLow.append(float(line[2])*factor)
		pricesListOpen.append(float(line[0])*factor)
	f.close()
	print('len of data:', cnt)
	return {'open': pricesListOpen,
			'high': pricesListHigh,
			'low': pricesListLow,
			'close': pricesList}
