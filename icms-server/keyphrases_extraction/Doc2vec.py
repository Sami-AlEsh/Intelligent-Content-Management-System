import gensim
from gensim import utils
from gensim.models import Word2Vec, Doc2Vec
from gensim.models.doc2vec import TaggedDocument
import json
import re
import subprocess
import os

import logging
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)


CHARS_MAP = [
  (["أ","إ","آ"], 'ا'),
  (['ة'], 'ه'),
  (['?', '؟'], ' ؟ '),
  (['!'], ' ! '),
  (['-', '_', 'ـ', '،', ','], ' ')
]


def preprocessArDoc(text, letters_map=CHARS_MAP):
  text = re.sub(r'[^\u0600-\u06ff1-9!?\. ]', r' ', text)
  # remove tashkeel
  text = re.sub(r'[\u0617-\u061A\u064B-\u0652]',r'', text)
  for m in letters_map:
    for l in m[0]:
      text = text.replace(l, m[1])
  text = re.sub(r'\s+', r' ', text)
  return text

def prepareData():
    try:
        import gdown
    except:
        subprocess.run('pip install gdown')
        import gdown
    
    url = 'https://drive.google.com/u/1/uc?id=1XuOdnjwBeSC7nMckFjY0b9IHxBdMvR_1'
    gdown.download(url, 'wiki_00', quiet=False)

# https://radimrehurek.com/gensim/models/doc2vec.html#gensim.models.doc2vec.Doc2Vec
def trainD2VModel(tagged_docs, vec_size=300, window=5, min_count=10, epochs=40,
                  **kwargs):
  
  model = Doc2Vec(tagged_docs, vector_size=vec_size, window=window, 
                  epochs=epochs, min_count=min_count)
  return model

class WikiDocs:
  def __init__(self, path, max_docs=1_000_000_000, preprocess_func=None):
    self.path = path
    self.max_docs = max_docs
    if preprocess_func is None:
      self.preprocess_func = lambda x: x
    self.preprocess_func = preprocess_func

  def __iter__(self):
    with open(self.path, 'r', encoding='utf8') as f:
      for i, doc in enumerate(f):
        if i > self.max_docs:
          return
        j_doc = json.loads(doc)
        text = self.preprocess_func(j_doc['text'])
        words = utils.simple_preprocess(text)
        yield TaggedDocument(words, [i])



def main():
    prepareData()
    tagged_docs = WikiDocs(path='./wiki_00', preprocess_func=preprocessArDoc)
    model = trainD2VModel(tagged_docs, epochs=50)
    name = 'wiki_full_50ep.bin'
    
    if os.path.exists('./outs'):
        print('save model ...')
    else:
        print('create output folder ...')
        os.mkdir('./outs')
        print('save model ...')
    
    model.save(f'./outs/{name}')


if __name__ == '__main__':
    main()