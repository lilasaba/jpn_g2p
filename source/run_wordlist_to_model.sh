#!/bin/bash

wlist=$1
wlist=${wlist%.*}
ext="${1##*.}"
echo $wlist $ext

## Kanji/hiragana/katakana to romaji conversion.
source activate py2
echo 'Converting from kanji/hiragana/katakana to romaji...'
python transliterate.py ${wlist}.${ext}
wlist=${wlist}_romaji

## Sort and uniq romaji wordlist.
sort ${wlist}.${ext} | uniq > ${wlist}_uniq.${ext}
wlist=${wlist}_uniq

## Romaji to katakana conversion.
source activate eudikt
echo 'Converting from romaji to katakana...'
python romaji2katakana.py ${wlist}.${ext}
wlist=${wlist}_to_katakana

## Uniq (but not sort) katakana wordlist.
sort ${wlist}.${ext} | uniq > ${wlist}_uniq.${ext}
wlist=${wlist}_uniq

## Get phonetic transcriptions with espeak.
echo 'Getting prons with espeak...'
python wlist2lex.py ${wlist}.${ext}
wlist=${wlist}_espeak

## Split lexicon into train and test set (ratio: 0.9-0.1)
echo 'Create train and test sets...'
python split_to_train_test.py ${wlist}.${ext}

## Create directory and move files for training.
dir=$(basename "$wlist")
cd ..
mkdir $dir
cd source
cp ${wlist}.train $dir 
cp ${wlist}.test $dir 

## Train and evaluate g2p model with phonetisaurus.
echo 'Training g2p model with phonetisaurus...'
source activate py2
./train_model $dir
