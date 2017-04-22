import httplib, urllib
from urlparse import urlparse
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

URL_PBOC_EXCHANGE_RATE = 'http://www.boc.cn/sourcedb/whpj/enindex.html'

class MyHTMLParser(HTMLParser):
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
            self.current_exchange_rate.append(self.current_data)
            self.current_data = ''
            self.in_td = False

        if tag == 'table':
            self.in_exchange_rate_table = False

    def handle_data(self, data):
        if self.in_exchange_rate_table and self.in_tr and self.in_td:
            self.current_data += data

    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        # print "Named ent:", c

    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        # print "Num ent  :", c


parser = MyHTMLParser()

u = urlparse(URL_PBOC_EXCHANGE_RATE)
conn = httplib.HTTPConnection(u.hostname, u.port)

conn.request("GET", u.path)
response = conn.getresponse()
html = response.read()
conn.close()

parser.feed(html)
for each in parser.exchange_rates:
    print each

