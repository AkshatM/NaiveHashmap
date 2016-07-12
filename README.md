_Note_: I made this for fun, and to help demonstrate the power of magic methods in Python. 

#About

This repository implements a hashmap in Python from scratch, with no internal dictionaries, sets, frozensets or other hashtable-like objects inside. It employs two dynamic arrays (lists) to keep the key and the values, with a naive hashfunction being used to compute the index of the value corresponding to a key from the key itself. On a hash collision or after a certain threshold, the list of values is dynamically resized until neither condition is encountered. Constant time lookup (even in the worst case) is guaranteed (although worst case constant time insertion is not, resorting to a linear solution instead).

The hashmap is implemented as a `HashMap` object, with inbuilt class methods (`__getitem__`,`__setitem__`) allowing for dictionary-like interaction. Instance variables `_keys` and `_values` are used to, respectively, maintain a list of keys and values. A class method `__resize__()` dynamically resizes values. Please see the code for more thorough documentation.

As a bonus, I implemented a neat string representation of the HashMap() object, as well as iteration, membership testing and indexing over the keys. The idea was to get very close to how dictionaries actually behave in Python, giving the user a familiar interface and a (almost) drop-in replacement for a dictionary if needed. I don't recommend using this implementation in production, but it should work if needed.

Demonstrations are provided in the code; docstrings and extensive commenting discuss every aspect of my solutions.

Unit tests for `hashmap.py` are found in `hashmap_tests.py`, where all of the above features are tested on select and random elements respectively. 
