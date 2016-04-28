import os
import sys
import time
import math
import sqlite3
from contextlib import contextmanager

import meta

@contextmanager
def timeit_msg(msg):
	print '{}...'.format(msg),
	sys.stdout.flush()

	start = time.time()
	yield
	stop = time.time()

	print ' ({:1.3f} s)'.format((stop-start))

def get_file_size(fname):
	fstats = os.stat(fname)
	size = fstats.st_size
	exponent = int(math.log(size, 10))
	divisor = {'B': 0, 'kB': 3, 'MB': 6, 'GB': 9}
	if exponent < 3:
		res = 'B'
	if exponent >= 3 and exponent < 6:
		res = 'kB'
	elif exponent >= 6 and exponent < 9:
		res = 'MB'
	else:
		res = 'GB'
	return '{:1.2f} {}'.format(float(size) / 10**divisor[res], res)

def get_ncbi_db_conn():
	dbfile = os.path.join(meta.__path__[0], 'data', 'NCBI.db')
	conn = sqlite3.connect(dbfile)
	conn.text_factory = str
	return conn


