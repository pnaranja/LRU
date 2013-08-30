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
        First check if length of value is not greater than 10
        Second check if max length already reached.
        If so, remove 1 item based on LRU
        '''
        #if the input value is > 10, disregard
        if len(str(self.inpt[2])) > 10:
            print 'Value cannot be greater than 10 characters'
            return
        key,value = self.inpt[1],self.inpt[2]
        if len(self.cache) >= self.max_length:
            self.removelru(1)
        self.cache[key] = (value,0)

    def get(self):
        '''
        Prints the value based on the key provided
        Increments 'used' value for the key
        '''
        try:
            key = self.inpt[1]
            value,used = self.cache[key]
            print key,value
            self.cache[key] = value,used+1
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
        #Build a new dict based on cache key and # of times used
        tempcache = { v[1]:k for v,k in zip(self.cache.viewvalues(),self.cache.viewkeys()) }

        #TODO - If all # of times is the same, then the last key alphabetically will be deleted
        #       In this situation, need to delete the last entered key
        #Find the key that corresponds to the minimum # of times used, and delete that value
        #Repeat num times
        for x in xrange(int(num)):
            #TODO - Wrong implementation.  Redo
            del self.cache[tempcache[0]] #Determine minumum based on dict value and not dict key



def main(): #pragma: no cover

    lru = LRU_Cache()
    numcmds = lru.numcmds()

    #Run the (numcmds) number of commands
    for x in xrange(int(numcmds)):
        lru.runcmd()


if __name__ == '__main__':
    main() #pragma: no cover

