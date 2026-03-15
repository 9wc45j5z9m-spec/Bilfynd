import os
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

cars = [
{"title":"Volvo V90 D4","brand":"Volvo","price":219000,"days":5},
{"title":"Audi A6 Avant","brand":"Audi","price":229000,"days":18},
{"title":"BMW 520d Touring","brand":"BMW","price":239000,"days":10},
{"title":"Toyota RAV4 Hybrid","brand":"Toyota","price":259000,"days":3},
{"title":"Tesla Model 3","brand":"Tesla","price":349000,"days":1},
{"title":"Mercedes E220d","brand":"Mercedes","price":279000,"days":25}
]


def analyze_deal(price, days):

    market_price = int(price * 1.15)

    discount = market_price - price
    percent = round((discount / market_price) * 100)

    recommended_bid = int(price * 0.9)

    if percent > 20:
        label = "🔥 SUPER DEAL"
    elif percent > 10:
        label = "✅ Bra pris"
    else:
        label = "Normal"

    seller_signal = "Normal"

    if days > 20:
        seller_signal = "📉 Motiverad säljare"

    return market_price, percent, label, recommended_bid, seller_signal


def pro_scan():

    sources = [
    "Blocket",
    "Wayke",
    "Bytbil"
    ]

    found = []

    for i in range(10):

        found.append({

        "title":f"Bilfynd {i+1}",
        "brand":random.choice(["Volvo","BMW","Audi","Toyota"]),
        "price":random.randint(180000,320000),
        "days":random.randint(1,30),
        "source":random.choice(sources)

        })

    return found


@app.route("/scan")
def scan():

    results = pro_scan()

    return {"found":results}


@app.route("/api/cars")
def api():

    return jsonify(cars)


@app.route("/")
def home():

    brand_filter = request.args.get("brand")
    max_price = request.args.get("max_price")

    filtered = cars

    if brand_filter:
        filtered = [c for c in filtered if c["brand"] == brand_filter]

    if max_price:
        filtered = [c for c in filtered if c["price"] <= int(max_price)]

    html = """
    <h1>🔥 Bilfynd Pro</h1>

    <form>

    Märke:
    <select name="brand">
    <option value="">Alla</option>
    <option>Volvo</option>
    <option>Audi</option>
    <option>BMW</option>
    <option>Toyota</option>
    <option>Tesla</option>
    <option>Mercedes</option>
    </select>

    Maxpris:
    <input name="max_price" placeholder="t.ex 250000">

    <button>Filtrera</button>

    </form>

    <p><a href="/scan">🚀 Kör Pro Scanner</a></p>

    <hr>
    """

    deals = []

    for car in filtered:

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

            html += f"<p>{car['title']} - {percent}% under marknad</p>"

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
