

import appLogConfig

from functools import wraps

class Log():

    def __init__(self):

        self._log = appLogConfig.app_log
        
        
    def __call__(self, func):

        def wraper(*args, **kwargs):

            result = func(*args, **kwargs)
            if result != {} and result is not None:

                msg = ("function: %s from module: %s with result: %s" %
                (func.__name__, func.__module__, result))
            
                self._log.info(msg)

            return result
        

        return wraper
        
        


