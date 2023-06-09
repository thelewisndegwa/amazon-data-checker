import sqlite3
from faker import Faker
import sqlalchemy as db

engine = db.create_engine('sqlite:///amazon.db')
connection = engine.connect()
metadata = db.MetaData()

class Supplies:
    supplies_table = db.Table('supplies', metadata,
    db.Column('SupplyID', db.INTEGER, primary_key=True),
    db.Column('SupplyName', db.TEXT),
    db.Column('SupplierID', db.INTEGER, db.ForeignKey('suppliers.SupplierID')),
    db.Column('Quantity', db.INTEGER),
    db.Column('BuyingPrice', db.REAL),
    db.Column('SellingPrice', db.REAL),
)

    def create_supplies_table():
        metadata.create_all(engine)

    def seed_supplies_table():
        conn = sqlite3.connect('amazon.db')
        c = conn.cursor()
        fake = Faker()
        supplies_data = []

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

        # Fetch the available supplier IDs
        query = db.select([db.column('SupplierID')])

        result = connection.execute(query)
        supplier_ids = [row[0] for row in result]

        # Prompt for a valid SupplierID
        SupplierID = None
        while SupplierID not in supplier_ids:
            SupplierID = int(input("Supplier ID: "))

        # Insert the supply with the provided SupplierID
        insertion_query = db.insert(Supplies.supplies_table).values(
            SupplyName=SupplyName,
            SupplierID=SupplierID,
            Quantity=Quantity,
            BuyingPrice=Buying_Price,
            SellingPrice=Selling_Price
        )
        connection.execute(insertion_query)

    def check_supplier_supplies(supplier_id):
        query = db.select(Supplies.supplies_table).where(Supplies.supplies_table.columns.SupplierID == supplier_id)
        result = connection.execute(query)

        if result.rowcount == 0:
            print("No supplies found for the supplier.")
        else:
            print("Supplies for the supplier:")
            for row in result:
                print("Supply ID:", row[0])
                print("Supply Name:", row[1])
                print("Quantity:", row[3])
                print("Buying Price:", row[4])
                print("Selling Price:", row[5])
                 

Supplies.create_supplies_table()
Supplies.seed_supplies_table()
