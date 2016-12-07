# this module exposes methods for getting statistics from articles and retrieving articles for users
import json
import heapq
import math

from urllib import request
from newspaper import Article
from newspaper import ArticleException


def get_stats(url):
    # get article
    article = __get_parsed_article(url)
    try:
        article.nlp()
    except ArticleException:
        return
    # get tf counts for all keywords
    keywords = __get_keyword_counts(article.keywords, article.text)
    return keywords


def get_relevant_urls(user):
    # get a collection of urls for recent articles
    articles = __get_corpus()
    # find cosine similarity for each article, keep top n
    return __top_n_articles(articles, user, 5)


def get_top_urls(urls, user, n):
    articles = __get_parsed_articles(urls)
    return __top_n_articles(articles, user, n)


def __top_n_articles(articles, user, num_articles):
    heap = []
    for article in articles:
        result = (__get_cosine_similarity(article, user), article.url)
        if len(heap) < num_articles:
            heapq.heappush(heap, result)
        elif heap[0][0] < result[0]:
            heapq.heappop(heap)
            heapq.heappush(heap, result)
    urls = []
    while len(heap) > 0:
        urls.append(heap[0])
        heapq.heappop(heap)
    return urls


def __get_cosine_similarity(article, user):
    user_centroid = user.get_centroid()
    article_centroid = __get_article_centroid(article, user)
    dot_product = sum([user_centroid[i] * article_centroid[i] for i in range(len(user_centroid))])
    user_magnitude = math.sqrt(sum([math.pow(x, 2) for x in user_centroid]))
    article_magnitude = math.sqrt(sum([math.pow(x, 2) for x in article_centroid]))
    return float(dot_product) / float(user_magnitude * article_magnitude) if (user_magnitude * article_magnitude) > 0 else 0


def __get_article_centroid(article, user):
    article_keyword_counts = __get_keyword_counts(user.keywords.keys(), article.text)
    centroid = []
    total_doc_count = user.num_docs_liked + 1
    for keyword in user.keywords.keys():
        word_doc_count = user.keywords[keyword]["num_docs"] + 1 if article_keyword_counts[keyword] > 0 else user.keywords[keyword]["num_docs"]
        result = math.fabs(math.log2(float(article_keyword_counts[keyword]) / (float(total_doc_count) / float(word_doc_count)))) if article_keyword_counts[keyword] > 0 else 0
        centroid.append(result)
    return centroid


def __get_corpus():
    sources = __get_sources()
    urls = []
    for source in sources:
        urls += __get_article_urls(source)
    return __get_parsed_articles(urls)


def __get_sources():
    url = "https://newsapi.org/v1/sources?language=en&country=us"
    response_json = __get_clean_json(url)
    source_ids = [source["id"] for source in response_json["sources"]]
    return source_ids


def __get_article_urls(source):
    url = "https://newsapi.org/v1/articles?source=" + source + "&apiKey=66e0dd0ca71043c09db31c1733d53a7e"
    response_json = __get_clean_json(url)
    article_urls = [article["url"] for article in response_json["articles"]]
    return article_urls


def __get_clean_json(url):
    response = str(request.urlopen(url).read().decode('utf-8'))
    response = str(response.encode('utf-8', 'replace'))
    response = response[2:-1]
    new_response = ""
    was_backslash = [False]
    for character in response:
        if character != '\\':
            new_response += "" if was_backslash[0] and character == "\"" else character
            was_backslash[0] = False
        else:
            was_backslash[0] = True
    return json.loads(new_response)


def __get_parsed_articles(article_urls):
    articles = []
    for url in article_urls:
        article = Article(url)
        # Single-threaded for now
        try:
            article.download()
            article.parse()
            # article.nlp()
        except ArticleException:
            continue
        # Hack to detect parsing error for now
        if article.title != "": 
            article.nlp()
            articles.append(article)
    return articles


def __get_parsed_article(url):
    return __get_parsed_articles([url])[0]


def __get_keyword_counts(article_keywords, article_text):
    clean_article_text = __get_clean_text(article_text)
    article_keywords_set = set(article_keywords)
    keywords = {}
    for keyword in article_keywords_set:
        keywords[keyword] = 0
    for word in clean_article_text:
        if word in article_keywords_set:
            __safe_increment(keywords, word)
    return keywords


def __safe_increment(_dict, key):
    if key not in _dict:
        _dict[key] = 0
    _dict[key] += 1


def __get_clean_text(text):
    legal_text = ""
    for character in text:
        if 0 <= ord(character) < 256:
            legal_text += character
    split_text = legal_text.split(' ')
    result_text = []
    for word in split_text:
        mutable_word = [word]
        mutable_word[0] = mutable_word[0].lstrip('\n')
        mutable_word[0] = mutable_word[0].rstrip('\n')
        if len(mutable_word[0]) > 0 and not mutable_word[0][0].isalnum():
            mutable_word[0] = mutable_word[0][1:]
        if len(mutable_word[0]) > 0 and not mutable_word[0][-1].isalnum():
            mutable_word[0] = mutable_word[0][:-1]
        if len(mutable_word[0]) > 0:
            result_text.append(mutable_word[0].lower())
    return result_text



