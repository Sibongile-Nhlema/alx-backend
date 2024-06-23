#!/usr/bin/env python3
'''
Module that handles the implementation of index_range
'''


def index_range(page: int, page_size: int) -> tuple:
    '''
    Args:
        page: the given page number, starting from 1
        page_size: the number of items per page
    Returns:
        tuple: tuple containing the start and end indices for the pagination
    '''
    start_index = (page - 1) * page_size
    end_index = page * page_size
    return start_index, end_index
