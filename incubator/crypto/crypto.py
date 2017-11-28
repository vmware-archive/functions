import requests
import urlparse

def handler(event):
   ticker = event.json['crypto']
   path = urlparse.urljoin('https://api.coinmarketcap.com/v1/ticker/', ticker)   
   return requests.get(path).json()[0]['price_usd']
