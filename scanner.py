import requests
from bs4 import BeautifulSoup


def scan_blocket():

    url = "https://www.blocket.se/bilar/sok"

    r = requests.get(url)

    soup = BeautifulSoup(r.text, "html.parser")

    cars = []

    for ad in soup.select("article")[:10]:

        title = ad.get_text()[:80]

        cars.append({
            "title": title,
            "price": 200000
        })

    return cars


if __name__ == "__main__":

    cars = scan_blocket()

    for c in cars:
        print(c)
