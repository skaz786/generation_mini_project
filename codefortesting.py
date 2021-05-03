
import sys
import csv
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()
host = os.environ.get("mysql_host")
user = os.environ.get("mysql_user")
password = os.environ.get("mysql_pass")
database = os.environ.get("mysql_db")


products = []
couriers = []
orders_list = []

products_csv = "c:\\Users\\sabih\\OneDrive\\Documents\\pythongeneration\\pythonminiproject\\data\\products.csv"
couriers_csv = "c:\\Users\\sabih\\OneDrive\\Documents\\pythongeneration\\pythonminiproject\\data\\couriers.csv"
orders_csv = "c:\\Users\\sabih\\OneDrive\\Documents\\pythongeneration\\pythonminiproject\\data\\orders.csv"

#------------------------------------------SQL CODE-----------------------------------------------------------

def connection_to_db():
    connection = pymysql.connect(
    host = host,
    user = user,
    password = password,
    database = database
    )
    return connection

def print_items_to_screen(table):
    connection = connection_to_db()
    cursor = connection.cursor()

    if table == "products":
        cursor.execute('SELECT * FROM products')
        rows = cursor.fetchall()
        for row in rows:
            print("\n")
            print(f'Product ID: {str(row[0])}\nProduct: {row[1]}\nPrice: {row[2]}')
    elif table == "couriers":
        cursor.execute('SELECT * FROM couriers')
        rows = cursor.fetchall()
        for row in rows:
            print("\n")
            print(f'Courier ID: {str(row[0])}\nName: {row[1]}\nPhone: {row[2]}')
    elif table == "orders":
        cursor.execute('SELECT * FROM orders')
        rows = cursor.fetchall()
        for row in rows:
            print("\n")
            print(f'Order ID: {str(row[0])}\nName: {row[1]}\nAddress: {row[2]}\nPostcode: {row[3]}\nPhone: {row[4]}\nCourier: {row[5]}\nStatus: {row[6]}\nItems: {row[7]}')
    cursor.close()
    connection.close()

#------------------------------------------SQL PRODUCTS CODE--------------------------------------------------

def append_product_table_to_list():
    products.clear()
    connection = connection_to_db()
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM products')
    rows = cursor.fetchall()
    for row in rows:
        pd = {"Product ID": str(row[0]), "Product": (row[1]), "Price": (row[2])}
        products.append(pd)

            
    cursor.close()
    connection.close()
    cache_products_table()


def add_product_name(userinput):
    print(("\nEnter name of new product\nor 0 to go back:\n"))
    while True:
        new_product_name = userinput()
        d = dict((i['Product'], i['Price']) for i in products)
        
        if new_product_name == str(0):
            product_menu()
            break
    
        try:      
            v = int(new_product_name)
        except:
            if new_product_name == "":
                print("Please enter a valid name")
                continue
            elif new_product_name in d:
                print("This product already exists, Please try again")
                continue
            else:
                print("\n{} has been added as a new product".format(new_product_name.lower()))
                return new_product_name.lower()
                break      
        else:
            print("Product cannot be a number")
            continue

def add_product_price():
    
    while True:
        try:
            new_product_price = float(input("\nEnter price of new product:\n"))
            if new_product_price == "":
                print("Please enter a valid value")
                continue
            elif type(new_product_price) == int or type(new_product_price) == float:
                print("\n{} has been added as the product price".format(new_product_price))
                return new_product_price
                break  
        except:
            print("Please enter a valid value")
            continue

def add_new_product_db():
    
    print_items_to_screen("products")
    
    connection = connection_to_db()
    cursor = connection.cursor()
    
    product_input = add_product_name(input)
    price_input = add_product_price()
    
    sql = "INSERT INTO products (product_name, product_price) VALUES (%s, %s)"
    val = (product_input, price_input)
    cursor.execute(sql, val)
    
    connection.commit()
    cursor.close()
    connection.close()
    
    append_product_table_to_list()
    cache_products_table()
    
    print("\nProduct has been added:\n")
    print_new_entry(products)



def id_update_product_func():
    append_product_table_to_list
    while True:
        id_input = input("\nChoose the ID of the product you want to update:\n")
        if id_input == "":
            print("Please enter an ID value")
            continue
        try:
            v = int(id_input)
        except:
            ("Please enter a ID value")
            continue
        else:
            for product in products:
                x = 0
                if id_input == product["Product ID"]:
                    print("This is the product to be updated:\n")
                    print(product)
                    x += 1
                    break
                else:
                    continue
            if x == 1:
                return id_input
                break
            else:
                incorrect_function()
                continue

def showing_current_product_name(id):
    for product in products:
        if product["Product ID"] == id:
            current_product = product["Product"]
            print("\nCurrent Product Name: {}" .format(current_product.title()))
            return current_product
            break
        else:
            continue

def update_chosen_product(current):
    d = dict((i['Product'], i['Price']) for i in products)
    while True:
        upd = input("\nType updated product name or press enter to skip:\n")
        if upd == "":
            return current
            break
        try:
            v = int(upd)
        except:
            if upd in d:
                print("This product already exists, Please try again")
                continue
            else:
                print("Name had been updated")
                return str(upd)
                break
        else:
            print("Product cannot be a number")
            continue

