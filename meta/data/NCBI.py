import os
import urllib
import sqlite3
from collections import OrderedDict

from meta.util import timeit_msg

ncbi_ftp = 'ftp://ftp.ncbi.nlm.nih.gov/genomes'

def _download_asm(database):
	assembly_file = 'assembly_summary_{}.txt'.format(database)
	asm_link = '{}/{}/{}'.format(ncbi_ftp, database, assembly_file)

	with timeit_msg('Downloading {}'.format(assembly_file)):
		urllib.urlretrieve(asm_link, assembly_file)
		line_cnt = 0
		with open(assembly_file) as fin:
			for line in fin:
				line_cnt += 1
		fstats = os.stat(assembly_file)
	print 'File size: {:1.3f} MB'.format(float(fstats.st_size)/2**20)
	print '# Lines  : {}'.format(line_cnt)

def _setup_db(database):
	asm_fname = 'assembly_summary_{}.txt'.format(database)
	db_fname = 'NCBI.db'

	conn = sqlite3.connect(db_fname)
	conn.text_factory = str
	c = conn.cursor()

	with open(asm_fname) as fin:
		cnames = fin.next().strip().split()[1:]
	column_names = OrderedDict()
	for cn in cnames:
		column_names[cn] = 'text'
	column_names['assembly_accession'] = 'text primary key'
	column_names['seq_rel_date'] = 'date'
	column_names['taxid'] = 'integer'
	column_names['species_taxid'] = 'integer'
	taxid_idx = column_names.keys().index('taxid')

	_drop_table_str = 'DROP TABLE IF EXISTS {}'.format(database)
	_create_table_str = '''CREATE TABLE {} ({})'''.format(database,
						', '.join('{} {}'.format(n, t) for n, t in column_names.items()))
	c.execute(_drop_table_str)
	c.execute(_create_table_str)

	_insert_str = 'INSERT INTO {} VALUES ({})'.format(database, ' ,'.join(['?' for i in range(len(column_names))]))
	_insert_values = []
	with open(asm_fname) as fin:
		fin.next()
		for line in fin:
			values = line.strip().split('\t')
			values[taxid_idx] = int(values[taxid_idx])
			values[taxid_idx + 1] = int(values[taxid_idx + 1])
			_insert_values.append(tuple(values))
	c.executemany(_insert_str, _insert_values)

	conn.commit()
	conn.close()

def _cleanup(database):
	os.remove('assembly_summary_{}.txt'.format(database))


def setup_assembly_info(database):
	database = database.lower()
	if database not in ('genbank', 'refseq'):
		raise ValueError('Database can be only genbank or refseq, not {}'.format(database))

	_download_asm(database)

	_setup_db(database)

	_cleanup(database)



if __name__ == '__main__':
	setup_assembly_info('genbank')
	setup_assembly_info('refseq')

