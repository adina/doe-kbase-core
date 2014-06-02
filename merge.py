'''Merges multiple sample abundance files into one abundance matrix'''

import sys

if len(sys.argv) < 2:
    print >> sys.stderr, \
    'Usage:  merge.py <input files>'
    sys.exit(1)

fp = open('merged.out', 'w')

d = {}
files = sys.argv[1:]
l_data = []

for file in files:
    l_file = []
    fi = open(file, 'r')
    for line in fi:
        l_file.append(line) 
    l_data.append(l_file)

for x in files:
    fp.write('\t%s' % x)

fp.write('\n')

d_transformed = {}

for n, x in enumerate(l_data):
    for m, y in enumerate(x):
        y = y.split('\t')
        contig = y[0]
        abundance = float(y[1])
        if d_transformed.has_key(contig):
            d_transformed[contig].append(abundance)
        else:
            d_transformed[contig] = [abundance]

for key in d_transformed:
    fp.write('%s' % key)
    for x in d_transformed[key]:
        fp.write('\t%f' % x)
    fp.write('\n')

