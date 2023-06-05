import sqlite3
from faker import Faker

def create_customers_table():
    conn = sqlite3.connect('amazon.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS customers (
                    CustomerID INTEGER PRIMARY KEY,
                    CustomerName TEXT,
                    CustomerAddress TEXT,
                    ContactNumber TEXT,
                    Email TEXT
                )''')
    conn.commit()
    conn.close()

def seed_customers_table():
    conn = sqlite3.connect('amazon.db')
    c = conn.cursor()
    fake = Faker()
    customers_data = []
    for _ in range(10):
        customer_name = fake.name()
        customer_address = fake.address()
        contact_number = fake.phone_number()
        email = fake.email()
        customers_data.append((None, customer_name, customer_address, contact_number, email))
    c.executemany('INSERT INTO customers VALUES (?, ?, ?, ?, ?)', customers_data)
    conn.commit()
    conn.close()

create_customers_table()
seed_customers_table()