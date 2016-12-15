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


def test_get_top_urls():
    test_user = User(1)
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
    print(repr(content.get_top_urls(["https://www.bluetooth.com/news/pressreleases/2016/12/07/bluetooth-5-now-available",
                                     "http://www.businessinsider.com/amazon-payments-way-ahead-of-apple-and-google-2016-12",
                                     "http://specialreports.dailydot.com/how-to-destroy-an-american-family",
                                     "http://www.governing.com/topics/public-justice-safety/courts-corrections/mississippi-correction-reform.html",
                                     "https://www.theguardian.com/world/2015/jan/14/-sp-roberto-saviano-my-life-under-armed-guard-gomorrah?CMP=twt_gu",
                                     "http://www.nybooks.com/articles/archives/2010/feb/11/the-chess-master-and-the-computer/?pagination=false",
                                     "http://www.nytimes.com/2010/06/20/magazine/20Computer-t.html?pagewanted=all",
                                     "http://www.guardian.co.uk/theobserver/2010/mar/21/tom-bissell-video-game-cocaine-addiction",
                                     "http://www.thestranger.com/seattle/Content?oid=4683741&mode=print",
                                     "http://www.ediblegeography.com/a-cocktail-party-in-the-street-an-interview-with-alan-stillman/",
                                     "http://www.slate.com/id/2277301/pagenum/all/#p2",
                                     "http://www.thenation.com/article/155400/postcard-palestine",
                                     "http://online.wsj.com/article/SB10001424052748704779704575553943328901802.html",
                                     "http://www.guardian.co.uk/society/2010/may/09/alcoholism-health-doctor-addiction-drug/print",
                                     "http://www.texasobserver.org/dateline/he-who-casts-the-first-stone",
                                     "http://www.esquire.com/features/argentine-ant-control-0810",
                                     "http://www.theamericanscholar.org/solitude-and-leadership/print/",
                                     "http://www.archaeology.org/1003/etc/neanderthals.html",
                                     "http://www.historynet.com/holy-terror-the-rise-of-the-order-of-assassins.htm",
                                     "http://www.nybooks.com/articles/archives/2010/jan/14/night/",
                                     "http://www.vanityfair.com/culture/features/2010/01/hadron-collider-201001?printable=true",
                                     "http://www.theatlantic.com/magazine/archive/2010/08/autism-8217-s-first-child/8227/",
                                     "http://motherjones.com/politics/2010/02/surrogacy-tourism-india-nayna-patel?page=1",
                                     "http://www.nytimes.com/2010/07/11/magazine/11cryonics-t.html",
                                     "http://www.guardian.co.uk/books/2010/oct/09/howard-jacobson-comic-novels"
                                     ], test_user, 25)))


def content_test_suite():
    test_get_stats()
    # test_get_urls()
    test_get_top_urls()


def main():
    db_test_suite()
    content_test_suite()

main()
