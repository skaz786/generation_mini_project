
def add_product_name(input):
    
    while True:
        new_product_name = (input("\nEnter name of new product\nor 0 to go back:\n".lower()))
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
                return new_product_name
                break      
        else:
            print("Product cannot be a number")
            continue