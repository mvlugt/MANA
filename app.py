import os
import sys
import json
from pathlib import Path
import requests
from flask import Flask, request

root = str(Path(__file__).resolve().parents[1])
sys.path.append(root)
from manapotion import user, db, content
from QA import quality

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
    ARTICLES = ["http://www.cnn.com/2016/12/06/politics/obama-trump-terrorism-views/index.html", "http://www.businessinsider.com/amazon-payments-way-ahead-of-apple-and-google-2016-12", "http://www.inquisitr.com/3765295/ann-coulters-twitter-if-trump-sells-out-its-not-the-fault-of-trump-voters-cuck-insults-fly/"]
    data = request.get_json()
    log(data) 

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                if message_text.lower().startswith("hello"):
                    send_message(sender_id, "Hey There! How can I help you today?")
                elif message_text.lower().startswith("http:"):
                    send_message(sender_id, "Great! I'll get to work on that. Any other articles?")
                elif message_text.lower().startswith("go"):
                    send_message(sender_id, "Here I go!")
                    current_user = user.User(1)
                    current_user.num_docs_liked = 7
                    current_user.keywords = {
                        "computer": {
                            "term_frequency": 10,
                            "num_docs": 4
                        },
                        "technology": {
                            "term_frequency": 17,
                            "num_docs": 3
                        },
                        "payment": {
                            "term_frequency": 32,
                            "num_docs": 5
                        },
                        "business": {
                            "term_frequency": 50,
                            "num_docs": 6
                        }
                    }

                    log(str(current_user.keywords))
                    # 1). gets quality
                    quality_articles = QA.filterArticles(ARTICLES)
                    
                    # 2). Returns a list of tuples (cosine, url)
                    results = content.__top_n_articles(quality_articles, current_user, 2)
                    # summary = results[len(results)-1].summary
                    summary = "Jk"
                    rel_message = "The article most relevant to you is: \n" + results[len(results)-1][1] + "\nIt has a relevance weight of: " + str(results[len(results)-1][0]) + "\n\nHere is a little summary: " + summary
                    send_message(sender_id, rel_message)
                    
                else:
                    send_message(sender_id, "Sorry I'm not very smart yet....can you try saying something else?")
                            
                            
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
