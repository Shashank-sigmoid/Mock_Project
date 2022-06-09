import requests as re
from datetime import date
import pymongo as pm


def query_6():

    try:
        # Establishing the connection with mongoDB server
        client = pm.MongoClient("mongodb://127.0.0.1:27017")
        print("Connection established successfully...")

        # Storing the database named "twitter_db" in variable mydb
        mydb = client["twitter_db"]

        # Creating a collection named "donations"
        donations = mydb["donations"]

        # Passing the date parameter as today's date
        # Sending the request to the API server using the Base URL
        response = re.get(f"https://covidfunding.eiu.com/api/funds?date={date.today()}")

        # Converting the response in JSON format
        data = response.json()

        # Ingesting the bulk data in the collection "donations"
        donations.insert_many(data["funds"])
        print("Data added successfully to the Database...")

    except:
        print("Error in connection")


if __name__ == "__main__":
    query_6()
