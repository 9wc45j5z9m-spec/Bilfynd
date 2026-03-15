import os
import sqlite3
import requests
from flask import Flask
from bs4 import BeautifulSoup

app = Flask(__name__)


def init_db():

    conn = sqlite3.connect("cars.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS cars(
        title TEXT,
        price INTEGER,
        link TEXT,
        source TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_car(car):

    conn = sqlite3.connect("cars.db")
    c = conn.cursor()

    c.execute("""
    INSERT INTO cars VALUES (?,?,?,?)
    """,(
        car["title"],
        car["price"],
        car["link"],
        car["source"]
    ))

    conn.commit()
    conn.close()


def get_cars():

    conn = sqlite3.connect("cars.db")
    c = conn.cursor()

    rows = c.execute("SELECT * FROM cars").fetchall()

    conn.close()

    cars=[]

    for r in rows:

        cars.append({
        "title":r[0],
        "price":r[1],
        "link":r[2],
        "source":r[3]
        })

    return cars


def crawl_blocket():

    url="https://www.blocket.se/bilar/sok"

    r=requests.get(url,headers={"User-Agent":"Mozilla/5.0"})

    soup=BeautifulSoup(r.text,"html.parser")

    ads=soup.find_all("a",href=True)

    found=[]

    for a in ads:

        link=a["href"]

        if "/annons/" in link:

            full_link="https://www.blocket.se"+link

            title=a.text.strip()

            if len(title)>5:

                car={

                "title":title,
                "price":200000,
                "link":full_link,
                "source":"Blocket"

                }

                found.append(car)

    return found[:20]


@app.route("/crawl")
def run_crawler():

    cars=crawl_blocket()

    for car in cars:

        save_car(car)

    return "Crawler klar! Gå tillbaka till startsidan."


@app.route("/")
def home():

    cars=get_cars()

    html="""
    <h1>🚗 Bilfynd Scanner</h1>

    <p><a href="/crawl">🔎 Kör crawler</a></p>

    <hr>
    """

    for car in cars:

        html+=f"""

        <div style='border:1px solid #ccc;padding:10px;margin:10px'>

        <h2>{car['title']}</h2>

        <p>Källa: {car['source']}</p>

        <a href="{car['link']}" target="_blank">🔗 Öppna annons</a>

        </div>

        """

    return html


init_db()


if __name__=="__main__":

    port=int(os.environ.get("PORT",5000))

    app.run(host="0.0.0.0",port=port)
