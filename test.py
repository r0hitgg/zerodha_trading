import logging
from kiteconnect import KiteConnect

logging.basicConfig(level=logging.DEBUG)

def main():
    user_input = create_menu()
    print(user_input,'USER Input')
    if user_input == 1:
        take_view_price_input()
        view_price()

def take_view_price_input():
    op_type = input('Enter Ninfy/Banknifty')
    flag = input('Enter Flag')
    strike_price = input('Enter Strice Price')
    strike_price = input('Enter CE/PE')

def view_price():
    kite.set_access_token('MI0WjCvsPeFpkWBKH7V8Du95kZBwgo06')

    res = kite.quote(['NSE:NIFTY'])
    print(res,'11111')


def create_menu():
    inp = input('''1) View Price
''')
    return inp

if __name__ == "__main__":
    main()
kite = KiteConnect(api_key="ge1fsvh1bto8z2os")
# # Redirect the user to the login url obtained
# # from kite.login_url(), and receive the request_token
# # from the registered redirect url after the login flow.
# # Once you have the request_token, obtain the access_token
# # as follows.
# # print(kite.login_url())


# data = kite.generate_session("BTNcDZjb7EVa2wD02CO95qh4XUxqvRII", api_secret="3f4sbjxkpxf2thpl5qcvvj05vde5egxp")
# print(data["access_token"],'TOEKN\n\n\n')
kite.set_access_token('MI0WjCvsPeFpkWBKH7V8Du95kZBwgo06')
res = kite.quote(['NFO:INFY'])
print(res,'11111')
# res = kite.quote(['NSE:NIFTY'])
# print(res,'222222')


