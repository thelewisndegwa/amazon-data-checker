import sqlite3
from faker import Faker

class Orders:
    def create_orders_table():
        conn = sqlite3.connect('amazon.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS orders (
                        OrderID INTEGER PRIMARY KEY,
                        CustomerID INTEGER,
                        SupplyID INTEGER,
                        OrderDate DATE,
                        Distance REAL,
                        TransportCharges REAL,
                        TotalAmount REAL,
                        FOREIGN KEY (CustomerID) REFERENCES customers (CustomerID),
                        FOREIGN KEY (SupplyID) REFERENCES supplies (SupplyID)
                    )''')
        conn.commit()
        conn.close()

    def seed_orders_table():
        conn = sqlite3.connect('amazon.db')
        c = conn.cursor()
        fake = Faker()
        orders_data = []
        
        # Retrieve existing customer and supply IDs from their respective tables
        c.execute("SELECT CustomerID FROM customers")
        customer_ids = [row[0] for row in c.fetchall()]
        
        c.execute("SELECT SupplyID FROM supplies")
        supply_ids = [row[0] for row in c.fetchall()]
        
        for _ in range(10):
            customer_id = fake.random_element(elements=customer_ids)
            supply_id = fake.random_element(elements=supply_ids)
            order_date = fake.date_between(start_date='-1y', end_date='today')
            distance = fake.random_int(min=1, max=10)
            transport_charges = distance * 200
            
            # Retrieve selling price from supplies table based on supply ID
            c.execute("SELECT SellingPrice FROM supplies WHERE SupplyID = ?", (supply_id,))
            selling_price = c.fetchone()[0]
            
            total_amount = transport_charges + selling_price
            orders_data.append((None, customer_id, supply_id, order_date, distance, transport_charges, total_amount))
        
        c.executemany('INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?)', orders_data)
        conn.commit()
        conn.close()

    create_orders_table()
    seed_orders_table()
    

    def make_order():
        conn = sqlite3.connect('amazon.db')
        c = conn.cursor()

        # Print available supplies
        print("Available Supplies:")
        c.execute("SELECT * FROM supplies")
        supplies = c.fetchall()
        for supply in supplies:
            print(supply)

        # Prompt user for supply ID
        supply_id = int(input("Enter the Supply ID you want to order: "))

        # Prompt user for distance
        distance = int(input("Enter the distance for delivery: "))

        # Retrieve supply details
        c.execute("SELECT SellingPrice FROM supplies WHERE SupplyID = ?", (supply_id,))
        selling_price = c.fetchone()[0]
        transport_charges = distance * 200
        total_amount = transport_charges + selling_price

        print(f"Total Cost: {total_amount}")

        # Insert order into orders table
        c.execute("INSERT INTO orders (CustomerID, SupplyID, OrderDate, Distance, TransportCharges, TotalAmount) VALUES (?, ?, date('now'), ?, ?, ?)",
                (1, supply_id, distance, transport_charges, total_amount))  # Assuming CustomerID is 1 for this example

        # Delete the supply from supplies table
        c.execute("DELETE FROM supplies WHERE SupplyID = ?", (supply_id,))

        conn.commit()
        conn.close()