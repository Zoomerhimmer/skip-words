import argparse
import warnings
import re

def removeCharacters(string, to_remove):
    for i in to_remove:
        string = string.replace(i, '')
    return string

def main(file, dictionary, skip_count, start, backwards, backwise, punct, numbers, quiet):
    with open(file) as f:
        doc = removeCharacters(f.read(), punct).replace('\n', ' ').lower()
    if numbers:
        doc = re.sub(r'\d+', '', doc)
    if backwards:
        doc = doc[::-1]
    if dictionary:
        with open(dictionary) as f:
            dic = sorted(f.read().splitlines())
    else:
        print('No dictionary provided. Bootstrapping from document...')
        setdic = set(doc.split(' '))
        setdic.discard('')
        dic = sorted(list(setdic))
    if backwise:
        for i, word in enumerate(dic):
            dic[i] = word[::-1]

    # Need to do this after opening files since bootstrapping requires spaces.
    doc = doc.replace(' ', '')
    if len(skip_count) > 1:
        second = skip_count[1]
    else:
        second = skip_count[0]
    for i in range(skip_count[0], second+1):
        newdoc = ''
        results = ''
        for j in range(start, len(doc), i):
            newdoc += doc[j]
        for word in dic:
            count = newdoc.count(word)
            if quiet and count > 1:
                results += ' '.join([word, str(count)]) + '\n'
            elif not quiet:
                results += ' '.join([word, str(count)]) + '\n'
            with open("{}_results{}at{}.txt".format(file, i, start), 'w') as f:
                f.write(results)

parser = argparse.ArgumentParser(
        prog='skip-words',
        description='Skip words are words that are found when one skips a fixed count of letters within a document. This program looks for word matches between a dictionary and a document.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('file', help='The document to find skip-words in.')
parser.add_argument('-d', '--dictionary', help='The dictionary of words to match, one line per word. This program does not conduct any extra permutations, so if inflected forms are desired they will need to be listed separately. If a dictionary is not given the program will bootstrap a list from the document to be analyzed.')
parser.add_argument('-r', '--range', nargs='+', action='extend', type=int, required=True, help='Enter the number of letters to skip. If desired you may enter a range: the second number will be the skip-count the program ends on incrementally and inclusively.')
parser.add_argument('-s', '--start', type=int, default=0, help='Start counting from this letter onwards. The first letter is 0.')
parser.add_argument('-b', '--backwards', action='store_true', default=False, help='Start counting at the end of the document and go backwards.')
parser.add_argument('-c', '--backwise', action='store_true', default=False, help='Reverse dictionary terms when matching.')
with warnings.catch_warnings():
    parser.add_argument('-p', '--punctuation', default='!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~«»', help='A string of language specific characters to remove in addition to the whitespace.')
parser.add_argument('-n', '--numbers', action='store_true', default=False, help='Removes numbers from the document. Helpful to remove verse numbers.')
parser.add_argument('-q', '--quiet', action='store_true', default=False, help='Do not show words that did not find a match. Speeds up the program significantly.')
args = parser.parse_args()
main(args.file, args.dictionary, args.range, args.start, args.backwards, args.backwise, args.punctuation, args.numbers, args.quiet)
