#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# <bitbar.title>Steemit Bar</bitbar.title>
# <bitbar.version>v0.1</bitbar.version>
# <bitbar.author>Tolgahan Üzün</bitbar.author>
# <bitbar.author.github>tolgahanuzun</bitbar.author.github>
# <bitbar.desc>A bar application for Steemit.</bitbar.desc>
# <bitbar.image> Coming. </bitbar.image>
# <bitbar.dependencies>python3</bitbar.dependencies>

# Steem         : https://api.coinmarketcap.com/v1/ticker/steem/
# Steem-dollars : https://api.coinmarketcap.com/v1/ticker/steem-dollars/ 

from os.path import expanduser
import urllib.request
import json

choose = ['steem', 'steem-dollars']
STEEM_NAME = 'tolgahanuzun' 

URL = 'https://api.coinmarketcap.com/v1/ticker/{}'
API = 'https://api.steemjs.com/'

def fetch(url):
    response = urllib.request.urlopen(url)
    data = response.read()
    data = json.loads(data)[0]
    return data

def get_coin(coin):
    url = URL.format(coin)
    data = fetch(url)
    return data['price_usd']

def steemit_api(steemit_name):
    url = '{}get_state?path=@{}'.format(API, steemit_name)
    return fetch(url)

def blog_list(steemit_name, number=10):
    posts = steemit_api(steemit_name)
    post = posts['content']
    result = {'result_blog': [], 'result_url': []}
    for pk in posts['accounts'][result]['blog'][:number]:
        if post[pk]['category'] == 'utopian-io':
            result['result_blog'].append(pk)
            result['result_url'].append(post[pk]['url'])
    return result


def main():
    steem_usd = get_coin(choose[0])
    sbd_usd = get_coin(choose[1])
    text = "Steem: $ {} - SBD: $ {}".format(steem_usd, sbd_usd )
    print(text)
    print("---")
    print('@'+ STEEM_NAME + "| color=black")
    print("---")

main()
