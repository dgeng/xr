import httplib, urllib
from urlparse import urlparse
from HTMLParser import HTMLParser

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

    u = urlparse(URL_EXCHANGE_RATE_CMB)
    conn = httplib.HTTPConnection(u.hostname, u.port)

    conn.request("GET", u.path)
    response = conn.getresponse()
    html = response.read()
    conn.close()

    parser.feed(html)
    for each in parser.exchange_rates:
        print each
