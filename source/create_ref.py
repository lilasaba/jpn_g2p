# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import glob
import re
import sys
from collections import OrderedDict

def test2ref(infile):
    outfile = infile.replace('.test','.ref')
    test_dict = OrderedDict()
    with open(infile) as inf:
        for line in inf:
            line = line.decode('utf-8')
            line = line.strip()
            written,pron = line.split('\t')
            try:
                test_dict[written].append(pron)
            except KeyError:
                test_dict[written] = [pron]

    with open(outfile,'wb') as outf:
        for written in test_dict:
            prons = ','.join(test_dict[written])
            line = '%s\t%s\n' % (written,prons)
            outf.write(line.encode('utf-8'))

if __name__ == '__main__':
    infile = sys.argv[-1]
    test2ref(infile) 
