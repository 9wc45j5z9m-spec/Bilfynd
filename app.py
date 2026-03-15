from flask import Flask, request

app = Flask(__name__)

cars = [
    {"title":"Volvo V90 D4","price":219000,"score":92},
    {"title":"Audi A6 Avant","price":229000,"score":96}
]

@app.route("/")
def home():

    html = "<h1>🔥 Bilfynd</h1>"

    for car in cars:

        html += f"""
        <div style='border:1px solid #ccc;padding:10px;margin:10px'>
        <h2>{car['title']}</h2>
        <p>Pris: {car['price']} kr</p>
        <p>Deal score: {car['score']}</p>
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

    <p>Vänligen återkom med ditt besked.</p>
    """
