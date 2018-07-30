# -*- coding: utf-8 -*-

import time
from functools import wraps
from pathlib import Path

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

def is_home(path:Path): # -> bool
    """Determines if the path is a User path or not.
    If the Path begins with '~', then True, else False"""

    if isinstance(path, str) and len(path) > 0:
        path = Path(path)

    if isinstance(path, Path) and len(path.parts) > 0:
        return path.parts[0] == '~'
    else:
        return False

def _requests_get(self, url:str = None, timeout:int = 60, **kwargs): # -> None
    """* Returns a standard requests get response given a url
    * Underdevelopment"""

    response = None
    if not url:
        proxies = kwargs['proxy'] or {}
        response = requests.get(url, timeout=timeout, proxies=proxies)
    return response