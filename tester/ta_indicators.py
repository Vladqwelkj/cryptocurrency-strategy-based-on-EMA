import numpy as np

def EMA(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a =  np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a

def ATR(period, H, L):
	TR, aver = [], []
	for ind, low in enumerate(L):
		TR.append(H[ind] - low)

	for ind, tr in enumerate(TR):
		if ind+1 < period:
			aver.append(None)
			continue
		current = TR[ind+1-period:ind+1]
		aver.append(sum(current) / len(current))
	return aver
