# Python w/ Mongo POC

from pymongo import MongoClient

def main():
	client = MongoClient()
	db = client.MANA_DB
	collection = db.UserProfile

	_id = collection.insert_one(
		{
			"user": {
				"name": "Yoav Hufflepuffer",
				"keywords": ["tech", "music"],
				"industry": "Technology"
			}
		}
	)

	print(_id)
	cursor = collection.find({"user.industry": "Technology"})
	for document in cursor:
		print document
	result = collection.delete_many({"user.name": "Yoav Hufflepuffer"})
	print "Number deleted " + str(result.deleted_count)

main()