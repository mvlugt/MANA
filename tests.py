from manapotion import db
from manapotion import content
from manapotion import user
User = user.User


def test_create_user():
    db.create_user("test1")
    db.delete_user("test1")


def test_get_user():
    db.create_user("test1")
    result_success = db.get_user("test1")
    assert not result_success is None
    result_failure = db.get_user("test2")
    assert result_failure is None
    db.delete_user("test1")


def test_update_user():
    _user = db.create_user("test1")
    _user.keywords["key1"] = {
        "term_frequency": 1,
        "num_docs": 2
    }
    db.update_user(_user)
    result = db.get_user("test1")
    assert result.keywords["key1"]["term_frequency"] == 1
    assert result.keywords["key1"]["num_docs"] == 2
    db.delete_user("test1")


def db_test_suite():
    test_create_user()
    test_get_user()
    test_update_user()


def test_get_stats():
    print(repr(content.get_stats("https://techcrunch.com/2016/12/05/flutterwave-aims-to-unify-africas-fragmented-payment-systems-and-empower-small-businesses/")))


def test_get_urls():
    test_user = User(1)
    test_user.num_docs_liked = 7
    test_user.keywords = {
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
    print(repr(content.get_relevant_urls(test_user)))


def content_test_suite():
    test_get_stats()
    test_get_urls()


def main():
    db_test_suite()
    content_test_suite()

main()
