import unittest
from finder import *

""" TODO:
    Real tests... this is just me being lazy.
    There are some sample_tweets included

"""
class TestTwitter(unittest.TestCase):
    def test_get_trucks(self):
        #results = get_trucks()
        pass

    def test_single_true(self):
        result = get_truck("Angel")
        print result

if __name__ == '__main__':
    unittest.main()
