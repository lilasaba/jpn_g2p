#!/bin/bash

wlist=$1
wlist=${wlist%.*}
ext="${1##*.}"
echo $wlist $ext

## Kanji/hiragana/katakana to romaji conversion.
echo 'Converting from kanji/hiragana/katakana to romaji...'
source activate py2
python transliterate.py ${wlist}.${ext}
wlist=${wlist}_romaji

## Sort and uniq romaji wordlist.
sort ${wlist}.${ext} | uniq > ${wlist}_uniq.${ext}
wlist=${wlist}_uniq

## Romaji to katakana conversion.
echo 'Converting from romaji to katakana...'
source activate py3
python romaji2katakana.py ${wlist}.${ext}
wlist=${wlist}_to_katakana

## Uniq (but not sort) katakana wordlist.
## This is needed to avoid identical word-pron pairs in the lexicon.
uniq ${wlist}.${ext} > ${wlist}_uniq.${ext}
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
mkdir -p $dir
cd source
cp ${wlist}.train ../${dir} 
cp ${wlist}.test ../${dir}

## Train and evaluate g2p model with phonetisaurus.
echo 'Training g2p model with phonetisaurus...'
source activate py2
./train_model.sh $dir
