import requests as re
from datetime import date
import pymongo as pm


def query_6():

    try:
        # Establishing the connection with mongoDB server
        client = pm.MongoClient("mongodb://root:root@127.0.0.1:27017")
        print("Connection established successfully...")

        # Storing the database in variable mydb
        mydb = client["twitter_db"]

        # Creating a collection
        donations = mydb["donations"]

        # Fetching data from Covid funding API
        response = re.get(f"https://covidfunding.eiu.com/api/funds?date={date.today()}")
        data = response.json()
        donations.insert_many(data["funds"])
        print("Data added successfully to the Database...")

    except:
        print("Error in connection")


if __name__ == "__main__":
    query_6()
