import unittest
from exchange_rate_boc import BOCHTMLParser

class BOCHTMLParserTest(unittest.TestCase):
    def test_parse(self):
        with open('boc.html') as f:
            parser = BOCHTMLParser()
            parser.feed(f.read())
            self.assertTrue(len(parser.exchange_rates) > 1)


if __name__ == '__main__':
    unittest.main()
