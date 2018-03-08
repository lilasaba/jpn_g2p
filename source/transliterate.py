# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import glob
import os
import re
import sys
from jNlp.jConvert import *

class Transliterate:
    '''
    Convert kanji, katanaka and hiragama scripts to Latin (romaji).
    Convert lexica or wordlists.
    How to run:
    >>> source activate <python2.7_env>
    >>> python transliterate.py <path/to/input_name>
    Output:
        <../input_name/input_name_romaji> 

    '''
    def __init__(self):
        self.romaji_pat = re.compile(r'^[a-zA-Z][a-zA-Z.-]*$')
        self.latin_count = 0
        self.omit_count = 0
        self.token_count = 0

    def transliterate_token(self,token):
        if self.romaji_pat.search(token):
            romaji = self.normalize_token(token)
            self.latin_count += 1
        else:
            romaji = ' '.join(tokenizedRomaji\
                    (token.decode('utf-8'))).encode('utf-8')

        return romaji

    def normalize_token(self,token):
        normalized = token.lower()
        normalized = normalized.replace('.','')
        normalized = normalized.replace('-','')

        return normalized

    def transliterate_lexicon(self,lexicon):
        bname = '.'.join(os.path.basename(lexicon).split('.')[:-1])
        bname = '%s_romaji' % bname
        extension = lexicon.split('.')[-1]
        pathname = os.path.dirname(lexicon)
        ## Create output directory, if it doesn't exist.
        if not os.path.exists('../%s' % bname):
            os.makedirs('../%s' % bname)
        ## Define output lexicon name.
        transliterated_lexicon = '%s/%s.%s' % (pathname,bname,extension) 
        with open(lexicon) as inf, open(transliterated_lexicon,'wb') as outf:
            for line in inf:
                self.token_count += 1
                line = line.strip()
                written,pron = line.split('\t')
                romaji = self.transliterate_token(written)
                ## Delete spaces from romanized token as it conflicts with
                ## the g2p alignment.
                romaji = romaji.replace(' ','')
                if romaji:
                    outf.write('%s\t%s\n' % (romaji,pron))
                else:
                    self.omit_count += 1

    def transliterate_wordlist(self,wordlist):
        bname = '.'.join(os.path.basename(wordlist).split('.')[:-1])
        bname = '%s_romaji' % bname
        extension = 'words'
        pathname = os.path.dirname(wordlist)
        ## Define output wordlist name.
        transliterated_wordlist = '%s/%s.%s' % (pathname,bname,extension) 
        with open(wordlist) as inf, open(transliterated_wordlist,'wb') as outf:
            for line in inf:
                self.token_count += 1
                line = line.strip()
                written = line
                romaji = self.transliterate_token(written)
                ## Delete spaces from romanized token as it conflicts with
                ## the g2p alignment.
                romaji = romaji.replace(' ','')
                if romaji:
                    outf.write('%s\n' % romaji)
                else:
                    self.omit_count += 1

if __name__ == '__main__':
    lexicon = sys.argv[1]
    example = Transliterate()
    extension = lexicon.split('.')[-1]
    if extension == 'words':
        example.transliterate_wordlist(lexicon)
    elif extension == 'lex':
        example.transliterate_lexicon(lexicon)
    else:
        print 'Only accepting wordlists (*.words) or lexica (*.lex)'

    print 'Token count: %d\nRoman word count: %d\nOmitting %d tokens' \
            % (example.token_count,example.latin_count,example.omit_count)
