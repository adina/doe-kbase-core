import sys, numpy

def check_file(filename):
    if filename.endswith('reads.mapped'):
        check_id = 'reads'
    else:
        check_id = 'bp'
    return check_id

def get_total_number_reads(filename):
    n = 0 
    for line in open(filename):
        if line.startswith('>'):
            n += 1
    return n
        
def get_coverage_dict(filename):
    d = {}
    for line in open(filename):
        dat = line.rstrip().split('\t')
        contig_id = dat[0]
        cov_bp = int(dat[-1])
        if d.has_key(contig_id):
            d[contig_id].append(cov_bp)
        else:
            d[contig_id] = [cov_bp]
    return d

def get_rpkm(filename, readcount):
    d = {}
    for line in open(filename):
        dat = line.rstrip().split('\t')
        contig = dat[0]
        mapped_reads = int(dat[-4])
        contig_len = int(dat[-2])
        rpkm = 1e9 * mapped_reads / (readcount * float(contig_len))
        d[contig] = rpkm
    return d

def get_stats_per_contig(d_coverage):
    sorted_keys = sorted(d_coverage.keys())
    for key in sorted_keys:
        l = d[key]
        summy = 0
        median = numpy.median(l)
        avg = numpy.average(l)
        minl = min(l)
        maxl = max(l)
        for n, x in enumerate(l):
            if x > 0:
                summy += 1
        total = n + 1
        cov_rat = float(summy)/total
        l = [key, str(median), str(avg), str(minl), str(maxl), str(summy), str(total), str(cov_rat)]
        return l
        

if __name__=='__main__':
    bedfile = sys.argv[1]
    readfile = sys.argv[1].split('.sam.bam')[0]
    fp = open(sys.argv[1] + '.rpkm', 'w')
    readcount = get_total_number_reads(readfile)
    if check_file(sys.argv[1]) == 'reads':
        d_rpkm = get_rpkm(bedfile, readcount)
    for x in d_rpkm:
        print >>fp, '%s\t%s' % (x, str(d_rpkm[x]))
