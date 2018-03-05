# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import glob
import os
import re
import sys
from jNlp.jConvert import *

class Transliterate:
    '''
    Convert kanji, katanaka and hiragama scripts to Latin (romanji).
    Convert lexica or wordlists.
    How to run:
    >>> source activate <python2.7_env>
    >>> python translitearte.py <path/to/input_name>
    Output:
        <../input_name/input_name_romanji> 

    '''
    def __init__(self):
        pass

    def transliterate_token(self,token):
        romanji = ' '.join(tokenizedRomaji(token.decode('utf-8'))).encode('utf-8')

        return romanji

    def transliterate_lexicon(self,lexicon):
        bname = '.'.join(os.path.basename(lexicon).split('.')[:-1])
        bname = '%s_romanji' % bname
        extension = lexicon.split('.')[-1]
        ## Create output directory, if it doesn't exist.
        if not os.path.exists('../%s' % bname):
            os.makedirs('../%s' % bname)
        ## Define output lexicon name.
        transliterated_lexicon = '../%s/%s.%s' % (bname,bname,extension) 
        with open(lexicon) as inf, open(transliterated_lexicon,'wb') as outf:
            for line in inf:
                line = line.strip()
                written,pron = line.split('\t')
                romanji = self.transliterate_token(written)
                ## Delete spaces from romanized token as it conflicts with
                ## the g2p alignment.
                romanji = romanji.replace(' ','')
                if romanji:
                    outf.write('%s\t%s\n' % (romanji,pron))

    def transliterate_wordlist(self,wordlist):
        bname = '.'.join(os.path.basename(wordlist).split('.')[:-1])
        bname = '%s_romanji' % bname
        extension = 'words'
        pathname = os.path.dirname(wordlist)
        ## Define output wordlist name.
        transliterated_wordlist = '%s/%s.%s' % (pathname,bname,extension) 
        with open(wordlist) as inf, open(transliterated_wordlist,'wb') as outf:
            for line in inf:
                line = line.strip()
                written = line
                romanji = self.transliterate_token(written)
                ## Delete spaces from romanized token as it conflicts with
                ## the g2p alignment.
                romanji = romanji.replace(' ','')
                if romanji:
                    outf.write('%s\n' % romanji)

if __name__ == '__main__':
    lexicon = sys.argv[1]
    example = Transliterate()
    extension = lexicon.split('.')[-1]
    if extension == 'words':
        example.transliterate_wordlist(lexicon)
    elif extension == 'train' or extension == 'test':
        example.transliterate_lexicon(lexicon)
    else:
        print('Only accepting wordlists (*.words) or lexica (*.train, *.test)')
