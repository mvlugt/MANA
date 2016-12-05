# defines the User class


class User:
    def __init__(self, fb_id):
        self.fb_id = fb_id
        self.keywords = {}
        self.num_docs_liked = 0

    def update_stats(self, keywords):
        for word in keywords:
            safe_increment(self.keywords, word, keywords[word])

    def as_dict(self):
        return {
            "fb_id": self.fb_id,
            "keywords": self.keywords,
            "num_docs_liked": self.num_docs_liked
        }


class WordStats:
    def __init__(self, term_frequency, num_articles):
        self.term_frequency = term_frequency
        self.num_articles = num_articles


def from_dict(_dict):
    user = User(_dict["fb_id"])
    user.keywords = _dict["keywords"]
    user.num_docs_liked = _dict["num_docs_liked"]
    return user


def safe_increment(keywords, keyword, amount):
    if keyword not in keywords:
        keywords[keyword] = WordStats(0, 0)
    keywords[keyword].term_frequency += amount
    keywords[keyword].num_articles += 1
