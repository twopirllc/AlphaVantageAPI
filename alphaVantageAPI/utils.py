#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from functools import wraps

def timed(fn):
    """Simple timing decorator that stores the elapsed time
    as a string property called 'timed' to the fn.
    """
    @wraps(fn)
    def _timer(*args, **kwargs):
        start = time.time()
        fn(*args, **kwargs)
        end = time.time()
        diff = end - start

        elapsed_time = f"[!] {fn.__name__} {diff * 1000:2.2f} ms ({diff:2.2f} s)"
        fn.timed = elapsed_time
        return fn
    return _timer

def _requests_get(self, url:str = None, timeout:int = 60, **kwargs): # -> None
    """* Returns a standard requests get response given a url
    * Underdevelopment"""

    response = None
    if not url:
        proxies = kwargs['proxy'] or {}
        response = requests.get(url, timeout=timeout, proxies=proxies)
    return response