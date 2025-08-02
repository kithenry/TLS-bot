#!/usr/bin/env python3

"""
safe executor: for avoiding redundant try except blocks
main features:
- avoiding redundant try except blocks

more:
- logging errors
- retrying runs
- waiting before retries
- both sync and async support

"""

import traceback
import time
import logging
from contextlib import contextmanager
from functools import wraps

class SafeExecutor:
    def __init__(self, log_file=None, verbose=True, catch=(Exception,), suppress=False):
        self.catch = catch
        self.verbose = verbose
        self.suppress = suppress

        self.logger = logging.getLogger("SafeExecutor")
        handler = logging.FileHandler(log_file) if log_file else logging.StreamHandler()
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
        handler.setFormatter(formatter)

        if not self.logger.handlers:
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.DEBUG)

    def _log(self, msg, level=logging.ERROR):
        if self.verbose or self.logger.handlers:
            self.logger.log(level, msg)


    def run(self, func, *args, default=None, retry=0, delay=0, **kwargs):
       """
       Run a function safely with retries and fallback
       """
       attempt = 0
       while attempt <= retry:
           try:
               return func(*args, **kwargs)
           except self.catch as e:
               self._log(f"Attempt {attempt + 1} failed: {e}")
               if not self.suppress:
                   traceback.print_exc()
               if attempt < retry:
                    time.sleep(delay)
               attempt += 1
       return default


    def wrap(self, default=None, retry=0, delay=0):
       """
       Decorator to wrap a function for safe execution
       """
       def decorator(func):
           @wraps(func)
           def wrapper(*args, **kwargs):
               return self.run(func, *args, default=default, retry=retry, delay=delay, **kwargs)
           return wrapper
       return decorator

    def run_block(self, block_func, default=None, retry=0, delay=0):
       """
       Run a procedural code block safely. Pass a lambda or def block w/o args
       """
       attempt = 0
       while attempt <= retry:
           try:
               yield
               break # success
           except self.catch as e:
               self._log(f"Context '{name}' failed at attempt {attempt+1}: {e}")
               if not self.suppress:
                   traceback.print_exc()
               if attempt < retry:
                  time.sleep(delay)
               else:
                   break

           attempt += 1
