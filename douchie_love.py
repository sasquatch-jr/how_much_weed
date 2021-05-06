# This is sooooo hacky. I would normally never ship something this bad. But why do it
# right when you can sloppily mash leafly and stripe together with bubble gum and string,
# leak your all of your customer's internal sales data and STILL dupe investors into 
# giving you $200mil to flush down the toilet instead of investing into actual engineering?

import json
import urllib
import requests

from datetime import datetime


header_template = """
<html><head><title>Douche Love Tracker</title></head>
Generated at {} Pacific Time.
<h1>Douche Love Realtime Inventory Tracker</h1>
<h3>Coming soon: historical sales data by SKU and location for every product sold by Douche Love!</h3>
<h2>Select a Douche Love Location:</h2>
<ul>
"""

shop_links_template = "<h3><li><a href=#{}>{}</a></li></h3>"

shop_template_head = """
<h1><a id={} />{}</h1>
<h3>Current Inventory:</h3>
<ul>
"""

product_template = """
<li>{} {} {} - Units in stock: {}</li>
"""

shop_template_footer = "</ul>"

footer_template = """
<h3>How was this made?</h3>
Dutchie exposes a bunch of information about menus in a public GraphQL database and claims they can't fix it! Thanks Dutchie!

<h3>How do I stop people from getting at my sales data?</h3>
Use Shopify for your online menu/pre order system. Unfortunately every other platform licensed for use in Canada at least is also poorly made. I checked both buddi and Highfyre and both also have this issue. Note that I have no relationshop with Shopify, they just appear to be the least bad option for this type of service in Canada.

<h3>Who are you?</h3>
You can email me at sasquatch__jr@outlook.com if you have any questions.
</html>
"""
ids = {
        'Vancouver Airport': 'NBS6kmrMiMtWFFwAe',
        'Vancouver Main Street': 'qsgEGGGcg7LE3P9Lz',
        'Vancouer Kitsilano': 'eQwt74AbmpdzvfiTW',
        'Vancouver Robson Street': 'uSba9ij7Fycszf67Y',
        'Lake Country Winfield': '5f51618d26c96d00cd61e0c0',
        'Kelowna Springfield': 'Fb69fqLTuGewASapD',
        'Toronto Bloorcourt': '5f9c46478f675300c58eef93',
        'Toronto Mount Dennis': '5fac37aae01cc600b8e07b20',
        'Toronto Danforth Villiage': '5ecfeb1f0d4f6001515c731b',
        'Toronto Leslieville': '5ecfe9ea9b89617f2264f34d',
        'Toronto Parkdale': '5f32dbfe0bfd8500b35e5695',
        'Toronto Theatre District': '5f91b4618f2c84010254aa61',
        'Toronto Younge Dundas': '5eac4630e64b1201089b3606',
        'Brampton Bramalea': '5ecfeb9fbd7b140150cbafe3',
        'Ottawa ByWard': 'fjySu4BPYqScFCR2t',
        'Ottawa Centretown': '5f03a722c696510135ab9ded',
        'Ottawa Merivale': '5e73d567a30878006b350303',
        'Timmins Mountjoy': '5e73d58c33102a006ad63d15',
        'Calgary Mission': '5eea506f34f00000ff761fa9',
        'Edmonton Whyte Ave': '5eea504d0b03ce00eb3b277b',
      }

url = """https://dutchie.com/graphql?operationName=FilteredProducts&variables={"productsFilter":{"dispensaryId":"BOOOM","bypassOnlineThresholds":false,"types":["Flower", "Pre-Rolls", "Vaporizers", "Concentrates", "Edibles", "Topicals", "Accessories"]},"useCache":true}&extensions={"persistedQuery":{"version":1,"sha256Hash":"66141e1331cbd1cd0ad2dbdbc41000536a3de81e39c265015f88e12610374d8c"}}"""

store_htmls = []
shop_links = []

for store, id in ids.items():
    menu_url = url.replace("BOOOM", id)
    menu = requests.get(menu_url)
    products = menu.json()['data']['filteredProducts']['products']
    shop_links.append(shop_links_template.format(id, store))
    product_htmls = []

    for p in products:
        prod_name = p['Name']
        brand = p['brandName']
        for s in p['POSMetaData']['children']:
            product_htmls.append(product_template.format(brand, prod_name, s['option'], s['quantity']))
    store_htmls.append(shop_template_head.format(id, store) + ''.join(product_htmls) + shop_template_footer)
open('douche_love.html', 'w').write(header_template.format(datetime.now()) + ''.join(shop_links) + ''.join(store_htmls) + footer_template)
