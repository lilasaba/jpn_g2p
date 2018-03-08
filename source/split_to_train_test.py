# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import glob
import numpy as np
import re
import sys

'''
Split file into train and test sets randomly with a given ratio.
How to run:
    >>> python split_to_train_test.py <path/to/wordlist>
Output:
    <path_to_wordlist>.train
    <path_to_wordlist>.test
'''

np.random.seed(908)

def count_lines(fname):
    '''
    Count number of lines in file.
    '''
    with open(fname) as f:
        for i,l in enumerate(f):
            pass
    return i + 1

def split_into_train_and_test(fname,line_count,ratio=0.9):
    '''
    Split file into train and test sets randomly selecting lines
    with probability ratio.
    '''
    extension = fname.split('.')[-1]
    train_name = fname.replace(extension,'train')
    test_name = fname.replace(extension,'test')
    a = np.random.binomial(1,ratio,line_count)
    with open(fname) as inf,\
            open(train_name,'wb') as train,\
            open(test_name,'wb') as test:
        for i,line in enumerate(inf):
            line = line.decode('utf-8')
            if a[i]:
                train.write(line.encode('utf-8'))
            else:
                test.write(line.encode('utf-8'))

if __name__ == '__main__':
    infile = sys.argv[1]
    line_count = count_lines(infile)
    print('Line count in %s: %s' % (infile,line_count))
    split_into_train_and_test(infile,line_count)
