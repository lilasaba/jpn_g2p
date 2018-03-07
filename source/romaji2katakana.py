# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

import glob
import re
import sys

'''
Convert romaji script to katakana.
Input:
    romaji wordlist
Output:
    katakana wordlist at the same directory
How to run:
    source activate python3
    python romaji2katakana.py <path/to/wordlist>
'''

class Romaji2Katakana:
    def __init__(self,chart):
        self.chart = ''
        with open(chart) as chrt:
            for line in chrt:
                #line = line.decode('utf-8')
                self.chart += line

    def chartParse(self):
        """
        Create chart dictionary.
        Based on https://github.com/kevincobain2000/jProcessing/blob/master/src/jNlp/jConvert.py
        """
        lines = self.chart.split('\n')
        chartDict = {}
        output = {}
        col_headings = lines.pop(0).split()
        for line in lines:
            cells = line.split()
            for i, c in enumerate(cells[1:]):
                output[c] = (cells[0], col_headings[i])
        for k in sorted(output.keys()):
            #@k = katakana
            #@r = first romaji in row
            #@c = concatinating romaji in column
            r, c = output[k]
            #k, r, c = [unicode(item,'utf-8') for item in [k,r,c]]
            if k == 'X':continue
            romaji = ''.join([item.replace('X', '') for item in [r,c]])
            chartDict[k] = romaji

        ## Invert dict to map romaji to katakana instead.
        chartDict = self.invert_dict(chartDict)
        self.chartdict = chartDict
        return chartDict

    def invert_dict(self,dct):
        inv_dict = {v: k for k, v in dct.items()}
        #inv_dict = {v: k for k, v in dct.iteritems()}
        
        return inv_dict

    def romaji2katakana(self,word):
        syllables = []
        c = 0
        while word:
            for n in reversed(range(1,4)):
                c += 1
                try:
                    syllable = word[:n]
                    if syllable in self.chartdict:
                        syllables.append(self.chartdict[syllable])
                        word = word[n:]
                except IndexError:
                    continue
            ## If it is not possible to syllabify to word
            ## (e.g. Eglish words like administration), skip the word.
            if c > 300:
                print('No katakana form for word %s' % word)
                break

        return ''.join(syllables)

if __name__ == '__main__':
    wordlist = sys.argv[1]
    out_name = wordlist.replace('.words','_to_katakana.words')
    chart = 'katakanaChart.txt'
    r2k =  Romaji2Katakana(chart)
    r2k.chartParse()
    with open(wordlist,encoding='utf-8') as inf, \
            open(out_name,'w',encoding='utf-8') as outf:
        for line in inf:
            word = line.strip()
            katakana = r2k.romaji2katakana(word)
            if katakana:
                outf.write('%s\n' % katakana)
