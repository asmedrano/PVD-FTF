import unittest
from finder import *

""" TODO:
    Real tests... this is just me being lazy.
    There are some sample_tweets included

"""
class TestTwitter(unittest.TestCase):
    def test_get_trucks(self):
        print get_trucks()

if __name__ == '__main__':
    unittest.main()
