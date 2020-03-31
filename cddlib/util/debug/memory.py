from cddlib.util.unix import is_unix
from cddlib.util.io import warn

# helper function to get rss size, see stat(5) under statm. This is in pages (4k on my linux)
def print_memory_usage():
    if is_unix():
        (vm_size, vmRSS, shrd, txt, lib_unused, data, dirty_unused) = \
            open('/proc/self/statm').read().split()
        warn("MEM vmSize=%-7s vmRSS=%-7s shared=%-7s data=%-7s" % 
             (vm_size, vmRSS, shrd, data))


def get_rss_gb():
    if is_unix():
        (vm_size, vmRSS, shrd, txt, lib_unused, data, dirty_unused) = \
            open('/proc/self/statm').read().split()
        return float(vmRSS)*4./1024./1024.
    else:
        return 0
