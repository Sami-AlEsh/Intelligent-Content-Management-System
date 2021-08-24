import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import itertools
from .bert_embedding import embed_text_bert
from .extract_ner_candidate import get_ner_candidates


def embed_rank_bert(text):
    doc_candidates = get_ner_candidates(text)
    doc_embedding = embed_text_bert(text).numpy()
    doc_candidate_embeddings = np.array([embed_text_bert(c).numpy() for c in doc_candidates]).squeeze()
    return (doc_candidates, doc_embedding, doc_candidate_embeddings)


def embed_rank_bert_cs(text, n=10): # cosine similarity
    doc_candidates, doc_embedding, doc_candidate_embeddings = embed_rank_bert(text)
    doc_keywords = consine_sims(doc_embedding, doc_candidate_embeddings, doc_candidates)
    n = min(n, len(doc_candidates))
    doc_keywords = sorted(doc_keywords, key= lambda tup: tup[1])
    for x in doc_keywords: print(x)
    return [tup[0] for tup in doc_keywords]


def embed_rank_bert_mmr(text, n=10): # maximum marginal relevance
    doc_candidates, doc_embedding, doc_candidate_embeddings = embed_rank_bert(text)
    doc_keywords_mmr = mmr(doc_embedding, doc_candidate_embeddings, doc_candidates, n, 0.8)
    return doc_keywords_mmr


def embed_rank_bert_mss(text, n=10): # max sum similarity
    doc_candidates, doc_embedding, doc_candidate_embeddings = embed_rank_bert(text)
    doc_keywords_mss = max_sum_sim(doc_embedding, doc_candidate_embeddings, doc_candidates, n, len(doc_candidates))
    return doc_keywords_mss


def embed_rank_doc2vec_cs(text, n=10): # cosine similarity
    pass


def embed_rank_doc2vec_mmr(text, n=10): # maximum marginal relevance
    pass


def embed_rank_doc2vec_mss(text, n=10): # max sum similarity
    pass



def consine_sims(text_embedding, candidate_embeddings, candidates):
    distances = cosine_similarity(text_embedding, candidate_embeddings)
    keywords_scores = [(candidates[index], distances[0][index]) for index in distances.argsort()[0][:]]
    return list(reversed(keywords_scores))


def max_sum_sim(text_embedding, candidate_embeddings, candidates, top_n, nr_candidates):

    top_n = min(top_n, len(candidates))

    # Calculate distances and extract keywords
    distances = cosine_similarity(text_embedding, candidate_embeddings)
    distances_candidates = cosine_similarity(candidate_embeddings, 
                                            candidate_embeddings)

    # Get top_n words as candidates based on cosine similarity
    words_idx = list(distances.argsort()[0][-nr_candidates:])
    words_vals = [candidates[index] for index in words_idx]
    distances_candidates = distances_candidates[np.ix_(words_idx, words_idx)]

    # Calculate the combination of words that are the least similar to each other
    min_sim = np.inf
    candidate = None
    for combination in itertools.combinations(range(len(words_idx)), top_n):
        sim = sum([distances_candidates[i][j] for i in combination for j in combination if i != j])
        if sim < min_sim:
            candidate = combination
            min_sim = sim

    return [words_vals[idx] for idx in candidate]


def mmr(text_embedding, candidate_embeddings, candidates, top_n, diversity):
    
    top_n = min(top_n, len(candidates))
    # Extract similarity within words, and between words and the document
    word_doc_similarity = cosine_similarity(candidate_embeddings, text_embedding)
    word_similarity = cosine_similarity(candidate_embeddings)
    
    # Initialize candidates and already choose best keyword/keyphras
    keywords_idx = [np.argmax(word_doc_similarity)]
    candidates_idx = [i for i in range(len(candidates)) if i != keywords_idx[0]]
    
    for _ in range(top_n - 1):
        # Extract similarities within candidates and
        # between candidates and selected keywords/phrases
        candidate_similarities = word_doc_similarity[candidates_idx, :]
        target_similarities = np.max(word_similarity[candidates_idx][:, keywords_idx], axis=1)
    
        # Calculate MMR
        mmr = (1-diversity) * candidate_similarities - diversity * target_similarities.reshape(-1, 1)
        mmr_idx = candidates_idx[np.argmax(mmr)]

        # Update keywords & candidates
        keywords_idx.append(mmr_idx)
        candidates_idx.remove(mmr_idx)

    return [candidates[idx] for idx in keywords_idx]