def showing_current_price(id):
    append_product_table_to_list()
    
    for product in products:
        if product["Product ID"] == id:
            current_price = product["Price"]
            print("Current Price: {}" .format(current_price))
            return current_price
            break
        else:
            continue

def update_chosen_price(current):    
    
    while True:
        new_product_price = input("\nType price of new product or press enter to skip:\n")
        if new_product_price == "":
            return current
            break    
        elif type(new_product_price) == int or type(new_product_price) == float:
            print("\n{} has been added as the product price".format(new_product_price))
            return new_product_price
            break  
        else:
            print("Please enter a valid value")
            continue

def update_product_db():

    print_items_to_screen("products")
    
    connection = connection_to_db()
    cursor = connection.cursor()  

    id_input = id_update_product_func()
    
    current_product = showing_current_product_name(id_input)
    updated_product = update_chosen_product(current_product) 
    
    current_price = showing_current_price(id_input) 
    updated_price = update_chosen_price(current_price)

    sql = ("UPDATE products SET product_name = %s, product_price = %s WHERE product_id = %s")
    val = (updated_product, updated_price, id_input)
    cursor.execute(sql, val)  
    
    connection.commit()
    cursor.close()
    connection.close()  
    
    append_product_table_to_list()
    cache_products_table()  
    
    print("\nUPDATED PRODUCT:\n")
    print_updated_entry(products, "Product ID", id_input)



def product_to_delete_func():
    while True:
        id_input = input("\nChoose the ID of the product you want to delete or 0 to go back:\n")
        if id_input == "0":
            return None
            break
        else:
            try:
                v = int(id_input)
            except:
                incorrect_function()
                continue
            else:
                x = 0
                for product in products:
                    if id_input == product["Product ID"]:
                        print("This is the product to be deleted:\n")
                        print(product)
                        x += 1
                        break
                    else:
                        continue
                if x == 1:
                    return id_input
                    break
                else:
                    incorrect_function()
                    continue

def delete_product_db(id):
    
    connection = connection_to_db()
    cursor = connection.cursor()

    product_to_delete = id
    
    sql = "DELETE FROM products WHERE product_id = %s"
    val = (product_to_delete)
    cursor.execute(sql, val)
    
    connection.commit()
    cursor.close()
    connection.close()
    
    append_product_table_to_list()
    cache_products_table()
    
    print("\nProduct has been deleted")

#------------------------------------------SQL COURIERS CODE--------------------------------------------------

def append_courier_table_to_list():
    couriers.clear()
    connection = connection_to_db()
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM couriers')
    rows = cursor.fetchall()
    for row in rows:
        pd = {"Courier ID": str(row[0]), "Name": (row[1]), "Phone": (row[2])}
        couriers.append(pd)
    cursor.close()
    connection.close()
    cache_couriers_table()


def add_courier_name():
    
    while True:
        new_courier_name = (input("\nEnter name of new courier\nor 0 to go back:\n".lower()))
        
        if new_courier_name == str(0):
            courier_menu()
            break
    
        try:      
            v = int(new_courier_name)
        except:
            if new_courier_name == "":
                print("Please enter a valid name")
                continue
            else:
                print("\n{} has been added as a new courier".format(new_courier_name.lower()))
                return new_courier_name
                break      
        else:
            print("courier name cannot be a number")
            continue

def add_courier_phone():
    while True:
        try:
            new_courier_phone = int(input("\nEnter phone contact of new courier:\n"))
            if new_courier_phone == "":
                incorrect_function()
                continue
            elif len(str(new_courier_phone)) == 10:
                print("\n{} has been added as the courier number".format(new_courier_phone))
                return new_courier_phone
                break
            else:
                print("Please enter a valid phone number")
                continue
        except:
            print("Please enter a valid value")
            continues

def add_new_courier_db():  
    
    print_items_to_screen("couriers")  
    
    connection = connection_to_db()
    cursor = connection.cursor()  

    courier_input = add_courier_name()
    number_input = str(add_courier_phone())
    
    sql = "INSERT INTO couriers (courier_name, courier_number) VALUES (%s, %s)"
    val = (courier_input, str(number_input))
    cursor.execute(sql, val)  
    
    connection.commit()
    cursor.close()
    connection.close()  
    
    append_courier_table_to_list()
    cache_couriers_table()
    
    print("\nCourier has been added:\n")
    print_new_entry(couriers)



def id_update_courier_func():
    append_courier_table_to_list()
    while True:
        id_input = input("\nChoose the ID of the courier you want to update:\n")
        if id_input == "":
            print("Please enter an ID value")
            continue
        try:
            v = int(id_input)
        except:
            ("Please enter a ID value")
            continue
        else:
            for courier in couriers:
                x = 0
                if id_input == courier["Courier ID"]:
                    print("This is the courier to be updated:\n")
                    print(courier)
                    x += 1
                    break
                else:
                    continue
            if x == 1:
                return id_input
                break
            else:
                incorrect_function()
                continue

