#!/usr/bin/python3
#-*- coding: utf-8 -*-

import requests
import json
import pprint
from bs4 import BeautifulSoup
from konlpy.tag import Okt
from collections import Counter
from elasticsearch import Elasticsearch
from datetime import datetime

def get_tags(text, ranking): #특수문자 및 한 글자 제거
	spliter = Okt()
	nouns = spliter.nouns(text)
	nounsException = [word for word in nouns if not word in exception]
	nouns_not1 = [n for n in nounsException if len(n) > 1]

	count = Counter(nouns_not1)
	return_list = []

	for n, c in count.most_common(ranking):
		temp = {'tag': n, 'count': c}
		return_list.append(temp)

	return return_list

def crawler_naver(category, sid2, sid1, date): #웹 크롤링 후 결과를 JSON에 저장
	list = []
	data = []
	page_num = 0
	count_news = 0
	page = 1
	num = 0

	while True:
		url = 'https://news.naver.com/main/list.nhn?mode=LS2D&sid2=' + str(sid2) + '&sid1=' + str(sid1) + '&mid=shm&date=' + str(date) + '&page=' + str(page)
		res = requests.get(url, headers=headers_naver).text
		soup = BeautifulSoup(res, 'html.parser')      
        	
		title = soup.select('.type06_headline > li > dl > dt > a')
		title1 = soup.select('.type06 > li > dl > dt > a')

		last_page = page_num
		page_num = soup.select('.paging > strong')
		
		if last_page == page_num:
			break
		
		for i in range(len(title)):
			if len(title[i].text) < 3:
				continue			
			count_news += 1
			list.append(title[i].text)
			data.append({
                '1.Platform': "네이버",
                '2.Category': category + '뉴스',
                '3.Title': title[i].text,               
                '4.Url': title[i]['href'],
                '5.Date': date,
                '6.Number': count_news
            })   
		for i in range(len(title1)):
			if len(title1[i].text) < 3:
				continue
			count_news += 1
			list.append(title1[i].text)
			data.append({
                '1.Platform': "네이버",
                '2.Category': category + '뉴스',
                '3.Title': title1[i].text,               
                '4.Url': title1[i]['href'],
                '5.Date': date,
                '6.Number': count_news
            })   
		page += 1
	tags = get_tags(' '.join(list), ranking)

	for tag in tags:
		num += 1
		noun = tag['tag']
		count = tag['count']
		print(f'{num}. ' + '{} {}'.format(noun, count))

	with open('Naver_news_Data[' + category + '].json', 'w', encoding='utf-8') as f:
		json.dump(data, f, indent='\t', ensure_ascii=False)
		
	print('총 페이지 : ' + str(page - 1))
 
def crawler_daum(category, date): #웹 크롤링 후 결과를 JSON에 저장
    list = []
    data = []
    count_news = 10000
    page = 1
    num = 0   

    while True:
        url = 'https://news.daum.net/breakingnews/' + category + \
            '?page=' + str(page) + '&regDate=' + str(date)
        res = requests.get(url, headers=headers_daum).text
        soup = BeautifulSoup(res, 'html.parser')

        title = soup.select('ul > li > div > strong > a')
        lastpage_check = soup.select('p')

        if len(lastpage_check) == 1:
            break	

        for i in range(len(title)):           
            count_news += 1
            data.append({
                '1.Platform': "다음",
                '2.Category': category + '뉴스',
                '3.Title': title[i].text,               
                '4.Url': title[i]['href'],
                '5.Date': date,
                '6.Number': count_news
            })
            list.append(title[i].text)

        page += 1

    tags = get_tags(' '.join(list), ranking)

    for tag in tags:
        num += 1
        noun = tag['tag']
        count = tag['count']
        print(f'{num}.' + '{} {}'.format(noun, count))

    with open('Daum_news_Data[' + category + '].json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent='\t', ensure_ascii=False)

    print('총 페이지 : ' + str(page - 1))

def check_index(): #Index 조회
   return es.indices.get_alias("*")

def create_index(mapping_json):	#Index 생성
	if not es.indices.exists(index=index):
		with open(mapping_json, 'r', encoding='utf-8') as f:
			mapping = json.load(f)
		res = es.indices.create(index=index, body = mapping)
		
		return res

def delete_index(): #Index 삭제
	if es.indices.exists(index=index):
		return es.indices.delete(index=index)

def insert(doc_json): #DB에 JSON 내용을 저장
	with open(doc_json, 'r', encoding='utf-8') as f:
		json_data = json.load(f)
	
	for i in json_data:
		res = es.index(index=index, body=i)
	
	return res

def search(keyword=None): #DB에 저장된 기사를 제목으로 검색
	body = {
		"from" : 0,
		"size" : 15,
		"query": {
			"match": {
				"3.Title" : keyword				
				}
		}
	}
	res = es.search(index=index, body=body, request_timeout= 30)

	return res

if __name__ == '__main__':
	headers_naver = { "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
	headers_daum = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
	exception = "동영상 기사 포토 사진 \r \t \n"
	url_elastic = '127.0.0.1'
	port = '9200'
	index = 'news'
	mapping_json = 'mapping_nori.json'
	naver_categories = ['society', 'politics', 'economic', 'foreign', 'culture', 'science', 'IT']
	daum_categories = ['society', 'politics', 'economic', 'foreign', 'culture', 'entertain', 'digital']
	naver_sid1 = [102, 100, 101, 104, 103, 105, 105]
	naver_sid2 = [257, 269, 263, 322, 245, 228 ,230]
	ranking = 10
	date = 20210606
	
	es = Elasticsearch(f'{url_elastic}:{port}')

	# ####### 네이버뉴스와 다음뉴스 크롤링 및 단어 빈도수 출력과 기사들 JSON에 저장
	# print("===NAVER NWES===")
	# for i in range(0,7):
	# 	print('\n'+ naver_categories[i] + ' 뉴스')
	# 	crawler_naver(naver_categories[i], naver_sid1[i], naver_sid2[i], date)
	
	# print("\n===DAUM NWES===")
	# for category in daum_categories:
	# 	print('\n'+ category + ' 뉴스')
	# 	crawler_daum(category, date)

	# ###### index 삭제 ( Index 초기화 할때 아니면 항상 주석 처리 )
	# delete_index()
	# ####### Index 생성 
	# create_index(mapping_json)

	# ###### 기사를 저장한 JSON 파일을 DB에 저장
	# for category in naver_categories:
	# 	insert('Naver_news_Data[' + category + '].json')

	# for category in daum_categories:
	# 	insert('Daum_news_Data[' + category + '].json')

	###### DB에 저장된 기사들 제목을 검색
	# r = search("바보")
	# for doc in r['hits']['hits']:
	# 	pprint.pprint(doc['_source'])
	#END

	# 실행 순서 (실행 할 번호를 제외한 나머지는 항상 나머지 주석처리)
	#1.네이버뉴스와 다음뉴스 크롤링 및 단어 빈도수 출력과 기사들 JSON에 저장
	#2.index 삭제 및 생성
	#3.기사를 저장한 JSON 파일을 DB에 저장
	#4.DB에 저장된 기사들 제목을 검색