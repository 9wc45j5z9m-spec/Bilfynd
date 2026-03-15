from flask import Flask, request

app = Flask(__name__)

cars = [
{
"title":"Volvo V90 D4",
"price":219000,
"score":92,
"image":"https://upload.wikimedia.org/wikipedia/commons/3/3a/Volvo_V90.jpg"
},
{
"title":"Audi A6 Avant",
"price":229000,
"score":96,
"image":"https://upload.wikimedia.org/wikipedia/commons/5/5c/Audi_A6_C8_Avant.jpg"
}
]

@app.route("/")
def home():

html = """

<style>

body{
font-family:Arial;
background:#111;
color:white;
padding:40px;
}

.car{
background:#1c1c1c;
padding:20px;
margin-bottom:20px;
border-radius:10px;
}

img{
width:300px;
border-radius:8px;
}

button{
background:#ff5a00;
color:white;
border:none;
padding:10px;
margin-top:10px;
}

input{
padding:10px;
}

</style>

<h1>🔥 Bilfynd</h1>

"""

for car in cars:

html += f"""

<div class='car'>

<img src="{car['image']}">

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
