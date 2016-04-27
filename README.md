# Metagenomix

Metagenomix is a tool which enables you to download, analyze and visualize metagenomic data.

## Installation
Clone this repository and change to its directory. Then run:
```bash
# Download and setup NCBI taxonomy tree
./setup-tax
# Download and setup NCBI assembly summaries
./setup-ncbi
# Install the meta package
python setup.py build install
```

After the installation you should have available the python package `meta`.

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
# Test if 83333 is child of 562
tt.is_child(83333, 562)	# returns True
# Let's find the Least Common Ancestor (LCA) of Escherichia coli and Bacillus subtilis
tt.get_org_name(tt.find_lca((1423, 562))) # returns Bacteria
```
### NCBI download with taxonomy filtering

## The MIT Licence

Copyright (c) 2016 abulovic

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.