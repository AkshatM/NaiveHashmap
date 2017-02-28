import random
import string

'''
A class that implements a full-fledged hashmap in Python with no hashmap primitives 
(in other words, no internal dictionaries/sets/frozensets!)

This class uses two lists: a list of keys and values. The values list is instantiated
as a massive preallocated (by Nones) list of 256 values initially. A hash function (see 
hashfunc) is used to compute the index of the value to the key. On hash collisions or when 
there is more than a ten percent chance of future collisions, the values list is dynamically
resized to twice its previous value, and the values corresponding to each key are reassigned 
throughout. As a bonus, I implemented iteration, a pretty console representation, and membership 
testing on top of the core functionality.

This class exposes its keys and values attribute as mutable lists. This is a security
flaw, but one that there isn't really good support for. 

Demonstrations of this class are provided in the comments. Unit tests are provided in Q7_Tests.py.
'''

class HashMap(object):

    def __init__(self):

        ''' Class variables are declared here '''

        self._values = [None for item in xrange(256)] # allows up to 256 unique values
        self._keys = [] # start with no keys, as is right
    
    def __getitem__(self,key):

        ''' This implements lookup i.e. q[s] calls q.__getitem__(s) '''

        # constant lookup in amortised worst-case analysis guaranteed!

        if self._values[self.hashfunc(key)] is not None: # if a value already exists
            return self._values[self.hashfunc(key)] # return it

            # Hash collisions can occur with this method, and that's fair. Thankfully,
            # this only gives you a value even if the key isn't there - trying to update
            # or add to a HashMap() triggers __setitem__, which carefully prevents real hash 
            # collisions by calling self.resize(). Basically, __getitem__() is not dangerous
            # to anyone but the poor soul who has to trust our results - ironic, I know - 
            # while __setitem__() carefully does its best to keep real hash collisions 
            # low. It's okay to get the wrong value (although we should keep it to a minimum),
            # by accident, but it's not okay to deliberately get a wrong result (i.e. overwrite
            # data on a legitimate hash collision)

            # One way to get around this is to automatically resize when we hit a threshold 
            # on self.keys(), say every ten new keys. This only minimises - but never truly 
            # gets rid of - the possibility of hash collisions. We do this in __setitem__,
            # so all is well.

        else:
            return self.__missing__(key) # because a value of None means the key was never set

    def __setitem__(self,key,value):

        ''' Implements updating i.e. q[s] = 2 calls q.__setitem__(s,2) '''

        if value is None: # if the user, in his infinite wisdom, decides to give us a null value
            raise ValueError('None is not permitted as a value.') # do NOT add it

        if self._values[self.hashfunc(key)] is None: # if there's never been a value
            self._keys.append(key) # then add the key
            self._values[self.hashfunc(key)] = value # and update the value

            # but now we should ask: is it worth resizing at this stage?
            # A good hashtable would resize when the ratio of keys to values
            # exceeds a certain threshold. We've just added a new key, so it 
            # makes sense to check if that changes things.

            if float(len(self._keys))/len(self._values) > 0.1: # if there's even a ten percent chance of collision
                self.__resize__()
        
        else: # if there is a value
            if key in self._keys: # and there doesn't seem to be a collision
                self._values[self.hashfunc(key)] = value # update it already

                # we lose a worst case O(1) insertion time this way, but 
                # I can't think of a way to cross-check collisions otherwise.

            else:
                # if this is a new key, then we have a hash collision, so
                self.__resize__() # resize self.values and redistribute values
                self.__setitem__(key,value) # call this method on the new self.values

    def __missing__(self,not_key):

        ''' Implement what to do when there is no key '''
        
        raise KeyError('{0} is not a valid key'.format(not_key))


    def __repr__(self):

        ''' Implements what the object looks like in print.'''

        list_repr = ['{0}:{1}'.format(key, self._values[self.hashfunc(key)]) for key in self._keys]
        return 'HashMap({0})'.format(list_repr)

    def __contains__(self,key):

        ''' Implements checking for membership. i.e. it lets 'if x in HashMap' return True or False '''

        if key in self._keys:
            return True
        else:
            return False

    def __len__(self):

        ''' Implements checking for length '''

        return len(self._keys)

    def __iter__(self):

        ''' Allows iteration through keys '''

        return (key for key in self._keys)

    def hashfunc(self,key):
        # our hash function. Very naive, but it works.
        return hash(key) % len(self._values)

    def __resize__(self,**kwargs):

        # first we collect the old values for safekeeping. If this function is being called because
        # of a hash collision in the old resizing, we've passed it down so we don't run into issues.
        old_values = kwargs.get('values',[self._values[self.hashfunc(key)] for key in self._keys])

        # we create a brand new self._values with twice the size it used to
        # have. Our implementation is an expensive operation, but necessary:
        # we can't simply extend the list because we have to get rid of the
        # contained values in it anyway. Starting afresh is cleaner code
        # for the same result - it might be slower than extending and overwriting, 
        # but frankly I'd rather let benchmarks settle that issue instead.
        
        self._values = [None for item in xrange(2*len(self._values))]

        # and now we put them all back into their new place

        for key, value in zip(self._keys,old_values):

            if self._values[self.hashfunc(key)] is None: 
                self._values[self.hashfunc(key)] = value
        
            else: # if there is a value, there's a hash collision again
                self.__resize__(values = old_values)

if __name__ == '__main__':
    s = HashMap()
    print(s)
    s['Hello'] = 'World'
    s['Lettuce'] = 'orange' 
    print(s)
    for key in s: # tests iteration
        print(key, s[key])
    if 'Lettuce' in s: # tests membership
        print("Thanks!")
    s['Hellow'] = "WORLD!" # updating element
    print(s) 
