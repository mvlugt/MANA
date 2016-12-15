#**MANA: My Adaptive News Aggregator**

MANA is an adaptive news aggregator built for the University of Michigan, EECS 498 - Natural Lanuage Processing. It takes in news articles and serves you back articles that you would want to read! It also learns from what you like to try and serve you better news over time.

##**System Overview**

####1) Quality filter

The code for the quality filter can be found in QA/quality.py. The code build and trains the classifier that we use for filter quality articles. Please do not run this file as it will ruin the uploaded classifier!

####2) Relevence Ranking

The relevence ranking code can be found in manapotion/content.py. This file exposes methods to get relevence rankings for a list of news articles. It depends on db.py and user.py.


####3) Facebook messenger

The chatbot code can be found in app.py and is a Flask application. This code uses the classifer provided from QA/quality.py and uses the methods exposed in manapotion/content.py. It receives and sends messages to the Facebook webhooks to communicate with a user. 


##*NewsPaper Setup - for OSX *
Using Homebrew or Macports

```
$ brew install libxml2 libxslt
$ brew install libtiff libjpeg webp little-cms2
$ pip3 install newspaper3k
$ curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python3
```

##**Mongo setup**

Install MongoDB for OSX:
```
brew update
brew install mongodb
```

Install PyMongo: 
```
pip install pymongo
```

#WRC setup
download sqlAlchemy
```
http://www.sqlalchemy.org/download.html
```

#Messenger Bot Set Up
1). Create a working endpoint that can return a 200 response code and can verify your bot with Facebook
2). Create a Facebook page for your bot
3). Create and register a Facebook App for your Bot

