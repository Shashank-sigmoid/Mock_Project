from pymongo import MongoClient
from datetime import timedelta


def summary_table2():

    try:
        # Establishing the connection with mongoDB server
        client = MongoClient("mongodb://127.0.0.1:27017")
        print("Connection established successfully...")

        # Storing the database named "twitter_db" in variable mydb
        mydb = client["twitter_db"]

        # Storing the collection "covid_tweets" in a variable named coll
        coll = mydb["covid_tweets"]

        # Creating a collection named "table2"
        coll2 = mydb["table2"]

        # Storing the timestamp of all the tweets from the collection covid_tweets
        timestamp = []
        for doc in coll.find():
            timestamp.append(doc["created_at"])

        # Fetching the minimum and maximum timestamp from all the tweets
        first = min(timestamp)
        last = max(timestamp)

        # Difference between the maximum and minimum timestamp
        delta = last.replace(second=0, hour=0, minute=0) - first.replace(second=0, hour=0, minute=0)

        # Looping from minimum to maximum date with a time window of 1 day
        for i in range(delta.days + 1):
            start_date = first.replace(second=0, hour=0, minute=0) + timedelta(days=i)
            end_date = first.replace(second=0, hour=0, minute=0) + timedelta(days=i+1)

            # entries contain documents having frequency of the word occurred in a tweet for a given day
            entries = coll.aggregate([
                {"$project": {"words": {"$split": ["$text", " "]}, "created_at": 1}},
                {"$unwind": "$words"},
                {"$match": {"$and": [{"words": {"$nin": ["a", "I", "are", "is", "to", "the", "of", "and", "RT"]}},
                                     {"created_at": {"$gt": start_date, "$lt": end_date}}]}},
                {"$group": {"_id": "$words", "total": {"$sum": 1}}},
                {"$sort": {"total": -1}},
                {"$limit": 100}
            ])

            # Generating the document record from entries to be ingested in the collection table2
            for entry in entries:
                record = {"word": entry["_id"], "count": entry["total"], "date": start_date}
                coll2.insert_one(record)

        print("Summary table created successfully...")

    except:
        print("Error in the connection...")


if __name__ == "__main__":
    summary_table2()
