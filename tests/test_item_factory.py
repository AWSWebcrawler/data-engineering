"""Class to test the item factory module."""
import unittest
from exceptions.item_factory_exception import LxmlTreeNotInitializedError
from crawler.item_factory import item_factory


class TestItemFactory(unittest.TestCase):
    """Test Class for item factory module"""

    def setUp(self) -> None:
        # url0 is just a dummy because we expect an error
        self.url0 = 'test_url'
        self.url1 = 'https://www.amazon.de/der-neue-echo-dot-4-generation-smarter-lautsprecher-mit-alexa-anthrazit/' \
                    'dp/B084DWG2VQ'
        self.url2 = 'https://www.amazon.de/Xbox-Wireless-Controller-Electric-Volt/dp/B091CK241X'
        self.url3 = 'https://www.amazon.de/Samsung-Galaxy-Buds-Pro-2-Wege-Lautsprecher/dp/B08QYRYH9J'
        with open('./test_item_factory_testfile1.html', 'r', encoding='utf8') as file:
            self.test_html_1 = file.read()
        with open('./test_item_factory_testfile2.html', 'r', encoding='utf8') as file:
            self.test_html_2 = file.read()
        with open('./test_item_factory_testfile3.html', 'r', encoding='utf8') as file:
            self.test_html_3 = file.read()

    def test_create_item(self):
        """Tests the create item function of the item_factory module"""

        with self.assertRaises(LxmlTreeNotInitializedError):
            product = item_factory.create_item("", self.url0)

        product = item_factory.create_item(self.test_html_1, self.url1)
        # the values for time and date are created dynamically so this is a problem for a test with a hardcoded string
        # as expected value, so i am setting it to None
        product["time"] = None
        product["date"] = None
        product["timestamp"] = None

        expected = "{'name': 'Echo Dot (4. Generation) | Smarter Lautsprecher mit Alexa | Anthrazit', 'current_price'" \
                   ": 29.18, 'price_regular': 59.99, 'prime': True, 'discount_in_euros': 30.81, 'percent_discount'" \
                   ": 51.0, 'sold_by_amazon': True, 'seller': 'Amazon', 'amazon_choice': True, 'asin': 'B084DWG2VQ', " \
                   "'url': 'https://www.amazon.de/der-neue-echo-dot-4-generation-smarter-lautsprecher-mit-alexa-" \
                   "anthrazit/dp/B084DWG2VQ', 'timestamp': None, 'date': None, 'time': None}"
        self.assertEqual(expected, str(product), "The created product does not match the expected output.")

        product = item_factory.create_item(self.test_html_2, self.url2)
        product["time"] = None
        product["date"] = None
        product["timestamp"] = None

        expected = "{'name': 'Xbox Wireless Controller Electric Volt', 'current_price'" \
                   ": None, 'price_regular': None, 'prime': False, 'discount_in_euros': None, 'percent_discount'" \
                   ": None, 'sold_by_amazon': False, 'seller': None, 'amazon_choice': False, 'asin': 'B091CK241X', " \
                   "'url': 'https://www.amazon.de/Xbox-Wireless-Controller-Electric-Volt/dp/B091CK241X'," \
                   " 'timestamp': None, 'date': None, 'time': None}"
        self.assertEqual(expected, str(product), "The created product does not match the expected output.")

        product = item_factory.create_item(self.test_html_3, self.url3)
        product["time"] = None
        product["date"] = None
        product["timestamp"] = None

        expected = "{'name': 'Samsung Galaxy Buds Pro, Kabellose Kopfhörer, Wireless Earbuds, ausdauernder Akku, 3 " \
                   "Mikrofone, Sound by AKG, 2-Wege-Lautsprecher inkl. Araree Clear Cover, Phantom Black " \
                   "(Deutsche Version)', 'current_price': 99.0, 'price_regular': 112.99, 'prime': True," \
                   " 'discount_in_euros': 13.99, 'percent_discount': 12.0, 'sold_by_amazon': True, 'seller': 'Amazon'" \
                   ", 'amazon_choice': True, 'asin': 'B08QYRYH9J', " \
                   "'url': 'https://www.amazon.de/Samsung-Galaxy-Buds-Pro-2-Wege-Lautsprecher/dp/B08QYRYH9J'," \
                   " 'timestamp': None, 'date': None, 'time': None}"
        self.assertEqual(expected, str(product), "The created product does not match the expected output.")
