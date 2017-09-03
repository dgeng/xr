import time
import json
import requests
from exchange_rate_boc import fetch_exchange_rates

ES_POST_URL = 'http://192.168.1.100:9200/forex/boc'

if __name__ == '__main__':
	rates = fetch_exchange_rates()
	for rate in rates:
		rate['@timpstamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
		rate['@version'] = 1
		payload = json.dumps(rate)
		resp = requests.post(ES_POST_URL, data=payload)
		print(resp.text)
