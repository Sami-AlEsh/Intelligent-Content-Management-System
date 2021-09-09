from camel_tools.tokenizers.morphological import MorphologicalTokenizer
from camel_tools.tokenizers.word import simple_word_tokenize
import nltk
import re
from .static_objects import get_mle_disambiguator



def clean(text):
    stopwords = nltk.corpus.stopwords.words('arabic')
    
    text = ' '.join([w for w in nltk.WhitespaceTokenizer().tokenize(text) if w not in stopwords])
    text = re.sub(r'[^\u0600-\u06ff\. ]', r' ', text)
    text = re.sub(r'\s+', r' ', text)
    
    return text

def morphological_tokenize(text, disambiguator=None):
    #     scheme = 'atbtok' || 'd3tok' || 'bwtok'
    morphologicalTokenizer = MorphologicalTokenizer(disambiguator=disambiguator, scheme='atbtok', split=True)
    tokens = [
        [w] if len(w) <= 3 else morphologicalTokenizer.tokenize([w])
        for w in simple_word_tokenize(text) if len(w) > 1
    ]
    tokens = [p for token in tokens for p in token if p.find('+') == -1]
    return tokens
