# Japanese G2P (grapheme-to-phoneme) and N2W (number-to-word) converter

## Python2 vs Python3

## Lexicon acquisition

### Wiktionary data
+ Grapheme-to-Phoneme Models for (Almost) Any Language (Deri and Knight, ACL 2016)
+ [data](https://drive.google.com/drive/folders/0B7R_gATfZJ2aWkpSWHpXUklWUmM)

### Leeds University wordlist

### Transliteration: kanji/katakana/hiragana-to-romaji
[This tool](http://jprocessing.readthedocs.io/en/latest/#kanji-katakana-hiragana-to-tokenized-romaji-jconvert-py) supports kanji/katakana/hiragana-to-romaji transcription.  
Transliteration is much needed to simplify the g2p training, as less input symbols / smaller grapheme inventory reduces the noise.

#### Installation
See instructions at [official documentation page](http://jprocessing.readthedocs.io/en/latest/#install).

#### Run kanji/katakana/hiragana-to-romaji transliteration

    cd source
    source activate <python2_env>
    python transliterate.py <path/to/wordlist_or_lexicon>
    ## Output in <path_to_wordlist_or_lexicon>

### Transliteration: romaji-tok-katakana

    cd source
    source activate <python3_env>
    python romaji2katakana.py <path/to/wordlist>.words
    ## Output in <path_to_wordlist>

### Transcribe wordlists with espeak

The Japanese voice of espeak accepts only hiragama script as input.

#### Installation
See instructions at the [github repo](https://github.com/espeak-ng/espeak-ng).

#### Run G2P transcription with espeak

    cd source
    source activate <python3_env>
    python wlist2lex.py <path/to/wordlist>.words
    ## Output in <path_to_wordlist>
    
### Split wordlist into train and test (0.9/0.1)

    cd source
    source activate <python3_env>
    python split_to_train_test.py <path/to/wordlist>.words
    ## Output in <path_to_wordlist>.train, <path_to_wordlist>.test

## G2P training with Phonetisaurus

#### Installation
See installation instructions at [the github repo](https://github.com/AdolfVonKleist/Phonetisaurus).

### Run G2P training and evaluation with Phonetisaurus

    cd source
    source activate <python2_env>
    ./train_model.sh <lexicon_dir_name>
    ## Output: 
    ## <lexicon_dir_name>/<lexicon_dir_name>oN.arpa
    ## <lexicon_dir_name>/<lexicon_dir_name>_oN.fst
    
## Number conversion

The main idea behind arabic-to-written/romaji/kanji conversion is to represent numbers as factors of the powers of ten.
`12345`  
would become  
`1*10^4 + 2*10^3 + 3*10^2 + 4*10^1 + 5*10^0`  
which can be represented as a list of factors  
`['1[E4]','2[E3]','3[E2]','4[E1]','5[E0]']`.  
This representation is easy to then to map to the written forms of numbers in a given language, but depending on the language a few further modifications of the list is needed.  

    cd source
    source activate <python3_env>
	## Arabic to kanji/romaji.
	python number_converter.py 123
	Input number: 123
    Kanji: 百二十三
    Romaji: hyakunijusan
	## Kanji to arabic.
    python number_converter.py 百二十三
    Input number: 百二十三
    Arabic number: 123

## Convert 'Words' or 'Numbers' token lists to pronunciations
