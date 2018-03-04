# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import glob
import re
import sys
from subprocess import check_output

class Word2Pron:
    def __init__(self):
        pass

    def word2ipa(self,word):
        pron = check_output(["espeak", "-q","--ipa",
            '-v','ja',
            word]).decode('utf-8')
        print(pron)

    def in2out(self,wlist):
        pass

if __name__ == '__main__':
    word = '少女'
    jpn_w2p = Word2Pron()
    jpn_w2p.word2ipa(word)
