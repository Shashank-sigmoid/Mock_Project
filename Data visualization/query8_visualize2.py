import requests as re
import matplotlib.pyplot as plt
import numpy as np


def compare_gdp():

    # Comparing the GDP of 2019 & 2020 for the top 10 countries
    response = re.get(f"http://127.0.0.1:8086/api/query8?startdate=2019-01-01&&enddate=2019-01-02")
    data = response.json()
    x_data = []
    y_data = []
    y_data1 = []
    for record in data:
        x_data.append(record["_id"])
        y_data.append(record["total"])

    response1 = re.get(f"http://127.0.0.1:8086/api/query8?startdate=2020-01-01&&enddate=2020-01-02")
    data1 = response1.json()
    for record in data1:
        y_data1.append(record["total"])

    # Plotting a double bar graph with Country on x-axis and GDP on y-axis
    x_axis = np.arange(len(x_data))
    plt.bar(x_axis - 0.2, y_data, 0.4, label="2019")
    plt.bar(x_axis + 0.2, y_data1, 0.4, label="2020")
    plt.xticks(x_axis, x_data)
    plt.xlabel("Country")
    plt.ylabel("GDP")
    plt.title("Comparing the GDP of top countries for 2019 & 2020")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    compare_gdp()
