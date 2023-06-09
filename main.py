import sqlalchemy as db
engine = db.create_engine('sqlite:///amazon.db')
connection = engine.connect()
metadata = db.MetaData()
from supplies import Supplies
from profit import Profit
from orders import Orders

choice = 0 
while choice != 4: 
    print("***Amazon Data Checker***")
    print("Who is using the program: ")
    print ("1) Supplier")
    print ("2) Customer")
    print ("3) Quit Program")

    choice = int(input("Select a choice >>>"))

    if choice == 1:
         id = int(input("Select your ID >>>"))
         print(f'Welcome Supplier {id}!')
         supplierChoice = 0
         print ("1) Add supply")
         print ("2) See profits")
         print ("3) See your supplies")
         
         supplierChoice = int(input("Select a choice >>>"))
         if supplierChoice == 1:
              Supplies.add_supplies()
          
         elif supplierChoice == 2:
              Profit.display_profits(id)
         elif supplierChoice == 3:
             Supplies.check_supplier_supplies(id)

    elif choice == 2 :
               customerChoice= 0
               print("Welcome Customer!")
               print ("1) Make an order ")
               customerChoice = int(input("Select a choice >>>"))
               if customerChoice == 1:
                Orders.make_order()