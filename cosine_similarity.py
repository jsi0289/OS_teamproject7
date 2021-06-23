#!/usr/bin/python3
#-*- coding: utf-8 -*-

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from elasticsearch import Elasticsearch
from konlpy.tag import Okt

url_elastic = '127.0.0.1'
port = '9200'
index = 'news'
body1 = {
    "from": 0,
    "size":10,
    "query": {
        "match_all": {			
            }
    }
}

es = Elasticsearch(f'{url_elastic}:{port}')    

result_cosine=[]
result_cosine1 = []
tfidf_vectorizer = TfidfVectorizer()
okt = Okt()
cosine_sim=[]
contents = []     
doc_list={}
i = 0

##### Elastic search DB에서 doc 불러오기    
doc1 = es.search(index=index, body=body1, request_timeout= 30)
max = doc1['hits']['total']['value']
body = {"from":0,"size":max,"query":{"match_all":{}}}
doc = es.search(index=index, body=body, request_timeout= 30)


##### 쓸모 없는 단어 제거 및 자연어 처리
stop_words = ['동영상', '동영상기사', '연합뉴스', '이제', '뉴스', '기자', '날씨', '오늘', '\n', '\t']

for doc in doc['hits']['hits']:
    doc_list[i] = doc['_source']
    i = i+1

for i in doc_list:
    doc_list[i]['7.Content'] = okt.nouns(doc_list[i]['7.Content'])
    doc_list[i]['7.Content'] = list(set(doc_list[i]['7.Content']))
    doc_list[i]['7.Content'] = list(filter(lambda x: len(x) > 1 and x not in stop_words, doc_list[i]['7.Content']))
    doc_list[i]['7.Content'] = ' '.join(doc_list[i]['7.Content'])
    contents.append(doc_list[i]['7.Content'])

##### 문서 tfidf 와 cosine 유사도 분석
feature_vect_simple = tfidf_vectorizer.fit_transform(contents)

num = 15 #선택 기사 번호
similarity_simple_pair = cosine_similarity(feature_vect_simple[num],feature_vect_simple)

for j in range(0,max):
    cosine_sim.append(similarity_simple_pair[0][j])

cosine_sim_sorted = sorted(cosine_sim, reverse=True)
check = cosine_sim.index(cosine_sim_sorted[0])

for k in range(1,11):
    check = cosine_sim.index(cosine_sim_sorted[k])
    result_cosine.append(doc_list[check]['3.Title'])
    result_cosine1.append(doc_list[check]['4.Url'])

#END

# nori 플러그인 설치
# sudo bin/elasticsearch-plugin install analysis-nori
# konply 모듈 설치
# pip install konlpy
# elasticsearch 설치
# 홈페이지 참고
# Beautifulsoup 설치
# pip install beautifulsoup4 
# scikit-learn 설치
# pip install --upgrade scikit-learn
