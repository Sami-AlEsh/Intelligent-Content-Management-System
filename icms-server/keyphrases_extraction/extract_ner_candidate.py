from camel_tools.ner import NERecognizer
from camel_tools.tagger.default import DefaultTagger
import stanza
from itertools import chain
import nltk
import multiprocessing
from fuzzywuzzy import fuzz
from .clean_text import clean, morphological_tokenize
from .static_objects import get_nlp_pipline, get_mle_disambiguator
from .utils import timeit


@timeit
def ner_recognize(sentences_tokens):
    # print(sentences_tokens)
    ner = NERecognizer.pretrained()
    labels = ner.predict(sentences_tokens)
    text_ner = list(zip(list(chain(*sentences_tokens)), list(chain(*labels))))
    return text_ner

@timeit
def filter_entities_types(text_ner):
    _candidates = [t for t in text_ner if t[1] != 'O']
    i=0

    candidates = []
    candidates_len = len(_candidates)
    while i < candidates_len:
        if _candidates[i][1].startswith('B-'):
            end, temp = i, [_candidates[i][0]]
            for j in range( i+1, candidates_len):
                if _candidates[j][1].startswith('I-'):
                    end = j
                    temp.append(_candidates[j][0])
                else:
                    break
      
            candidates.append(' '.join(temp))
            i += (end - i + 1)
        else:
            candidates.append(_candidates[i][0])
            i += 1
    

    candidates = list(set(candidates))
    return candidates

@timeit
def get_ner_candidates_ct(text): # camel tools
    return []
    cleaned_sents = [clean(sent) for sent in nltk.sent_tokenize(text)]
    mleDisambiguator = get_mle_disambiguator()
    sents_tokens = [morphological_tokenize(sent, mleDisambiguator) for sent in cleaned_sents]
    tokens_ne = ner_recognize(sents_tokens)
    ner_candidates = filter_entities_types(tokens_ne)
    return ner_candidates

@timeit
def get_ner_candidates_st(text): # stanza
  nlp = get_nlp_pipline()
  doc = nlp(text)
  candidates = set(map(lambda x: x.text, doc.entities))
  return list(candidates)

@timeit
def get_ner_candidates_ct_(text, return_dict):
  try:
    res = get_ner_candidates_ct(text)
    return_dict['candidates_ct'] = res
  except:
    return_dict['candidates_ct'] = []

@timeit
def get_ner_candidates_st_(text, return_dict):
  res = get_ner_candidates_st(text)
  return_dict['candidates_st'] = res

@timeit
def get_ner_candidates(text):
  manager = multiprocessing.Manager()
  return_dict = manager.dict()

  p1 = multiprocessing.Process(target=get_ner_candidates_ct_, args=(text, return_dict))
  p2 = multiprocessing.Process(target=get_ner_candidates_st_, args=(text, return_dict))

  p1.start()
  p2.start()

  p1.join()
  p2.join()

  candidates = list(set([*return_dict['candidates_ct'], *return_dict['candidates_st']]))

  to_remove = list()

  for i in range(len(candidates)):
    for j in range(i+1, len(candidates)):
      
      short,long = sorted([candidates[i], candidates[j]], key=len)
      
      # if short in long:
      #   print(short, long)
      #   to_remove.append(short)
      
      ratio = fuzz.ratio(short, long)
      if(ratio > 75):
        # print(short, long, ratio)
        to_remove.append(short)

  return [c for c in candidates if c not in to_remove]
