import requests as re
import matplotlib.pyplot as plt


def top_donors():

    # Visualizing the top n countries who donated the most amount in total
    n = 10
    response = re.get(f"http://127.0.0.1:8086/api/query6?sort=total&&limit={n}")
    data = response.json()
    x_data = []
    y_data = []
    for record in data:
        x_data.append(record["_id"])
        y_data.append(record["Total"])

    # Plotting a bar graph with Country on x-axis and total amount donated on y-axis
    plt.bar(x_data, y_data)
    plt.title("Top donations by countries")
    plt.xlabel("Country")
    plt.ylabel("Donated")
    plt.show()


if __name__ == "__main__":
    top_donors()
