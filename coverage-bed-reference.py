import screed, sys

f_out = open(sys.argv[1] + '.bed', 'w')

for record in screed.open(sys.argv[1]):
    l = [record.name.rstrip(), str(int(1)), str(len(record.sequence))]
    f_out.write('%s\n' % '\t'.join(l))
      
