import requests as re
import pymongo as pm
from dateutil.parser import parse
import csv


def query_7():

    try:
        # Establishing the connection with mongoDB server
        client = pm.MongoClient("mongodb://127.0.0.1:27017")
        print("Connection established successfully...")

        # Storing the database named "twitter_db" in variable mydb
        mydb = client["twitter_db"]

        # Creating a collection named "cases_data"
        cases_data = mydb["cases_data"]

        # Base URL to call the API server
        url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/total"

        # Headers containing the API key
        headers = {
            "X-RapidAPI-Host": "covid-19-coronavirus-statistics.p.rapidapi.com",
            "X-RapidAPI-Key": "40b27a5d62mshead33450c6e50ccp159aeejsn1841eea50cff"
        }

        # Reading the name of the countries from a CSV file using with open method
        with open("/Users/shashankdey/PycharmProjects/Mock_Project/Queries/countries.csv", "r") as file:
            reader = csv.reader(file)
            k = 0
            for row in reader:
                # Ignoring the first line of the CSV file as it contains the header
                if k == 0:
                    k = 1
                else:
                    # Creating querystring with the country name fetched from CSV file
                    querystring = {"country": row[0]}

                    # Passing the country parameter to the Base URL, sending the request to the API server
                    # Storing the response in a variable
                    response = re.request("GET", url, headers=headers, params=querystring)

                    # Converting the response in JSON format
                    data = response.json()

                    # Structure of the document to be inserted in the collection
                    # Country: (String) Name of the country
                    # Code: (String) Country's code
                    # Confirmed cases: (INT32) No. of confirmed cases in that country
                    # Deaths: (INT32) No. of deaths in that country
                    # Last Updated: (Date) Timestamp when the data last updated
                    entry = {
                        "Country": data["data"]["location"],
                        "Code": row[1],
                        "Confirmed cases": data["data"]["confirmed"],
                        "Deaths": data["data"]["deaths"],
                        "Last Updated": parse(data["data"]["lastReported"])
                    }

                    # Document inserted in the collection
                    cases_data.insert_one(entry)
                    print(f"Data for {row[0]} is successfully added to the database...")

    except:
        print("Error in connection")


if __name__ == "__main__":
    query_7()
