import requests as re
from datetime import date
import pymongo as pm


def query_6():
    # Establishing the connection with mongoDB server
    client = None
    try:
        client = pm.MongoClient('mongodb://127.0.0.1:27017')
        print("Connection established successfully...")
    except:
        print("Error in connection")

    # Storing the database in variable mydb
    mydb = client['twitter_db']

    # Creating a collection
    donations = mydb["donations"]

    # Fetching data from Covid funding API
    response = re.get(f"https://covidfunding.eiu.com/api/funds?date={date.today()}")
    data = response.json()
    donations.insert_many(data['funds'])
    print("Data added successfully to the Database...")


if __name__ == "__main__":
    query_6()
