# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import glob
import os
import re
import sys
from jNlp.jConvert import *

class Transliterate:
    def __init__(self):
        pass

    def transliterate_token(self,token):
        '''
        Convert from Japanese (kanji, katanama, hiragama) script to
        Latin characters.
        >>> 
        '''
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

if __name__ == '__main__':
    wikt = Transliterate()
    wikt.transliterate_lexicon('../jpn_wiktionary/jpn_wiktionary.train')
    wikt.transliterate_lexicon('../jpn_wiktionary/jpn_wiktionary.test')
