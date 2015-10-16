import unittest
import random
import string
from hashmap import HashMap

# Executable tests for hashmap.py follow.

class TestBasicHashMap(unittest.TestCase):

    ''' Tests our HashMap() object. '''

    @classmethod
    def setUpClass(cls):
        # class variable run before the test suite.
        # We'll be making changes to this with each
        # test.

        cls.hashmap = HashMap()

    def test_01(self):

        ''' Is it initialised with the right number of keys i.e. 0 ? '''

        self.assertEqual(len(self.hashmap._keys), 0)

    def test_02(self):

        ''' Is the inital size of the table of values correct? '''

        self.assertEqual(len(self.hashmap._values), 256)

    def test_03(self):

        ''' Does inserting an element work? '''

        self.hashmap[1] = 'First'
        self.assertEqual(self.hashmap[1], 'First')
    
    def test_04(self):

        ''' Does updating an element work? '''

        self.hashmap[1] = 'Second'
        self.assertEqual(self.hashmap[1], 'Second')

    def test_05(self):
        
        ''' Does my implementation break on having multiple (non-random) elements? Are the keys correctly stored? '''

        self.hashmap['a'] = 'Do'
        self.hashmap['bab'] = 'Re'
        self.hashmap['mht'] = 'Fa'
        self.assertEqual(self.hashmap._keys, [1,'a','bab','mht'])

    def test_06(self):

        ''' Tests if iteration obtains a list of keys using 'for x in HashMap()' syntax '''

        keys = [key for key in self.hashmap]
        self.assertEqual(keys, [1,'a','bab','mht'])

    def test_07(self):
        
        ''' Does my implementation get values for multiple elements efficiently? Iteration has been tested. '''

        values = [self.hashmap[key] for key in self.hashmap]
        self.assertEqual(values, ['Second','Do','Re','Fa'])

    def test_08(self):
        
        ''' Does my implementation break on updating multiple (non-random) elements? '''

        self.hashmap['a'] = 'DoDo'
        self.hashmap['bab'] = 'ReRe'
        self.hashmap['mht'] = 'FaFa'
        values = [self.hashmap[x] for x in self.hashmap]
        self.assertEqual(values, ['Second','DoDo','ReRe','FaFa'])

    def test_09(self):
        
        ''' Does resizing work? '''

        self.hashmap.__resize__()
        self.assertEqual(len(self.hashmap._values), 512)

    def test_10(self):

        ''' Did resizing alter my ability to retrieve keys? '''

        values = [keys for keys in self.hashmap]
        self.assertEqual(values, [1,'a','bab','mht'])

    def test_11(self):

        ''' Did resizing alter my ability to retrieve values? '''

        values = [self.hashmap[keys] for keys in self.hashmap]
        self.assertEqual(values, ['Second','DoDo','ReRe','FaFa'])

    def test_12(self):

        ''' Will it resize if it detects a collision? '''

        # hash() on integers yields the integer itself, and
        # 513 % 512 == 1 % 512, so this should colllide if
        # there is already a 1 in our table of keys - which
        # there is.

        self.hashmap[513] = 'Collision'
        self.assertEqual(len(self.hashmap._values), 1024)

    def test_13(self):

        ''' After resizing on a collision, are the keys safe? '''
        keys = [key for key in self.hashmap]

        self.assertEqual(keys, [1,'a','bab','mht',513])

    def test_14(self):

        ''' After resizing on a collision, are the values safe? '''
        values = [self.hashmap[key] for key in self.hashmap]

        self.assertEqual(values, ['Second','DoDo','ReRe','FaFa','Collision'])

class TestStressedHashMap(unittest.TestCase):

    ''' 

    Stress tests our HashMap() object by overloading it where possible. The ability to resize
    when the load factor of 10 percent is exceeded is tested, as are the safety of the keys.

    Random variables are used throughout for the keys and values.

    '''

    @classmethod
    def setUpClass(cls):
        # class variable run before the test suite.
        # We'll be making changes to this with each
        # test.

        cls.hashmap = HashMap()
        cls.key_list = [''.join(random.choice(string.lowercase) for i in xrange(100)) for j in xrange(26)]# 26 random keys
        cls.value_list = random.sample(range(1000), 26) # 26 random values

    def test_01(self):

        ''' Does the hashmap resize its values when load factor is exceeded? '''

        for key, value in zip(self.key_list,self.value_list):
            self.hashmap[key] = value

        # ten percent of 256 is 25.6, so this should trigger a resize when it hits
        # the 26th element. 

        # This method can occasionally yield values of hashmap greater than 512. 
        # That's okay - all we're doing is testing to see if resize works when
        # load factor is exceeded. If this test fails, and the following ones do
        # too, then we're in trouble - if they don't, chill.

        self.assertGreaterEqual(len(self.hashmap._values), 512)

    def test_02(self):

        ''' After load factor is exceeded, are the keys safe? '''

        keys = [key for key in self.hashmap]

        # ten percent of 256 is 25.6, so this should trigger a resize when it hits
        # the 26th element.

        self.assertEqual(keys, self.key_list)

    def test_03(self):

        ''' After load factor is exceeded, are the values safe? '''

        values = [self.hashmap[key] for key in self.hashmap]

        # ten percent of 256 is 25.6, so this should trigger a resize when it hits
        # the 26th element.

        self.assertEqual(values, self.value_list)


if __name__ == '__main__':
    unittest.main()