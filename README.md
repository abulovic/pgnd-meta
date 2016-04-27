# Metagenomix

Metagenomix is a tool which enables you to download, analyze and visualize metagenomic data.

## Installation
1. Clone this repository
2. Change directory to pgnd-meta
3. Run: `./setup-tax`
4. Run: `python setup.py build install`

After the installation you should have available the python package `meta`.

Script setup-tax

## Features
### Taxonomy Tree
Metagenomix provides a tree-like structure for browsing taxonomy. Taxonomy is inferred from the `taxdmp.zip` downloaded from `ftp://ftp.ncbi.nih.gov/pub/taxonomy/`. 
Using taxonomy tree, you can easily explore the NCBI taxonomy. For instance,

```python
from meta.data.tax import TaxTree

tt = TaxTree() # takes some time to load taxonomy
tt.get_org_name(83333) # 83333 is taxid of Escherichia coli K-12
tt.get_org_rank(83333) # has no rank assignment
tt.get_parent_with_rank(83333, 'species') # we find the species parent of this strain, returns 562
tt.get_org_name(562) # returns Escherichia coli
```
### NCBI download with taxonomy filtering
