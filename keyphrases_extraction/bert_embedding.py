import torch
from .static_objects import get_bert_model, get_bert_tokenizer


def embed_text_bert(text):
    bert_tokenizer = get_bert_tokenizer()
    bert_model = get_bert_model()
    
    text_ids = bert_tokenizer.encode(text, return_tensors='pt', max_length=512, truncation=True)
    # print(text)
    # print(text_ids.size())
    with torch.no_grad():
        out = bert_model(input_ids=text_ids)

    hidden_states = out[2]
    embedding = torch.mean(hidden_states[-1], dim=1)
    # print(embedding.shape)
    return embedding.numpy()