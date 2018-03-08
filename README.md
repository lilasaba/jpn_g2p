# Japanese G2P (grapheme-to-phoneme) and N2W (number-to-word) converter

## Dependencies

### Python 2.7 environment with numpy

Create conda environment from [requirements file](requirements_py27.txt).

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

Finding non-propietary Japanese pronunciation lexica, that could be used as tarining data for the grapheme-to-phoneme (g2p) modeling,
turned out to be non-straightforward, so for the basic g2p modeling they need to be created.
Here I used two ways to create pronunciation lexica:

+ scrape Japanese Wiktionary for word-pron pairs
+ transcribe Japanese wordlists with [espeak](https://github.com/espeak-ng/espeak-ng) (an open source TTS system)

### Wiktionary data

One option is to download the Japanese Wiktionary dump, and extract the wod-pronunciation pairs.  
Fortunately this work has already been done in [this paper](https://aclweb.org/anthology/P/P16/P16-1038.pdf) with the [data](https://drive.google.com/drive/folders/0B7R_gATfZJ2aWkpSWHpXUklWUmM) made available publicly.  
The Japanese part of the data contains an overall 2k word-pron pairs - which is not too much.
This lexicon consists of words written in kanji, katakana, hiragana and the Latin alphabet and their respective pronunciation of ipa symbols.

### Leeds University wordlist

Another possibility is to find Japanese wordlists (easier than finding lexica),
and transcribe them with espeak.
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

    cd source
    python wlist2lex.py <path/to/wordlist>.words
    ## Output in <path/to/wordlist_espeak>.words
    
### Split wordlist/lexicon into train and test sets

    cd source
    python split_to_train_test.py <path/to/wordlist:or_lexicon>.words/lex
    ## Output in <path/to/wordlist>.train, <path_to_wordlist>.test

## G2P training with Phonetisaurus

To get the pronunciation of words that are not already in the lexicon, a g2p model has to be trained, using the lexicon as training data.
Here I used [Phonetisaurus](https://github.com/AdolfVonKleist/Phonetisaurus), an open source WFST-based

### Run G2P training and evaluation with Phonetisaurus

    cd source
    ./train_model.sh <lexicon_dir_name>
    ## Output: 
    ## <lexicon_dir_name>/<lexicon_dir_name>.oN.arpa, where N is the n-gram order
    ## <lexicon_dir_name>/<lexicon_dir_name>.oN.fst
    
## Run wordlist/lexicon to g2p model scripts

All the above:

+ kanji/katakana/hirgama to romaji conversion
+ optional: romaji to katakana conversion
+ optional: katakana to ipa conversion with espeak
+ splitting into train and test sets
+ g2p modeling with Phonetisaurus

are wrapped in two runfiles, which can be run as follows: 

    ## For lexica, e.g. 'wordlists/jpn_wiktionary.lex'
    cd source
    ./run_lexicon_to_model.sh <path/to/lexicon>
    ## For wordlists, e.g. 'wordlists/jpn.words'
    cd source
    ./run_lexicon_to_model.sh <path/to/wordlist>
    
The interim wordlists/lexica are created in the [wordlists](wordlists) directory,
the fst models are in a directory whose name is identical to the lexicon name.
    
## Number conversion

The main idea behind arabic-to-written (romaji or kanji) conversion is to represent numbers as factors of the powers of ten.  
`12045`  
would become  
`1*10^4 + 2*10^3 + 0*10^2 + 4*10^1 + 5*10^0`  
which can be represented as a list of factors  
`['1[E4]','2[E3]','0[E2]','4[E1]','5[E0]']`.  
This representation is easy to then to map to the written forms of numbers in a given language,
but depending on the language, a few further modifications of the list are needed. 
First, the zero factors, e.g. `0[E2]`, have to be removed as they are not present in the written/spoken form.  
Then the factors which have no distinctive written form (e.g. `[E5]`) have to be converted 
In western number factorization `[E1], [E2], [E3], [E6], [E9]` have distinctive names `ten, hundred, thousand, million, billion`,
and everything in between is an iteration from `[E1]` to `[E3]`.
So basically adding three to the exponent or by every three digit group, there is new distinctive name.  
In the Japanese number system `[E1], [E2], [E3], [E4], [E8], [E12]` have distinct names `ju, hyaku, sen, man, oku, cho`,
and everything in between is an iteration from `` (four digit/kanji groups).

After mapping the factors according to the Japanese factorization, the factors themselves are also split
into the basic elements that make up the written form;
e.g. `2[E3]` to `2` and `[E3]`.
From then on, we just need a dictionary that maps the basic elements into their written romaji or kanji forms,
so `[E3]` to `` and `` to ``.

The [number converter](source/number_converter.py) supports both kanji-to-arabic and arabic-to-kanji/romaji conversions.

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

## Convert 'Words' or 'Numbers' objects to pronunciations

The following input format is supported:

    Words\ttoken1 token2 token3
    Numerals\ttoken4 token5 token6
    
An [exaple input file](input/input_tokens.txt) is in the repo.

### Run object to pronunciations conversion

    cd source
    python token2pron.py <path/to/input>
    
The output is written in the [output directory](output), in the following format:

    token_type\tinput_token\pron
    Words\ttoken1\tp r o n 1
    Words\ttoken2\tp r o n 2
    Words\ttoken3\tp r o n 3
    Numerals\ttoken1\tp r o n 1
    Numerals\ttoken2\tp r o n 2
    Numerals\ttoken3\tp r o n 3
    
## Caveats

+ need more data
+ merged phoneme inventory
+ `一〇〇`
+ only one pron as output
