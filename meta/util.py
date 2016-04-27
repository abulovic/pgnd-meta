import sys
import time
from contextlib import contextmanager

@contextmanager
def timeit_msg(msg):
	print '{}...'.format(msg),
	sys.stdout.flush()

	start = time.time()
	yield
	stop = time.time()

	print ' ({:1.3f} s)'.format((stop-start))