def showing_current_courier_name(id):
    for courier in couriers:
        if courier["Courier ID"] == id:
            current_courier = courier["Name"]
            print("\nCurrent Courier Name: {}" .format(current_courier.title()))
            return current_courier
            break
        else:
            continue

def update_chosen_courier_name(current):
    while True:
        upd = input("\nType updated courier name or press enter to skip:\n")
        if upd == "":
            return current
            break
        try:
            v = int(upd)
        except:
                print("Name had been updated")
                return str(upd)
                break
        else:
            print("courier name cannot be a number")
            continue

def showing_current_courier_phone(id):
    for courier in couriers:
        if courier["Courier ID"] == id:
            current_courier = courier["Phone"]
            print("\nCurrent Courier Phone: {}" .format(current_courier.title()))
            return current_courier
            break
        else:
            continue

def update_chosen_courier_phone(current_phone):
    while True:
        updated_phone = (input("\nPlease enter updated phone or enter to skip:\n"))
        if updated_phone == "":
            return (current_phone)
            break
        else:
            try:
                v = int(updated_phone)
            except:
                print("Please enter a valid value")
                continue
            else:
                if len(str(v)) == 10:
                    print("\n{} has been added as a new customer phone".format(updated_phone.upper()))
                    return (updated_phone)
                    break
                else:
                    print("Please enter a valid phone number")
                    continue

def update_courier_db(): 
    
    print_items_to_screen("couriers")
    
    connection = connection_to_db()
    cursor = connection.cursor()  
    
    cursor.execute("SELECT * FROM couriers")
    rows = cursor.fetchall()  
    
    id_input = id_update_courier_func()
    
    current_name = showing_current_courier_name(id_input)
    updated_name = update_chosen_courier_name(current_name)
    
    current_phone = showing_current_courier_phone(id_input)
    updated_phone = update_chosen_courier_phone(current_phone)
    
    sql = "UPDATE couriers SET courier_name = %s, courier_number = %s WHERE courier_id = %s"
    val = (updated_name, updated_phone, id_input)
    cursor.execute(sql, val)  
    
    connection.commit()
    cursor.close()
    connection.close()  
    
    append_courier_table_to_list()
    cache_couriers_table()  
    
    print("\nUPDATED COURIER:\n")
    print_updated_entry(couriers, "Courier ID", id_input)



def check_against_orders(id):
    append_order_table_to_list
    orders_using_courier = []
    print("\nChecking against orders")
    for order in orders_list:
        if order["Courier ID"] == int(id):
            orders_using_courier.append(order["Order ID"])
            continue
        else:
            continue
    
    if not orders_using_courier:
        print("\nCourier is not in any orders")
        return id
    else:
        print ("\nCourier found in order(s):")
        print(orders_using_courier)
        print("\nSorry, this courier is being used for orders,\nplease choose a new courier for the order before deleting\n")
        return None

def courier_to_delete_func():
    while True:
        id_input = input("\nChoose the ID of the courier you want to delete or 0 to go back:\n")
        if id_input == str(0):
            return None
            break
        else:
            try:
                v = int(id_input)
            except:
                incorrect_function()
                continue
            else:
                x = 0
                for courier in couriers:
                    if id_input == courier["Courier ID"]:
                        print("This is the courier to be deleted:\n")
                        print(courier)
                        x += 1
                        break
                    else:
                        continue
                if x == 1:
                    return id_input
                    break
                else:
                    incorrect_function()
                    continue

def delete_courier_db(id):
    
    connection = connection_to_db()
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM couriers")
    rows = cursor.fetchall()
    
    courier_to_delete = id
    
    sql = "DELETE FROM couriers WHERE courier_id = %s"
    val = (courier_to_delete)
    cursor.execute(sql, val)
    
    connection.commit()
    cursor.close()
    connection.close()
    
    append_courier_table_to_list()
    cache_couriers_table()
    
    print("Courier has been deleted")

#------------------------------------------SQL ORDERS CODE--------------------------------------------------

def append_order_table_to_list():
    orders_list.clear()
    connection = connection_to_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM orders')
    rows = cursor.fetchall()
    for row in rows:
        pd = {"Order ID": str(row[0]), "Customer Name": (row[1]), "Customer Address": (row[2]), "Customer Postcode": (row[3]), "Customer Phone": (row[4]), "Courier ID": (row[5]), "Order Status": (row[6]), "Items": (row[7])}
        orders_list.append(pd)

    cursor.close()
    connection.close()
    cache_couriers_table()


def add_customer_name():  
    while True:
        new_customer_name = (input("\nEnter firstname and surname of new customer\nor 0 to go back:\n".title()))      
        if new_customer_name == str(0):
            order_menu()
            break  
        try:      
            v = int(new_customer_name)
        except:
            if new_customer_name == "":
                print("Please enter a valid name")
                continue
            elif len(new_customer_name) < 2:
                print("Please enter the full name")
                continue
            else:
                print("\n{} has been added as a new customer".format(new_customer_name.title()))
                return (new_customer_name.title())
                break      
        else:
            print("customer name cannot be a number")
            continue

