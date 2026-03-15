import os
import random
from flask import Flask, request

app = Flask(__name__)

cars = [
{"title":"Volvo V90 D4","brand":"Volvo","price":219000,"days":5,"link":"https://www.blocket.se"},
{"title":"Audi A6 Avant","brand":"Audi","price":229000,"days":18,"link":"https://www.blocket.se"},
{"title":"BMW 520d Touring","brand":"BMW","price":239000,"days":10,"link":"https://www.wayke.se"},
{"title":"Toyota RAV4 Hybrid","brand":"Toyota","price":259000,"days":3,"link":"https://www.bytbil.com"},
{"title":"Tesla Model 3","brand":"Tesla","price":349000,"days":1,"link":"https://www.blocket.se"},
{"title":"Mercedes E220d","brand":"Mercedes","price":279000,"days":25,"link":"https://www.bytbil.com"}
]


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

    seller_signal = ""

    if days > 20:
        seller_signal = "📉 Motiverad säljare"

    return market_price, percent, label, recommended_bid, seller_signal


def pro_scan():

    sources = [
    ("Blocket","https://www.blocket.se"),
    ("Wayke","https://www.wayke.se"),
    ("Bytbil","https://www.bytbil.com")
    ]

    found = []

    for i in range(12):

        source = random.choice(sources)

        found.append({

        "title":f"Bilannons {i+1}",
        "brand":random.choice(["Volvo","BMW","Audi","Toyota"]),
        "price":random.randint(180000,320000),
        "days":random.randint(1,30),
        "link":source[1],
        "source":source[0]

        })

    return found


@app.route("/scan")
def scan():

    results = pro_scan()

    html = "<h1>🔎 Scannerresultat</h1>"

    for car in results:

        html += f"""
        <div style='border:1px solid #ccc;padding:10px;margin:10px'>

        <h2>{car['title']}</h2>

        <p>Märke: {car['brand']}</p>

        <p>Pris: {car['price']} kr</p>

        <p>Källa: {car['source']}</p>

        <a href="{car['link']}" target="_blank">🔗 Öppna annons</a>

        </div>
        """

    return html


@app.route("/")
def home():

    html = """
    <h1>🔥 Bilfynd AI</h1>

    <p><a href="/scan">🚀 Kör AI Scanner</a></p>

    <hr>
    """

    deals = []

    for car in cars:

        market_price, percent, label, recommended_bid, seller_signal = analyze_deal(car["price"],car["days"])

        deals.append((percent, car))

        html += f"""

        <div style='border:1px solid #ccc;padding:10px;margin:10px'>

        <h2>{car['title']}</h2>

        <p>Märke: {car['brand']}</p>

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

    html += "<h2>📡 Deal Radar</h2>"

    deals.sort(key=lambda x: x[0], reverse=True)

    for percent, car in deals:

        if percent > 10:

            html += f"<p><a href='{car['link']}' target='_blank'>{car['title']}</a> - {percent}% under marknad</p>"

    return html


@app.route("/bid")
def bid():

    car = request.args.get("car")
    bid = request.args.get("bid")

    return f"""

    <h2>Mail att skicka</h2>

    <p>Hej,</p>

    <p>Jag är intresserad av din bil {car}.</p>

    <p>Mitt bud är {bid} kr.</p>

    <p>Jag utlovar en smidig affär om du accepterar mitt bud.</p>

    <p>Vänligen återkom till mig.</p>

    """


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)
