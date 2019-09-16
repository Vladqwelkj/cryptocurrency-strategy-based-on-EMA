from matplotlib import pylab

file = open('balance.txt', 'r')
balance_changes = []
for line in file:
	balance_changes.append(float(line))

pylab.plot(balance_changes, alpha=0.3)

procent_changes = []

for i, val in enumerate(balance_changes):
	try:
		procent_changes.append(balance_changes[i+1]/val)
	except:
		print('end procent calculate')
		break

balance = 1000
procent_one_deal = 200

balance_changes = []

for val in procent_changes:
	qty = balance*procent_one_deal/100 
	balance += qty*val - qty
	balance_changes.append(balance)

print(balance)
pylab.plot(balance_changes)
pylab.show()