def add_customer_address():  
    while True:
        new_customer_address = (input("\nEnter address of new customer:\n".title()))
        try:      
            v = int(new_customer_address)
        except:
            if new_customer_address == "":
                print("Please enter a valid address")
                continue
            elif len(new_customer_address) < 5:
                print("Please enter the full address")
                continue
            else:
                print("\n{} has been added as a new customer address".format(new_customer_address.title()))
                return new_customer_address
                break
        else:
            print("Please enter the full address")
            continue

def add_customer_postcode():  
    while True:
        new_customer_postcode = (input("\nEnter Postcode:\n".lower()))
        try:      
            v = new_customer_postcode
            if new_customer_postcode == "":
                print("Please enter a valid postcode")
                continue
            elif len(new_customer_postcode) > 9:
                print("Please enter a valid postcode")
                continue
            else:
                print("\n{} has been added as a new customer postcode".format(new_customer_postcode.upper()))
                return new_customer_postcode
                break 
        except:
            incorrect_function()
            continue

def add_customer_phone():
    while True:
            new_customer_phone = (input("\nEnter phone contact of new customer:\n"))
            if new_customer_phone == "":
                print("Cannot leave blank")
                continue
            try:
                v = int(new_customer_phone)
            except:
                print("Please enter a number")
                continue
            else:
                if len(str(v)) != 10:
                    print("Please enter a full number")
                    continue
                else:
                    print("\n{} has been added as the customer phone".format(new_customer_phone))
                    return v
                    break  

def choose_courier():
    print("\n")
    print_items_to_screen("couriers")
    
    while True:
        chosen_courier = (input("\nPlease enter the ID for the courier of your choice:\n"))
        if chosen_courier == "":
            print ("Please choose a courier")
            continue
        else:
            try:
                v = int(chosen_courier)
            except:
                incorrect_function()
                continue
            else:
                x = 0
                for courier in couriers:
                    if chosen_courier in courier["Courier ID"]:
                        name = courier["Name"]
                        print("\n {} is your chosen courier".format(name.title()))
                        x +=1
                        break
                    else:
                        continue
                if x ==1:
                    return chosen_courier
                    break        
                else:
                    incorrect_function()
                    continue

def choose_orders():
    product_order_list = []
    print("\n")
    print_items_to_screen("products")
    
    while True:
        product_entry = (input("\nPlease enter the ID for the product you would like or enter 0 to cancel:\n"))
        if product_entry == "":
            print("Please choose an ID")
            continue
        else:
            try:
                v = int(product_entry)
            except:
                incorrect_function()
                continue
            else:
                if product_entry == str(0):
                        if len(product_order_list) > 0:
                            print("\nThis is your product order:\n")
                            print(product_order_list)
                            return (','.join(product_order_list))
                            break
                        else:
                            print("Please add items to your order")
                            continue
                for product in products:
                    if product_entry in str(product["Product ID"]):
                        product_order_list.append(product["Product ID"])
                        print("Product has been added")
                        break
                    else:
                        continue
                continue

def add_new_order_db():    
    
    connection = connection_to_db()
    cursor = connection.cursor()    

    customer_name = add_customer_name()
    address = add_customer_address()
    postcode = add_customer_postcode()
    phone = add_customer_phone()
    chosen_courier = choose_courier()
    order_status = "Preparing"
    items = choose_orders()

    sql = "INSERT INTO orders (customer_name, customer_address, customer_postcode, customer_number, courier_id, order_status, order_items)  VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (customer_name, address, postcode, phone, chosen_courier, order_status, items)
    cursor.execute(sql, val)    
    
    connection.commit()
    cursor.close()
    connection.close()    
    
    append_order_table_to_list()
    cache_orders_table()
    print("\nOrder has been added:\n")
    print_new_entry(orders_list)



def id_update_order_func():
    append_order_table_to_list()
    while True:
        id_input = input("\nChoose the ID of the order you want to update:\n")
        if id_input == "":
            print("Please enter an ID value")
            continue
        try:
            v = int(id_input)
        except:
            ("Please enter a ID value")
            continue
        else:
            for order in orders_list:
                x = 0
                if id_input == order["Order ID"]:
                    print("\nThis is the order to be updated:\n")
                    print(order)
                    x += 1
                    break
                else:
                    continue
            if x == 1:
                return id_input
                break
            else:
                incorrect_function()
                continue            

def showing_current_status(id):
    append_order_table_to_list()
    for order in orders_list:
        for key, value in order.items():
            if order["Order ID"] == id:
                current_status = order["Order Status"]
                print("\nCurrent Status: {}" .format(current_status))
                return current_status
                break
            else:
                continue

