import requests as re
import matplotlib.pyplot as plt


def worst_affected():

    # Visualizing the data for countries worst affected by Covid
    response = re.get(f"http://127.0.0.1:8086/api/query7?startdate=2022-01-01&&enddate=2022-06-10")
    data = response.json()
    x_data = []
    y_data = []
    for record in data:
        x_data.append(record["location"])
        y_data.append(record["confirmedCases"])

    # Plotting bar graph with Country on x-axis and Confirmed cases on y-axis
    plt.bar(x_data, y_data)
    plt.xlabel("Country")
    plt.ylabel("Confirmed cases")
    plt.title("Worst affected countries all over the world")
    plt.show()


if __name__ == "__main__":
    worst_affected()
