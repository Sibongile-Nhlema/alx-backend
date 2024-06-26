#!/usr/bin/python3
'''
Module for the LRUCache class
'''

BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    '''
    LRUCache defines:
    - a caching system that inherits from BaseCaching.
    - implements caching using the Cache replacement policies - LRU
    '''
    def __init__(self):
        '''
        Initialize the cache
        '''
        super().__init__()
        # track the order of the aged bits
        self.age_bits_order = []

    def put(self, key, item):
        '''
        method that adds an item in the cache
        '''
        if key is None or item is None:
            return
        if key in self.cache_data:
            # Remove the existing key to update the order (hit)
            self.age_bits_order.remove(key)
        elif len(self.cache_data) >= self.MAX_ITEMS:
            # Remove the least recently used item
            lru_key = self.age_bits_order.pop(0)
            del self.cache_data[lru_key]
            print("DISCARD: {}".format(lru_key))

        self.cache_data[key] = item
        # update the order
        self.age_bits_order.append(key)

    def get(self, key):
        '''
        method that gets an item by it's key
        '''
        if key is None or key not in self.cache_data:
            return None
        # Move the accessed key to the end, marking it as recently used
        self.age_bits_order.remove(key)
        self.age_bits_order.append(key)

        return self.cache_data[key]
