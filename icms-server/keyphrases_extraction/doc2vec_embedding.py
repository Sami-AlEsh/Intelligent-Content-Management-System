from keyphrases_extraction.static_objects import get_doc2vec_model
from gensim import utils
from .utils import timeit

@timeit
def embed_text_doc2vec(text, doc2vec_model=None):
    print(text)
    print(doc2vec_model)
    print('embed_text_doc2vec:', len(text))
    # doc2vec_model = get_doc2vec_model()
    embedding = doc2vec_model.infer_vector(utils.simple_preprocess(text))
    # print(embedding.shape)
    return embedding.reshape(1, -1)