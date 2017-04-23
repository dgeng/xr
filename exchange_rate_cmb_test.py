import unittest
from exchange_rate_cmb import CMBHTMLParser

class CMBHTMLParserTest(unittest.TestCase):
    def test_parse(self):
        with open('cmb.html') as f:
            parser = CMBHTMLParser()
            parser.feed(f.read())
            self.assertTrue(len(parser.exchange_rates) > 1)


if __name__ == '__main__':
    unittest.main()
