from nltk.tokenize import word_tokenize
from sklearn.svm import SVC
from newspaper import Article

from MRC import setupDB
from MRC import queryDB
from manapotion.content import __get_parsed_articles


def getArticles(mode):
    articleList = []

    if mode == "B": badArticleFile = open("badArticles.txt", 'r')
    else: badArticleFile = open("goodArticles.txt", 'r')

    for url in badArticleFile.readlines():
        articleList.append(url)
    return articleList

def extractFeatures(articles, session):
    featureVector = []
    for article in articles:
        tokenDict = {}
        numSentences = numTokens = uniqueTokens = mrcWords = 0

        articleText = word_tokenize(article.text)
        for sentence in articleText.split('.'):
            #get avg len
            numSentences+= 1 
            sentence = sentence.split()
            numTokens += len(sentence)
             
            fam = conc = imag = 0
            for word in sentence:
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
    return featureVector

def trainClassifier():
    badArticles = getArticles("B")
    goodArticles = getArticles("G")

    badArticles = __get_parsed_articles(badArticles)
    goodArticles = __get_parsed_articles(goodArticles)

    session = setupDB()
    solutionVector = (["bad"]*50 + ["good"]*50) 
    featureVector = extractFeatures(badArticles) + extractFeatures(goodArticles)

    classifier = SVC()
    classifier.fit(featureVector, solutionVector)
    return classifier

    #uncomment if you want to check accuracy with 5 fold
    """
    for i in range(0, 5):
        lower = i*10
        upper = lower + 10
        
        classifier = SVC()
        classifier.fit(featureVector[:lower] + featureVector[upper:], \
                solutionVector[:lower] + featureVector[upper:])
        predictList = clf.predict(featureVector[lower:upper])

        correct = 0
        for i in range(lower, upper):
            if predictList[i] == solutionVector[i]:
                correct +=1
        print correct
        """


