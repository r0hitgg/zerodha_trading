import api
from kiteconnect import KiteConnect

orders = []
kite = KiteConnect(api_key="ge1fsvh1bto8z2os")


def main():
    user_input = int(create_menu())
    if user_input == 1:
        instrument_input = take_view_price_input()
        instrument, flag = api.view_price_kite_api(kite, instrument_input['stock'])
        if instrument:
            order = take_place_order_input({'stock': flag})
            order_obj = Order(stock=order['stock'],
                strike_price=instrument_input['strike_price'],
                raw_tradingsymbol=instrument_input['stock'],
                option=instrument_input['option'],
                quantity=order['quantity'],
                entry_price=order['entry_price'],
                target=order['target'],
                sl=order['sl'],
            )
            order_place(order_obj)
        else:
            main()
    elif user_input == 7:
        for order in orders:
            print(order)
        main()

class Order:
    def __init__(order, stock, strike_price, option, quantity, entry_price, target, sl, raw_tradingsymbol, status='pending'):
        order.stock = stock
        order.strike_price = strike_price
        order.option = option
        order.quantity = quantity
        order.entry_price = entry_price
        order.target = target
        order.sl = sl
        order.raw_tradingsymbol = raw_tradingsymbol
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
    current_price, flag = api.view_price_kite_api(kite, order.stock)
    print(current_price)
    if validation_order_place(order.entry_price, current_price, order.sl, order.target) ==  False:
        print("INFO: Sorry!! Your Order is not placed.")
        return

    if order.entry_price - current_price <= 10:
        # Todo : Commenting For Now
        api.order_place_kite_api(kite, order)
        insert_order_queue(order)
        return


def take_view_price_input():
    op_type = input('Enter Ninfy/Banknifty (n or b) -> ')
    flag = input('Enter Flag -> ')
    strike_price = input('Enter Strice Price -> ')
    ce = input('Enter CE/PE -> ')
    return {
        'stock': str('NIFTY' if op_type == 'n' else 'BANKNIFTY') + str(flag) + str(strike_price) + str(ce).upper(),
        'op_type': op_type,
        'strike_price': strike_price,
        'option': ce,
        'flag': flag
    }

def take_place_order_input(instrument):
    instrument['quantity'] = int(input('Enter Quantity -> '))
    instrument['entry_price'] = int(input('Enter Entry Price -> '))
    instrument['target'] = int(input('Enter Target -> '))
    instrument['sl'] = int(input('Enter Sl -> '))
    return instrument


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
    # data = kite.generate_session("tDa8BTnzSAEgJ0w3NZxFampVxBbHZoVr", api_secret="3f4sbjxkpxf2thpl5qcvvj05vde5egxp")
    # print(data["access_token"],'TOEKN\n\n\n')
    kite.set_access_token('5tIBfhchSRU6qJ2VuqARqQyraP3cT70s')
    main()


# data = kite.generate_session("BTNcDZjb7EVa2wD02CO95qh4XUxqvRII", api_secret="3f4sbjxkpxf2thpl5qcvvj05vde5egxp")
# print(data["access_token"],'TOEKN\n\n\n')
# kite.set_access_token('MI0WjCvsPeFpkWBKH7V8Du95kZBwgo06')
# res = kite.quote(['NFO:INFY'])
# print(res,'11111')



