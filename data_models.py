import sqlite3

class Model:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS ZodiacSigns
                          (name TEXT, description TEXT, date TEXT)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS TarotCards
                          (name TEXT, description TEXT, image TEXT)''')
        self.conn.commit()

    def insert_zodiac_sign(self, sign):
        self.c.execute("INSERT INTO ZodiacSigns VALUES (?, ?, ?)", (sign.name, sign.description, sign.date))
        self.conn.commit()

    def insert_tarot_card(self, card):
        self.c.execute("INSERT INTO TarotCards VALUES (?, ?, ?)", (card.name, card.description, card.image))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
    
    def get_zodiac_signs(self):
        self.c.execute("SELECT * FROM ZodiacSigns")
        rows = self.c.fetchall()
        signs = [ZodiacSign(row[0], row[1], row[2]) for row in rows]
        return signs

    def get_tarot_cards(self):
        self.c.execute("SELECT * FROM TarotCards")
        rows = self.c.fetchall()
        cards = [TarotCard(row[0], row[1], row[2]) for row in rows]
        return cards

    def remove_duplicates_if_exists(self):
        self.c.execute("DELETE FROM ZodiacSigns WHERE rowid NOT IN (SELECT MIN(rowid) FROM ZodiacSigns GROUP BY name)")
        self.c.execute("DELETE FROM TarotCards WHERE rowid NOT IN (SELECT MIN(rowid) FROM TarotCards GROUP BY name)")
        self.conn.commit()
class ZodiacSign():
    def __init__(self, name, description, date):
        self.name = name
        self.description = description
        self.date = date

class TarotCard():
    def __init__(self, name, description, image):
        self.name = name
        self.description = description
        self.image = image
