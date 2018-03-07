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

    def wlist2pron(self,word_list):
        for i,(word,score,pron) in enumerate(self.runG2PCommand(word_list)):
            token = self.original_list[i].decode('utf-8')
            line = u""
            line = u"%s\t%s\t%s" % (token,word,pron)
            print(line.encode("utf8"))

    def object2pron(self,objct):
        '''
        Get pronunciation of tokens in 'Words' or 'Numerals' type objects.
        Input:
        ('Words',['日本','すごい','食べる','パソコン','Sony'])
        ('Numerals',['32802','3,209','一〇〇','四百六十九'])
        Output:
        '''
        object_type = objct[0]
        token_list = objct[1]
        self.original_list = token_list[:]
        token_list = [self.token2romaji(token) for token in token_list]
        tmpwordlist = self.create_tempwordlist(token_list)
        self.wlist2pron(tmpwordlist.name)

    def token2romaji(self,token):
        romaji = self.transliterate.transliterate_token(token)

        if not romaji:
            print('Failing transliteration for token: %s' % token,\
                    file=sys.stderr)
            self.original_list.remove(token)
        else:
            return romaji

    def create_tempwordlist(self,token_list):
        tmpwordlist = tempfile.NamedTemporaryFile(delete=False)
        for token in token_list:
            if token:
                token = token.decode('utf-8')
                print(token.encode('utf-8'),file=tmpwordlist)
        tmpwordlist.close()

        return tmpwordlist

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

if __name__ == '__main__':

    jpn_g2p_espeak = Token2Pron(\
            '../jpn_leeds_romaji_uniq_espeak/jpn_leeds_romaji_uniq_espeak.o7.fst')
    jpn_g2p = Token2Pron(\
            '../jpn_wiktionary_romaji/jpn_wiktionary_romaji.o7.fst')
    objects = [('Words',['日本','すごい','食べる','パソコン','Sony']),
            ('Numerals',['32802','3,209','一〇〇','四百六十九'])]
    for objct in objects:
        jpn_g2p.object2pron(objct)
