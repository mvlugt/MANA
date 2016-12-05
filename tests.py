from manapotion import db


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
    _user.keywords["key1"] = 1
    db.update_user(_user)
    result = db.get_user("test1")
    assert result.keywords["key1"] == 1
    db.delete_user("test1")


def db_test_suite():
    test_create_user()
    test_get_user()
    test_update_user()


def main():
    db_test_suite()

main()
