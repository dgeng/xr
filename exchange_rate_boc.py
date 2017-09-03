import httplib, urllib
from urlparse import urlparse
from HTMLParser import HTMLParser

URL_EXCHANGE_RATE_BOC = 'http://www.boc.cn/sourcedb/whpj/enindex.html'

class BOCHTMLParser(HTMLParser):
    def __init__(self):
        self.in_exchange_rate_table = False
        self.in_tr = False
        self.in_td = False
        HTMLParser.__init__(self)
        self.exchange_rates = []
        self.current_exchange_rate = []
        self.current_data = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'table' and ('bgcolor', '#EAEAEA') in attrs:
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
            self.current_exchange_rate.append(self._normalize(self.current_data))
            self.current_data = ''
            self.in_td = False

        if tag == 'table':
            self.in_exchange_rate_table = False

    def handle_data(self, data):
        if self.in_exchange_rate_table and self.in_tr and self.in_td:
            self.current_data += data


    def _normalize(self, data):
        data = data.strip()
        if not data:
            return '-'
        return data.replace('\n\t\t', ' ')

def fetch_raw_exchange_rates():
    parser = BOCHTMLParser()

    u = urlparse(URL_EXCHANGE_RATE_BOC)
    conn = httplib.HTTPConnection(u.hostname, u.port)

    conn.request("GET", u.path)
    response = conn.getresponse()
    html = response.read()
    conn.close()
    parser.feed(html)
    return parser.exchange_rates

def fetch_exchange_rates():
    raw_rates = fetch_raw_exchange_rates()[1:] # remove header
    rates = []
    for currency, buying_rate, cash_buying_rate, selling_rate, cach_selling_rate, middle_rate, pub_time in raw_rates:
        rate = {
            "currency": currency,
            "buying_rate": buying_rate,
            "cash_buying_rate": cash_buying_rate,
            "selling_rate": selling_rate,
            "cach_selling_rate": cach_selling_rate,
            "middle_rate": middle_rate,
            "pub_time": pub_time
        }

        for k, v in rate.items():
            if v == '-':
                rate[k] = '0.0'

        rates.append(rate)

    return rates

if __name__ == '__main__':
    exchange_rates = fetch_raw_exchange_rates()
    import prettytable
    x = prettytable.PrettyTable()

    header = exchange_rates[0]
    x.field_names = header
    for row in exchange_rates[1:]:
        x.add_row(row)
    # Change some column alignments; default was 'c'

    # x.hrules = prettytable.ALL
    x.align = "r"
    x.align[header[0]] = 'l'
    print x
