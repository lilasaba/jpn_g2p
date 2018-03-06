#!/bin/bash

## Train g2p model from lexicon.
## Dependencies: 
##     - phonetisaurus (https://github.com/AdolfVonKleist/Phonetisaurus).
##     - python 2.7 environment
## Lexicon a directory name should be identical.
## How to run:
## ./train_model.sh <lexicon_name_without_extension> 

dict=$1
dir=../${1}
ngram_order=7
mkdir -p ${dir}

## Train model.
phonetisaurus-align --input=${dir}/${dict}.train \
	--ofile=${dir}/${dict}.corpus
estimate-ngram -o $ngram_order -t ${dir}/${dict}.corpus \
	-wl ${dir}/${dict}.o${ngram_order}.arpa
phonetisaurus-arpa2wfst --lm=${dir}/${dict}.o${ngram_order}.arpa \
	--ofile=${dir}/${dict}.o${ngram_order}.fst

## Test model.
cat ${dir}/${dict}.test | cut -f1 > ${dir}/${dict}.words
cat ${dir}/${dict}.test > ${dir}/${dict}.ref
phonetisaurus-apply --model ${dir}/${dict}.o${ngram_order}.fst \
	--word_list ${dir}/${dict}.words \
	-n 2 -g -v > ${dir}/${dict}.hyp

python calculateER.py --hyp ${dir}/${dict}.hyp \
	--ref ${dir}/${dict}.ref
