import logging
import os

# Project 5
from pymongo import MongoClient

# Set up MongoDB connection
client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
# Use database brevets
db = client.brevets
# Use conlection "items" in the database
collection = db.items


def fetch_items():

    data = collection.find().sort("_id", -1).limit(1)

    for item in data:
        return item["distance"], item["start_time"], item["items"]



def insert_items(distance, start_time, items):

    output = collection.insert_one({
                     "distance": distance,
                     "start_time": start_time,
                     "items": items
                  })
    
    _id = output.inserted_id # this is how you obtain the primary key (_id) mongo assigns to your inserted document.
    return str(_id)



