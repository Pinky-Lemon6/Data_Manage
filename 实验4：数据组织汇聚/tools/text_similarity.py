# 本文件实现了各种可能用到的文本匹配技术
import Levenshtein

# 编辑距离（Levenshtein 距离）
def text_similarity_levenshtein(text1, text2):
    return 1 - Levenshtein.distance(text1, text2) / max(len(text1), len(text2))

# 海明距离
def text_similarity_hamming(text1, text2):
    if len(text1) != len(text2):
        raise ValueError("Strings must be of the same length")
    return sum(el1 != el2 for el1, el2 in zip(text1, text2)) / len(text1)

# Jaccard Distance
def text_similarity_jaccard(text1, text2):
    set1, set2 = set(text1.split()), set(text2.split())
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union

# Jaro-Winkler Distance
from jellyfish import jaro_winkler_similarity

def text_similarity_jw(text1, text2):
    return jaro_winkler_similarity(text1, text2)

# 余弦相似性
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def text_similarity_cosine(text1, text2):
    tfidf_vectorizer = TfidfVectorizer().fit_transform([text1, text2])
    cosine_sim = cosine_similarity(tfidf_vectorizer[0:1], tfidf_vectorizer[1:2])
    return cosine_sim[0][0]

# 欧氏距离
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import euclidean

def text_similarity_euclidean(text1, text2):
    tfidf_vectorizer = TfidfVectorizer().fit_transform([text1, text2]).toarray()
    return 1 / (1 + euclidean(tfidf_vectorizer[0], tfidf_vectorizer[1]))

# TF-IDF 实现文本语义相似性
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def text_similarity_tfidf(text1, text2):
    tfidf_vectorizer = TfidfVectorizer().fit_transform([text1, text2])
    cosine_sim = cosine_similarity(tfidf_vectorizer[0:1], tfidf_vectorizer[1:2])
    return cosine_sim[0][0]

# wordnet 词库判断(只能用于英文)
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 下载必要的NLTK资源
nltk.download('punkt')
nltk.download('stopwords')

def text_similarity_wordnet_tfidf(desc1, desc2):
    # Tokenization and stopwords removal
    stop_words = set(stopwords.words('english'))

    def preprocess_text(text):
        tokens = word_tokenize(text.lower())
        filtered_tokens = [token for token in tokens if token.isalnum() and token not in stop_words]
        return ' '.join(filtered_tokens)

    clean_desc1 = preprocess_text(desc1)
    clean_desc2 = preprocess_text(desc2)

    # Computing TF-IDF vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([clean_desc1, clean_desc2])

    # Calculating cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]

    return cosine_sim

from transformers import BertTokenizer, BertModel
import torch
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def text_similarity_bert(text1, text2):
    # 加载预训练的BERT模型和tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
    model = BertModel.from_pretrained('bert-base-chinese')

    # 对输入文本进行tokenization
    inputs1 = tokenizer(text1, return_tensors='pt')
    inputs2 = tokenizer(text2, return_tensors='pt')

    # 获取BERT的embedding
    with torch.no_grad():
        outputs1 = model(**inputs1)
        outputs2 = model(**inputs2)

    # 获取 [CLS] token 的embedding
    cls_embedding1 = outputs1.last_hidden_state[:, 0, :].numpy()
    cls_embedding2 = outputs2.last_hidden_state[:, 0, :].numpy()

    # 计算余弦相似性
    cosine_sim = cosine_similarity(cls_embedding1, cls_embedding2)
    return cosine_sim[0][0]