def update_order_status_func(current_status):
    
    status_list = ["Cancelled","Preparing","Out for Delivery", "Delivered"]
    
    print("\nOrder Statuses:\n")
    for i, stat in enumerate(status_list):
        print("{}) {}".format(i, stat))
    
    while True:
        updated_status = (input("\nSelect the number corresponding to the status of your choice or Enter to skip\n"))
        if updated_status == "":
            return current_status
            break
        else:
            try:
                v = int(updated_status)
            except:
                print("Please enter a number")
                continue
            else:
                x = 0
                for i, stat in enumerate(status_list):    
                    if updated_status == str(i):
                        new = stat
                        print("status updated to: {}".format(new))
                        x+=1
                        break
                    else:
                        continue
                if x ==1:
                    return new
                    break
                else:
                    incorrect_function()
                    continue



def showing_current_name(id):
    for order in orders_list:
        for key, value in order.items():
            if order["Order ID"] == id:
                current_name = order["Customer Name"]
                print("Current Customer Name: {}" .format(current_name.title()))
                return current_name
                break
            else:
                continue

def update_order_name(current_name):
    while True:
        updated_name = (input("\nPlease enter updated name or enter to skip:\n"))
        if updated_name == "":
            return (current_name.title())
            break
        else:
            try:      
                v = int(updated_name)
            except:
                if len(updated_name) < 2:
                    print("Please enter the full name")
                    continue
                else:
                    print("\n{} has been added as a new customer".format(updated_name.title()))
                    return (updated_name.title())
                    break      
            else:
                print("customer name cannot be a number")
                continue


def showing_current_address(id):
    for order in orders_list:
        for key, value in order.items():
            if order["Order ID"] == id:
                current_address = order["Customer Address"]
                print("Current Customer Address: {}" .format(current_address.title()))
                return current_address
                break
            else:
                continue

def update_order_address(current_address):
    while True:
        updated_address = (input("\nPlease enter updated address or enter to skip:\n"))
        if updated_address == "":
            return (current_address.title())
            break
        else:
            if len(updated_address) < 5:
                print("Please enter the full address")
                continue
            print("\n{} has been added as a new customer address".format(updated_address.title()))
            return (updated_address.title())
            break   


def showing_current_postcode(id):
    for order in orders_list:
        for key, value in order.items():
            if order["Order ID"] == id:
                current_postcode = order["Customer Postcode"]
                print("Current Customer Postcode: {}" .format(current_postcode.upper()))
                return current_postcode
                break
            else:
                continue

def update_order_postcode(current_postcode):
    while True:
        updated_postcode = (input("\nPlease enter updated postcode or enter to skip:\n"))
        if updated_postcode == "":
            return (current_postcode.upper())
            break
        else:
            if len(updated_postcode)> 9:
                print("Please enter valid postcode")
                continue
            else:
                print("\n{} has been added as a new customer postcode".format(updated_postcode.upper()))
                return (updated_postcode.upper())
                break   


def showing_current_phone(id):
    for order in orders_list:
        for key, value in order.items():
            if order["Order ID"] == id:
                current_phone = order["Customer Phone"]
                print("Current Customer Phone: {}" .format(current_phone))
                return current_phone
                break
            else:
                continue

def update_order_phone(current_phone):
    while True:
        updated_phone = (input("\nPlease enter updated phone or enter to skip:\n"))
        if updated_phone == "":
            return (current_phone.upper())
            break
        else:
            try:
                v = int(updated_phone)
            except:
                print("Please enter a valid number")
                continue
            else:
                if len(str(v)) == 10:
                    print("\n{} has been added as a new customer phone".format(updated_phone.upper()))
                    return (updated_phone.upper())
                    break
                else:
                    print("Please enter a valid number")
                    continue


def showing_current_courier(id):
    append_courier_table_to_list()
    for order in orders_list:
        for key, value in order.items():
            if order["Order ID"] == id:
                current_courier = order["Courier ID"]
                print("Current Courier ID: {}".format(current_courier))
                return current_courier
                break
            else:
                continue

def update_order_courier(current_courier):
    append_courier_table_to_list()
    
    print("\nID : Name")
    for courier in couriers:
        print("{} : {}".format(courier["Courier ID"], courier["Name"]))
        
    while True:
        updated_courier = (input("\nPlease enter the ID for the courier of your choice or press enter to skip:\n"))
        if updated_courier == "":
            return (current_courier)
            break
        else:
            try:
                v = int(updated_courier)
            except:
                incorrect_function()
                continue
            else:
                x = 0
                for courier in couriers:
                    if updated_courier in courier["Courier ID"]:
                        name = courier["Name"]
                        print("\n {} is your updated courier".format(name.title()))
                        x +=1
                        break
                    else:
                        continue
                if x ==1:
                    return updated_courier
                    break        
                else:
                    incorrect_function()
                    continue


def showing_current_products(id):
    append_product_table_to_list()
    for order in orders_list:
        for key, value in order.items():
            if order["Order ID"] == id:
                current_products = order["Items"]
                print("Current products: {}" .format(current_products))
                return current_products
                break
            else:
                continue

