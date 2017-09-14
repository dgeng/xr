import time
import json
import requests
import schedule
from exchange_rate_boc import fetch_exchange_rates


def job():
    rates = fetch_exchange_rates()
    for rate in rates:
        payload = json.dumps(rate)
        f = open('/data/crawler.log', 'a')
        f.write(payload); f.write('\n')
        f.close()


schedule.every(5).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)

