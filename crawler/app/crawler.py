import time
import json
import sys
import traceback
import requests
import schedule
from exchange_rate_boc import fetch_exchange_rates


def job():
    try:
        rates = fetch_exchange_rates()
        f = open('/data/crawler.log', 'a')
        for rate in rates:
            payload = json.dumps(rate)
            f.write(payload); f.write('\n')
        f.close()
    except:
        traceback.print_exc(file=sys.stderr)


schedule.every(5).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)


if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
