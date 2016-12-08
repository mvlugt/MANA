from nltk.tokenize import word_tokenize
from sklearn.svm import SVC
from sklearn.externals import joblib
from newspaper import Article

from .MRC import setupDB
from .MRC import queryDB
import re
from sklearn.tree import DecisionTreeClassifier


def filterArticles(article_urls):
    classifier = joblib.load("quality.pkl")
    dummy = open("dummy.txt", "w")
    dummy_sesion = setupDB()
    articles = parseUrls(article_urls)
    features = extractFeatures(articles, dummy_sesion, dummy)
    quality_predictions = classifier.predict(features)
    to_return = []
    for index, prediction in enumerate(quality_predictions):
        if prediction:
            to_return.append(articles[index])
    return to_return


def getArticles(mode):
    articleList = []

    if mode == "B": articleFile = open("badArticles.txt", 'r')
    else: articleFile = open("goodArticles.txt", 'r')

    for url in articleFile.readlines():
        articleList.append(url)
    return articleList

def parseUrls(articleUrls):
    parsedArticles = []
    for url in articleUrls:
        if url.endswith('\n'): url = url[:-1]
        article = Article(url)

        article.download()
        if article.html == "":
            print(url)
            continue

        article.parse()
        if article.text == "":
            print (url)
            continue
        parsedArticles.append(article)
    return parsedArticles


def extractFeatures(articles, session, out):
    featureVector = []
    i = 0
    for article in articles:
        i += 1
        print("extracting features for " + str(i))
        tokenDict = {}
        numSentences = numTokens = uniqueTokens = mrcWords = fam = conc = imag = 0

        articleText = word_tokenize(article.text)
        for word in articleText:
            #get len stuff
            numTokens += 1
            if word == ".": numSentences += 1

            else:
                #get mrc stuff
                mrcList = queryDB(word, session)
                if len(mrcList) > 0:
                    mrcWords += 1
                    fam += mrcList[0]
                    conc += mrcList[1]
                    imag += mrcList[2]
                #get TTR stuff
                if word not in tokenDict:
                    tokenDict[word] = None
                    uniqueTokens += 1

        fam = float(fam)/float(mrcWords)
        conc = float(conc)/float(mrcWords)
        imag = float(imag)/float(mrcWords)
        TTR = float(uniqueTokens)/float(numTokens)
        length = len(article.text)
        avgLen = float(length)/float(numSentences)
        featureVector.append([length, avgLen, TTR, fam, conc, imag])
        out.write(str([length, avgLen, TTR, fam, conc, imag]))
        out.write('\n')
    return featureVector

def trainClassifier():
    #get articles
    badArticles = getArticles("B")
    goodArticles = getArticles("G")

    #parse articles
    badArticles = parseUrls(badArticles)
    goodArticles = parseUrls(goodArticles)
    
    #get features
    session = setupDB()
    solutionVector = ([0]*100 + [1]*100) 
    bOut = open("badFeatures.txt", "w")
    gOut = open("goodFeatures.txt", "w")

    featureVector = (extractFeatures(badArticles, session, bOut) + \
            extractFeatures(goodArticles, session, gOut))

    classifier = DecisionTreeClassifier()
    #uncomment below for 5 fold, if doing this testing you need to balance feature vector above
    """
    for i in range(0, 5):
        print ("classifying " + str(i))
        lower = i*40
        upper = lower + 40
        
        classifier.fit(featureVector[:lower] + featureVector[upper:], \
                solutionVector[:lower] + solutionVector[upper:])

        predictList = classifier.predict(featureVector[lower:upper])

        correct = 0
        j = lower
        for item in predictList:
            if item  == solutionVector[j]:
                correct +=1
            j += 1
        print (correct)
        """

    #save classifier trained on all training data
    classifier.fit(featureVector, solutionVector)
    joblib.dump(classifier, "quality.pkl")

if __name__ == "__main__":
    print("meow")
