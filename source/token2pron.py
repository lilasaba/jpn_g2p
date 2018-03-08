# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

from __future__ import print_function
import glob
import logging
import os
import re
import subprocess
import sys
import tempfile
from number_converter import ConvertNumber
from romaji2katakana import Romaji2Katakana
from transliterate import Transliterate

'''
Words: 日本 すごい 食べる パソコン Sony
Numerals: 32802 3,209 一〇〇 四百六十九
'''

class Token2Pron:
    def __init__(self,model,**kwargs):
        self.model = model
        self.lexicon_file = kwargs.get ("lexicon", None)
        self.nbest = kwargs.get ("nbest", 1)
        self.thresh = kwargs.get ("thresh", 99)
        self.beam = kwargs.get ("beam", 10000)
        self.greedy = kwargs.get ("greedy", False)
        self.accumulate = kwargs.get ("accumulate", False)
        self.pmass = kwargs.get ("pmass", 0.0)
        self.probs = kwargs.get ("probs", False)
        self.transliterate = Transliterate()
        self.romaji2katakana = Romaji2Katakana()
        self.katakana = False
        if 'katakana' in self.model:
            self.katakana = True
        self.num_converter = ConvertNumber()
        self.arabic_pat = re.compile(r'^[0-9,]+$')
        self.numeral = False

    def wlist2pron(self,word_list):
        '''
        Input:
            list of words
        Output:
            list of tuples of word-pron pairs
        '''
        word_pron_pair_list = []
        for i,(word,score,pron) in enumerate(self.runG2PCommand(word_list)):
            token = self.original_list[i].decode('utf-8')
            line = u""
            line = u"%s\t%s\t%s" % (token,word,pron)
            word_pron_pair_list.append((token.encode("utf8"),pron.encode("utf8")))

            print(line.encode("utf8"))

        return word_pron_pair_list

    def object2pron(self,objct):
        '''
        Get pronunciation of tokens in 'Words' or 'Numerals' type objects.
        Input:
            tuple of (token_type,toke_list), e.g.:
            ('Words',['日本','すごい','食べる','パソコン','Sony'])
            ('Numerals',['32802','3,209','一〇〇','四百六十九'])
        Output:
            list of tuples of (word,pron)
        '''
        object_type = objct[0]
        token_list = objct[1]
        if object_type == 'Numerals':
            self.numeral = True
        self.original_list = token_list[:]
        ## Handle number conversion.
        if self.numeral:
            token_list = [self.number2written(num) for num in token_list]
        ## Character conversions.
        new_list = []
        for token in token_list:
            out = None
            if not self.numeral:
                out = self.token2romaji(token)
            elif self.numeral:
                out = token
            ## Convert to katakana if model is katakana-based.
            if out and self.katakana:
                out = self.rom2kata(out,token) 
            if out:
                new_list.append(out)
        ## Create temp wordlist from list as phonetisaurus only 
        ## accept files as input.
        tmpwordlist = self.create_tempwordlist(new_list)
        word_pron_pair_list = self.wlist2pron(tmpwordlist.name)

        return word_pron_pair_list

    def token2romaji(self,token):
        romaji = self.transliterate.transliterate_token(token)

        if not romaji:
            print('Failing transliteration for token: %s' % token,\
                    file=sys.stderr)
            self.original_list.remove(token)
        else:
            return romaji

    def rom2kata(self,token,orig):
        katakana = self.romaji2katakana.romaji2katakana(token)

        if not katakana:
            print('Failing romaji to katakana conversion for token: %s' % token,\
                    file=sys.stderr)
            self.original_list.remove(orig)
        else:
            return katakana

    def create_tempwordlist(self,token_list):
        tmpwordlist = tempfile.NamedTemporaryFile(delete=False)
        for token in token_list:
            if token:
                token = token.decode('utf-8')
                print(token.encode('utf-8'),file=tmpwordlist)
        tmpwordlist.close()

        return tmpwordlist

    def number2written(self,number):
        '''
        '''
        number = number.decode('utf-8') 
        out = None
        input_len = len(number)
        kanji_len = len([k for k in number if k in self.num_converter.kanji2arabic_dict])

        ## Convert arabic to romaji.
        if self.arabic_pat.search(number):
            _,out = self.num_converter.num2written(number)
        ## Convert kanji to arabic, and arabic to romaji.
        elif input_len == kanji_len:
            out = self.num_converter.kanji2num(number)
            _,out = self.num_converter.num2written(out)
        else:
            print('Input format is not supported for %s' % number,
                    file=sys.stderr)
            self.original_list.remove(number)

        if out:
            return out

    def makeG2PCommand (self, word_list) :
        """Build the G2P command.
        Build the G2P command from the provided arguments.
        Returns:
            list: The command in subprocess list format.
        """

        command = [
            u"phonetisaurus-g2pfst",
            u"--model={0}".format (self.model),
            u"--nbest={0}".format (self.nbest),
            u"--beam={0}".format (self.beam),
            u"--thresh={0}".format (self.thresh),
            u"--accumulate={0}".format (str (self.accumulate).lower ()),
            u"--pmass={0}".format (self.pmass),
            u"--nlog_probs={0}".format (str(not self.probs).lower ()),
            u"--wordlist={0}".format (word_list)
        ]
        
        #self.logger.debug (u" ".join (command))

        return command

    def runG2PCommand (self, word_list_file) :
        """Generate and run the actual G2P command.
        
        Generate and run the actual G2P command.  Each synthesized
        entry will be yielded back on-the-fly via the subprocess
        stdout readline method.
        Args:
            word_list_file (str): The input word list.
        """
        g2p_command = self.makeG2PCommand (word_list_file)
        
        #self.logger.debug ("Applying G2P model...")

        with open (os.devnull, "w") as devnull :
            proc = subprocess.Popen (
                g2p_command,
                stdout=subprocess.PIPE,
                stderr=devnull #if not self.verbose else None
            )
            
            for line in iter (proc.stdout.readline, "") :
                parts = re.split (ur"\t", line.decode ("utf8").strip ())
                if not len (parts) == 3 :
                    #self.logger.warning (
                     #   u"No pronunciation for word: '{0}'".format (parts [0])
                    #)
                    print('No pron for word %s' % parts[0],file=sys.stderr)
                    continue
                
                yield parts

        return

    def in_to_out(self,infile):
        out_name = infile.replace('input','output')
        model_basename = os.path.basename(self.model)
        out_name = out_name.replace('.txt','_%s.txt' % \
                model_basename)
        objects = []
        with open(infile) as inf, open(out_name,'wb') as outf:
            for line in inf:
                line = line.strip()
                obj_type,obj_tokens = line.split('\t')
                obj_token_list = obj_tokens.split(' ')
                objct = (obj_type,obj_token_list)
                output = self.object2pron(objct)
                for tple in output:
                    outf.write('%s\t%s\t%s\n' % (obj_type,tple[0],tple[1]))

if __name__ == '__main__':
    infile = sys.argv[1]
    jpn_g2p_katakana = Token2Pron(\
            '../jpn_romaji_uniq_to_katakana_uniq_espeak/jpn_romaji_uniq_to_katakana_uniq_espeak.o7.fst')
    jpn_g2p = Token2Pron(\
            '../jpn_wiktionary_romaji_uniq/jpn_wiktionary_romaji_uniq.o7.fst')
#    objects = [('Words',['日本','すごい','食べる','パソコン','Sony']),
#            ('Numerals',['32802','3,209','一〇〇','四百六十九'])]
#    for objct in objects:
#        jpn_g2p.object2pron(objct)
#    for objct in objects:
#        jpn_g2p_katakana.object2pron(objct)
    jpn_g2p_katakana.in_to_out(infile)
    jpn_g2p.in_to_out(infile)
