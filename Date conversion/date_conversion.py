from pymongo import MongoClient
from dateutil.parser import parse


def date_conversion():

    try:
        # Establishing connection with the MongoDB
        client = MongoClient("mongodb://localhost:27017")
        print("Connection established successfully...")

        # Storing the database named "twitter_db" in variable mydb
        mydb = client["twitter_db"]

        # Storing the collection "covid_tweets" in a variable named coll
        coll = mydb["covid_tweets"]

        # Storing the collection "who_tweets" in a variable named coll1
        coll1 = mydb["who_tweets"]

        # Converting field "created_at" of collection "covid_tweets" from string to ISO Date format using dateutil
        for doc in coll.find():
            dtime = doc["created_at"]
            if type(dtime) == str:
                new_datetime = parse(dtime)
                my_query = {"created_at": doc["created_at"]}
                new_value = {"$set": {"created_at": new_datetime}}
                coll.update_one(my_query, new_value)

        # Converting field "created_at" of collection "who_tweets" from string to ISO Date format using dateutil
        for doc in coll1.find():
            dtime = doc["created_at"]
            if type(dtime) == str:
                new_datetime = parse(dtime)
                my_query = {"created_at": doc["created_at"]}
                new_value = {"$set": {"created_at": new_datetime}}
                coll1.update_one(my_query, new_value)

        print("Date converted successfully...")

    except:
        print("Error in the connection...")


if __name__ == "__main__":
    date_conversion()
