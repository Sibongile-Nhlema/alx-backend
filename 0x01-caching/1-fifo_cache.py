#!/usr/bin/python3
'''
Module for the FIFOCache class
'''

BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    '''
    FIFOCache defines:
    - a caching system that inherits from BaseCaching.
    - implements caching using the Cache replacement policies - FIFO
    '''
    def __init__(self):
        '''
        Initialize the cache
        '''
        super().__init__()
        # track insertion order
        self.order = []

    def put(self, key, item):
        '''
        method that adds an item in the cache
        '''
        if key is None or item is None:
            return
        if key not in self.cache_data and len(self.cache_data) >= self.MAX_ITEMS:
            first_key = self.order.pop(0)
            del self.cache_data[first_key]
            print("DISCARD: {}".format(first_key))
        if key not in self.cache_data:
            self.order.append(key)
        else:
            # Remove key from order and re-add
            self.order.remove(key)
            self.order.append(key)
        self.cache_data[key] = item

    def get(self, key):
        '''
        method that gets an item by it's key
        '''
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
