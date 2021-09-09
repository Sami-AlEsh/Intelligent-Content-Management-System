from .topic_rank import topic_rank
from .position_rank import position_rank
from .embed_rank import embed_rank
from functools import partial


def extract_keyphrases(text, n=10, method='bert_mmr'):

    options = {
        'bert_cs': partial(embed_rank, method='bert_cs'),
        'bert_mss': partial(embed_rank, method='bert_mss'),
        'bert_mmr': partial(embed_rank, method='bert_mmr'),
        'doc2vec_cs': partial(embed_rank, method='doc2vec_cs'),
        'doc2vec_mss': partial(embed_rank, method='doc2vec_mss'),
        'doc2vec_mmr': partial(embed_rank, method='doc2vec_mmr'),
        'topic_rank': topic_rank,
        'position_rank': position_rank,
    }

    return options[method](text=text, n=n)