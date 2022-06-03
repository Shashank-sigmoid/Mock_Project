import requests as re
import pymongo as pm
import csv


def query_7():

    try:
        # Establishing the connection with mongoDB server
        client = pm.MongoClient("mongodb://127.0.0.1:27017")
        print("Connection established successfully...")

        # Storing the database in variable mydb
        mydb = client["twitter_db"]

        # Creating a collection
        cases_data = mydb["cases_data"]

        url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/total"
        headers = {
            "X-RapidAPI-Host": "covid-19-coronavirus-statistics.p.rapidapi.com",
            "X-RapidAPI-Key": "40b27a5d62mshead33450c6e50ccp159aeejsn1841eea50cff"
        }

        with open("/Users/shashankdey/PycharmProjects/Mock_Project/Queries/countries.csv", "r") as file:
            reader = csv.reader(file)
            k = 0
            for row in reader:
                if k == 0:
                    k = 1
                else:
                    querystring = {"country": row[0]}
                    response = re.request("GET", url, headers=headers, params=querystring)
                    data = response.json()
                    entry = {
                        "Country": data["data"]["location"],
                        "Code": row[1],
                        "Confirmed cases": data["data"]["confirmed"],
                        "Deaths": data["data"]["deaths"],
                        "Last Updated": data["data"]["lastReported"]
                    }
                    cases_data.insert_one(entry)
                    print(f"Data for {row[0]} is successfully added to the database...")

    except:
        print("Error in connection")


if __name__ == "__main__":
    query_7()
