#!/usr/bin/python3
'''
Module for the LFUCache class
'''

BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    '''
    LFUCache defines:
    - a caching system that inherits from BaseCaching.
    - implements caching using the Cache replacement policies - LFU
    '''
    def __init__(self):
        '''
        Initialize the cache
        '''
        super().__init__()
        self.frequency = {}
        self.aged_bits_order = {}

    def put(self, key, item):
        '''
        Method that adds an item in the cache
        '''
        if key is None or item is None:
            return

        if key in self.cache_data:
            # Update the existing item
            # implement FIFO if there is a tie
            self.cache_data[key] = item
            # Increase the frequency
            self.frequency[key] += 1
        else:
            if len(self.cache_data) >= self.MAX_ITEMS:
                lfu_key = min(self.frequency, key=lambda k:
                              (self.frequency[k], self.aged_bits_order[k]))
                del self.cache_data[lfu_key]
                del self.frequency[lfu_key]
                del self.aged_bits_order[lfu_key]
                print("DISCARD: {}".format(lfu_key))

            # Add the new item
            self.cache_data[key] = item
            self.frequency[key] = 1

        self.aged_bits_order[key] = len(self.aged_bits_order)

    def get(self, key):
        '''
        Method that gets an item by its key
        '''
        if key is None or key not in self.cache_data:
            return None

        self.frequency[key] += 1
        self.aged_bits_order[key] = len(self.aged_bits_order)

        return self.cache_data[key]
