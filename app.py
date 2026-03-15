import os
import random
import sqlite3
import time
from flask import Flask, request

app = Flask(__name__)


def init_db():

    conn = sqlite3.connect("cars.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS cars(
        title TEXT,
        brand TEXT,
        price INTEGER,
        days INTEGER,
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
    INSERT INTO cars VALUES (?,?,?,?,?,?)
    """,(
        car["title"],
        car["brand"],
        car["price"],
        car["days"],
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
        "brand":r[1],
        "price":r[2],
        "days":r[3],
        "link":r[4],
        "source":r[5]
        })

    return cars


def analyze(price,days):

    market=int(price*1.15)

    percent=round(((market-price)/market)*100)

    bid=int(price*0.9)

    label="Normal"

    if percent>20:
        label="🔥 SUPER DEAL"

    elif percent>10:
        label="✅ Bra pris"

    seller=""

    if days>20:
        seller="📉 Motiverad säljare"

    return market,percent,label,bid,seller


def mega_crawl():

    brands=["Volvo","Audi","BMW","Toyota","Tesla","Mercedes"]

    sources=[
    ("Blocket","https://www.blocket.se"),
    ("Wayke","https://www.wayke.se"),
    ("Bytbil","https://www.bytbil.com")
    ]

    for i in range(200):

        src=random.choice(sources)

        car={

        "title":f"Bil {random.randint(10000,99999)}",
        "brand":random.choice(brands),
        "price":random.randint(150000,400000),
        "days":random.randint(1,30),
        "link":src[1],
        "source":src[0]

        }

        save_car(car)


@app.route("/mega")
def run_mega():

    mega_crawl()

    return "Mega crawler körd! Uppdatera startsidan."


@app.route("/")
def home():

    cars=get_cars()

    html="""
    <h1>🔥 Bilfynd Mega</h1>

    <p><a href="/mega">🚀 Kör Mega Crawler</a></p>

    <hr>
    """

    deals=[]

    for car in cars:

        market,percent,label,bid,seller=analyze(car["price"],car["days"])

        deals.append((percent,car))

        html+=f"""

        <div style='border:1px solid #ccc;padding:10px;margin:10px'>

        <h2>{car['title']}</h2>

        <p>Märke: {car['brand']}</p>

        <p>Källa: {car['source']}</p>

        <p>Pris: {car['price']} kr</p>

        <p>Annons ute: {car['days']} dagar</p>

        <p>Marknadspris: {market} kr</p>

        <p>Pris under marknad: {percent}%</p>

        <p>{label}</p>

        <p>{seller}</p>

        <p>AI budförslag: {bid} kr</p>

        <a href="{car['link']}" target="_blank">🔗 Öppna annons</a>

        </div>

        """

    html+="<h2>📡 Deal Radar</h2>"

    deals.sort(key=lambda x:x[0],reverse=True)

    for percent,car in deals:

        if percent>10:

            html+=f"<p><a href='{car['link']}' target='_blank'>{car['title']}</a> - {percent}% under marknad</p>"

    return html


init_db()


if __name__=="__main__":

    port=int(os.environ.get("PORT",5000))

    app.run(host="0.0.0.0",port=port)
