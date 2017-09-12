import time
import json
import requests
import redis
from exchange_rate_boc import fetch_exchange_rates

if __name__ == '__main__':
    rates = fetch_exchange_rates()
    r = redis.StrictRedis(host='10.0.0.30', port=6379, db=0)
    for rate in rates:
        payload = json.dumps(rate)
        r.rpush('logstash', payload)
