from nltk.tokenize import word_tokenize
from MRC import setupDB
from MRC import queryDB
from newspaper import Article
from manapotion.content import __get_parsed_articles

def getArticles(mode):
    articleList = []

    if mode == "B": badArticleFile = open("badArticles.txt", 'r')
    else: badArticleFile = open("goodArticles.txt", 'r')

    for url in badArticleFile.readlines():
        articleList.append(url)
    return articleList

def extractFeatures(articles, featureVector):
    for article in articles:
        tokenDict = {}
        numSentences = numTokens = uniqueTokens = 0

        #Len
        totalLen = len(article.text) 

        #sentenceLen + TTR + MRC
        articleText = word_tokenize(article.text)
        for sentence in articleText.split('.')
            numSentences+= 1 
            sentence = sentence.split()
            numTokens += len(sentence)
            
            for word in sentence:
                if word not in tokenDict:
                    tokenDict[word] = None
                    uniqueTokens += 1

        TTR = float(uniqueTokens)/float(numTokens)
        avgLen = float(totalLen)/float(numSentences)

if __name__ == "__main__":
    badArticles = getArticles("B")
    goodArticles = getArticles("G")

    badArticles = __get_parsed_articles(badArticles)
    goodArticles = __get_parsed_articles(goodArticles)

    session = setupDB()
