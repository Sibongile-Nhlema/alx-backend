#!/usr/bin/env python3
'''
Module that handles the implementation of index_range (helper function)
and
adds the Server class
'''
import csv
import math
from typing import List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
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


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        '''
        Args:
            page(int): the given page number, starting from 1
            page_size(int): the number of items per page
        Returns:
            List[List]: page number
        '''
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0
        start_index, end_index = index_range(page, page_size)
        dataset = self.dataset()
        if start_index >= len(dataset):
            return []
        return dataset[start_index:end_index]
