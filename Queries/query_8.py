import quandl as qd
import time as t
import pymongo as pm
import csv


def query_8():

    try:
        # Establishing the connection with mongoDB server
        client = pm.MongoClient("mongodb://127.0.0.1:27017")
        print("Connection established successfully...")

        # Storing the database in variable mydb
        mydb = client["twitter_db"]

        # Creating a collection
        global_economy = mydb["global_economy"]

        # Fetching data from the nadaq API
        qd.ApiConfig.api_key = "Ji81cMm63Vm7UxPXq6CZ"

        # Reading the name of the countries and their codes from a CSV file using with open method
        with open("/Users/shashankdey/PycharmProjects/Mock_Project/Queries/Query_8_GDP.csv", "r") as file:
            reader = csv.reader(file)
            k = 0
            for row in reader:
                # Ignoring the first line of the CSV file as it contains the header
                if k == 0:
                    k = 1
                else:
                    data = qd.get(f"FRED/{row[2]}")
                    data.reset_index(inplace=True)
                    data_dict = data.to_dict("records")
                    data_to_insert = []

                    # Structure of the document to be inserted in the collection
                    # Country: (String) Name of the country
                    # Code: (String) Country's code
                    # Date: (Date) Year of the record
                    # GDP: (Double) GDP of the country for that given year
                    for record in data_dict:
                        entry = {
                            "Country": row[0],
                            "Code": row[1],
                            "Date": record["Date"],
                            "GDP": record["Value"]
                        }
                        data_to_insert.append(entry)

                    # Document inserted in the collection
                    global_economy.insert_many(data_to_insert)
                    print(f"Data for {row[0]} is successfully added to the database...")
                    t.sleep(31)

    except:
        print("Error in connection")


if __name__ == "__main__":
    query_8()
