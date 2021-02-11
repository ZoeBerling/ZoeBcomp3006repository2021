import unittest
import sys
sys.path.insert(0, "/home/zoebe/PycharmProjects/DUAssignments/Project1")  # my path was broken so this is here to fix it
import count

"""Make sure to write test cases for every combination of flags."""
"""List of possible combinations:
c
z
l
cz
zl
cl
czl
czl
"""


class TestArg(unittest.TestCase):

    def test_c(self):
        """checks if -c is working correctly using text from count.txt"""
        self.assertNotEqual(count.add_frequencies({}, 'count_txt', False),
                         {'h': 2, 'e': 2, 'l': 2, 'o': 2})  # checks if letters change to lowercase:
        self.assertEqual(len(count.add_frequencies({}, 'count_txt', True)), 4)  # Check length of c:


    def test_z(self):
        """checks if -z is working correctly using text from count.txt"""
        list.extend(sys.argv, ['-z', 'count_txt'])
        self.assertEqual(len(count.og_function()), 26*2) # Check length of z:


    def test_l(self): # Check length of l
        """checks if -l is working correctly using text form count.txt"""
        list.extend(sys.argv, ['-l', 'eo', 'count_txt'])
        self.assertEqual(count.og_function(), {'E': -1, 'H': -1, 'L': -1, 'O': -1, 'e': 1, 'h': -1, 'l': -1, 'o': 1}) # check if all other letters are -1


    def test_c_z(self):
        """check if -z + -c is 26 letters long"""
        list.extend(sys.argv, ['-c', '-z', 'count_txt'])
        self.assertEquals(len(count.og_function()),
                          26)  # This fails because -c is handled before -z in original code


    def test_z_l(self):
        """check if -z + -l is 2 letters long"""
        list.extend(sys.argv, ['-l', 'oe', '-z', 'count_txt'])
        dictionary = count.og_function()
        self.assertEquals(sum(x != -1 for x in dictionary.values()), 2)  # test if the only values counted are oe


    def test_c_l(self):
        """check if c and l are additive"""
        list.extend(sys.argv, ['-l', 'f', '-c', 'count_txt'])
        self.assertEquals(count.og_function(),
                          {i: -1 for i in 'HELOhelo'})  # test if -l forces -c to show letters that aren't in the -l argument

    def test_c_l_z(self):
        # def test_c_l_z(self):
        # self.assertEqual(count.og_function(), '')
        """check if clz = lzc = zlc"""

    def test_c_l_z(self):
        list.extend(sys.argv, ['-l', 'e','-c', 'z', 'count_txt'])
        self.assertEqual(count.og_function().get('e'), 1) # e is counted correctly
        self.assertEqual(len(count.og_function()), 52) # even though -l trumps ever other argument, -z should still populate the dictionary with every value: this fails.