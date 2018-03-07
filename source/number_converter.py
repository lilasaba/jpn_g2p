# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

from __future__ import print_function

import re
import sys

'''
Number converter modul:
    + kanji to arabic
    + arabic to kanji
    + arabic to romaji
'''

class ConvertNumber:
    def __init__(self):

        ## Dicts for kanji to arabic conversion.
        self.num_map = ((0,u"〇"),
                (1,u"一"),
                (2,u"二"),
                (3,u"三"),
                (4,u"四"),
                (5,u"五"),
                (6,u"六"),
                (7,u"七"),
                (8,u"八"),
                (9,u"九"),
                (10,u"十"),
                (100,u"百"),
                (1000,u"千"),
                (10000,u"万"),
                (100000000,u"億"),
                (1000000000000,u"兆"))

        self.kanji2arabic_dict = dict((kanji,num) for (num,kanji) in self.num_map)

        ## Dicts for arabic number to kanji/romaji conversion.
        self.factor_map_kanji = {
                '1':u"一",
                '2':u"二",
                '3':u"三",
                '4':u"四",
                '5':u"五",
                '6':u"六",
                '7':u"七",
                '8':u"八",
                '9':u"九",
                '[E1]':u"十",
                '[E2]':u"百",
                '[E3]':u"千",
                '[E4]':u"万",
                '[E8]':u"億",
                '[E12]':u"兆"}

        self.factor_map_romaji = {
                '1':'ichi',
                '2':'ni',
                '3':'san',
                '4':'yon',
                '5':'go',
                '6':'roku',
                '7':'nana',
                '8':'hachi',
                '9':'kyu',
                '[E1]':'ju',
                '[E2]':'hyaku',
                '[E3]':'sen',
                '[E4]':'man',
                '[E8]':'oku',
                '[E12]':'cho'}

        self.japanese_factors = {
                '[E0]':'',
                '[E5]':'[E1]',
                '[E6]':'[E2]',
                '[E7]':'[E3]',
                '[E9]':'[E1]',
                '[E10]':'[E2]',
                '[E11]':'[E3]'}

    def _break_down_nums(self,nums):
        first,second,third,rest = nums[0],nums[1],nums[2],nums[3:]
        if first < third or third < second:
            return [first+second,third] + rest
        else:
            return [first,second*third] + rest

    def kanji2num(self,kanji,enc="utf-8"):
        """
        Convert the kanji number to a Python integer.
        Supply `kanji` as a unicode string,or a byte string
        with the encoding specified in `enc`.

        Based on:
        http://ginstrom.com/scribbles/2009/04/28/converting-kanji-numbers-to-integers-with-python/
        """
        #if not isinstance(kanji,unicode):
         #   kanji = unicode(kanji,enc)

        ## Get the string as list of numbers.
        nums = [self.kanji2arabic_dict[x] for x in kanji]

        num = 0
        while len(nums) > 1:
            first,second,rest = nums[0],nums[1],nums[2:]
            if second < first: # e.g. [10,3,…]
                if any(x > first for x in rest): # e.g. [500,3,10000,…]
                    nums = self._break_down_nums(nums)
                else: # e.g. [500,3,10,…]
                    num += first
                    nums = [second] + rest
            else: # e.g. [3,10,…]
                nums = [first*second] + rest

        return str(num + sum(nums))

    def num2factors(self,num):
        '''
        Factorize arabic numbers.
        Input:
            int
        Output:
            list of factors
        E.g.:
        >>> num2factors(120456)
        >>> ['1[E5]', '2[E4]', '0[E3]', '4[E2]', '5[E1]', '6[E0]']
        '''
        num_list = []
        for i in range(len(str(num))):
            exp = len(str(num)) - 1 - i
            component = int(str(num)[i]) * 10**exp
            factor = int(component / 10**exp)
            E = '%s[E%s]' % (factor,exp)
            num_list.append(E)

        return num_list

    def remove_zero_factors(self,num_list):
        '''
        Remove zero factors.
        Input:
            list of factors
        Output:
            list of factors
        E.g.:
        >>> remove_zero_factors(['1[E5]', '2[E4]', '0[E3]', '4[E2]', '5[E1]', '6[E0]'])
        >>> ['1[E5]', '2[E4]', '4[E2]', '5[E1]', '6[E0]']
        '''
        new_list = [factor for factor in num_list if '0[' not in factor]

        return new_list

    def apply_japanese_factorization(self,num_list):
        '''
        Convert factors to the Japanese number system.
        Input:
            list of factors
        Output:
            list of factors
        E.g.:
        >>> apply_japanese_factorization(['1[E5]', '2[E4]', '4[E2]', '5[E1]', '6[E0]'])
        >>> ['1[E1]', '2[E4]', '4[E2]', '5[E1]', '6']
        '''
        new_list = []
        for factor in num_list:
            count,power = factor.split('[')
            power = '[%s' % power
            if power in self.japanese_factors:
                power = self.japanese_factors[power]
            factor = '%s%s' % (count,power)
            new_list.append(factor)

        return new_list

    def factors2written(self,num_list,factor_map):
        '''
        Convert final factor list to kanji or romaji script.
        Input:
            factor list
        Output:
            str
        E.g.:
        >>> factors2written(['1[E2]', '2[E1]', '3'],self.kanji_factor_map)
        >>> '百二十三'
        >>> factors2written(['1[E2]', '2[E1]', '3'],self.romaji_factor_map)
        >>> 'hyakunijusan'
        '''
        written = ''
        non_ichi_set = {'[E1]','[E2]','[E3]'}
        first_factor = True
        for factor in num_list:
            ## Check for [E0] (10**0) numbers first.
            if factor in factor_map:
                written += ' %s' % factor_map[factor]
            else:
                count,power = factor.split('[')
                power = '[%s' % power
                ## Add "count" part first; e.g. 4 from "4[E2]"
                ## "4[E2]" --> "yon hyaku"
                ## Restrict ichi at the beginning of the number for [E1],[E2],[E3].
                ## Source: https://en.wikipedia.org/wiki/Japanese_numerals
                if first_factor and count == '1' and power in non_ichi_set:
                    pass
                else:
                    written += ' %s' % factor_map[count]
                ## Add "power" part second; e.g. [E2] from "4[E2]"
                written += ' %s' % factor_map[power]
            first_factor = False

        return written.replace(' ','')

    def num2written(self,number):
        '''
        Convert arabic number to kanji or romaji script.
        Input:
            str
        Output:
            str
        E.g.:
        >>> num2written('123')
        >>> ('百二十三','hyakunijusan')
        '''
        number = number.replace(',','')
        if number == '0':
            return '〇','rei'

        factor_list = self.num2factors(number)
        factor_list = self.remove_zero_factors(factor_list)
        factor_list = self.apply_japanese_factorization(factor_list)
        kanji = self.factors2written(factor_list,self.factor_map_kanji)
        romaji = self.factors2written(factor_list,self.factor_map_romaji)
        
        return kanji,romaji

if __name__ == '__main__':
    num_converter = ConvertNumber() 
    input_number = sys.argv[1]
    input_len = len(input_number)
    kanji_len = len([k for k in input_number if k in num_converter.kanji2arabic_dict])
    if re.search(r'^[0-9,]+$',input_number):
        kanji,romaji = num_converter.num2written(input_number)
        print('Input number: %s\nKanji: %s\nRomaji: %s' \
                % (input_number,kanji,romaji))
    elif input_len == kanji_len:
        out = num_converter.kanji2num(input_number)
        print('Input number: %s\nArabic number: %s' \
                % (input_number,out))
    else:
        print('Input format not supported.')
