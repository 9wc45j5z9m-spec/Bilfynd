import os
from flask import Flask, request

app = Flask(__name__)

cars = [
    {"title": "Volvo V90 D4", "price": 219000},
    {"title": "Audi A6 Avant", "price": 229000}
]


def analyze_deal(price):

    market_price = int(price * 1.15)
    discount = market_price - price
    percent = round((discount / market_price) * 100)

    if percent > 20:
        label = "🔥 SUPER DEAL"
    elif percent > 10:
        label = "✅ Bra pris"
    else:
        label = "Normal"

    recommended_bid = int(price * 0.9)

    return market_price, percent, label, recommended_bid


@app.route("/")
def home():

    html = "<h1>🔥 Bilfynd</h1>"

    for car in cars:

        market_price, percent, label, recommended_bid = analyze_deal(car["price"])

        html += f"""
        <div style='border:1px solid #ccc;padding:10px;margin:10px'>

        <h2>{car['title']}</h2>

        <p>Pris: {car['price']} kr</p>

        <p>Marknadspris: {market_price} kr</p>

        <p>Pris under marknad: {percent}%</p>

        <p>{label}</p>

        <p>AI rekommenderat bud: {recommended_bid} kr</p>

        <form action='/bid'>
        <input name='car' value='{car['title']}' hidden>
        <input name='bid' placeholder='Ditt bud'>
        <button>Skicka bud</button>
        </form>

        </div>
        """

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

    """


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
