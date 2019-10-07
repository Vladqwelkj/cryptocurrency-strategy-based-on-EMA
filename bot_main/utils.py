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


@error_handler
def usd_balance(client, btcusd_price):
    logging.debug('req for usd_balance')
    out = client.User.User_getMargin(currency='XBt').result()[0]['walletBalance'] / (10**8) * btcusd_price
    logging.debug('balance: %d $'%(out))
    return out


@error_handler
def limit_order(client, side, orderQty, price, execInst='ParticipateDoNotInitiate', symbol='XBTUSD'):
    global TIMEOUT_ERROR, MAX_ERR
    logging.debug('limit order: side %s, orderQty: %d, price %.1f, execInst %s'%(side, orderQty, price, execInst))
    out = client.Order.Order_new( #take (limit)
                                symbol = symbol,
                                side = side,
                                orderQty = orderQty,
                                price = price,
                                execInst = execInst,
                                ordType='Limit'
                                ).result()[0]
    logging.debug('limit made')
    return out



@error_handler
def stop_market_order(client, side, orderQty, stopPx, execInst='Close', symbol='XBTUSD'):
    logging.debug('stop_market order: side %s, orderQty: %d, stopPx %.1f, execInst %s'%(side, orderQty, stopPx, execInst))
    out = client.Order.Order_new( #stop (market)
                                symbol = symbol,
                                side = side,
                                orderQty = orderQty,
                                stopPx = stopPx,
                                execInst = execInst,
                                ordType='Stop'
                                ).result()[0]
    logging.debug('stop_market made')
    return out


@error_handler
def order_cancel(client, orderID):
    logging.debug('cancel order, ID: ' + str(orderID))
    out = client.Order.Order_cancel(orderID).result()[0]
    logging.debug('canceled')
    return out


def edit_order_price(client, orderID, new_price):
    