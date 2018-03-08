#!/bin/bash

lexicon=$1
lexicon=${lexicon%.*}
ext="${1##*.}"
echo $lexicon $ext

## Kanji/hiragana/katakana to romaji conversion.
echo 'Converting from kanji/hiragana/katakana to romaji...'
source activate py2
python transliterate.py ${lexicon}.${ext}
lexicon=${lexicon}_romaji

## Sort and uniq romaji wordlist.
sort ${lexicon}.${ext} | uniq > ${lexicon}_uniq.${ext}
lexicon=${lexicon}_uniq

## Split lexicon into train and test set (ratio: 0.9-0.1)
source activate py3
echo 'Create train and test sets...'
python split_to_train_test.py ${lexicon}.${ext}

## Create directory and move files for training.
dir=$(basename "$lexicon")
cd ..
mkdir -p $dir
cd source
cp ${lexicon}.train ../${dir} 
cp ${lexicon}.test ../${dir}

## Train and evaluate g2p model with phonetisaurus.
echo 'Training g2p model with phonetisaurus...'
source activate py2
./train_model.sh $dir
