import everpay
import permaswap
from binance.client import Client

# initial Permaswap account
api_server = 'https://api.everpay.io'
pk = ''
signer = everpay.ETHSigner(pk)
account = everpay.Account(api_server, signer)
router_host = 'wss://router.permaswap.network/'
swap = permaswap.Permaswap(router_host, account)

# initial Binance account
Public_Key = ''
Private_key = ''
client = Client(Public_Key, Private_key)

ar_buy_price_permaswap = 5

while True:
    try:
        while True:
            ar_binance = client.get_symbol_ticker(symbol='ARUSDT')
            ar_price_binance = float(ar_binance['price'])
            ar_sell_order = swap.get_order('AR', 'USDC', 15*10 ** 12)
            ar_sell_price_permaswap = 1 / float(ar_sell_order['price'])
            price_spread1 = (ar_sell_price_permaswap - ar_price_binance) / ar_sell_price_permaswap
            print('price_spread1:',price_spread1)
            if price_spread1 > 0.01:
                sell_permaswap = swap.place_order(ar_sell_order)
                buy_binance = client.order_market_buy(symbol='ARUSDT', quantity=15)
                print(sell_permaswap,buy_binance)
            if price_spread1 < 0:
                break
        while True:
            ar_binance = client.get_symbol_ticker(symbol='ARUSDT')
            ar_price_binance = float(ar_binance['price'])
            ar_buy_order = swap.get_order('USDC', 'AR', 80*10**6)
            ar_buy_price_permaswap = float(ar_buy_order['price'])
            price_spread2 = (ar_buy_price_permaswap - ar_price_binance) / ar_buy_price_permaswap
            print('price_spread2:',price_spread2)
            if price_spread2 < -0.01:
                buy_permaswap = swap.place_order(ar_buy_order)
                sell_binance = client.order_market_sell(symbol='ARUSDT', quantity=round(80/ar_buy_price_permaswap,2))
                print(buy_permaswap,sell_binance)
            if price_spread2 >0:
                break
    except:
        print('erro')
