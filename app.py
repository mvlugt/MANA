import os
import sys
import json
from pathlib import Path
import requests
from flask import Flask, request

root = str(Path(__file__).resolve().parents[1])
sys.path.append(root)
from manapotion import user, db, content

app = Flask(__name__)

# list of Article URLS, as a default this should start with our "seed" urls
ARTICLES = ["http://www.cnn.com/2016/12/06/politics/obama-trump-terrorism-views/index.html", "http://www.cnn.com/2016/12/06/entertainment/grammy-nominations-2017/index.html"]

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200

# endpoint for processing incoming messaging events
@app.route('/', methods=['POST'])
def webhook():

    # list of Article URLS, as a default this should start with our "seed" urls
    ARTICLES = ["http://www.cnn.com/2016/12/06/politics/obama-trump-terrorism-views/index.html", "http://www.cnn.com/2016/12/06/entertainment/grammy-nominations-2017/index.html"]
    data = request.get_json()
    log(data) 

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                    current_user = db.get_user(sender_id)
                    # If current_user returns null, then this user does not exist in our database yet
                    if not current_user:
                        # 1). Create a user
                        current_user = db.create_user(sender_id)
                        # 2). Send a lil greeting 
                        send_message(sender_id, "Hi I'm MANA! Please tell me which of these articles interested you most")
                        article_list_message = ""
                        # 3). Send the list of our default initial articles
                        for i in range(0, len(ARTICLES)):
                            article_list_message += (str(i) + ": " + ARTICLES[i] + "\n")
                        send_message(sender_id, article_list_message)
                    else:
                        # Get the numbers of the article the user likes
                        articles_user_likes = [int(s) for s in message_text.split() if s.isdigit()]
                        send_message(sender_id, "Thanks for giving me that feedback.")
                        for index in articles_user_likes:
                            log("updating user profile")
                            # For each article the user likes, grab the keywords and update the user profile
                            url = ARTICLES[index]
                            key_words = content.get_stats(url)
                            db.update_stats(sender_id, key_words)
                        
                        # This should reflect the updated user profile
                        log("attempting to get relevant urls")
                        ARTICLES = content.get_top_urls(ARTICLES, user, 2)
                        log("got articles")

                        send_message(sender_id, "I found these articles I thought you might like. As always, please let me know which articles interested you most")
                        article_list_message = ""
                        # 3). Send the list of our default initial articles
                        for i in range(0, len(ARTICLES)):
                            article_list_message += (str(i) + ": " + ARTICLES[i] + "\n")
                        send_message(sender_id, article_list_message)
                            
                            
                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print (str(message))
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
