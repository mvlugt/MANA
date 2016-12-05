# this module exposes methods for getting statistics from articles and retrieving articles for users
import json

from urllib import request
from newspaper import Article


def get_stats(url):
    # get article
    article = __get_parsed_article(url)
    # get tf counts for all keywords
    keywords = {}
    for keyword in article.keywords:
        __safe_increment(keywords, keyword)
    return keywords


def get_relevant_urls(user):
    raise NotImplementedError


def __get_article_urls():
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


def __get_parsed_articles(article_urls):
    articles = []
    for url in article_urls:
        article = Article(url)
        # Single-threaded for now
        article.download()
        article.parse()
        # Hack to detect parsing error for now
        if article.title != "":
            articles.append(article)
        article.nlp()
    return articles


def __get_parsed_article(url):
    return __get_parsed_articles([url])[0]


def __safe_increment(_dict, key):
    if key not in _dict:
        _dict[key] = 0
    _dict[key] += 1
