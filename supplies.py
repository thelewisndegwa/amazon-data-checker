import sqlite3
from faker import Faker
import sqlalchemy as db

engine = db.create_engine('sqlite:///amazon.db')
connection = engine.connect()
metadata = db.MetaData()

class Supplies:
    def create_supplies_table():
        conn = sqlite3.connect('amazon.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS supplies (
                        SupplyID INTEGER PRIMARY KEY,
                        SupplyName TEXT,
                        SupplierID INTEGER,
                        Quantity INTEGER,
                        BuyingPrice REAL,
                        SellingPrice REAL,
                        FOREIGN KEY (SupplierID) REFERENCES suppliers (SupplierID)
                    )''')
        conn.commit()
        conn.close()

    def seed_supplies_table():
        conn = sqlite3.connect('amazon.db')
        c = conn.cursor()
        fake = Faker()
        supplies_data = []

        # Retrieve existing supplier IDs from the suppliers table
        c.execute("SELECT SupplierID FROM suppliers")
        supplier_ids = [row[0] for row in c.fetchall()]

        for _ in range(10):
            supply_name = fake.company()
            supplier_id = fake.random_element(elements=supplier_ids)
            quantity = fake.random_int(min=10, max=50)
            buying_price = fake.random_int(min=1500, max=4000)
            selling_price = buying_price + fake.random_int(min=1500, max=4000)
            supplies_data.append((None, supply_name, supplier_id, quantity, buying_price, selling_price))

        c.executemany('INSERT INTO supplies VALUES (?, ?, ?, ?, ?, ?)', supplies_data)
        conn.commit()
        conn.close()

    def add_supplies():
        SupplyName = input("Supply Name: ")
        Quantity = int(input("Quantity: "))
        Buying_Price = int(input("Buying Price: "))
        Selling_Price = int(input("Selling Price: "))
        insertion_query = db.insert(metadata.tables['supplies']).values(
            SupplyName=SupplyName,
            Quantity=Quantity,
            BuyingPrice=Buying_Price,
            SellingPrice=Selling_Price
        )
        connection.execute(insertion_query)

Supplies.create_supplies_table()
Supplies.seed_supplies_table()

