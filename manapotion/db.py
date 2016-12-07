# surfaces methods for interacting with the database

from pymongo import MongoClient
import os

from . import user

User = user.User


def create_user(fb_id):
    new_user = User(fb_id)
    collection = __get_profile_collection()
    collection.insert_one(new_user.as_dict())
    return new_user


def get_user(fb_id):
    collection = __get_profile_collection()
    doc = collection.find_one({"fb_id": fb_id})
    if doc is None:
        return None
    return user.from_dict(doc)


def update_user(_user):
    collection = __get_profile_collection()
    result = collection.find_one_and_replace({"fb_id": _user.fb_id}, _user.as_dict())
    if result is None:
        raise KeyError("Tried to update non-existent user")


def delete_user(fb_id):
    collection = __get_profile_collection()
    result = collection.find_one_and_delete({"fb_id": fb_id})
    if result is None:
        raise KeyError("Tried to delete non-existent user")


def __get_profile_collection():
    mongohq_url = os.environ['MONGOHQ_URL']
    client = MongoClient(mongohq_url)
    db = client.MANA_DB
    return db.UserProfile
