#!/usr/bin/python3
'''
Module for the LIFOCache class
'''

BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    '''
    LIFOCache defines:
    - a caching system that inherits from BaseCaching.
    - implements caching using the Cache replacement policies - LIFO
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
        if key not in self.cache_data:
            if len(self.cache_data) >= self.MAX_ITEMS:
                last_key = self.order.pop()
                del self.cache_data[last_key]
                print("DISCARD: {}".format(last_key))
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
