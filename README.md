# MarkovTextGeneration

A function `finish_sentence(sentence, n, corpus, deterministic=False)`

inputs:

  -  a sentence [list of tokens] that we’re trying to build on

  - n [int], the length of n-grams to use for prediction
  
  - a source corpus [list of tokens]
  
  - a flag indicating whether the process should be deterministic [bool]
  
output:

  - an extended sentence until the first ., ?, or ! is found OR until it has 15 total tokens

If the input flag deterministic is true, choose at each step the single most probable next
token. When two tokens are equally probable, choose the one that occurs first in the corpus.
If deterministic is false, draw the next word randomly from the appropriate distribution.
Use stupid backoff and no smoothing.
