#!/bin/bash

dict=$1
ngram_order=7
mkdir -p ${dict}

phonetisaurus-align --input=${dict}/${dict}.train --ofile=${dict}/${dict}.corpus
estimate-ngram -o $ngram_order -t ${dict}/${dict}.corpus -wl ${dict}/${dict}.o${ngram_order}.arpa
phonetisaurus-arpa2wfst --lm=${dict}/${dict}.o${ngram_order}.arpa --ofile=${dict}/${dict}.o${ngram_order}.fst
## Test model.
cat ${dict}/${dict}.test | cut -f1 > ${dict}/${dict}.words
cat ${dict}/${dict}.test | cut -f2 > ${dict}/${dict}.ref
phonetisaurus-apply --model ${dict}/${dict}.o${ngram_order}.fst --word_list ${dict}/${dict}.words | cut -f2 > ${dict}/${dict}.hyp
