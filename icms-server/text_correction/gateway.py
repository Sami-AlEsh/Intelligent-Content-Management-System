import requests
import multiprocessing
from requests_toolbelt.multipart.encoder import MultipartEncoder

def get_word_suggestions(word):
    response = requests.post(
        'https://api.arabicspellchecker.com/get_word_suggestions', 
        json= {'word': word },
        headers= {
            'token': 'OfaUFFcyjIQObEPSkl7sxCroM1uvrOO2',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            },
    )
   
    return response.json()


def get_incorrect_words(text):

    multipart_data = MultipartEncoder(
    fields={
            'text': text, 
           }
    )

    response = requests.post(
        'https://api.arabicspellchecker.com/get_incorrect_words', 
        data=multipart_data,
        headers= {
            'token': 'OfaUFFcyjIQObEPSkl7sxCroM1uvrOO2',
            'Content-Type': multipart_data.content_type,
            'Accept': '*/*',
            },
    )
    res = response.json()
    if res['outcome'] == 'success':
        return res['data']
    
    return []


def correct_text(text):
    wrong_words = get_incorrect_words(text)
    pool = multiprocessing.Pool(4)
    sugg = pool.map(get_word_suggestions, wrong_words)
    pool.close()
    pool.join()


    res = []

    for i in range(len(wrong_words)):
        res.append({
            'word': wrong_words[i],
            'correction': sugg[i]
        })

    return res
    
# if __name__ == '__main__':

#     text = u'بعد تأجيل جولة مفاوضات ترسيم الحدود.. عون: لبنان متمسسك بسيادته علن أررضه ومياهه'

#     res = get_incorrect_words(text)

#     pool = multiprocessing.Pool(4)
#     sugg = pool.map(get_word_suggestions, res)
#     pool.close()
#     pool.join()

#     # sugg = [get_word_suggestions(w) for w in res]

#     print(res)
#     print(sugg)

# print(run(u'العباسيية'))
# print(run(u'قمو'))
# print(run(u'اطقال'))