import os
import random
import sqlite3
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


def analyze_deal(price, days):

    market_price = int(price * 1.15)

    percent = round(((market_price-price)/market_price)*100)

    recommended_bid = int(price * 0.9)

    if percent > 20:
        label = "🔥 SUPER DEAL"
    elif percent > 10:
        label = "✅ Bra pris"
    else:
        label = "Normal"

    seller_signal=""

    if days > 20:
        seller_signal="📉 Motiverad säljare"

    return market_price, percent, label, recommended_bid, seller_signal


def crawl():

    brands=["Volvo","BMW","Audi","Toyota","Tesla","Mercedes"]

    sources=[
    ("Blocket","https://www.blocket.se"),
    ("Wayke","https://www.wayke.se"),
    ("Bytbil","https://www.bytbil.com")
    ]

    for i in range(20):

        source=random.choice(sources)

        car={

        "title":f"Bilannons {random.randint(1000,9999)}",
        "brand":random.choice(brands),
        "price":random.randint(180000,320000),
        "days":random.randint(1,30),
        "link":source[1],
        "source":source[0]

        }

        save_car(car)


@app.route("/crawl")
def run_crawler():

    crawl()

    return "Crawler körd! Gå tillbaka till startsidan."


@app.route("/")
def home():

    cars=get_cars()

    html="""
    <h1>🔥 Bilfynd AI</h1>

    <p><a href="/crawl">🚀 Kör Crawler</a></p>

    <hr>
    """

    deals=[]

    for car in cars:

        market_price, percent, label, recommended_bid, seller_signal = analyze_deal(car["price"],car["days"])

        deals.append((percent,car))

        html+=f"""

        <div style='border:1px solid #ccc;padding:10px;margin:10px'>

        <h2>{car['title']}</h2>

        <p>Märke: {car['brand']}</p>

        <p>Källa: {car['source']}</p>

        <p>Pris: {car['price']} kr</p>

        <p>Annons ute: {car['days']} dagar</p>

        <p>Marknadspris: {market_price} kr</p>

        <p>Pris under marknad: {percent}%</p>

        <p>{label}</p>

        <p>{seller_signal}</p>

        <p>AI rekommenderat bud: {recommended_bid} kr</p>

        <a href="{car['link']}" target="_blank">🔗 Öppna annons</a>

        <br><br>

        <form action='/bid'>

        <input name='car' value='{car['title']}' hidden>

        <input name='bid' placeholder='Ditt bud'>

        <button>Skicka bud</button>

        </form>

        </div>

        """

    html+="<h2>📡 Deal Radar</h2>"

    deals.sort(key=lambda x: x[0], reverse=True)

    for percent, car in deals:

        if percent>10:

            html+=f"<p><a href='{car['link']}' target='_blank'>{car['title']}</a> - {percent}% under marknad</p>"

    return html


@app.route("/bid")
def bid():

    car=request.args.get("car")
    bid=request.args.get("bid")

    return f"""

    <h2>Mail att skicka</h2>

    <p>Hej,</p>

    <p>Jag är intresserad av din bil {car}.</p>

    <p>Mitt bud är {bid} kr.</p>

    <p>Jag utlovar en smidig affär om du accepterar mitt bud.</p>

    <p>Vänligen återkom till mig.</p>

    """


init_db()


if __name__ == "__main__":

    port=int(os.environ.get("PORT",5000))

    app.run(host="0.0.0.0",port=port)
