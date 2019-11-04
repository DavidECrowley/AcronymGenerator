#!/usr/bin/env node

# David E.Crowley
# An implementation of a basic Acronym Generator.

#import textblob       # needed for NLTK, parser
#import nltk           # Natural Language Toolkit
import re              # for Regular Expressions
import itertools       # for permutations
import multiprocessing # for multithreading. Need Python3
from expletives import badwords, okayish # this is an expletives

# taking our bad words from expletives
# new set with elements in 's' but not in 't'
# where 's' is our really_badwords and 't' is our okayish words set.
really_badwords = badwords.difference(okayish) 
really_badwords = set((w.lower() for w in really_badwords))

def to_acronym(words, detect_acronyms = True):
    """ to_acronym will take in input 'words'
        for each word it will create an acronym
    """
    acronym = ''
    acronym2 = ''
    for word in words:
        if detect_acronyms and word.isupper():
            #print(acronym)
            acronym += word
            acronym2 += word
        else:
            acronym += word[0].upper()
            acronym2 += word[0:1].upper()
    # return so we can assign later
    return (acronym, acronym2, words)


def return_list(permutation):
    return list(permutation)
    
if __name__ == '__main__':
    conf_min = 3  # minimum length of result acronym
    conf_max = 6  # maximum length of result acronym
    conf_max_permutations = 5000 # number of permutations we want to run
    conf_extended_acronyms = False  # True for two-character acronyms
    conf_detect_acronyms = False  # True to include full acronyms in the resulting acronym.
    
    words = list()
    acronyms = dict()
    skipped_words = 0
    removed_acronyms = 0
    added_acronyms = 0 

    # open our file to be read as 'f'
    with open('word_list.txt', 'r') as file:
        for line in file:
            # basic regex searching for only alphabetic
            if re.search(r'[\d-]', line):
                skipped_words += 1
                continue
            words.append(line.strip())
    
    total_acronyms = 0

    # we are in range of (3 - 6) letter acronyms
    for pLen in range(conf_min, (conf_max+1)):
        # Here I am using some multithreading, generally gives slight performance increase
        # can test this using timeit module if needed
        with multiprocessing.Pool() as pool:
            # map to chop iterable into chunks, submits to process pool as seperate tasks
            # .islice() is creating the iterator that returns the selected element from iterable
            # we finally permutate. Reasoning for this was so that we could create a large number of acronyms
            # permutations can take time as they can become exponentially more difficult to process
            word_sets = pool.map(return_list, itertools.islice( \
                itertools.permutations(words, pLen), conf_max_permutations ))

        # for each of our word sets
        for wset in word_sets:
            # assign acronyms to new_acronyms with function call
            new_acronyms = to_acronym(wset, conf_detect_acronyms)
            #print(new_acronyms)
            new_acronym = new_acronyms[0] if conf_extended_acronyms else new_acronyms[1]
            #print(new_acronym)
            # some counting of removed acro's
            if new_acronym.lower() in really_badwords:
                removed_acronyms += 1
                continue
            else:
                added_acronyms += 1

            # for said length in acronyms
            if pLen in acronyms :
                #print(pLen)
                acronyms[pLen].add(new_acronym)
            else:
                acronyms[pLen] = set([new_acronym])
        #total count
        total_acronyms += len(acronyms[pLen])

    # and some output to see whats going on a bit better.
    print( acronyms )
    print( len(acronyms) )
    print( "Ignored Words:  {}".format(skipped_words) )
    print( "Removed Acronyms:  {}".format(removed_acronyms) )
    print( "Total Acronyms Listed:  {}".format(total_acronyms) )
    print( "Total Acronyms Processed:  {}".format(added_acronyms) )
    
    
