#!/usr/bin/python3
'''
BasicCache Module is implemented here
'''


BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    '''
    BasicCache defines:
    - a caching system that inherits from BaseCaching.
    '''
    def put(self, key, item):
        '''
        method that adds an item in the cache
        '''
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        '''
        method that gets an item by it's key
        '''
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
