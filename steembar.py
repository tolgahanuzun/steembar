#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# <bitbar.title>Steemit Bar</bitbar.title>
# <bitbar.version>v0.1</bitbar.version>
# <bitbar.author>Tolgahan Üzün</bitbar.author>
# <bitbar.author.github>tolgahanuzun</bitbar.author.github>
# <bitbar.desc>A bar application for Steemit.</bitbar.desc>
# <bitbar.image>https://raw.githubusercontent.com/tolgahanuzun/steembar/master/steembar.png</bitbar.image>
# <bitbar.dependencies>python3</bitbar.dependencies>

# Steem         : https://api.coinmarketcap.com/v1/ticker/steem/
# Steem-dollars : https://api.coinmarketcap.com/v1/ticker/steem-dollars/
# Bitcoin       : https://api.coinmarketcap.com/v1/ticker/bitcoin/
# Steem Api Exp : https://api.steemjs.com/get_state?path=@tolgahanuzun
# Steem APi     : https://steemit.com/@tolgahanuzun.json

import requests
import os
from math import ceil
from math import log
from math import isnan

global STEEM_NAME

choose = ['steem', 'steem-dollars', 'bitcoin']
URL = 'https://api.coinmarketcap.com/v1/ticker/{}'
API = 'https://api.steemjs.com/'

def fetch(url):
    response = requests.get(url).json()
    return response

def get_coin(coin):
    url = URL.format(coin)
    data = fetch(url)[0]
    return data['price_usd'], data['percent_change_24h']

def steemit_api(steemit_name):
    url = '{}get_state?path=@{}'.format(API, steemit_name)
    return fetch(url)


def get_vp_rp(steemit_name):
    url = '{}get_accounts?names[]=%5B%22{}%22%5D'.format(API, steemit_name)
    data = fetch(url)[0]
    vp = data['voting_power']
    _reputation = data['reputation']
    _reputation = int(_reputation)

    rep = str(_reputation)
    neg = True if rep[0] == '-' else False
    rep = rep[1:] if neg else rep
    srt = rep
    leadingDigits = int(srt[0:4])
    log_n = log(leadingDigits / log(10), 2.71828)
    n  = len(srt) - 1
    out = n + (log_n - int(log_n))
    if isnan(out): out = 0
    out = max(out - 9, 0)

    out = (-1 * out) if neg else (1 * out)
    out = out * 9 + 25
    out = int(out)
    return [ceil(vp / 100), out]

def blog_list(steemit_name, number=10):
    posts = steemit_api(steemit_name)
    post = posts['content']

    result = []
    for pk in posts['accounts'][steemit_name]['blog'][:number]:
        result.append({"result_blog":pk,
                       "result_url": 'https://steemit.com{}.json'.format(post[pk]['url']),
                       "tittle":post[pk]['root_title'],
                       "votes":post[pk]['net_votes'],
                       "balance":post[pk]['pending_payout_value']})

    return result

def balance(steemit_name):
    data = steemit_api(steemit_name)
    balance = data['accounts'][steemit_name]['sbd_balance']
    balance = balance.split(' SBD')[0]
    return balance

def main():
    print("---")
    print('@{} ({})'.format(STEEM_NAME, get_vp_rp(STEEM_NAME)[1]) +
          "| color=black href=https://steemit.com/@{}".format(STEEM_NAME))
    print('Voting Power: %{}'.format(get_vp_rp(STEEM_NAME)[0]))
    print("---")
    for blog in blog_list(STEEM_NAME):
        if STEEM_NAME in blog['result_url']:
            print(blog['tittle'].encode('utf-8').strip()[0:30].decode('ascii', 'ignore')+ '| ')
            print('--' + "Votes: {}".format(blog['votes']))
            print('--' + "Balance: {}".format(blog['balance']))
            print('--' + "Go to Post | href=" + blog['result_url'])


if __name__ == '__main__':
    try:
        STEEM_NAME = os.environ['steemitname']
    except:
        STEEM_NAME = 'tolgahanuzun'

    try:
        steem_usd, steem_change_24 = get_coin(choose[0])
        sbd_usd, sbd_change_24 = get_coin(choose[1])
        bitcoin_usd, btc_change_24 = get_coin(choose[2])
        text = "Steem: $ {} - SBD: $ {}".format(steem_usd, sbd_usd)
        print(text)
        print('---')
        text = "Bitcoin: $ {} (% {})".format(bitcoin_usd, btc_change_24)
        print(text)
        balance = balance(STEEM_NAME)
        text = "Balance:  {} - USD to $ {:.2f}".format(balance, float(steem_usd) * float(balance))        
        print(text)
        main()
    except requests.ConnectionError:
        text = "Please check your internet connection."
        print(text)
    