import quandl as qd
import time as t
import pymongo as pm
import csv


def query_8():
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
    global_economy = mydb["global_economy"]

    # Fetching data from the nadaq API
    qd.ApiConfig.api_key = 'Ji81cMm63Vm7UxPXq6CZ'

    with open('/Users/shashankdey/PycharmProjects/Mock_Project/Queries/Query 8 - GDP.csv', 'r') as file:
        reader = csv.reader(file)
        k = 0
        for row in reader:
            if k == 0:
                k = 1
            else:
                data = qd.get(f"FRED/{row[1]}")
                data.reset_index(inplace=True)
                data_dict = data.to_dict("records")
                data_to_insert = []
                for record in data_dict:
                    entry = {"Country": row[0], "Date": record['Date'], "GDP": record['Value']}
                    data_to_insert.append(entry)
                global_economy.insert_many(data_to_insert)
                print(f"Data for {row[0]} is added to the database...")
                t.sleep(31)


if __name__ == '__main__':
    query_8()
