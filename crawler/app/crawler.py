import os
import time
import json
import sys
import traceback
import asyncio
import logging
import requests
from exchange_rate_boc import fetch_exchange_rates


logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


LOG_FILENAME = '/data/crawler.log'

DEBUG = 'DEV' == os.environ.get('ENV')

prev_payload = ''

def job():
    global prev_payload
    try:
        rates = fetch_exchange_rates()
        payload = '\n'.join([json.dumps(rate) for rate in rates])

        # same as before?
        if payload == prev_payload:
            logger.debug("same payload, don't queue!")
            return

        prev_payload = payload

        f = open(LOG_FILENAME, 'a')
        f.write(payload) # json lines
        f.write('\n') # extra new line
        f.close()
    except:
        traceback.print_exc(file=sys.stderr)


interval = 5 * 60
if DEBUG:
    interval = 60


@asyncio.coroutine
def my_coroutine(seconds_to_sleep=interval):
    while True:
        job()
        yield from asyncio.sleep(seconds_to_sleep)

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(my_coroutine()))
loop.close()


if __name__ == '__main__':
    job() # run it now
    while True:
        schedule.run_pending()
        time.sleep(1)

