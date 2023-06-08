import sqlite3
from faker import Faker

def create_suppliers_table():
    conn = sqlite3.connect('amazon.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS suppliers (
                    SupplierID INTEGER PRIMARY KEY,
                    SupplierName TEXT,
                    SupplierAddress TEXT,
                    ContactNumber TEXT,
                    Email TEXT
                )''')
    conn.commit()
    conn.close()

def seed_suppliers_table():
    conn = sqlite3.connect('amazon.db')
    c = conn.cursor()
    fake = Faker()
    suppliers_data = []
    for _ in range(10):
        supplier_name = fake.name()
        supplier_address = fake.address()
        contact_number = fake.phone_number()
        email = f"{supplier_name}@{fake.domain_name()}"
        suppliers_data.append((None, supplier_name, supplier_address, contact_number, email))
    c.executemany('INSERT INTO suppliers VALUES (?, ?, ?, ?, ?)', suppliers_data)
    conn.commit()
    conn.close()


create_suppliers_table()
seed_suppliers_table()