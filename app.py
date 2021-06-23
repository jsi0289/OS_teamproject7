# -*- coding: utf8 -*- 

from flask import Flask, jsonify, request
from flask import render_template
from news_naver import *
from cosine_similarity import *

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	return render_template('home.html',item = result_ranking, item1 = result_ranking1)

@app.route('/naver',methods=['POST'])
def naver():
	if request.method == 'POST':
		search(request.form['keyword'])
		return render_template('naver.html',item  = result_search, item1 = result_search1)

@app.route('/naver/result',methods=['POST'])
def result():
	if request.method == 'POST':
		return render_template('result.html', item  = result_search, item1 = result_search1 )

@app.route('/naver/result/cosine',methods=['POST'])
def cosine():
	if request.method == 'POST':
		return render_template('cosine.html',item  = result_cosine, item1 = result_cosine1 )

if __name__ == '__main__':
	app.run(debug=True)

	# nori 플러그인 설치
	# sudo bin/elasticsearch-plugin install analysis-nori
	# konply 모듈 설치
	# pip install konlpy
	# elasticsearch 설치 (JAVA_HOME 경로 설정 및 엘라스틱 서치 실행)
	# 홈페이지 참고
	# Beautifulsoup 설치
	# pip install beautifulsoup4 
	# scikit-learn 설치
	# pip install --upgrade scikit-learn

