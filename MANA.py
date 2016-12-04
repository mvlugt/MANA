from bs4 import BeautifulSoup
from urllib import request
import json
from newspaper import Article

# Install newspaper for OSX 
# $ brew install libxml2 libxslt
# $ brew install libtiff libjpeg webp little-cms2
# $ pip3 install newspaper3k
# $ curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python3


def get_article_urls():
    url = "https://newsapi.org/v1/articles?source=techcrunch&apiKey=66e0dd0ca71043c09db31c1733d53a7e"
    response = str(request.urlopen(url).read().decode('utf-8'))
    response = str(response.encode('utf-8', 'replace'))
    response = response[2:]
    response = response[:-1]
    new_response = ""
    for character in response:
        if character != '\\':
            new_response += character
    response_json = json.loads(new_response)
    article_urls = [article["url"] for article in response_json["articles"]]
    return article_urls

def get_parsed_articles(article_urls):
    articles = []
    for url in article_urls:
        article = Article(url)
        # Single-threaded for now
        article.download()
        article.parse()
        # Hack to detect parsing error for now
        if article.title != "":
            articles.append(article)
    return articles

def main():
    article_urls = get_article_urls()
    parsed_articles = get_parsed_articles(article_urls)
    # NLP Example:
    for article in parsed_articles:
        article.nlp()
        print(article.keywords)
main()