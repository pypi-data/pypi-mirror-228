"""Thingsboard utilites."""

import logging
from typing import Callable

from tb_vendor.models import TbPagination


logger = logging.getLogger(__name__)


def tb_paginate(func: Callable, *, page_size: int, page: int = 0,
                max_pages: int = None, **kwargs) -> list:
    """Paginate Thingsboard rest client methods.

    Args:
        func: method of TB rest client.
        page_size: page size.
        page: page number start from 0.
        max_pages: maximum number of pages to be requests.
        **kwargs: keyword arguments for that method.

    Returns:
        List of data.

    Raises:
        ValueError: if max_pages is invalid
    """
    n_max, n = 0, page
    container = []
    if max_pages:
        n_max = max_pages
    if max_pages and max_pages <= 0:
        raise ValueError(f'Invalid max_pages: {max_pages}. Must be grater than 0.')
    while True:
        logger.debug(f'{func.__name__} Request Page: {n}')
        result: TbPagination = func(page=n, page_size=page_size, **kwargs)
        container += result.data
        if result.has_next is False:
            break
        if n_max and n_max >= n:
            break
        page += 1
    return container
