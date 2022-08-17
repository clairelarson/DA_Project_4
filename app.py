#imports
from models import (Base, session, Brand, Product, engine)
import csv
import datetime
import time

# main menu - add, search, analysis, view, exit
def menu():
    while True:
        print('''
        \rINVENTORY MENU
        \rView Details of Product - "V"
        \rAdd New Product - "N"
        \rAnalysis - "A"
        \rMake Backup of Database - "B"
        \rExit - "E"
        ''')
        user_input = input("Please type the letter next to your choice to select from Menu:\n")
        user_input = user_input.upper()
        if user_input in ('V', 'N', 'A', 'B', 'E'):
            return user_input
        else:
            input("You must enter the letter next to your choice, please hit enter to try again:")

            
def sub_menu():
    while True:
        print('''
        \r1) EDIT
        \r2) DELETE
        \r3) RETURN TO MAIN MENU
        ''')
        user_input = input("Please type 1-3 to select from Menu:\n")
        if user_input in ('1',  '2', '3'):
            return user_input
        else:
            input("You must enter 1-3, please hit enter to try again:")


# edit products
def edit_check(column_name, current_value):
    print(f"\n**** EDIT {column_name} ****\n")
    if column_name == 'Product Price':
        print(f"\rCurrent Value: {current_value/100}")
    elif column_name == 'Date Updated':
        print(f"\rCurrent Value: {current_value.strftime('%m/%d/%Y')}")
    else:
        print(f"\rCurrent Value: {current_value}")
        
    if column_name == "Date Updated" or column_name == "Product Price" or column_name == "Product Quantity":
        while True:
            changes = input("\nWhat would you like to change the value to?\n")
            changes = changes.lower()
            if column_name == 'Date Updated':
                changes = clean_date(changes)
                if type(changes) == datetime.datetime:
                    return changes
            elif column_name == 'Product Price':
                changes = clean_price(changes)
                if type(changes) == int:
                    return changes
            elif column_name == 'Product Quantity':
                changes = clean_quantity(changes)
                if type(changes) == int:
                    return changes
    else:
        return input("\nWhat would you like to change the value to?\n")


# add csv files
def inventory_add_csv():
    with open("inventory.csv", newline='') as inventory_csv:
        data = csv.reader(inventory_csv, delimiter=',')
        next(data)
        data = list(data)
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
            if product_in_db == None:
                product_name = row[0]
                price = row[1]
                price = price.split('$')
                price = price[1]
                product_price = clean_price(price)
                product_quantity = clean_quantity(row[2])
                date_updated = clean_date(row[3])
                get_id = session.query(Brand).filter(Brand.brand_name == row[4]).one_or_none()
                brand_id = get_id.brand_id
                brand_name = row[4]
                new_product = Product(product_name=product_name,
                    product_price=product_price,
                    product_quantity=product_quantity,
                    date_updated=date_updated, brand_name=brand_name, brand_id=brand_id)
                session.add(new_product)
        session.commit() 
                
        
def brand_add_csv():
    with open('brands.csv', newline='') as brands_csv:
        data = csv.reader(brands_csv, delimiter=',')
        next(data)
        for row in data:
            brand_in_db = session.query(Brand).filter(Brand.brand_name==row[0]).one_or_none()
            if brand_in_db == None:
                add_to_db = Brand(brand_name=row[0])
                session.add(add_to_db)
        session.commit()
        

def backup_csv():
    # Inventory csv
    with open('backup_inventory.csv', 'a') as csvfile:
        field_names = ['product_name', 'product_price', 'product_quantity', 'date_updated', 'brand_name', 'brand_id']
        backup_writer = csv.DictWriter(csvfile, fieldnames=field_names)
        backup_writer.writeheader()
    # Get Products
        data = session.query(Product)
        for rows in data:
            product_name = rows.product_name
            product_price = '$' + str(format(rows.product_price / 100, '.2f'))
            product_quantity = rows.product_quantity
            date_updated = rows.date_updated.strftime('%m/%d/%Y')
            brand_name = rows.brand_name
            brand_id = rows.brand_id
            backup_writer.writerow({
                'product_name': product_name,
                'product_price': product_price,
                'product_quantity': product_quantity,
                'date_updated': date_updated,
                'brand_name': brand_name,
                'brand_id': brand_id})
    # Brands csv
    with open('backup_brand.csv', 'a') as csvfile:
        brand_field_names = ['brand_id', 'brand_name']
        brand_backup = csv.DictWriter(csvfile, fieldnames=brand_field_names)
        brand_backup.writeheader()
    # Get Brands
        data = session.query(Brand)
        for rows in data:
            brand_name = rows.brand_name
            brand_id = rows.brand_id
            brand_backup.writerow({
                'brand_id': brand_id,
                'brand_name': brand_name})


#Clean Data
def clean_date(row):
    try:
        return_date = datetime.datetime.strptime(row, "%m/%d/%Y")
    except ValueError:
        input('''
          \n****** Date Error ******
          \rThe date format should be formatted MM/DD/YYYY
          \rPress Enter to Try Again
          \r***************************\n''')
        return
    else:
        return return_date
        
