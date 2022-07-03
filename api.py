from kiteconnect import KiteConnect

def view_price_kite_api(kite, instrument):
    try:
        token = 'NFO:%s' % instrument if 'NFO:' not in instrument else instrument
        res = kite.quote([token])
        print('Current Price For %s Is %s' % (token, res.get(token).get('last_price')))
        return res.get(token).get('last_price'), token
    except Exception as e:
        print('Error: Can Not Get Price For %s' % token)
        print('Error: %s' % e)
        return False, False


def order_place_kite_api(kite, order):
    order_id = kite.place_order(tradingsymbol=order.raw_tradingsymbol,
                                exchange=kite.EXCHANGE_NFO,
                                transaction_type=kite.TRANSACTION_TYPE_BUY,
                                quantity=order.quantity,
                                variety=kite.VARIETY_REGULAR,
                                order_type=kite.ORDER_TYPE_LIMIT,
                                product=kite.PRODUCT_MIS,
                                price=order.entry_price,
                                validity=kite.VALIDITY_DAY)
    print(order)
    print(order_id,'ORDdddddddd')
    return order_id
