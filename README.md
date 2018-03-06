# Japanese G2P (grapheme-to-phoneme) and N2W (number-to-word) converter

## Python2 vs Python3

## Lexicon acquisition

### Wiktionary data
+ Grapheme-to-Phoneme Models for (Almost) Any Language (Deri and Knight, ACL 2016)
+ [data](https://drive.google.com/drive/folders/0B7R_gATfZJ2aWkpSWHpXUklWUmM)

### Transcribe wordlists with espeak

The Japanese voice of espeak accepts only hiragama script as input.

#### Installation
See instructions at the [github repo](https://github.com/espeak-ng/espeak-ng).

## Transliteration
[This tool](http://jprocessing.readthedocs.io/en/latest/#kanji-katakana-hiragana-to-tokenized-romaji-jconvert-py) supports kanji/katakana/hirgana-to-romaji transcription.  
Transliteration ismuch neede to simplify the g2p training, as less input symbols / smaller grapheme inventory reduces the noise.

#### Installation
See instructions at [official documentation page](http://jprocessing.readthedocs.io/en/latest/#install).

## G2P training with Phonetisaurus

#### Installation
See installation instructions at [the github repo](https://github.com/AdolfVonKleist/Phonetisaurus).

## Number conversion

    cd source
	## Arabic to kanji/romaji.
	python number_converter.py 123
	Input number: 123
    Kanji: 百二十三
    Romaji: hyakunijusan
	## Kanji to arabic.
    python number_converter.py 百二十三
    Input number: 百二十三
    Arabic number: 123


