import pandas as pd
import regex as re
import utils
from vncorenlp import VnCoreNLP
import emoji


# file_vncore = '/home/hieunpd/Documents/VnCoreNLP/VnCoreNLP-1.1.1.jar'
# annotator = VnCoreNLP(file_vncore, annotators="wseg,pos,ner,parse", max_heap_size='-Xmx2g')

EMAIL = re.compile(r"([\w0-9_\.-]+)(@)([\d\w\.-]+)(\.)([\w\.]{2,6})")
URL = re.compile(r"https?:\/\/(?!.*:\/\/)\S+")
PHONE = re.compile(r"(09|01[2|6|8|9])+([0-9]{8})\b")
MENTION = re.compile(r"@.+?:")
NUMBER = re.compile(r"\d+.?\d*")
DATETIME = '\d{1,2}\s?[/-]\s?\d{1,2}\s?[/-]\s?\d{4}'

RE_HTML_TAG = re.compile(r'<[^>]+>')
RE_CLEAR_1 = re.compile("[^_<>\s\p{Latin}]")
RE_CLEAR_2 = re.compile("__+")
RE_CLEAR_3 = re.compile("\s+")



class TextPreprocess:
    @staticmethod
    def replace_common_token(txt):
        txt = re.sub(EMAIL, ' ', txt)
        txt = re.sub(URL, ' ', txt)
        txt = re.sub(MENTION, ' ', txt)
        txt = re.sub(DATETIME, ' ', txt)
        txt = re.sub(NUMBER, ' ', txt)
        return txt

    @staticmethod
    def remove_html_tag(txt):
        return re.sub(RE_HTML_TAG, ' ', txt)

    def preprocess(self, txt, tokenize=True):
        txt = self.remove_html_tag(txt)
        txt = re.sub('&.{3,4};', ' ', txt)
        txt = utils.convertwindown1525toutf8(txt)
        # print(txt)
        # if tokenize:
        #     txt = word_tokenize(txt)
        txt = txt.lower()
        txt = self.replace_common_token(txt)
        # txt = self.remove_emoji(txt)
        txt = re.sub(RE_CLEAR_1, ' ', txt)
        txt = re.sub(RE_CLEAR_2, ' ', txt)
        txt = re.sub(RE_CLEAR_3, ' ', txt)
        txt = utils.chuan_hoa_dau_cau_tieng_viet(txt)
        return txt.strip()

def detect_emoji(text):
    allchars = [str for str in text]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    return emoji_list

def detect_hashtag(txt):
    hash_tag = re.findall(r"#(\w+)",txt)
    return hash_tag

def detect_url(txt):
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', txt)
    return url

def spell_check(txt):
    vietnamese_dic = pd.read_csv("./Dataset/Vietnamese.csv")
    spell_list = []
    for word in txt:
        if word not in vietnamese_dic:
            spell_list.append(word)
    return spell_list

def toxic_word_check(txt):
    toxic_dic = pd.read_csv("./Dataset/bad_word.csv")
    toxic_word_list = []
    for word in txt:
        if word not in toxic_dic:
            toxic_word_list.append(word)
    return toxic_word_list
    

if __name__ == "__main__":
    txt = 'Bảo dùng "dsd" là mê mà lại 🥰 👍 😡 #best #dssad https://www.messenger.com/t/sudohainguyen'
    test,emoji = detect_emoji(txt)
    print(test)
    print(emoji)
    hash_tag = detect_hashtag(txt)
    print(hash_tag)
    url = detect_url(txt)
    print(url)