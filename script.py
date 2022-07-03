import logging
import threading
import config
import api
from pyautogui import typewrite
import uuid

# logging.basicConfig(level=logging.DEBUG)

orders = []

class Order:
    def __init__(order, stock, strike_price, option, quantity, entry_price, target, sl, instrument, status='pending', buy_id="", sell_id=""):
        order.stock = stock
        order.strike_price = strike_price
        order.option = option
        order.quantity = quantity
        order.entry_price = entry_price
        order.target = target
        order.sl = sl
        order.instrument = instrument
        order.status = status
        order.buy_id = buy_id or str(uuid.uuid4())
        order.sell_id = sell_id

    def __str__(order):
        return '''
            ID: %s
            Stock: %s
            Strike Price: %s
            Option: %s
            Quantity: %s
            Entry Price: %s
            Target: %s
            Stop Loss: %s
            Status: %s
            Instrument: %s
        ''' % (order.id, order.stock, order.strike_price, order.option,
        order.quantity, order.entry_price, order.target, order.sl, order.status, order.instrument)

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

def order_placed_to_pending_cron():

    if len(orders) == 0: return
  
    threading.Timer(3.0, order_placed_to_pending_cron).start()
  
    for order in orders:

        if order.status == "PLACED":
            
            current_price = view_price_kite_api(order);
        
            if order.entry_price - current_price > 15:
                api.order_cancel_kite_api(order)
                order.status = "PENDING"

def order_pending_to_placed_cron():

    if len(orders) == 0: return

    threading.Timer(3.0, order_pending_to_placed_cron).start()
  
    for order in orders:

        if order.status == "PENDING":

            current_price = view_price_kite_api(order);

            if 0 <= order.entry_price - current_price <= 10:
                order_place(order)

            if order.entry_price < current_price:
                order.status = "CANCELLED"

def update_order_status_cron():

    if len(orders) == 0: return

    threading.Timer(3.0, update_order_status_cron).start()
  
    for order in orders:
        
        if order.status == "PLACED" or order.status == "IN_PROGRESS":
            status = api.view_order_status_kite_api(order)
            order.status = status

def sell_inprogress_order():

    if len(orders) == 0: return

    threading.Timer(3.0, sell_inprogress_order).start()
  
    for order in orders:

        if order.status == "IN_PROGRESS":

            current_price = api.view_price_kite_api(order);
        
            if current_price < sl:
                print("current_price: ", current_price , ", sl: ", sl)
                print("current price less than sl so exit order immediately.")
                api.exit_sell_order_kite_api(order)

            elif current_price > target:
                print("current_price: ", current_price , ", sl: ", sl)
                print("current price is greater than target so exit order immediately.")
                api.exit_sell_order_kite_api(order)

            elif 0 <= (current_price - sl) <= 15:
                print("current_price: ", current_price , ", sl: ", sl)
                print("order near by stoploss. making stoploss order")
                api.sl_sell_order_kite_api(order)

            elif 0 <= (target - current_price) <= 15:
                print("current_price: ", current_price , ", target: ", target)
                print("order near by target. making target order")
                api.target_sell_order_kite_api(order)

def any_running_order():
    for order in orders:
        if order.status == "PLACED" or order.status == "IN_PROGRESS":
            return True
    return False

def order_place(order):

    current_price = api.view_price_kite_api(order.instrument)

    if current_price == -1:
        return

    if validation_order_place(order.entry_price, current_price, order.sl, order.target) ==  False:
        print("INFO: Sorry!! Your Order is not placed.")
        return

    if  order.entry_price - current_price <= 10:

        if config.ONE_ORDER_AT_TIME == True and any_running_order() == True:
            print("ERROR: not able to place order because one order at a time")
            order.status = "CANCELLED"

        api.order_place_kite_api(order)
        return

    order.status = "PENDING"
    orders.append(order)
    print("INFO: your order place in pending queue")

def get_order_by_id(order_id):

    for order in orders:
        if order.id == order_id:
            return order 

    print("ERROR: No order Found with order id = " + order_id)
    return -1

