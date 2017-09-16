import os
import time
import json
import sys
import traceback
import requests
import schedule
from exchange_rate_boc import fetch_exchange_rates


LOG_FILENAME = '/data/crawler.log'

DEBUG = 'DEV' == os.environ.get('ENV')

prev_payload = ''

def job():
    global prev_payload
    try:
        rates = fetch_exchange_rates()
        payload = '\n'.join([json.dumps(rate) for rate in rates])

        # same as before?
        if payload == prev_payload and not DEBUG:
            return

        prev_payload = payload

        f = open(LOG_FILENAME, 'a')
        f.write(payload) # json lines
        f.write('\n') # extra new line
        f.close()
    except:
        traceback.print_exc(file=sys.stderr)


interval = 5
if DEBUG:
    interval = 1

schedule.every(interval).minutes.do(job)


if __name__ == '__main__':
    job() # run it now
    while True:
        schedule.run_pending()
        time.sleep(1)

