import time
from cddlib.util.io import warn


class MyTimer():
    """
    Example:
            with time_it.MyTimer(dev):
                test(dev, tin)
    """
    
    def __init__(self, prefix):
        self.start = time.time()
        self.prefix = prefix
 
    def __enter__(self):
        return self
 
    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.time()
        runtime = end - self.start
        msg = '%s The function took %10.4f seconds to complete' % (
               self.prefix, runtime)
        print(msg)

