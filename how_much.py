# This is sooooo hacky. I would normally never ship something this bad. But why do it
# right when you can sloppily mash leafly and stripe together with bubble gum and string,
# leak your all of your customer's internal sales data and STILL dupe investors into 
# giving you $200mil to flush down the toilet instead of investing into actual engineering?

import json
import requests

from datetime import datetime


header_template = """
<html><head><title>How much weed does Berner have?</title></head>
<h2>As of {} Pacific Time, Berner has {} grams of flower on the shelf at Cookies shops that use Dutchie. That's {} pounds!
<br />
Here's the breakdown by location:<h2>
<ul>
"""

item_template = """
<li>{} has {}g on the self right now. That's {} pounds! (<a href={}>Source for figures</a>)</li>
"""

no_dutchie_template = """
<li>{} does not use Dutchie. Ask Berner to switch so we know how much weed is at this location too!</li>
"""

no_pos_md_template = """
<li>{} does use Dutchie, but their menu does have stock information. Ask Dutchie how this can be if they can't fix this issue?</li>
"""

footer_template = """
</ul>
<h3>How was this made?</h3>
<a href="https://github.com/sasquatch-jr/how_much_weed/blob/master/how_much.py">Here's the source code</a>. Dutchie exposes a bunch of information about menus in a public GraphQL database. This for some reason includes real time stock levels! This is a very basic demo, but one could track all kinds of fun stuff about their competition using this information. Looking to open a dispo near a shop that uses Dutchie? Now you can get real time sales data from the other guys and know if that area is worth your time. Thanks Dutchie!

<h3>How do I stop people from getting at my sales data?</h3>
Stop using Dutchie. In the US <a href='https://www.iheartjane.com/'>Jane</a> seems popular. In Canada <a href='https://buddi.io/'>Buddi</a> seems to have been built by people who actually thought about privacy and security. Note, I have no relationship with either of those companies!

<h3>Who are you?</h3>
You can email me at sasquatch__jr@outlook.com if you have any questions.
</html>
"""
ids = {
        'Redding': 'jZkf8BxpLkgKrCjmM',
        'Denver': 'o33FJMsYrRBPb5c4n',
        'Hayward': '5efcea98abc6530139021996',
        'La Mesa': '5ed6b411f6561400b4f04283',
        'OKC South Penn': '601c9f7e932ccd00bf6a9160',
        'OKC': '5faca3a0d891d700c126d754',
        'Maywood': 'Z6RTWRL9Dwgw7oPtp',
        'Corvallis': '601ca07d5b57ca00dd1ada1a',
        'Detroit': '5e28b8bbe67a5300752a2c02',
        'Melrose': 'C5jbN7mG4CBXQRr25',
        'Oakland': 'AL9szbLmyDNYBtPuN',
        'Modesto': 'pyEyQ5arpHrk5At2G',
        'Merced': 'Z6RTWRL9Dwgw7oPtp',
        'Sacramento': '5fc6a21c0b0a0a00c96cdc16',
        'Tacoma': '5f5fe0cc8a0ba700e30da786',
        'Kalamazoo': None,
        'Lompoc': None,
        'Pueblo': None,
        'Tree Lounge': None,
        'Haight': None,
        'Missoula': None,
        'Las Vegas': None,
        'Tel Aviv': None,
        'Woodland Hills': None
       }

url = """https://dutchie.com/graphql?operationName=FilteredProducts&variables={"productsFilter":{"dispensaryId":"BOOOM","bypassOnlineThresholds":false,"types":["Flower"]},"useCache":true}&extensions={"persistedQuery":{"version":1,"sha256Hash":"66141e1331cbd1cd0ad2dbdbc41000536a3de81e39c265015f88e12610374d8c"}}"""

options = {"1/8oz": 3.5,
           "1/4oz": 7.0,
           "1/2oz": 14.0,
           "1oz": 28.0}

grams = 0

item_htmls = []

for store, id in ids.items():
    if id is None:
        item_htmls.append(no_dutchie_template.format(store))
        continue


    menu_url = url.replace("BOOOM", id)
    menu = requests.get(menu_url)
    products = menu.json()['data']['filteredProducts']['products']

    if not products[0].get('POSMetaData'):
        item_htmls.append(no_pos_md_template.format(store))
        continue

    store_grams = 0
    for p in products:
        skus = p['POSMetaData']['children']
        for s in skus:
            if 'g' in s['option']:
                grams_sku = float(s['option'].split('g')[0])
            else:
                grams_sku = options[s['option']]
            store_grams += (grams_sku * s['quantity'])
    item_htmls.append(item_template.format(store, store_grams, store_grams / 453.592, menu_url))
    grams += store_grams

open('index.html', 'w').write(header_template.format(datetime.now(), grams, grams / 453.592) + ''.join(item_htmls) + footer_template)
