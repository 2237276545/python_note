# https://github.com/spro/char-rnn.pytorch
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
import unidecode
import string
import random
import time
import math
import torch
from torch.autograd import Variable

USE_CUDA = False

# Reading and un-unicode-encoding data

all_characters = string.printable
n_characters = len(all_characters)
SOS = n_characters
EOS = n_characters + 1
n_characters += 2

def read_file(filename):
    file = unidecode.unidecode(open(filename,encoding='utf-8').read())
    return file, len(file)

# Turning a string into a tensor
# 将字符串变成张量
def char_tensor(string):
    size = len(string) + 1
    tensor = torch.zeros(size).long()
    for c in range(len(string)):
        tensor[c] = all_characters.index(string[c])
    tensor[-1] = EOS
    tensor = Variable(tensor)
    if USE_CUDA:
        tensor = tensor.cuda()
    return tensor

# Turn a tensor into a string

def index_to_char(top_i):
    if top_i == EOS:
        return '$'
    elif top_i == SOS:
        return '^'
    else:
        return all_characters[top_i]

def tensor_to_string(t):
    s = ''
    for i in range(t.size(0)):
        ti = t[i]
        top_k = ti.data.topk(1)
        top_i = top_k[1][0]
        s += index_to_char(top_i)
        if top_i == EOS: break
    return s

def longtensor_to_string(t):
    s = ''
    for i in range(t.size(0)):
        top_i = t.data[i]
        s += index_to_char(top_i)
    return s

# Readable time elapsed

def time_since(since):
    s = time.time() - since
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)

def tf_idf(data,law_data,k):
    with open('data/tyc.txt', 'r', encoding='utf-8') as f:
        tyc_data = f.readlines()
    sent_words = [" ".join(jieba.cut(sent0)) for sent0 in data]
    tfidf_model = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b", stop_words=tyc_data).fit(law_data)
    vocab = tfidf_model.vocabulary_
    law_list = tfidf_model.transform(sent_words).toarray()
    return law_list,len(vocab)