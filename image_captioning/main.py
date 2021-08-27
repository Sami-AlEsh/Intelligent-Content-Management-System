from PIL import Image
from .__init__ import *
from .encoder import CNN_Encoder
from .decoder import RNN_Decoder
from .config import *

physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)


def load_inceptionV3():

    image_model = tf.keras.applications.InceptionV3(include_top=False, weights='imagenet')
    new_input = image_model.input
    hidden_layer = image_model.layers[-1].output

    return tf.keras.Model(new_input, hidden_layer)
    

def load_tokenizer():
    if os.path.isdir(m_path) and os.path.isfile(m_path + '/tokenizer.pickle'):
        with open(m_path + '/tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)
            tokenizer.word_index['<pad>'] = 0
            tokenizer.index_word[0] = '<pad>'
            print('Tokenizer is loaded!')
            return tokenizer
    else:
        raise Exception('Couldn\'t find Tokenizer file at ' + m_path + '/tokenizer.pickle')


def load_encoder_decoder():

    if os.path.isfile(f'{m_path}/encoder{enc_dec_num}.weights.index') and os.path.isfile(f'{m_path}/decoder{enc_dec_num}.weights.index'):
        encoder = CNN_Encoder(embedding_dim)
        decoder = RNN_Decoder(embedding_dim, units, vocab_size)
        encoder.load_weights(f'{m_path}/encoder{enc_dec_num}.weights')
        decoder.load_weights(f'{m_path}/decoder{enc_dec_num}.weights')
        print('encoder/decode are loaded!')
        return (encoder, decoder)
    else:
        raise Exception(f'encoder{enc_dec_num}/decoder{enc_dec_num} not found!')


def load_image(image: bytes):

    with open('./image.img', 'wb') as f:
        f.write(image)
    
    img = tf.io.read_file('./image.img')
    img = tf.image.decode_jpeg(img, channels=3)
    img = tf.image.resize(img, (299, 299))
    img = tf.keras.applications.inception_v3.preprocess_input(img)
    return img


def evaluate(image: bytes):
    tokenizer = load_tokenizer()
    encoder, decoder = load_encoder_decoder()
    inceptionV3 = load_inceptionV3()


    attention_plot = np.zeros((max_length, attention_features_shape))

    hidden = decoder.reset_state(batch_size=1)

    temp_input = tf.expand_dims(load_image(image), 0)
    img_tensor_val = inceptionV3(temp_input)
    img_tensor_val = tf.reshape(img_tensor_val, (img_tensor_val.shape[0],
                                                 -1,
                                                 img_tensor_val.shape[3]))

    features = encoder(img_tensor_val)

    dec_input = tf.expand_dims([tokenizer.word_index['<start>']], 0)
    result = []

    for i in range(max_length):
        predictions, hidden, attention_weights = decoder(dec_input,
                                                         features,
                                                         hidden)

        attention_plot[i] = tf.reshape(attention_weights, (-1, )).numpy()

        predicted_id = tf.random.categorical(predictions, 1)[0][0].numpy()
        result.append(tokenizer.index_word[predicted_id])

        if tokenizer.index_word[predicted_id] == '<end>':
            return result, attention_plot

        dec_input = tf.expand_dims([predicted_id], 0)

    attention_plot = attention_plot[:len(result), :]
    return result, attention_plot


def plot_attention(image, result, attention_plot):
    temp_image = np.array(Image.open(image))

    fig = plt.figure(figsize=(10, 10))

    len_result = len(result)
    for i in range(len_result):
        temp_att = np.resize(attention_plot[i], (8, 8))
        grid_size = max(np.ceil(len_result/2), 2)
        ax = fig.add_subplot(grid_size, grid_size, i+1)
        ax.set_title(result[i])
        img = ax.imshow(temp_image)
        ax.imshow(temp_att, cmap='gray', alpha=0.6, extent=img.get_extent())

    plt.tight_layout()
    plt.show()
