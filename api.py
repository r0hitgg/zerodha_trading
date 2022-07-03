from kiteconnect import KiteConnect
kite = KiteConnect(api_key="ge1fsvh1bto8z2os", root='https://zerodha-sandbox.herokuapp.com/')
kite.set_access_token('5tIBfhchSRU6qJ2VuqARqQyraP3cT70s')

def view_price_kite_api(instrument):
    try:
        instrument = 'NFO:%s' % instrument
        res = kite.quote([instrument])
        print('Current Price For %s Is %s' % (instrument, res.get(instrument).get('last_price')))
        return int(res.get(instrument).get('last_price'))
    except Exception as e:
        print('Error: Can Not Get Price For %s' % instrument)
        print('Error: %s' % e)
        return -1

def order_place_kite_api(order):
    try:
        order_id = kite.place_order(tradingsymbol=order.instrument,
                                    exchange=kite.EXCHANGE_NFO,
                                    transaction_type=kite.TRANSACTION_TYPE_BUY,
                                    quantity=order.quantity,
                                    variety=kite.VARIETY_REGULAR,
                                    order_type=kite.ORDER_TYPE_LIMIT,
                                    product=kite.PRODUCT_MIS,
                                    price=order.entry_price,
                                    trigger_price=order.entry_price,
                                    validity=kite.VALIDITY_DAY)
        print('Info: Order Placed Succesfully -> %s' % (order.instrument))
        order.status = 'PLACED'
        order.buy_id = order_id
        return order_id
    except Exception as e:
        print('Error: Order Place Unsuccessfull For %s -> %s' % (order.instrument , e))
        return False

def order_cancel_kite_api(order):
    try:
        if order.buy_id:
            cancel_order = kite.cancel_order(variety=kite.VARIETY_REGULAR, 
            order_id=order.buy_id)
            print('Info: Order Cancelled Succesfully -> %s' % (order.instrument))
            order.status = 'CANCELED'
            return cancel_order
        else:
            print('Error: Order Id Not Found For: %s' %(order.instrument))
            return False
    except Exception as e:
        print('Error: Order Cancel Unsuccessfull For %s -> %s' % (order.instrument , e))
        return False

def order_modify_kite_api(order):
    try:
        if order.buy_id:
            mod_order = kite.modify_order(variety=kite.VARIETY_REGULAR, 
            order_id=order.buy_id, price=order.entry_price,
            trigger_price=order.entry_price)
            print('Info: Order Modified Succesfully -> %s' % (order.instrument))
            return mod_order
        else:
            print('Error: Order Id Not Found For: %s', order.instrument)
            return False
    except Exception as e:
        print('Error: Order Modify Unsuccessfull For %s -> %s' % (order.instrument , e))
        return False

def exit_sell_order_kite_api(order):
    try:
        if order.sell_id:
            order_id = kite.modify_order(order_id=order.sell_id,
                                    quantity=order.quantity,
                                    variety=kite.VARIETY_REGULAR,
                                    order_type=kite.ORDER_TYPE_MARKET,
                                    validity=kite.VALIDITY_DAY)
            order.status = 'COMPLETED'
        else:
            order_id = kite.place_order(tradingsymbol=order.instrument,
                                    exchange=kite.EXCHANGE_NFO,
                                    transaction_type=kite.TRANSACTION_TYPE_SELL,
                                    quantity=order.quantity,
                                    variety=kite.VARIETY_REGULAR,
                                    order_type=kite.ORDER_TYPE_MARKET,
                                    product=kite.PRODUCT_MIS,
                                    validity=kite.VALIDITY_DAY)
            order.sell_id = order_id
            order.status = 'COMPLETED'
        print('Info: Sell Order Executed Succesfully -> %s' % (order.instrument))
        return order_id
    except Exception as e:
        print('Error: Sell Order Execution Unsuccessfull For %s -> %s' % (order.instrument , e))
        return False

def sl_sell_order_kite_api(order):
    try:
        if order.sell_id:
            order_id = kite.modify_order(quantity=order.quantity,
                                    variety=kite.VARIETY_REGULAR,
                                    order_type=kite.ORDER_TYPE_LIMIT,
                                    order_id=order.sell_id,
                                    price=order.sl,
                                    trigger_price=order.sl,
                                    validity=kite.VALIDITY_DAY)
        else:
            order_id = kite.place_order(tradingsymbol=order.instrument,
                                    exchange=kite.EXCHANGE_NFO,
                                    transaction_type=kite.TRANSACTION_TYPE_SELL,
                                    quantity=order.quantity,
                                    variety=kite.VARIETY_REGULAR,
                                    order_type=kite.ORDER_TYPE_LIMIT,
                                    price=order.sl,
                                    trigger_price=order.sl,
                                    product=kite.PRODUCT_MIS,
                                    validity=kite.VALIDITY_DAY)
            order.sell_id = order_id

        order.status = 'IN_PROGRESS'
        print('Info: Sell SL Order Executed Succesfully -> %s' % (order.instrument))
        return order_id
    except Exception as e:
       print('Error: Sell SL Order Execution Unsuccessfull For %s -> %s' % (order.instrument , e))
       return False

def target_sell_order_kite_api(order):
    try:
        if order.sell_id:
            order_id = kite.modify_order(quantity=order.quantity,
                                    variety=kite.VARIETY_REGULAR,
                                    order_type=kite.ORDER_TYPE_LIMIT,
                                    order_id=order.sell_id,
                                    price=order.target,
                                    validity=kite.VALIDITY_DAY)
        else:
            order_id = kite.place_order(tradingsymbol=order.instrument,
                                    exchange=kite.EXCHANGE_NFO,
                                    transaction_type=kite.TRANSACTION_TYPE_SELL,
                                    quantity=order.quantity,
                                    variety=kite.VARIETY_REGULAR,
                                    order_type=kite.ORDER_TYPE_LIMIT,
                                    price=order.target,
                                    product=kite.PRODUCT_MIS,
                                    validity=kite.VALIDITY_DAY)
            order.sell_id = order_id

        order.status = 'IN_PROGRESS'
        print('Info: Sell Target Order Executed Succesfully -> %s' % (order.instrument))
        return order_id
    except Exception as e:
        print('Error: Sell Target Order Execution Unsuccessfull For %s -> %s' % (order.instrument , e))
        return False

def orders_status_kite_api(order):
    try:
        orders = kite.orders()
        is_buy = filter(lambda o: o.order_id == order.buy_id, orders) if order.buy_id else False
        is_sell = filter(lambda o: o.order_id == order.sell_id, orders) if order.sell_id else False

        if not is_buy:
            return 'CANCELLED'
        elif is_sell:
            if is_sell['status'] == 'COMPLETE':
                return 'COMPLETE'
            else:
                return 'IN_PROGRESS'
        else:
            return 'PLACED'

    except Exception as e:
        print('Error: Fetch Order Status -> ', e)
        return False
