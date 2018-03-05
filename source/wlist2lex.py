# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import glob
import re
import sys
from subprocess import check_output

class Word2Pron:
    '''
    Convert written form to phonemic form (IPA) with espeak.
    Dependencies: espeak (https://github.com/espeak-ng/espeak-ng/blob/master/README.md).
    Convert string (word2ipa) or lexicon (in2out).
    How to run:
        >>> source activate python3.5
        >>> python wlist2lex.py <path/to/wordlist>.ext
    Output:
        <path/to/wordlist>_espeak.ext
    '''
    def __init__(self):
        self.espeak_phoneme_set = set()
        self.wikt_phoneme_set = {'ɾ','a','b','d̪','ɛ','h','i','j',
                'k','m','n̪','ɔ','p','s̪','t̪','w','z̪'}

    def word2ipa(self,word):
        pron = check_output(["espeak", "-q","--ipa",
            '--sep=|',
            '-v','ja',
            word]).decode('utf-8')
        return pron

    def remove_espeak_markup(self,pron):
        pron = pron.replace('(en)','')
        pron = pron.replace('(ja)','')
        pron = pron.replace(' ','')
        ## Remove accent (marked by u'\u02c8').
        pron = pron.replace(chr(712),'')
        ## 
        pron = pron.replace('|',' ')
        pron = pron.strip()

        return pron

    def in2out(self,wlist):
        extension = wlist.split('.')[-1]
        extension = '.%s' % extension
        out_name = wlist.replace(extension,'_espeak%s' % extension)
        with open(wlist,encoding='utf-8') as wordlist,\
                open(out_name,'w',encoding='utf-8') as lexicon:
            for word in wordlist: 
                word = word.strip()
                pron = self.word2ipa(word)
                pron = self.remove_espeak_markup(pron)
                if pron:
                    #print(word,pron)
                    for ph in pron.split(' '):
                        self.espeak_phoneme_set.add(ph)
                    lexicon.write('%s\t%s\n' % (word,pron))

        print(self.espeak_phoneme_set)
        print(self.espeak_phoneme_set & self.wikt_phoneme_set)
        print(self.espeak_phoneme_set - self.wikt_phoneme_set)
        print(self.wikt_phoneme_set - self.espeak_phoneme_set)

if __name__ == '__main__':
    wordlist = sys.argv[1]
    jpn_w2p = Word2Pron()
    jpn_w2p.in2out(wordlist)
