from bs4 import BeautifulSoup
from urllib import request
import json
from newspaper import 



def get_articles():
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


def main():
    articles = get_articles()
    print(repr(articles))

main()