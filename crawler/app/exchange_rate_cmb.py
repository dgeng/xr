import logging
import requests
from html.parser import HTMLParser

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

URL_EXCHANGE_RATE_CMB = 'http://fx.cmbchina.com/hq/'

class CMBHTMLParser(HTMLParser):
    def __init__(self):
        self.in_exchange_rate_table = False
        self.in_tr = False
        self.in_td = False
        HTMLParser.__init__(self)
        self.exchange_rates = []
        self.current_exchange_rate = []
        self.current_data = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'table' and ('class', 'data') in attrs:
            self.in_exchange_rate_table = True

        if self.in_exchange_rate_table and tag == 'tr':
            self.in_tr = True

        if self.in_exchange_rate_table and self.in_tr and tag in ['td', 'th']:
            self.in_td = True

    def handle_endtag(self, tag):
        if self.in_exchange_rate_table and tag == 'tr':
            self.exchange_rates.append(self.current_exchange_rate)
            self.current_exchange_rate = []
            self.in_tr = False

        if self.in_exchange_rate_table and self.in_tr and tag in ['td', 'th']:
            self.current_exchange_rate.append(self.current_data.strip())
            self.current_data = ''
            self.in_td = False

        if tag == 'table':
            self.in_exchange_rate_table = False

    def handle_data(self, data):
        if self.in_exchange_rate_table and self.in_tr and self.in_td:
            self.current_data += data


if __name__ == '__main__':
    parser = CMBHTMLParser()

    r = requests.get(URL_EXCHANGE_RATE_CMB)
    parser.feed(r.text)

    from prettytable import PrettyTable
    x = PrettyTable()

    header = parser.exchange_rates[0]
    x.field_names = header
    for row in parser.exchange_rates[1:]:
        x.add_row(row)
    # Change some column alignments; default was 'c'

    x.align = "r"
    x.align[header[0]] = 'l'
    print(x)
