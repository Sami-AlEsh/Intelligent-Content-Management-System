import os

max_length = 49  # maximum length of any caption in MS-COCO
m_path = os.path.abspath('./image_captioning/models')
top_k = 10000
embedding_dim = 256
units = 512
vocab_size = top_k + 1
# Shape of the vector extracted from InceptionV3 is (64, 2048)
attention_features_shape = 64
enc_dec_num = '34'