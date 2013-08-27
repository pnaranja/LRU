#!/usr/bin/python

import sys,os
import unittest
import LRU



class Test_LRU(unittest.TestCase):
    '''
    TEST CLASS FOR LRU.PY
    '''

    def setUp(self):
        self.lru=LRU.LRU_Cache()

    def tearDown(self):
        pass

    def stdoutnull(self,func,*params):
        '''
        Redirects a function's stdout to null

        INPUT:      Function and then any parameters to that function
        OUTPUT:     None
        '''
        #Save stdout
        tmp = sys.stdout

        #Sends stdout to "null"
        sys.stdout = open(os.devnull,'wb')

        #If there are any parameters (len>0) then invoke function with those parameters
        #Else just invoke the function
        func(*params) if len(params) else func()

        #Restablish stdout
        sys.stdout = tmp


    def bound(self,x):
        '''
        Runs the lru.bound command - BOUND x
        Created seperate function since most tests depend on a BOUND cmd
        '''
        LRU.raw_input = lambda : 'BOUND '+str(x)
        self.lru.runcmd()

    def set(self,x,y):
        '''
        Runs the lru.bound command - SET x y
        Created seperate function since most tests depend on a SET cmd
        '''
        LRU.raw_input = lambda : 'SET '+str(x)+' '+str(y)
        self.lru.runcmd()

    def get(self,x):
        '''
        Runs the lru.bound command - GET x
        Created seperate function since most tests depend on a GET cmd
        '''
        LRU.raw_input = lambda : 'GET '+str(x)
        self.lru.runcmd()


    def test_badcommand(self):
        '''
        Test using a bad command
        '''
        LRU.raw_input = lambda : 'MUST ERROR'
        self.stdoutnull(self.lru.runcmd)
        self.assertRaises(AttributeError)

    def test_bound(self):
        '''
        Tests the Bound cmd.
        Checks if Bound <num> sets the max_length
        '''
        self.bound(2)
        self.assertEqual(self.lru.max_length, 2)

    def test_set(self):
        '''
        Tests the Set cmd.
        Sets one item in the Cache.  Verify key value is correct
        SET <key> <value>
        VALUE becomes (<value>,0) where 0 is # of times used
        '''
        self.bound(1)
        self.set('a',2)
        self.assertEqual(self.lru.cache['a'],('2',0))

    def test_get(self):
        '''
        Tests the Get cmd.
        Once you get an item from the cache, the # of times used should be incremented
        '''
        self.bound(1)
        self.set('a',45)
        self.stdoutnull(self.get,'a')
        self.assertEqual(self.lru.cache['a'],('45',1))

    def test_peek(self):
        '''
        Tests the peek cmd
        Very similar to testing the set cmd
        '''
        self.bound(1)
        self.set('a',5000)
        LRU.raw_input = lambda : 'PEEK a'
        self.stdoutnull(self.lru.runcmd)
        self.assertEqual(self.lru.cache['a'][0],'5000')

    def test_dump(self):
        '''
        Tests the dump cmd
        Verify keys are in alphabetical order
        '''
        self.bound(5)
        keys = ('e','d','a','b','c')
        values = (5000,9999999999,0,-100,'fdsa')
        for key,value in zip(keys,values):
            self.set(key,value)

        LRU.raw_input = lambda : 'DUMP'
        self.stdoutnull(self.lru.runcmd)

        self.assertEqual(self.lru.ordered_keys,['a','b','c','d','e'])

    def test_removelru(self):
        '''
        Tests the remove lru function
        Removes LRU by setting values above the bound
        '''
        self.bound(2)
        self.set('a',3)
        self.set('p',3)
        self.set('o',3)
        self.assertEqual(self.lru.cache.keys(),['p','o'])

    def test_removelru2(self):
        '''
        Tests the remove lru function
        Removes LRU by setting changing the bound
        '''
        self.bound(3)
        self.set('a',3)
        self.set('p',3)
        self.set('o',3)
        self.bound(2)
        self.assertEqual(self.lru.cache.keys(),['p','o'])

if __name__ == '__main__':
    unittest.main()


