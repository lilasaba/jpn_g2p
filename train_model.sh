#!/bin/bash

## Train g2p model from lexicon.
## Dependencies: 
##     - phonetisaurus (https://github.com/AdolfVonKleist/Phonetisaurus).
##     - python 2.7 environment
## Lexicon a directory name should be identical.
## How to run:
## ./train_model.sh <lexicon_name_without_extension> 

dict=$1
ngram_order=7
mkdir -p ${dict}

## Train model.
phonetisaurus-align --input=${dict}/${dict}.train \
	--ofile=${dict}/${dict}.corpus
estimate-ngram -o $ngram_order -t ${dict}/${dict}.corpus \
	-wl ${dict}/${dict}.o${ngram_order}.arpa
phonetisaurus-arpa2wfst --lm=${dict}/${dict}.o${ngram_order}.arpa \
	--ofile=${dict}/${dict}.o${ngram_order}.fst

## Test model.
cat ${dict}/${dict}.test | cut -f1 > ${dict}/${dict}.words
cat ${dict}/${dict}.test > ${dict}/${dict}.ref
phonetisaurus-apply --model ${dict}/${dict}.o${ngram_order}.fst \
	--word_list ${dict}/${dict}.words \
	-n 2 -g -v > ${dict}/${dict}.hyp
