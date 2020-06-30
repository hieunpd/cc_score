import sys
import os
import pandas as pd
import re
from utils import *



common_file = pd.read_csv('./Dataset/word_common.csv')
conmon_words = common_file['Word'].to_list()


def find_difficult_word(words_segmented,common_words):
    # difficult_words = [re.sub("\d*$", "", word) for word in words if word not in common_words]
    difficult_words = []
    for word in words_segmented:
        if word not in common_words:
            difficult_words.append(re.sub("\d*$", "", word))
    difficult_words = list(filter(None, difficult_words)) 
    return difficult_words

def word_segmented(data,annotator):
    document = []
    document.extend(annotator.tokenize(data))

    #Count in text
    sentences = []
    words = []    
    for sent in document:
        sentences.append(sent)
        for word in sent:
            word =RE_clear(word)
            words.append(word)

    # remove empty strings
    while("" in words):
        words.remove("")

    return words,sentences

def dale_chall_formula(pdw,aslw):
    '''
    Parameters:

        argument1 (float):per difficult words
        argument2 (float):Average sentences length words

    Return:
        float: Readability score
    '''
    if pdw >= 0.005:
        readability_score = 0.1579 * (pdw * 100)+ 0.0496 * aslw + 3.6365
    else:
        readability_score = 0.1579 * ( pdw * 100)+ 0.0496 * aslw
    
    return readability_score

# Percentage of Difficult Words:
def PDW(difficult_words,words):
    pdwi_formula = len(difficult_words)/len(words)
    return pdwi_formula

# Average Sentence Length in Words
def ASLW(words,sentences):
    aslw_formula = len(words)/len(sentences)
    return aslw_formula

# def score(content):
#     words_segmented,sentences = word_segmented(str(content))
#     if len(words_segmented) == 0:
#         dale_chall_readability_score = 0
#         dif_word = []
#     else:    
#         dif_word = find_difficult_word(words_segmented,conmon_words)
#         print('Words: ',words_segmented)
#         print('Difficult: ',dif_word)
#         pdw = PDW(dif_word,words_segmented)
#         aslw = ASLW(words_segmented,sentences)
#         dale_chall_readability_score = dale_chall_formula(pdw, aslw)
#     return dale_chall_readability_score,dif_word

def score(content,annotator):
    words_segmented,sentences = word_segmented(str(content),annotator)
    if len(words_segmented) == 0:
        dale_chall_readability_score = 0
    else:    
        dif_word = find_difficult_word(words_segmented,conmon_words)
        print('Words: ',words_segmented)
        print('Difficult: ',dif_word)
        pdw = PDW(dif_word,words_segmented)
        aslw = ASLW(words_segmented,sentences)
        dale_chall_readability_score = dale_chall_formula(pdw, aslw)
    return dale_chall_readability_score
