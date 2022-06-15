import requests as re
import matplotlib.pyplot as plt


def max_times_donors():

    # Visualizing the top n countries who donated the most no. of times
    n = 10
    response = re.get(f"http://127.0.0.1:8086/api/query6?sort=count&&limit={n}")
    data = response.json()
    x_data = []
    y_data = []
    for record in data:
        x_data.append(record["_id"])
        y_data.append(record["Count"])

    # Plotting a bar graph with Country on x-axis and No. of times donated on y-axis
    plt.bar(x_data, y_data)
    plt.title("Maximum no. of times donations made by countries")
    plt.xlabel("Country")
    plt.ylabel("No. of times donation made")
    plt.show()


if __name__ == "__main__":
    max_times_donors()
