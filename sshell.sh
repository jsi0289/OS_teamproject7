#!/bin/bash
#assuming that all the necessary files are in the OS_Teamproject directory

cd OS_Teamproject
echo "moving to OS_Teamproject directory"

#install essential modules

sudo apt-get install python3-pip
sudo pip install flask
sudo bin/elasticsearch-plugin install analysis-nori
sudo pip install konlpy
sudo pip install beautifulsoup4
sudo pip install --upgrade scikit-learn
echo "installing essential modules"

echo "running flask"
flask run --host=0.0.0.0

# news_naver.py is executed every 6 hours

HOUR=`date +%H`
AFTER=$HOUR+6

echo "news_naver.py is executed every 6 hours"
while [ $HOUR != $AFTER ]; do
   cd ..
   cd elasticsearch-7.6.2
   ./bin/elasticsearch -d
   cd ..
   cd OS_Teamproject
   python3 news_naver.py
   sleep 21600
   HOUR=`date +%H`
   AFTER=$HOUR+6
done