def create_index_order_object(order_input_str):
    
    order_input_array = order_input_str.split(" ")
    stock = order_input_array[0]
    strike_price = int(order_input_array[1])
    option = order_input_array[2]
    entry_price = int(order_input_array[3])
    sl = int(order_input_array[4])
    target = int(order_input_array[5])
    quantity = int(50*config.lot if stock == "N" else 25*config.lot)
    instrument = str('NIFTY' if stock == 'N' else 'BANKNIFTY') + str(config.expiry_flag) + str(strike_price) + str(option).upper()

    return Order(stock=stock,
        strike_price=strike_price,
        instrument=instrument,
        option=option,
        quantity=quantity,
        entry_price=entry_price,
        target=target,
        sl=sl,
    )

def create_stock_order_object(order_input_str): 
    order_input_array = order_input_str.split(" ")
    instrument = order_input_array[0]
    entry_price = int(order_input_array[2])
    sl = int(order_input_array[3])
    target = int(order_input_array[4])
    quantity = int(order_input_array[1])
    
    return Order(stock="",
        strike_price="",
        instrument=instrument,
        option="",
        quantity=quantity,
        entry_price=entry_price,
        target=target,
        sl=sl,
    )

def create_order_string(order):
    return order.stock + " " + str(order.strike_price) + " " + order.option + " " + str(order.entry_price) + " " + str(order.sl) + " " + str(order.target)

def create_menu():

    menu = "\n\n1) Place An Order with NIFTY/BANKNIFTY\n"
    menu += "2) Place An Order with Instrument\n"
    menu += "3) View All Pending Orders\n"
    menu += "4) View All Placed/In-Progress Orders\n"
    menu += "5) Cancel Specific Order\n"
    menu += "6) Cancel All Order\n"
    menu += "7) Modification Of Index Order\n"
    menu += "8) View All Order Information\n"
    menu += "9) Exit\n\nchoice: "
    return input(menu)

if __name__ == "__main__":

    while True:

        try:
            user_input = int(create_menu())
            
            if user_input == 1:
                # order_input_str = input("\n\nPlace order as mentioned Below format\nBN/N strike_price option(CE/PE) entry_price sl target\n")
                print("Place order as mentioned Below format\nBN/N strike_price option(CE/PE) entry_price sl target\n")
                typewrite("BN 33400 CE 550 540 560")
                order_input_str = input()
                order_place(create_index_order_object(order_input_str))

            elif user_input == 2:
                order_input_str = input("\n\nPlace order as mentioned Below format\nInstrument quantity entry_price sl target\n")
                order_place(create_stock_order_object(order_input_str))

            elif user_input == 3:
                for order in orders:
                    if order.status == "PENDING":
                        print(order)

            elif user_input == 4:
                for order in orders:
                    if order.status == "PLACED" or order.status == "IN_PROGRESS":
                        print(order)

            elif user_input == 5:
                order_id = input("\nplease enter order id: ")
                order = get_order_by_id(order_id)
                if order == -1: continue
                if order.status == "PLACED": 
                    api.order_cancel_kite_api(order)
                else: 
                    order.status = "CANCELLED"

            elif user_input == 6:
                for order in orders:
                    if order.status == "PLACED": 
                        api.order_cancel_kite_api(order)
                    else: 
                        order.status = "CANCELLED"

            elif user_input == 7:
                order_id = input("\nplease enter order id: ")
                order = get_order_by_id(order_id)
                if order == -1: continue
                print("Place order as mentioned Below format\nBN/N strike_price option(CE/PE) entry_price sl target\n")
                typewrite(create_order_string(order))
                order_input_str = input()
                order_input_array = order_input_str.split(" ")
                order.stock = order_input_array[0]
                order.strike_price = int(order_input_array[1])
                order.option = order_input_array[2]
                order.entry_price = int(order_input_array[3])
                order.sl = int(order_input_array[4])
                order.target = int(order_input_array[5])
                order.quantity = int(50*config.lot if order.stock == "N" else 25*config.lot)
                order.instrument = str('NIFTY' if order.stock == 'N' else 'BANKNIFTY') + str(config.expiry_flag) + str(order.strike_price) + str(order.option).upper()
                
                if order.status == "PLACED": 
                    api.order_modify_kite_api(order)                    

            elif user_input == 8:
                for order in orders:
                    print(order)

            elif user_input == 9:
                break

        except Exception as e:
            print('Error: %s' % e)
