import os
import sys
import json
from pathlib import Path
import requests

root = str(Path(__file__).resolve().parents[1])
sys.path.append(root)
from manapotion import user, db, content
from QA import quality

# list of Article URLS, as a default this should start with our "seed" urls



def send_articles(ARTICLES):
    article_message =  ""
    for i in range(0, len(ARTICLES)):
        article_message += (str(i) + ": " + ARTICLES[i] + "\n")
    print(article_message)


def get_feedback(user, ARTICLES):
    feedback = input("Which of these articles interest you most? ")
    articles_user_likes = [int(s) for s in feedback.split() if s.isdigit()]
    for index in articles_user_likes:
        # For each article the user likes, grab the keywords and update the user profile
        url = ARTICLES[index]
        key_words = content.get_stats(url)
        user.update_stats(key_words)
    print("Thanks for that feedback!")


def main():

    name = input("Hello there! I'm MANA. What is your name? ")
    
    # Check to see if user already exists in DB
    current_user = db.get_user(name)
    
    # If not, create user and send seed articles and ask for feedback
    if not current_user:
        current_user = db.create_user(name)
        print("Welcome to MANA " + name)
        print("Here are some initial articles, please take a look: ")
        ARTICLES = ["https://techcrunch.com/2016/12/08/uber-spells-out-what-causes-riders-to-lose-access-in-new-policy/", "http://www.cnn.com/2016/12/06/entertainment/grammy-nominations-2017/index.html", "http://www.dailytimesgazette.com/36308-2/36308/"]
        send_articles(ARTICLES)
        get_feedback(current_user, ARTICLES)
        response = input("Would you like to continue using MANA? ")
        if response == "yes":
            go_on = True
        else:
            go_on = False

    # If they do exist, send them some articles they may like and ask for feedback
    else:
        go_on = True
        print("Welcome back " + name)
        print ("Here are some articles I think you might like: ")
    
    while go_on:
        rel_articles = content.get_relevant_urls(current_user)
        rel_articles = [item[1] for item in rel_articles]
        qual_articles = quality.filterArticles(rel_articles)
        print (qual_articles)
        ARTICLES = [item.url for item in qual_articles]
        send_articles(ARTICLES)
        get_feedback(current_user, ARTICLES)
        response = input("Would you like to continue using MANA? ")
        if response == "yes":
            go_on = True
        else:
            go_on = False


if __name__ == '__main__':
    main()