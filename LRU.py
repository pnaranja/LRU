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

    def runcmd(self):
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
        First check if max length already reached.
        If so, remove 1 item based on LRU
        '''
        key,value = self.inpt[1],self.inpt[2]
        if len(self.cache) >= self.max_length:
            self.removelru(1)
        self.cache[key] = (value,0)

    def get(self):
        '''
        Prints the value based on the key provided
        Increments 'used' value for the key
        '''
        key = self.inpt[1]
        print key,self.cache[key][0]
        value,used = self.cache[key]
        self.cache[key] = value,used+1

    def peek(self):
        '''
        Just prints the key and value given the key provided
        '''
        key = self.inpt[1]
        print key,self.cache[key][0]

    def dump(self):
        '''
        Displays the cache in alphabetical order based on the keys
        '''
        for key,value in zip(self.cache.viewkeys(),self.cache.viewvalues()):
            print key,value[0]

    def removelru(self,num):
        '''
        Remove (num) number of entries from cache based on LRU
        '''
        #Build a new dict based on cache key and # of times used
        tempcache = { k:t[1] for k,t in zip(self.cache.viewkeys(),self.cache.viewvalues()) }

        #Find the key that corresponds to the minimum # of times used, and delete that value
        #Repeat num times
        for x in xrange(int(num)):
            del self.cache[ min( tempcache,key=tempcache.get )] #Determine minumum based on dict value and not dict key


def main():

    lru = LRU_Cache()
    #First user input is the # of commands that will be run
    try:
        numcmds = raw_input('Please enter # of commands to run: ')
    except ValueError:
        print 'ERROR: Must enter a number'
        sys.exit(0)

    #Run the (numcmds) number of commands
    for x in xrange(int(numcmds)):
        lru.runcmd()


if __name__ == '__main__':
    main()

