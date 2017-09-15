import time
import json
import sys
import traceback
import requests
import schedule
from exchange_rate_boc import fetch_exchange_rates


prev_payload = ''

def job():
    global prev_payload
    try:
        rates = fetch_exchange_rates()
        payload = '\n'.join([json.dumps(rate) for rate in rates])

        # don't log if it's the same as before
        if payload == prev_payload:
            return
        prev_payload = payload

        f = open('/data/crawler.log', 'a')
        f.write(payload) # json lines
        f.write('\n') # extra new line
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
