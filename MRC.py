"""
this script:
    1. builds the db
    2. connects to db for querying
    3. provides a nice querying abstraction
"""
from wordmodel import Word

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc

import os

#check if db needs to be built (1)
if not os.path.isfile('./mrc2.db'):
    import extract

#Run this once before querying DB (2)
#Return a session with the db
def setupDB():
    engine = create_engine('sqlite:///mrc2.db')
    Session = sessionmaker(bind = engine)
    return Session()

#Use the session created above to query db (3)
#Return list of [fam, conc, imag]
def queryDB(word, session):
    item = 0
    if not word.isupper() and word[0].isupper(): #handles capitalized word
        word = word.upper()
        item = session.query(Word).filter(Word.word==word).\
            filter(Word.cap == "C").order_by(desc(Word.fam)).first()

    else: #handles not capital word
        word = word.upper()
        item = session.query(Word).filter(Word.word==word).\
            filter(Word.cap != "C").order_by(desc(Word.fam)).first()

    features = []
    #not every item in dictionary is totally annotated
    if item.fam != 0 or item.imag != 0 or item.conc != 0:
        features.extend([item.fam, item.imag, item.conc])
    return features