def update_order_products(current_products):

    while True:
        updated_products = (input("\nPlease enter 1 to update order products or enter to skip:\n"))
        if updated_products == "":
            old  = list(current_products.split(",")) 
            return (','.join(old))
            break
        elif updated_products == "1":
            new_list = choose_orders()
            return new_list
        else:
            continue


def update_order_status_db():   
    
    print_items_to_screen("orders")  
    
    connection = connection_to_db()
    cursor = connection.cursor()    
    
    id_input = id_update_order_func()
    current = showing_current_status(id_input)
    updated_status = update_order_status_func(current)    
    
    sql = ("UPDATE orders SET order_status = %s WHERE order_id = %s")
    val = (updated_status, id_input)
    cursor.execute(sql, val)    
    
    connection.commit()
    cursor.close()
    connection.close()    
    
    append_order_table_to_list()
    cache_orders_table()    
    
    print("\nUPDATED ORDER:\n")
    print_updated_entry(orders_list,"Order ID", id_input)

def update_order_db():     
    
    append_order_table_to_list()
    print_items_to_screen("orders")    
    
    connection = connection_to_db()
    cursor = connection.cursor()
    
    id_input = id_update_order_func()
    
    current_name = showing_current_name(id_input)
    updated_name = update_order_name(current_name)
    
    current_address = showing_current_address(id_input)
    updated_address = update_order_address(current_address)
    
    current_postcode = showing_current_postcode(id_input)
    updated_postcode = update_order_postcode(current_postcode)
    
    current_phone = showing_current_phone(id_input)
    updated_phone = update_order_phone(current_phone)
    
    current_courier = showing_current_courier(id_input)
    updated_courier = update_order_courier(current_courier) 
    
    current_status = showing_current_status(id_input)
    updated_status = update_order_status_func(current_status)
    
    current_products = showing_current_products(id_input) 
    updated_products = update_order_products(current_products)
    
    sql = ("UPDATE orders SET customer_name = %s, customer_address = %s, customer_postcode = %s, customer_number = %s, courier_id = %s, order_status = %s, order_items = %s WHERE order_id = %s")
    val = (updated_name, updated_address, updated_postcode, updated_phone, updated_courier, str(updated_status), updated_products, id_input)
    cursor.execute(sql, val)     
    
    connection.commit()
    cursor.close()
    connection.close()      
    
    append_order_table_to_list()
    cache_orders_table()      
    
    print("\nUPDATED ORDER LIST:\n")
    print_updated_entry(orders_list,"Order ID", id_input)


def choose_order_delete():
    while True:
        id_input = input("\nChoose the ID of the order you want to delete or 0 to go back:\n")
        if id_input == str(0):
            return None
            break   
        else:
            try:
                v = int(id_input)
            except:
                incorrect_function()
                continue
            else:
                x = 0
                for order in orders_list:
                    if id_input == order["Order ID"]:
                        print("This is the order to be deleted:\n")
                        for key, value in order.items():
                            print("{}: {}".format(key, value))
                            x += 1
                            break
                    else:
                        continue
                if x == 1:
                    return id_input
                    break
                else:
                    incorrect_function()
                    continue

def delete_order_db(id):
    connection = connection_to_db()
    cursor = connection.cursor()
    
    order_to_delete = id
    
    sql = ("DELETE FROM orders WHERE order_id = %s")
    val = (order_to_delete)
    cursor.execute(sql, val)
    
    connection.commit()
    cursor.close()
    connection.close()
    
    append_order_table_to_list()
    cache_orders_table()
    
    print("\n Order has been deleted.\n")
    print("\nNEW ORDER LIST:\n")
    print_items_to_screen("orders")


#------------------------------------------LOADING CSV FILES INTO LISTS------------------------------------------

def load_products_file():
    products.clear()
    try:
        with open(products_csv, "r") as file:
            csv_file = csv.DictReader(file)  
            for row in csv_file:
                    products.append(row)
    except FileNotFoundError as fnfe:
        print('Unable to open file: ' + str(fnfe))
    except Exception as e:
        print('An error occurred: ' + str(e))

def print_products_list():
    print("Current List:\n")
    print("PRODUCT ----------> PRICE\n")
    for i, product in enumerate(products):
        price_float = "{:.2f}".format(float(product["Price"]))
        print("{})".format("Product ID")+product["Product"]+" ----------> £"+ str(price_float))

def load_couriers_file():
    couriers.clear()
    try:
        with open(couriers_csv, "r") as file:
            csv_file = csv.DictReader(file)  
            for row in csv_file:
                    couriers.append(row)
    except FileNotFoundError as fnfe:
        print('Unable to open file: ' + str(fnfe))
    except Exception as e:
        print('An error occurred: ' + str(e))

def load_orders_file():
    orders_list.clear()
    try:
        with open(orders_csv, "r") as file:
            csv_file = csv.DictReader(file)  
            for row in csv_file:
                    orders_list.append(row)
    except FileNotFoundError as fnfe:
        print('Unable to open file: ' + str(fnfe))
    except Exception as e:
        print('An error occurred: ' + str(e))


#---------------------------------------------MENU CODE-----------------------------------------------

