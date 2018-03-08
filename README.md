# Japanese G2P (grapheme-to-phoneme) and N2W (number-to-word) converter

## Dependencies

### Python 2.7 environment with numpy

Create conda environment from `requirements_py27.txt`

    conda create --name py2 --file requirements_py27.txt

### JProcessing

#### Installation
See instructions at the [github repo](https://github.com/kevincobain2000/jProcessing).

### Espeak

#### Installation
See instructions at the [github repo](https://github.com/espeak-ng/espeak-ng).

### Phonetisaurus

#### Installation
See installation instructions at the [github repo](https://github.com/AdolfVonKleist/Phonetisaurus).

## Lexicon acquisition

As I could only 

### Wiktionary data

One option is to download the Japanese Wiktionary dump, and extract the wod-pronunciation pairs.  
Fortunately this work has already been done in [this paper](https://aclweb.org/anthology/P/P16/P16-1038.pdf) with the [data](https://drive.google.com/drive/folders/0B7R_gATfZJ2aWkpSWHpXUklWUmM) made available publicly.  
The Japanese part of the data contains an overall 2k word-pron pairs - which is not too much.
This lexicon consists of words written in kanji, katakana, hiragana and the Latin alphabet and their respective pronunciation of ipa symbols.

### Leeds University wordlist

[Japanese wordlist](http://corpus.leeds.ac.uk/frqc/internet-jp-forms.num) from the University of Leeds, containing 44k words.
The wordlist consists of words written in kanji, katakana, hiragana and the Latin alphabet.

Both the wiktionary lexicon and the Japanese wordlist are shared
[here in the wordlists directory](https://drive.google.com/open?id=1HPOvT5NNR5pWzAG0e09P99jPaEbiAJvq),
as `wordlists/jpn_wiktionary.lex` and `wordlists/jpn.words`.

### Transliteration: kanji/katakana/hiragana-to-romaji

As the japanese writing system uses four "alphabets" (kanji, katakana, hiragana and romaji) and the lexical resources are scarce,
transliteration (to romaji) is much needed to simplify the g2p training, as less input symbols / smaller grapheme inventory reduces the noise.

The [jProcessing tool](http://jprocessing.readthedocs.io/en/latest/#kanji-katakana-hiragana-to-tokenized-romaji-jconvert-py)
supports kanji/katakana/hiragana-to-romaji conversion.  

#### Run kanji/katakana/hiragana-to-romaji transliteration

    cd source
    python transliterate.py <path/to/wordlist_or_lexicon>
    ## Output in <path/to/wordlist_or_lexicon_romaji>

### Transliteration: romaji-to-katakana

The Japanese voice of espeak accepts only hiragama script as input,
thus the already transliterated romaji words need to be converted to katakana.
This step is only needed if the data needs to be processed with espeak (so for wordlists, not lexica).

    cd source
    python romaji2katakana.py <path/to/wordlist>.words
    ## Output in <path/to/wordlist_to_katakana>.words

### Transcribe wordlists with espeak

#### Run G2P transcription with espeak

    cd source
    python wlist2lex.py <path/to/wordlist>.words
    ## Output in <path/to/wordlist_espeak>.words
    
### Split wordlist into train and test (0.9-0.1 ratio)

    cd source
    python split_to_train_test.py <path/to/wordlist>.words
    ## Output in <path/to/wordlist>.train, <path_to_wordlist>.test

## G2P training with Phonetisaurus

From the acquired lexica

### Run G2P training and evaluation with Phonetisaurus

    cd source
    ./train_model.sh <lexicon_dir_name>
    ## Output: 
    ## <lexicon_dir_name>/<lexicon_dir_name>.oN.arpa, where N is the n-gram order
    ## <lexicon_dir_name>/<lexicon_dir_name>.oN.fst
    
### Run wordlist/lexicon to g2p model scripts

    ## For lexica, e.g. 'wordlists/jpn_wiktionary.lex'
    cd source
    ./run_lexicon_to_model.sh <path/to/lexicon>
    ## For wordlists, e.g. 'wordlists/jpn.words'
    cd source
    ./run_lexicon_to_model.sh <path/to/wordlist>
    
## Number conversion

The main idea behind arabic-to-written/romaji/kanji conversion is to represent numbers as factors of the powers of ten.  
`12345`  
would become  
`1*10^4 + 2*10^3 + 3*10^2 + 4*10^1 + 5*10^0`  
which can be represented as a list of factors  
`['1[E4]','2[E3]','3[E2]','4[E1]','5[E0]']`.  
This representation is easy to then to map to the written forms of numbers in a given language,
but depending on the language, a few further modifications of the list are needed. 
First

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

The input format

    cd source
    python token2pron.py <path/to/input>
