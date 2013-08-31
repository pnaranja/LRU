#!/usr/bin/python
import sys

class LRU_Cache:
    '''
    LRU implementation
    Each value in cache must have the following:
        key
        value
        age

    BOUND - Sets max length of cache
    SET - sets key and value and 'used' variable.  'Used' set to 0
    GET - return key and value.  Increments 'used' variable
    PEEK - return key and value
    DUMP - return cache's key and value pairs IN ALPHABETICAL ORDER!
    '''

    def __init__(self):
        '''
        Initialize cache and max length of cache
        The cache will be a dict of tuples (value, # of times used)
        '''
        self.cache = {}
        self.max_length = 0
        self.numkeys = 0

    def numcmds(self):
        '''
        Ask user how many cmds to run.
        Not allow more than 1 million cmds
        Returns number of cmds entered form the user
        '''

        try:
            numcmds = raw_input('Please enter # of commands to run: ')
            while int(numcmds) > 1000000:
                try: numcmds = self.raw_input2('\nWill not process more than 1 million commands.\nPlease enter # of commands to run: ')
                except AttributeError: numcmds = raw_input('\nWill not process more than 1 million commands.\nPlease enter # of commands to run: ')

            return numcmds

        except ValueError:
            print 'ERROR: Must enter a number'
            sys.exit(0)

    def runcmd(self):
        '''
        Runs the commands based on user input
        '''
        self.inpt = raw_input().split(' ')
        try:
            getattr(self,self.inpt[0].lower())()
        except AttributeError:
            print 'Incorrect Command'

    def bound(self):
        '''
        Sets the max length of the cache
        If new max length < current max length, remove values based on LRU
        '''
        num = int(self.inpt[1])
        if num < self.max_length:
            self.removelru(self.max_length - num)
        self.max_length = num

    def set(self):
        '''
        Enters the key and value in the cache
        1. Check if length of the key or value is not greater than 10
        2. Check if this is setting a new key.  If so, if
        max length already reached, remove 1 item based on LRU
        If setting an old key, set new value no change with # times
        used and nth key in cache

        key:(value, # of times key is used, nth key in the cache)
        '''
        #store key and value from input
        key,value = str(self.inpt[1]),str(self.inpt[2])

        #if the input key or value is > 10 characters, disregard
        if len(key) > 10 or len(value) > 10:
            print 'Value cannot be greater than 10 characters'
            return

        #Check if key already exists in the cache
        if key in self.cache.viewkeys():
            old_value, num_times, nthkey = self.cache[key]
            self.cache[key] = (value, num_times, nthkey)

        else:
            #Check if cache is already at max size
            if len(self.cache) >= self.max_length:
                self.removelru(1)
            self.numkeys += 1
            self.cache[key] = (value,0,self.numkeys)

    def get(self):
        '''
        Prints the value based on the key provided
        Increments 'used' value for the key
        '''
        try:
            key = self.inpt[1]
            value,used,nthkey = self.cache[key]
            print key,value
            self.cache[key] = value,used+1,nthkey
        except KeyError:
            print 'Null'

    def peek(self):
        '''
        Just prints the key and value given the key provided
        '''
        try:
            key = self.inpt[1]
            value = self.cache[key][0]
            print key,value
        except KeyError:
            print 'Null'

    def dump(self):
        '''
        Displays the cache in alphabetical order based on the keys
        '''
        self.ordered_keys = self.cache.keys()
        self.ordered_keys.sort()
        for key in self.ordered_keys:
            print key,self.cache[key][0]

    def removelru(self,num):
        '''
        Remove (num) number of entries from cache based on LRU
        '''
        for x in xrange(num):
            #Find the value of the lowest # of times used in the cache
            lowest_times = min([v[1] for v in self.cache.viewvalues() ])

            #Find the key(s) that has/have the lowest # of times used
            #Create a dict of {nthkey : key}.  Each nthkey value should be unique
            lowest_keys ={ v[2]:k for v,k in zip(self.cache.viewvalues(),self.cache.viewkeys()) if v[1] == lowest_times }

            #Within that list, delete the key that has been in the cache the longest
            #Cache the longest = smallest nthkey value
            del self.cache[min(lowest_keys.viewvalues())]



def main(): #pragma: no cover

    lru = LRU_Cache()
    numcmds = lru.numcmds()

    #Run the (numcmds) number of commands
    for x in xrange(int(numcmds)):
        lru.runcmd()


if __name__ == '__main__':
    main() #pragma: no cover

