import sqlite3
from faker import Faker


class Profit:
    def create_profits_table():
        conn = sqlite3.connect('amazon.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS profits (
                        SupplyID INTEGER PRIMARY KEY,
                        SupplyName TEXT,
                        SupplierID INTEGER,
                        SupplierName TEXT,
                        Profit REAL,
                        ProfitPercentage REAL,
                        FOREIGN KEY (SupplyID) REFERENCES supplies (SupplyID),
                        FOREIGN KEY (SupplierID) REFERENCES suppliers (SupplierID)
                    )''')
        conn.commit()
        conn.close()

    def seed_profits_table():
        conn = sqlite3.connect('amazon.db')
        c = conn.cursor()
        fake = Faker()
        profits_data = []

        c.execute("SELECT supplies.SupplyID, supplies.SupplyName, supplies.BuyingPrice, supplies.SellingPrice, supplies.SupplierID, suppliers.SupplierName FROM supplies INNER JOIN suppliers ON supplies.SupplierID = suppliers.SupplierID")
        supplies_data = c.fetchall()

        for supply in supplies_data:
            supply_id, supply_name, buying_price, selling_price, supplier_id, supplier_name = supply
            profit = selling_price - buying_price
            profit_percentage = (profit / buying_price) * 100
            profits_data.append((supply_id, supply_name, supplier_id, supplier_name, profit, profit_percentage))

        c.execute("PRAGMA foreign_keys = ON")  # Enable foreign key support
        c.executemany('INSERT OR REPLACE INTO profits VALUES (?, ?, ?, ?, ?, ?)', profits_data)
        conn.commit()
        conn.close()

    def display_profits(supplier_id):
        conn = sqlite3.connect('amazon.db')
        c = conn.cursor()

        c.execute("SELECT * FROM profits WHERE SupplierID = ?", (supplier_id,))
        profits = c.fetchall()

        print("Profits:")
        print("Supply ID | Supply Name | Supplier ID | Supplier Name | Profit | Profit Percentage")
        for profit in profits:
            supply_id, supply_name, supplier_id, supplier_name, profit_amount, profit_percentage = profit
            print(f"{supply_id} | {supply_name} | {supplier_id} | {supplier_name} | {profit_amount} | {profit_percentage:.2f}%")

        conn.close()



Profit.create_profits_table()
Profit.seed_profits_table()

