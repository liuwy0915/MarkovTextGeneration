"""Markov Text Generator.

Weiyi Liu, 2021

Resources:
Jelinek 1985 "Markov Source Modeling of Text Generation"
"""

import random
import re

import nltk
import numpy as np



def ngram_freq(n, token):
    """
    save the frequency of n-gram's for each prefix in a dictionary
    """
    
    ngram_list = [[token[i+j] for j in range(n)] for i in range(len(token) - n + 1)]
    
    freq_dict = {}
    
    for word in ngram_list:
        if tuple(word[0:n-1]) not in freq_dict.keys():
            freq_dict.update({tuple(word[0:n-1]): {word[n-1]: 1}})
        else:
            if word[n-1] not in freq_dict[tuple(word[0:n-1])].keys():
                freq_dict[tuple(word[0:n-1])].update({word[n-1]:1})
            else:
                freq_dict[tuple(word[0:n-1])][word[n-1]] += 1
    
       
    return freq_dict



def most_prob_next_token(freq_dict, prefix):
    """
    generate the single most probable next token
    """
    next_token_dict = freq_dict[tuple(prefix)]
    
    max_freq = 0
    next_token = ""
    
    for token in next_token_dict.keys():
        if next_token_dict[token] > max_freq:
            max_freq = next_token_dict[token]
            next_token = token
    
    return next_token



def random_choice_next_token(freq_dict, prefix):
    """
    generate the next token by random choice
    """
    
    next_token_dict = freq_dict[tuple(prefix)]
    
    choices = list(next_token_dict)
    
    probs = [i / sum(next_token_dict.values()) for i in next_token_dict.values()]
    
    next_token = random.choices(choices, probs)
    
    return next_token[0]




def finish_sentence(sentence, n, corpus, deterministic=False):
    """
    Markov text generator 
    """
    
    freq_dict = {}
    k = n
    while k >= 1:
        freq_dict.update({k: ngram_freq(k, corpus)})
        k = k - 1
    
    prefix = tuple(sentence[-(n-1):])
        
    if deterministic == True:
        
        while (len(sentence) < 15) & (sentence[-1] not in [".", "?", "!"]):
            sentence.append(most_prob_next_token(freq_dict[n], prefix))
            prefix = tuple(sentence[-(n-1):])
            
    if deterministic == False:
        
        while (len(sentence) < 15) & (sentence[-1] not in [".", "?", "!"]):
            if prefix in freq_dict[n].keys():
                sentence.append(random_choice_next_token(freq_dict[n], prefix))
                prefix = tuple(sentence[-(n-1):])     
                
            # stupid backoff and no smoothing    
            else:
                m = n - 1
                prefix = tuple(sentence[-(m-1):])
                while (m >= 1) & (prefix not in freq_dict[m].keys()):
                    m = m - 1
                    prefix = prefix[1:]
                sentence.append(random_choice_next_token(freq_dict[m], prefix))
                prefix = tuple(sentence[-(n-1):])
                
    
    
    return sentence



