import requests as re
import matplotlib.pyplot as plt


def country_gdp():

    # Visualizing the GDP of a country over a long period of time
    country = "india"
    response = re.get(f"http://127.0.0.1:8086/api/query8?country={country}")
    data = response.json()
    x_data = []
    y_data = []
    for record in data:
        x_data.append(record["Date"])
        y_data.append(record["GDP"])

    # Plotting a scatter graph with Year on x-axis and GDP on y-axis
    plt.scatter(x_data, y_data)
    plt.title(f"GDP of {country.title()}")
    plt.xlabel("Year")
    plt.ylabel("GDP")
    plt.show()


if __name__ == "__main__":
    country_gdp()
