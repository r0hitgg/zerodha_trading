from kiteconnect import KiteConnect
kite = KiteConnect(api_key="ge1fsvh1bto8z2os", root='https://zerodha-sandbox.herokuapp.com/')
kite.set_access_token('5tIBfhchSRU6qJ2VuqARqQyraP3cT70s')

def view_price_kite_api(instrument):
    # try:
    token = 'NFO:%s' % instrument if 'NFO:' not in instrument else instrument
    res = kite.quote([token])
    print(res,'>>>>>RES')
    print('Current Price For %s Is %s' % (token, res.get(token).get('last_price')))
    
    return res.get(token).get('last_price'), token
    # except Exception as e:
        # print('Error: Can Not Get Price For %s' % token)
        # print('Error: %s' % e)
        # return False, False


def order_place_kite_api(order):
    print(order)
    try:
        order_id = kite.place_order(tradingsymbol=order.instrument,
                                    exchange=kite.EXCHANGE_NFO,
                                    transaction_type=kite.TRANSACTION_TYPE_BUY,
                                    quantity=order.quantity,
                                    variety=kite.VARIETY_REGULAR,
                                    order_type=kite.ORDER_TYPE_LIMIT,
                                    product=kite.PRODUCT_MIS,
                                    price=order.sl,
                                    trigger_price=order.sl,
                                    validity=kite.VALIDITY_DAY)
        order.id = order_id
        return order_id
    except Exception as e:
        print('Erro: Can Not Place Order ->', e)
        return False

def order_cancel_kite_api(order):
    try:
        if order.id:
            cancel_order = kite.cancel_order(variety=kite.VARIETY_REGULAR, 
            order_id=order.id)
            order.status = 'CANCELED'
            return cancel_order
        else:
            print('Error: Order Id Not Found For: %s & Order Id: %s' %(order.stock, order.id))
            return False
    except Exception as e:
        print('Error: Cancel Order -> ', e)
        return False

def order_modify_kite_api(order):
    try:
        if order.id:
            mod_order = kite.modify_order(variety=kite.VARIETY_REGULAR, 
            order_id=order.id, price=order.entry_price)
            return mod_order
        else:
            print('Error: Order Id Not Found For: %s', order.stock)
            return False
    except Exception as e:
        print('Error: Modify Order -> ', e)
        return False

def exit_sell_order_kite_api(order):
    try:
        if order.id:
            order_id = kite.place_order(tradingsymbol=order.instrument,
                                    exchange=kite.EXCHANGE_NFO,
                                    transaction_type=kite.TRANSACTION_TYPE_SELL,
                                    quantity=order.quantity,
                                    variety=kite.VARIETY_REGULAR,
                                    order_type=kite.ORDER_TYPE_MARKET,
                                    product=kite.PRODUCT_MIS,
                                    validity=kite.VALIDITY_DAY)
            order.status = 'COMPLETED'
            return order_id
        else:
            print('Error: Order Id Not Found For: %s', order.stock)
            return False
    except Exception as e:
        print('Error: Sell Order -> ', e)
        return False

def sl_sell_order_kite_api(order):
    try:
        if order.id:
            order_id = kite.modify_order(quantity=order.quantity,
                                    variety=kite.VARIETY_REGULAR,
                                    order_type=kite.ORDER_TYPE_LIMIT,
                                    order_id=order.id,
                                    price=order.sl,
                                    trigger_price=order.sl,
                                    validity=kite.VALIDITY_DAY)
            order.status = 'COMPLETED'
            return order_id
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
            order.id = order_id
            order.status = 'PLACED'
            return order_id
    except Exception as e:
        print('Error: SL Sell Order -> ', e)
        return False

def target_sell_order_kite_api(order):
    try:
        if order.id:
            order_id = kite.modify_order(quantity=order.quantity,
                                    variety=kite.VARIETY_REGULAR,
                                    order_type=kite.ORDER_TYPE_LIMIT,
                                    order_id=order.id,
                                    price=order.target,
                                    validity=kite.VALIDITY_DAY)
            return order_id
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
            order.id = order_id
            order.status = 'PLACED'
            return order_id
    except Exception as e:
        print('Error: SL Sell Order -> ', e)
        return False

def orders_status_kite_api(order):
    try:
        order_id = kite.orders()
        if order_id:
            for o in order_id:
                if o['order_id'] == order.id:
                    return o['status']
        return False
    except Exception as e:
        print('Error: Order Status -> ', e)
        return False
