import threading
import logging

def thread_decor(my_func):
	def wrapper(*args, **kwargs):
		my_thread = threading.Thread(target=my_func, args=args, kwargs=kwargs)
		my_thread.start()
	return wrapper


def error_handler(func):
	err_now = 0
	def wrapper(*args, **kwargs):
		while err_now<MAX_ERR:
			try:
				func(*args, **kwargs)
			except Exception as er:
				logging.error('Error:' + str(er))
				time.sleep(5)
				err_now += 1
		logging.warning('Limit of errors!')
	return wrapper


@error_handler
def status_by_id(client, ordersID):
	global TIMEOUT_ERROR, MAX_ERR
	logging.debug('orders to check: '+str(ordersID))
	result = {}
	orders = client.Order.Order_getOrders(symbol='XBTUSD',
										count= 50,
										reverse=True).result()[0]
	for order in orders:
		if order['orderID'] in orders:
			result[order['orderID']] = order['ordStatus']
	logging.debug('out: '+str(result))
	return result