def clean_price(row):
    try:
        price_float = float(row)
        return int(price_float *100)
    except ValueError:
        input('''
              \n****** Price Error ******
              \rThe price format should be an integer
              \rEx: 99.99
              \rPress Enter to Try Again
              \r***************************\n''')
        return
        

def clean_quantity(row):
    try:
        quantity_int = int(row)
    except ValueError:
        input('''
              \n****** Quantity Error ******
              \rThe Quantity should be an integer
              \rPress Enter to Try Again
              \r***************************\n''')
        return
    else:
        return quantity_int
    
    
def clean_id(id_input, options):
    try:
        product_id = int(id_input) 
    except ValueError:
        input('''
              \n****** ID Error ******
              \rThe ID format should be an integer
              \rPress Enter to Try Again
              \r***************************''')
        return
    else:
        if product_id in options:
            return product_id
        else:
            input(f'''
              \n****** ID Error ******
              \rOptions: {options}
              \rPress Enter to Try Again
              \r***************************''')
            return 


#run program            
def app():
    app_running = True
    while app_running:
        user_input = menu()
        # Displaying a product by its ID
        if user_input == 'V':
            id_options = []
            for product in session.query(Product):
                id_options.append(product.product_id)
            id_error = True
            while id_error:
                id_choice = input(f'''
                    \rID Options: {id_options}
                    \rProduct ID:  ''')
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
            the_product = session.query(Product).filter(Product.product_id==id_choice).first()
            print(f'''
                \nProduct Name: {the_product.product_name}
                \rProduct Quantity: {the_product.product_quantity}
                \rProduct Price: {the_product.product_price}
                \rDate Updated: {the_product.date_updated}
                \rBrand: {the_product.brand_name}
                ''')
            sub_choice = int(sub_menu())
            if sub_choice == 1:
                the_product.product_name = edit_check('Product Name', the_product.product_name)
                the_product.product_quantity = edit_check('Product Quantity', the_product.product_quantity)
                the_product.product_price = edit_check('Product Price', the_product.product_price)
                the_product.date_updated = edit_check('Date Updated', the_product.date_updated)
                the_product.brand_name = edit_check('Brand', the_product.brand_name)
                print("Product was updated successfully!")
                time.sleep(1.5)
            elif sub_choice == 2:
                session.delete(the_product)
                session.commit()
                print("Product was deleted successfully!")
                time.sleep(1.5)
            elif sub_choice == 3:
                pass
        # Adding a new product to the database
        elif user_input == 'N':
            product_name = input("Product Name: ")
            price_error = True
            quant_error = True
            while quant_error:
                product_quantity = input("Quantity: ")
                product_quantity = clean_quantity(product_quantity)
                if type(product_quantity) == int:
                    quant_error = False
            date_error = True
            while date_error:
                date = input("Date Updated (MM/DD/YYYY): ")
                date_updated = clean_date(date)
                if type(date_updated) == datetime.datetime:
                    date_error = False
            while price_error:
                product_price = input("Price (Ex: 25.64) : ")
                product_price = clean_price(product_price)
                if type(product_price) == int:
                    price_error = False
            brand_name = input("Brand Name: ")
            new_product = Product(product_name=product_name,
                    product_price=product_price,
                    product_quantity=product_quantity,
                    date_updated=date_updated,
                    brand_name=brand_name)
            product_in_db = session.query(Product).filter(Product.product_name==new_product.product_name).one_or_none()
            if product_in_db == None:
                session.add(new_product)
                session.commit()
                print("\nProduct was added successfully!\n")
                time.sleep(1.5)
            else:
                if product_in_db.date_updated < new_product.date_updated:
                    product_in_db.product_name=new_product.product_name,
                    product_in_db.product_price=new_product.product_price,
                    product_in_db.product_quantity=new_product.product_quantity,
                    product_in_db.date_updated=new_product.date_updated,
                    product_in_db.brand_name=new_product.brand_name
                    session.commit()
                    print("\nProduct was updated successfully!\n")
                    time.sleep(1.5)
        # Analyzing the Database
        elif user_input == 'A':
            exsp_product = session.query(Product).order_by(Product.product_price.desc()).first()
            cheap_product = session.query(Product).order_by(Product.product_price).first()
            brand_count = []
            for brand in session.query(Product.brand_name).all():
                brand_count.append(brand)
            most_products = max(brand_count, key=brand_count.count)
            least_products = min(brand_count, key=brand_count.count)
            total_products = session.query(Product).count()
            print(f'''
            \n***** INVENTORY ANALYSIS *****
            \rMost Expensive Product: {exsp_product.product_name}
            \rLeast Expensive Product: {cheap_product.product_name}
            \rBrand with most products: {most_products}
            \rBrand with the least products: {least_products}
            \rTotal Number of Products: {total_products}
            \r****************************
            ''')
            input("\nPress enter to return to the main menu.\n")
            time.sleep(.5)
        #Backup the database (Export new CSV) 
        elif user_input == 'B':
            backup_csv()
            input("Backup created successfuolly! Hit enter to continue")
            time.sleep(.5)
        else:
            print("Goodbye, have a good day!")
            app_running = False
            

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    
    brand_add_csv()
    inventory_add_csv()
    app()
