import api
import uuid
orders = []
class Order():
     def __init__(order, stock, strike_price, option, quantity, entry_price, target, sl, instrument, status='pending', id=''):
        order.stock = stock
        order.strike_price = strike_price
        order.option = option
        order.quantity = quantity
        order.entry_price = entry_price
        order.target = target
        order.sl = sl
        order.instrument = instrument
        order.status = status
        order.id = id or uuid.uuid4()

order = Order('INFY' ,25, 'PE', 25, 300, 320, 280, 'INFY', 'PENDING')
orders.append(order)
res = api.order_place_kite_api(order)
print(res,'<- Place Order \n')
for o in orders:
    o.entry_price = 200
    modify = api.order_modify_kite_api(o)
    print(modify,'<- Modified \n')


    res = api.orders_status_kite_api(o)
    print(res,'<- STATUS \n')

    sell = api.exit_sell_order_kite_api(o)
    print(sell , '<- Sell \n')

    cancel = api.order_cancel_kite_api(o)
    print(cancel,'.<- Cancelled \n')

    sell = api.sl_sell_order_kite_api(o)
    print(sell , '<- Sl Sell \n')
    
    sell = api.target_sell_order_kite_api(o)
    print(sell , '<- Target Sell \n')

    o.id = False
    print('Order Id -> ', o.id)
    sell = api.sl_sell_order_kite_api(o)
    print(sell , '<- Sl Sell')
    print('Order Id -> ', o.id,' \n')

    o.id = False
    print('Order Id -> ', o.id)
    sell = api.target_sell_order_kite_api(o)
    print(sell , '<- Target Sell')
    print('Order Id -> ', o.id,' \n')


