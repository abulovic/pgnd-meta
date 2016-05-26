import sys
import argparse
from Bio import SeqIO

def _get_fq2fa_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument('fastq')
	parser.add_argument('fasta')
	return parser


def fq2fa():
	parser = _get_fq2fa_parser()
	args = parser.parse_args()

	count = SeqIO.convert(args.fastq, 'fastq', args.fasta, 'fasta')
	sys.stderr.write('Converted %d sequences.\n' % count)

