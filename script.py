import logging
from kiteconnect import KiteConnect

orders = []
kite = KiteConnect(api_key="ge1fsvh1bto8z2os")


def main():
    user_input = int(create_menu())
    if user_input == 1:
        instrument_input = take_view_price_input()
        instrument = view_price_kite_api(instrument_input['stock'])
        if instrument:
            order = take_place_order_input(instrument)
            order_obj = Order(order)
            order_place(order_obj)
        else:
            main()
    elif user_input == 7:
        for order in orders:
            print(order)
        main()

class Order:
    def __init__(order, stock, strike_price, option, quantity, entry_price, target, sl, status):
        order.stock = stock
        order.strike_price = strike_price
        order.option = option
        order.quantity = quantity
        order.entry_price = entry_price
        order.target = target
        order.sl = sl
        order.status = status

    def __str__(order):
        return ''''
            Stock -> %s
            Strike Price -> %s
            Option -> %s
            Quantity -> %s
            Entry Price -> %s
            Target -> %s
            Stop Loss -> %s
            Status -> %s
        '''


def validation_order_place(entry_price, current_price, sl, target):

    if sl > entry_price or sl > target:
        print("ERROR: sl should be less than entry-price")
        return False

    if target < entry_price or target < sl:
        print("ERROR: target should be greater than entry price")
        return False

    if (entry_price - sl) > 40:
        print("ERROR: more than 40 points sl is not allowed")
        return False

    if (target - entry_price) > 50:
        print("ERROR: more than 50 points target is not allowed")
        return False

    if current_price > entry_price:
        print("ERROR: current_price is already more than entry price.")
        return False

    return True


def insert_order_queue(order):
    order.status = "PENDING"
    orders.append(order)
    print("INFO: your order place in pending queue")


def order_place(order):

    current_price = view_price_kite_api(order.stock)

    if validation_order_place(order.entry_price, current_price, order.sl, order.target) ==  False:
        print("INFO: Sorry!! Your Order is not placed.")
        return

    if order.entry_price - current_price <= 10:
        # Todo : Commenting For Now
        # order_place_kite_api(order)
        return

    insert_order_queue(order)


def order_place_kite_api(order):
    order_id = kite.place_order(tradingsymbol=order.stock,
                                exchange=kite.EXCHANGE_NFO,
                                transaction_type=kite.TRANSACTION_TYPE_BUY,
                                quantity=order.quantity,
                                variety=kite.VARIETY_REGULAR,
                                order_type=kite.ORDER_TYPE_LIMIT,
                                product=kite.PRODUCT_MIS,
                                validity=kite.VALIDITY_DAY)


def take_view_price_input():
    op_type = input('Enter Ninfy/Banknifty (n or b) -> ')
    flag = input('Enter Flag -> ')
    strike_price = input('Enter Strice Price -> ')
    ce = input('Enter CE/PE -> ')
    return {
        'stock': str('NIFTY' if op_type == 'n' else 'BANKNIFTY') + str(flag) + str(strike_price) + str(ce).upper()
    }

def take_place_order_input(instrument):
    instrument['strike_price'] = input('Enter Strike Price -> ')
    instrument['option'] = input('Enter Option -> ')
    instrument['quantity'] = input('Enter Quantity -> ')
    instrument['entry_price'] = input('Enter Entry Price -> ')
    instrument['target'] = input('Enter Target -> ')
    instrument['sl'] = input('Enter Sl -> ')
    return instrument


def view_price_kite_api(instrument):
    try:
        token = 'NFO:%s' % instrument
        res = kite.quote([token])
        print('Current Price For %s Is %s' % (token, res.get(token).get('last_price')))
        return res.get(token).get('last_price')
    except:
        print('Error: Can Not Get Price For %s' % token)
        print(res)
        return False


def create_menu():
    inp = input('''1) Place An Order
2) View All Pending Orders
3) View All Current Orders
4) Cancel Specific Order
5) Cancel All Order
6) Modification Of Order
7) View All Order Information
''')
    return inp


if __name__ == "__main__":
    kite.set_access_token('MI0WjCvsPeFpkWBKH7V8Du95kZBwgo06')
    main()


# data = kite.generate_session("BTNcDZjb7EVa2wD02CO95qh4XUxqvRII", api_secret="3f4sbjxkpxf2thpl5qcvvj05vde5egxp")
# print(data["access_token"],'TOEKN\n\n\n')
# kite.set_access_token('MI0WjCvsPeFpkWBKH7V8Du95kZBwgo06')
# res = kite.quote(['NFO:INFY'])
# print(res,'11111')



