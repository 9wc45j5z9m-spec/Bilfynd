import sqlite3

def init_db():

    conn = sqlite3.connect("cars.db")

    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS cars(
        title TEXT,
        brand TEXT,
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
    INSERT INTO cars VALUES (?,?,?,?,?)
    """,(
        car["title"],
        car["brand"],
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
        "brand":r[1],
        "price":r[2],
        "link":r[3],
        "source":r[4]
        })

    return cars
