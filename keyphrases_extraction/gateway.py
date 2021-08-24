from .topic_rank import topic_rank
from .position_rank import position_rank
from .embed_rank import embed_rank_bert_cs, embed_rank_bert_mss, embed_rank_bert_mmr
from .embed_rank import embed_rank_doc2vec_cs, embed_rank_doc2vec_mss, embed_rank_doc2vec_mmr



def extract_keyphrases(text, n=10, method='bert_mmr'):

    options = {
        'bert_cs': embed_rank_bert_cs,
        'bert_mss': embed_rank_bert_mss,
        'bert_mmr': embed_rank_bert_mmr,
        'doc2vec_cs': embed_rank_doc2vec_cs,
        'doc2vec_mss': embed_rank_doc2vec_mss,
        'doc2vec_mmr': embed_rank_doc2vec_mmr,
        'topic_rank': topic_rank,
        'position_rank': position_rank,
    }

    return options[method](text=text, n=n)