def main_menu():
    print("-----------------------------------------------")
    print("         DEL'S DINER ORDERING SYSTEM           ")
    print("                  MAIN MENU                    ")
    print("-----------------------------------------------")
    try:
        first_input = int(input("Welcome! To start:\nEnter 1 to see our Product Menu\nEnter 2 to see our Courier Menu\nEnter 3 to see our Order Menu or\nEnter 0 to Exit the App:\n"))
        if first_input == 0:
            close_app()
        elif first_input == 1:
            product_menu()
        elif first_input == 2:
            courier_menu()
        elif first_input == 3:
            order_menu()
        else:
            incorrect_function()
            main_menu()
    except ValueError:
        incorrect_function()
        main_menu()

def navigation():
    try:
        navigation_input = int(input("\nEnter 0 to return to Main Menu\nEnter 1 to return to Product Menu\nEnter 2 to return to Courier Menu\nEnter 3 to return to Order Menu:\n"))
        if navigation_input == 0:
            main_menu()
        elif navigation_input == 1:
            product_menu()
        elif navigation_input == 2:
            courier_menu()
        elif navigation_input == 3:
            order_menu()        
        else:
            incorrect_function()
            main_menu()
    except ValueError:
        incorrect_function()
        main_menu()

#------------------------------------------PRODUCT MENU CODE------------------------------------------

def product_menu():
    print("-----------------------------------------------")
    print("                PRODUCT MENU                   ")
    print("-----------------------------------------------")
    try:
        second_input = int(input("Enter 0 to Return to Main Menu\nEnter 1 to View Existing Products\nEnter 2 to Add a New Product\nEnter 3 to Update an Existing Product\nEnter 4 to Delete a Product:\n"))
        if second_input == 0:
            main_menu()
        elif second_input == 1:  
            view_products()
        elif second_input == 2:
            add_product()
        elif second_input == 3:
            update_product()
        elif second_input == 4:
            delete_product()     
        else:
            incorrect_function()
            product_menu()
    except ValueError:
        incorrect_function()
        product_menu()

def view_products():
    print("-----------------------------------------------")
    print("                PRODUCT LIST                   ")
    print("-----------------------------------------------")
    print_items_to_screen("products")
    navigation()

def add_product():
    print("-----------------------------------------------")            
    print("                ADD NEW PRODUCT                ")            
    print("-----------------------------------------------") 
    add_new_product_db()
    navigation()

def update_product():
    print("-----------------------------------------------")
    print("           MODIFY EXISTING PRODUCT             ")
    print("-----------------------------------------------")
    update_product_db()
    navigation()    

def delete_product():
    print("-----------------------------------------------")
    print("                REMOVE A PRODUCT               ")
    print("-----------------------------------------------")
    print_items_to_screen("products")
    x = product_to_delete_func()
    if x is not None:
        y = confirmation_func(x)
    else:
        product_menu()
    if y is not None:
        delete_product_db(y)
    else:
        product_menu()
    navigation()

#------------------------------------------COURIER MENU CODE------------------------------------------

def courier_menu():
    print("-----------------------------------------------")
    print("                COURIER MENU                   ")
    print("-----------------------------------------------")
    try:
        second_input = int(input("Enter 0 to Return to Main Menu\nEnter 1 to View Existing Couriers\nEnter 2 to Add a New Courier\nEnter 3 to Update an Existing Courier\nEnter 4 to Delete a Courier:\n"))
        if second_input == 0:
            main_menu()
        elif second_input == 1:  
            view_couriers()
        elif second_input == 2:
            add_courier()
        elif second_input == 3:
            update_courier()
        elif second_input == 4:
            delete_courier()     
        else:
            incorrect_function()
            courier_menu()
    except ValueError:
        incorrect_function()
        courier_menu()

def view_couriers():
    print("-----------------------------------------------")
    print("                COURIER LIST                   ")
    print("-----------------------------------------------")
    print_items_to_screen("couriers")
    navigation()

def add_courier():
    print("-----------------------------------------------")            
    print("                ADD NEW COURIER                ")            
    print("-----------------------------------------------") 
    add_new_courier_db()
    navigation()

def update_courier():
    print("-----------------------------------------------")
    print("           MODIFY EXISTING COURIER             ")
    print("-----------------------------------------------")
    update_courier_db()
    navigation()

def delete_courier():
    print("-----------------------------------------------")
    print("                REMOVE A COURIER               ")
    print("-----------------------------------------------")
    print_items_to_screen("couriers")
    x = courier_to_delete_func()
    if x is not None:
        y = check_against_orders(x)
    else:
        courier_menu()
    
    if y is not None:
        z = confirmation_func(y)
    else:
        navigation()
    
    if z is not None:
        delete_courier_db(z)
    else:
        courier_menu()
    
    navigation()

#--------------------------------------------ORDER MENU CODE-------------------------------------------

