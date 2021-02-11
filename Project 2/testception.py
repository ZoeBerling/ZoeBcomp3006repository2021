import unittest
import count
import sys
import string

class TestArg(unittest.TestCase):

    def test_c_l_z(self):
        list.extend(sys.argv, ['-l', 'e','-c', 'z', 'count_txt'])
        self.assertEqual(count.og_function().get('e'), 1) # e is counted correctly
        self.assertEqual(len(count.og_function()), 52) # even though -l trumps ever other argument, -z should still populate the dictionary with every value: this fails.