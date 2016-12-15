#**MANA: My Adaptive News Aggregator**

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

download scikit-learn
```
pip install -U scikit-learn
```
if missing numPy and sciPy
```
pip install -U scikit-learn[alldeps]
```

#Messenger Bot Set Up
```
1). Create a working endpoint that can return a 200 response code and can verify your bot with Facebook
2). Create a Facebook page for your bot
3). Create and register a Facebook App for your Bot
```
#Running The Code Locally
local_app.py will simulate our processes without the Facebook Messenger Bot interface. To run local_app.py, please clone our directory, download all the dependencies, and run
```
python3 local_app.py
```
Once you enter your name, you will be prompted with some initial articles. When MANA asks for feedback, your response should include the numbers corresponding to the articles you were most intersted in. To continue using MANA, respond "yes" when she asks if you would like to continue using her. Enjoy!