def order_menu():
    print("-----------------------------------------------")
    print("                 ORDER MENU                    ")
    print("-----------------------------------------------")
    try:
        second_input = int(input("Enter 0 to Return to Main Menu\nEnter 1 to View Existing Orders\nEnter 2 to Add a New Order\nEnter 3 to Update the Status of an Order\nEnter 4 to Update an Order\nEnter 5 to Delete an Order\nEnter 6 to View Order by Status\nEnter 7 to View Order by Courier:\n"))
        if second_input == 0:
            main_menu()
        elif second_input == 1:  
            view_orders()
        elif second_input == 2:
            add_order()
        elif second_input == 3:
            update_order_status()
        elif second_input == 4:
            update_order()
        elif second_input == 5:
            delete_order()
        elif second_input == 6:
            sort_order_status()
        elif second_input == 7:
            sort_order_courier()
        else:
            incorrect_function()
            order_menu()
    except ValueError:
        incorrect_function()
        order_menu()

def view_orders():
    print("-----------------------------------------------")
    print("                 ORDER LIST                    ")
    print("-----------------------------------------------")
    append_order_table_to_list()
    for i, order in enumerate(orders_list, 1):
        print("\n")
        print("Order {}".format(i))
        for key, value in order.items():
            print("{}: {}".format(key.title(), value))
    navigation()

def add_order():
    print("-----------------------------------------------")            
    print("                 ADD NEW ORDER                 ")            
    print("-----------------------------------------------")
    add_new_order_db()
    navigation()

def update_order_status():
    print("-----------------------------------------------")
    print("             MODIFY ORDER STATUS               ")
    print("-----------------------------------------------")
    update_order_status_db()
    navigation()

def update_order():
    print("-----------------------------------------------")
    print("            MODIFY EXISTING ORDER              ")
    print("-----------------------------------------------")
    update_order_db()
    navigation()

def delete_order():
    print("-----------------------------------------------")
    print("               REMOVE AN ORDER                 ")
    print("-----------------------------------------------")
    print_items_to_screen("orders")
    x = choose_order_delete()
    if x is not None:
        y = confirmation_func(x)
    else:
        order_menu()
    if y is not None:
        delete_order_db(y)    
    else:
        order_menu()
    navigation()

def sort_order_status():
    print("-----------------------------------------------")
    print("            LIST ORDER BY STATUS               ")
    print("-----------------------------------------------")
    
    sortstatus = sorted(orders_list, key=lambda k: k['Order Status'])
    for dict in sortstatus:
        print("\n")
        for key, value in dict.items():
            print("{}: {}".format(key, value))
    navigation()

def sort_order_courier():
    print("-----------------------------------------------")
    print("            LIST ORDER BY COURIER              ")
    print("-----------------------------------------------")
    sortstatus = sorted(orders_list, key=lambda k: k['Courier ID'])
    for dict in sortstatus:
        print("\n")
        for key, value in dict.items():
            print("{}: {}".format(key, value))
    navigation()
#----------------------------------------------OTHER CODE-----------------------------------------------

def incorrect_function():
    print("\nSorry that entry was not recognised, please try again")

def cache_products_table():
    try:
        with open(products_csv, "w", newline="") as outputfile:
            fieldnames = ["Product ID","Product","Price"]
            fc = csv.DictWriter(outputfile, fieldnames=fieldnames)
            fc.writeheader()
            fc.writerows(products)
    except:
        print('\nFailed to open products file')

def cache_couriers_table():
    try:
        with open(couriers_csv, "w", newline="") as outputfile:
            fieldnames = ["Courier ID", "Name","Phone"]
            fc = csv.DictWriter(outputfile, fieldnames=fieldnames)
            fc.writeheader()
            fc.writerows(couriers)
    except:
        print('\nFailed to open couriers file')

def cache_orders_table():
    try:
        with open(orders_csv, "w", newline="") as outputfile:
            fieldnames = ["Order ID","Customer Name","Customer Address", "Customer Postcode","Customer Phone","Courier ID","Order Status", "Items"]
            fc = csv.DictWriter(outputfile, fieldnames=fieldnames)
            fc.writeheader()
            fc.writerows(orders_list)
    except:
        print('\nFailed to open orders file')

def print_new_entry(listentry):
    new = listentry[-1]
    for key, value in new.items():
        print("{}: {}".format(key.title(), value))

def print_updated_entry(listentry, name, id):
    for new in listentry:
        if new[name] == id:
            for key, value in new.items():
                print("{}: {}".format(key.title(), value))
        else: 
            continue

def confirmation_func(item_to_return):
    while True:
        try:
            con = int(input("\nEnter 1 to confirm your choice or 0 to start again:\n"))
        except:
            incorrect_function()
            continue
        else:
            if con == 1:
                return item_to_return
                break
            elif con == 0:
                return None
                break
            else:
                incorrect_function()
                continue

def close_app():
    cache_products_table()
    cache_couriers_table()
    cache_orders_table()
    print("Thank you, goodbye!")
    sys.exit()

# append_product_table_to_list()
# append_courier_table_to_list()
# append_order_table_to_list()
# main_menu()

#TO DO:

#3) ADD SOME UNIT TESTS

#4) START POWERPOINT


