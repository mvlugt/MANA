# defines the User class
import math


class User:
    def __init__(self, fb_id):
        self.fb_id = fb_id
        self.keywords = {}
        self.num_docs_liked = 0

    def update_stats(self, keywords):
        for word in keywords:
            safe_increment(self.keywords, word, keywords[word])
        self.num_docs_liked += 1

    def as_dict(self):
        return {
            "fb_id": self.fb_id,
            "keywords": self.keywords,
            "num_docs_liked": self.num_docs_liked
        }

    def get_centroid(self):
        centroid = []
        for keyword in self.keywords.keys():
            tf = self.keywords[keyword]["term_frequency"]
            log_prob = math.log2(float(self.num_docs_liked) / float(self.keywords[keyword]["num_docs"])) if self.num_docs_liked > 0 else 0
            centroid.append(tf * log_prob)
        return centroid


def from_dict(_dict):
    user = User(_dict["fb_id"])
    user.keywords = _dict["keywords"]
    user.num_docs_liked = _dict["num_docs_liked"]
    return user


def safe_increment(keywords, keyword, amount):
    if keyword not in keywords:
        keywords[keyword] = {
            "term_frequency": 0,
            "num_docs": 0
        }
    keywords[keyword]["term_frequency"] += amount
    keywords[keyword]["num_docs"] += 1
