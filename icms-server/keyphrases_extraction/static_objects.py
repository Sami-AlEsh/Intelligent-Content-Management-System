import stanza
from transformers import BertModel, BertTokenizer
from camel_tools.disambig.mle import MLEDisambiguator
from gensim.models import Doc2Vec
from .utils import timeit


# nlp = stanza.Pipeline('ar')
# mle_disambiguator = MLEDisambiguator.pretrained('calima-msa-r13') # Take long time
# bert_tokenizer = BertTokenizer.from_pretrained('./keyphrases_extraction/models/bert-large-arabertv2')
# bert_model = BertModel.from_pretrained('./keyphrases_extraction/models/bert-large-arabertv2', output_hidden_states=True)

@timeit
def get_nlp_pipline():
    # return nlp
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.')
    return stanza.Pipeline('ar', processors='tokenize,ner', use_gpu=True)

@timeit
def get_bert_model():
    # return bert_model
    return BertModel.from_pretrained('./keyphrases_extraction/models/bert-base-arabic', output_hidden_states=True)

@timeit
def get_bert_tokenizer():
    # return bert_tokenizer
    return BertTokenizer.from_pretrained('./keyphrases_extraction/models/bert-base-arabic')

@timeit
def get_mle_disambiguator():
    # return mle_disambiguator
    return MLEDisambiguator.pretrained('calima-msa-r13') # Take long time

@timeit
def get_doc2vec_model():
    return Doc2Vec.load('./keyphrases_extraction/models/doc2vec/wiki_full_50ep.bin')