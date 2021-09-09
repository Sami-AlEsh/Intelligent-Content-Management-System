import pke
import nltk
import string



def topic_rank(text, n=10, threshold=0.8):
    pos = {'NOUN', 'ADJ', 'PRON'}
    stoplist = list(string.punctuation)
    stoplist += nltk.corpus.stopwords.words('arabic')

    extractor = pke.unsupervised.TopicRank()
    extractor.load_document(input=text, language='ar')
    extractor.candidate_selection(pos=pos, stoplist=stoplist)
    extractor.candidate_weighting(threshold=threshold)
    keyphrases = extractor.get_n_best(n=n, redundancy_removal=False)

    return [tup[0] for tup in keyphrases]