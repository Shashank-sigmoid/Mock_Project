from pymongo import MongoClient
from datetime import datetime


def date_conversion():

    try:
        # Establishing connection with the MongoDB
        client = MongoClient("mongodb://root:root@mongo:27017")
        print("Connection established successfully...")

        # Storing the database named "twitter_db" in variable mydb
        mydb = client["twitter_db"]

        # Storing the collection "donations" in a variable named coll
        coll = mydb["donations"]

        # Converting field "datePledged" and "dateConfirmed" of collection "donations" from INT to ISO Date format using datetime
        for doc in coll.find():
            dtime1 = doc["datePledged"]
            dtime2 = doc["dateConfirmed"]

            if dtime1 != "":
                new_datetime = datetime.fromtimestamp(dtime1)
                my_query = {"datePledged": doc["datePledged"]}
                new_value = {"$set": {"datePledged": new_datetime}}
                coll.update_one(my_query, new_value)

            if dtime2 != "":
                new_datetime = datetime.fromtimestamp(dtime2)
                my_query = {"dateConfirmed": doc["dateConfirmed"]}
                new_value = {"$set": {"dateConfirmed": new_datetime}}
                coll.update_one(my_query, new_value)

        print("Date converted successfully...")

    except:
        print("Error in the connection...")


if __name__ == "__main__":
    date_conversion()
