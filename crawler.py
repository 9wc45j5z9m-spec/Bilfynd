import random
from database import save_car

def crawl():

    brands=["Volvo","Audi","BMW","Toyota"]

    for i in range(20):

        car={

        "title":f"Annons {i}",
        "brand":random.choice(brands),
        "price":random.randint(180000,320000),
        "link":"https://www.blocket.se",
        "source":"Blocket"

        }

        save_car(car)
