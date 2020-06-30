import pandas as pd
import numpy as np
import datetime
from pymongo import MongoClient
from time import time
from data_prep import *
from utils import *
import readability


def connect_database():
    client1 = MongoClient('54.169.171.51:27017',  # IP address of database
                          username='kapiReadOnly',  # Username
                          password='pl2oieAt9#tnWV!Yc0',  # Password
                          authSource='kapi',  # name of database
                          authMechanism='SCRAM-SHA-1')
    kapi = client1['kapi']
    return kapi


def get_post(users,start_date,end_date):

    kapi = connect_database()
    Anno = Annotator("/home/hieunpd/Documents/VnCoreNLP/VnCoreNLP-1.1.1.jar")
    annotator = Anno.get_annotator()
    # start_date = datetime.datetime(2020, 1, 20)
    # end_date = datetime.datetime(2020, 5, 17)
    cluster = kapi['posts'].find({'to_user': {'$in': users}, 'created_date': {'$gte': start_date, '$lt': end_date}},
                                 {'_id': 0, 'fid': 1, 'to_user': 1, 'created_date': 1,
                                  'comments_count': 1, 'shares_count': 1, 'likes_count': 1, 'message': 1})

    tb = pd.DataFrame(list(cluster))
    tb['total_int'] = [np.nansum([x, y, z]) for x, y, z in
                       zip(tb['comments_count'], tb['likes_count'], tb['shares_count'])]

    emoji_list = []
    hash_tag_list = []
    url_list = []
    clean_text_list = []
    readalitily_score = []
    for content in tb['message']:
        content = str(content)
        emoji = detect_emoji(content)
        hash_tag = detect_hashtag(content)
        url = detect_url(content)
        # clear free text
        clean_text = " ".join([str for str in content.split(
        ) if not any(i in str for i in emoji+hash_tag+url)])
        clean_text = TextPreprocess().preprocess(''.join(clean_text))
        emoji_list.append(emoji)
        hash_tag_list.append(hash_tag)
        url_list.append(url)
        readalitily_score.append(readability.score(clean_text,annotator))
        clean_text_list.append(clean_text)
    tb['emoji'] = emoji_list
    tb['hash_tag'] = hash_tag_list
    tb['url'] = url_list
    tb['text cleaned'] = clean_text_list
    tb['readability'] = readalitily_score

    #close vncoreNLP
    annotator.close()

    return tb
