from data import stock
from datetime import datetime as dt


def rearrange_stock_based_on_warehouse(grouped_by_warehouse=None):
    if grouped_by_warehouse is None:
        grouped_by_warehouse = {}

    for dict in stock:
        key = dict["warehouse"]

        if key not in grouped_by_warehouse:
            grouped_by_warehouse[key] = []

        grouped_by_warehouse[key].append(dict)

    return grouped_by_warehouse

# product = rearrange_stock_based_on_warehouse()

# for key, value in product.items():
#     print(value)

def searching_for_item(
    name, data = None, total_1=0, total_2=0, days_since_then1=None, days_since_then2=None
):
    """
    Search item and validate the amount of the item in each warehouse.

    Parameters:
    - name (str): The name of the user.
    - total_1 (int, default = 0): Total amount of the item in warehouse 1
    - total_2 (int): Total amount of the item in warehouse 2
    - days_since_then1 (list, default = None): The list contains information
      about how many days the product has been stocked in warehouse 1.
    - days_since_then2 (list, default = None): The list contains information
      about how many days the product has been stocked in warehouse 2.
    Returns:
    None. This function only interacts with the user via
    print statements and input prompts.

    Note:
    This function is intended to be called after 'option()'.
    This function is executed if the user selects number 2 in option().
    This function compares the amount of the searched item in each warehouse .
    If there is no searched item it will quit the process.
    This function makes use of list of dictionary 'stock', from data module
    """
    if data is None:
        data = rearrange_stock_based_on_warehouse()

    total_amount = 0
    while True:
        looking_for_item = input("What is the name of the item?: ")

        for warehouse_number, product in data.items():
            count = 0
            for dct in product:
                
                if looking_for_item.lower() == dct['state'].lower() + ' ' + dct['category'].lower():
                    
                    date = (dt.today() - dt.strptime(dct['date_of_stock'], "%Y-%m-%d %H:%M:%S")).days
                    
                    print(f'- {looking_for_item.capitalize()} (in stock for {date} days) in Warehouse {warehouse_number}')
                    count += 1
                    total_amount += 1
            print(f'Maximim availability: {count} in Warehouse {warehouse_number}')
            # print(total_amount)
        

        if total_amount == 0:
            print(f"Amount available: {total_amount}")
            print("Location: Not in stock")
            print()
            print(f"Thank you for your visit, {name}!")
            break

        else:
            ask_for_placing_order(name, total_amount, looking_for_item)
        
        return

searching_for_item('SangDoo')

def ask_for_placing_order():
    pass

