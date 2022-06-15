import requests as re
import matplotlib.pyplot as plt


def covid_cases():

    # Visualizing the data of Covid for a particular country
    country = "india"
    response = re.get(f"http://127.0.0.1:8086/api/query7?country={country}")
    data = response.json()
    x_data = []
    y_data = []
    y_data1 = []
    for record in data:
        x_data.append(record["Last Updated"])
        y_data.append(record["Confirmed cases"])
        y_data1.append(record["Deaths"])

    # Plotting line graph with Date on x-axis and Confirmed cases, Deaths on y-axis
    plt.plot(x_data, y_data, label="Confirmed cases")
    plt.plot(x_data, y_data1, label="Deaths")
    plt.title(f"Covid scenario in {country.title()}")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    covid_cases()
