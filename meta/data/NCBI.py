import os
import gzip
import urllib
import sqlite3
from ftplib import FTP
from contextlib import nested
from collections import OrderedDict

import meta
from meta.util import timeit_msg, get_file_size
from meta.data.tax import TaxTree


def _download_asm(database):
	assembly_file = 'assembly_summary_{}.txt'.format(database)

	with timeit_msg('Downloading {}'.format(assembly_file)):
		ftp = FTP('ftp.ncbi.nlm.nih.gov')
		ftp.login()
		ftp.cwd('genomes/{}'.format(database))
		ftp.retrbinary('RETR {}'.format(assembly_file), open(assembly_file, 'wb').write)
		line_cnt = 0
		with open(assembly_file) as fin:
			for line in fin:
				line_cnt += 1
		fstats = os.stat(assembly_file)
	print 'File size: {}'.format(get_file_size(assembly_file))
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

def download_urllist(url_file, outdir, extract):
	line_cnt = 0
	with open(url_file) as fin:
		for line in fin:
			line_cnt += 1

	from ftplib import FTP 
	ftp = FTP('ftp.ncbi.nlm.nih.gov')
	ftp.login()
	ftp.cwd('genomes/all')

	with open(url_file) as fin:
		for idx, line in enumerate(fin, 1):
			line = line.strip()
			_id = line.split('/')[-1]
			url = '{}/{}_genomic.fna.gz'.format(line, _id)
			fname = '{}_genomic.fna.gz'.format(_id)
			outfile = os.path.join(outdir, fname)
			with timeit_msg('Downloading {:6d}/{}'.format(idx, line_cnt)):
				ftp.cwd(_id)
				ftp.retrbinary('RETR {}'.format(fname), open(outfile, 'wb').write)
				ftp.cwd('..')
				if extract:
					with nested(gzip.open(outfile, 'rb'),
						        open(outfile[:-3], 'w')) as (gzin, txtout):
						txtout.write(gzin.read())
					os.remove(outfile)

def download_taxid(database, taxid, outdir, download_children, extract):
	tt = TaxTree()
	print 'Downloading {} data for organism {}...'.format(database, tt.get_org_name(taxid))

	dbfile = os.path.join(meta.__path__[0], 'data', 'NCBI.db')
	conn = sqlite3.connect(dbfile)
	conn.text_factory = str
	c = conn.cursor()

	c.execute('SELECT taxid, ftp_path FROM {}'.format(database))
	res = c.fetchall()


	entries = 0
	tmpfile = '_tmp_url_file.txt'
	with open(tmpfile, 'w') as fout:
		for _taxid, ftp_path in res:
			_taxid = int(_taxid)
			if _taxid == taxid or (download_children and tt.is_child(_taxid, taxid)):
				entries += 1
				fout.write(ftp_path)
				fout.write('\n')
	print 'Found {} entries matching the provided description.'.format(entries)
	download_urllist(tmpfile, outdir, extract)
	os.remove(tmpfile)


def _get_parser():
	import argparse
	parser = argparse.ArgumentParser()
	subs = parser.add_subparsers()

	tax_pars = subs.add_parser('tax', help='Download using taxonomy filtering')
	url_pars = subs.add_parser('url', help='Download using file with list of URLs')

	tax_pars.add_argument('db', choices=('genbank', 'refseq'), help='Database from which to download')
	tax_pars.add_argument('taxid', help='taxid to download')
	tax_pars.add_argument('outdir', help='Directory where to store downloaded files')
	tax_pars.add_argument('--children', action='store_true', help='Download children of the specified taxid')
	tax_pars.add_argument('--extract', action='store_true', help='Extract from .gz archive while downloading')

	url_pars.add_argument('url_file', help='Path to textual file containing a newline-separated list of URLs of genomes to download')
	url_pars.add_argument('outdir', help='Directory where to store downloaded files')
	url_pars.add_argument('--extract', action='store_true', help='Extract from .gz archive while downloading')

	return parser

def __download__():
	parser = _get_parser()
	args = parser.parse_args()

	if hasattr(args, 'taxid'):
		download_taxid(args.db, int(args.taxid), args.outdir, args.children, args.extract)
	else:
		download_urllist(args.url_file, args.outdir, args.extract)


if __name__ == '__main__':
	setup_assembly_info('genbank')
	setup_assembly_info('refseq')

