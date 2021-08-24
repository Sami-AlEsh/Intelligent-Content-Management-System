import pke
import nltk
import string

def position_rank(text, n=10, window=5):

    pos = {'NOUN', 'ADJ', 'PRON'}
    stoplist = list(string.punctuation)
    stoplist += nltk.corpus.stopwords.words('arabic')
    grammar = "NP: {<NOUN|PROPN>+<ADJ>*}"

    extractor = pke.unsupervised.PositionRank()
    extractor.load_document(input=text,language='ar',normalization=None)
    extractor.candidate_selection(grammar=grammar, maximum_word_number=4)
    extractor.candidate_weighting(window=window,pos=pos)
    keyphrases = extractor.get_n_best(n=n, redundancy_removal=True)

    return [tup[0] for tup in keyphrases]