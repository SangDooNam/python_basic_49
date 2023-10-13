from data import stock
from datetime import datetime as dt

VALID_MENU_CHOICES = ["1", "2", "3", "4"]
YES_OR_NO = ["y", "n"]


def get_user_name():
    """Ask the user to provide a name."""
    name = input("What is your user name?: ")
    return name


def greet(name):
    """Greet the user."""
    return f"Hello, {name}"


def get_int(prompt):
    """
    Prompt the user for an integer input and validate it.
    Parameters:
    - prompt (str): The message displayed to the user.

    Returns:
    int: The validated integer provided by the user.

    Note:
    The function will repeatedly ask the user until
    a valid integer is provided.
    """
    while True:
        value = input(prompt)
        try:
            return int(value)
        except ValueError:
            print("Please enter integer.")


def lst_of_items(name, data=None, product_counter=None, items_per_page=50):
    """
    Displays items in a paginated manner based on the warehouse.

    This function retrieves and displays items
    from a dataset organized by warehouses.
    The display is paginated to ensure that a
    large number of items can be easily navigated.

    Parameters:
    - name (str): Name of the user.
    - data (dict, optional): A dictionary of items
                            organized by warehouses. If not provided,
                            it defaults to the output of the function
                            `rearrange_stock_based_on_warehouse()`.
    - product_counter (dict, optional): A dictionary to keep track of the
                                        number of products per warehouse.
                                        If not provided, an empty
                                        dictionary is initialized.
    - items_per_page (int, default=50): The number of items displayed
                                        per page during pagination.

    Returns:
    None. This function interacts with the user
    through print statements and input prompts.

    Note:
    The items from different warehouses are displayed in separate sections.
    """
    if data is None:
        data = rearrange_stock_based_on_warehouse()
        # prevent to change items by iterating
    if product_counter is None:
        product_counter = {}
        # prevent to change items by iterating
    for key, value in data.items():
        print()
        print(f"Items in warehouse {key}:")
        print()
        page = 0
        count = 0
        while page * items_per_page < len(value):
            start_idx = page * items_per_page
            end_idx = start_idx + items_per_page
            for dct in value[start_idx:end_idx]:
                count += 1
                print(f"{count}. {dct['state']} {dct['category']}")
            page += 1
            if page * items_per_page < len(value):
                print()
                prompt = input(
                    f'Displaying {start_idx + 1}-{end_idx} of {len(value)} products in warehouse {key}. Press enter for next page or "q" for next warehouse: '
                )
                print()
                if prompt == "q":
                    break
            else:
                break
    for key, value in data.items():
        for dct in value:
            amount_each_warehouse = dct["warehouse"]
            if amount_each_warehouse in product_counter:
                product_counter[amount_each_warehouse] += 1
            else:
                product_counter[amount_each_warehouse] = 1
    print()
    for number, amount_product in product_counter.items():
        print(f"Total items in warehouse {number}: {amount_product}")
    print()
    print(f"Thank you for your visit, {name}!")


def ask_for_max(name, total, item_name):
    """
    Prompt to order up to the maximum quantity available.
    Parameters:
    - name (str): The name of the user.
    - total (int): The total available quantity of the item.
    - item_name (str): The name of the item user is interested in.
    Note:
    This function is following the function 'ask_for_placing_order()'.
    This function is executed when user types in more amount
    than the 'total' parameter.
    """
    while True:
        ask_again = input("Would you like to order the maximum available?(y/n): ")
        if ask_again.lower() not in YES_OR_NO:
            print(f"{ask_again} is not a valid operation. please try again.")
            continue
        if ask_again.lower() == "n":
            print(f"Thank you for your visit, {name}!")
            break
        elif ask_again.lower() == "y":
            print(f"{total} {item_name} have been ordered")
            print()
            print(f"Thank you for your visit, {name}")
            break


def ask_for_placing_order(name, total, item_name):
    """
    Prompt the user to place an order for a specific item.

    Parameters:
    - name (str): The name of the user.
    - total (int): The total available quantity of the item.
    - item_name (str): The name of the item user is interested in.

    Returns:
    None. This function only interacts with the user
    via print statements and input prompts.

    Note:
    The function loops until the user provides
    a valid input or decides not to order.
    If the user wishes to order, they're prompted for the desired quantity.
    Various messages are shown based
    on the available stock and desired quantity.
    """
    continue_loop = True

    while continue_loop:
        ask_for_order = input("Would you like to order this item?(y/n): ")

        if ask_for_order.lower() not in YES_OR_NO:
            print(f"{ask_for_order} is not a valid operation. please try again.")
            continue

        if ask_for_order.lower() == "n":
            print(f"Thank you for your visit, {name}!")

            continue_loop = False

        elif ask_for_order.lower() == "y":
            while True:
                ask_for_amount = get_int("How many would you like?: ")

                if ask_for_amount <= 0:
                    print("Nothing has been ordered")
                    print()
                    print(f"Thank you for your visit, {name}!")
                    continue_loop = False
                    break

                if ask_for_amount > total:
                    print("**************************************************")
                    print(
                        f"There are not this many available. The maximum amount that can be ordered is {total}"
                    )
                    print("**************************************************")
                    ask_for_max(name, total, item_name)

                elif total >= ask_for_amount > 0:
                    print(f"{ask_for_amount} {item_name} have been ordered")
                    print()
                    print(f"Thank you for your visit, {name}")
                    continue_loop = False
                    break

                return


def rearrange_stock_based_on_warehouse(grouped_by_warehouse=None):
    if grouped_by_warehouse is None:
        grouped_by_warehouse = {}

    for dict in stock:
        key = dict["warehouse"]

        if key not in grouped_by_warehouse:
            grouped_by_warehouse[key] = []

        grouped_by_warehouse[key].append(dict)

    return grouped_by_warehouse


def searching_for_item(name, data=None):
    """
    Search item and validate the amount of the item in each any number of warehouse.

    Parameters:
    - name (str): The name of the user.
    - data (dict, optional): A dictionary of items
                            organized by warehouses. If not provided,
                            it defaults to the output of the function
                            `rearrange_stock_based_on_warehouse()`.
    Returns:
    None. This function only interacts with the user via
    print statements and input prompts.

    Note:
    This function is intended to be called after 'option()'.
    This function is executed if the user selects number 2 in option().
    This function compares the amount of the searched item in each warehouse .
    If there is no searched item it will quit the process.
    """
    if data is None:
        data = rearrange_stock_based_on_warehouse()

    total_amount = 0
    while True:
        looking_for_item = input("What is the name of the item?: ")

        for warehouse_number, product in data.items():
            count = 0
            for dct in product:
                if (
                    looking_for_item.lower()
                    == dct["state"].lower() + " " + dct["category"].lower()
                ):
                    date = (
                        dt.today()
                        - dt.strptime(dct["date_of_stock"], "%Y-%m-%d %H:%M:%S")
                    ).days

                    print(
                        f"- {looking_for_item.capitalize()} (in stock for {date} days) in Warehouse {warehouse_number}"
                    )
                    count += 1
                    total_amount += 1
            print(f"Maximim availability: {count} in Warehouse {warehouse_number}")

        print(f"Total available amount is: {total_amount}")

        if total_amount == 0:
            print(f"Amount available: {total_amount}")
            print("Location: Not in stock")
            print()
            print(f"Thank you for your visit, {name}!")
            break

        else:
            ask_for_placing_order(name, total_amount, looking_for_item)

        return


def browse_by_category(name, counter=1, product_counter=None, product_dct=None, data=None):
    """
    Display a menu of available product categories.
    Upon selecting a category number, it prints all products
    in that category along with their warehouses.

    Parameters:
    - name (str): The name of the user.
    - counter (int, default = 1): a numeric code for the categories
    - product_counter (dict): the dictionary
      contains the amount of stocked product
    - product_dct (dict): The dictionary contains numeric keys,
      with product names and amounts as values.

    Returns:
    None. This function only interacts with the user
    via print statements and input prompts.

    Note:
    This function is intended to be called after 'option()'.
    This function is executed if the user selects number 3 in option().
    This function makes use of list of dictionary 'stock', from data module

    """
    if product_counter is None:
        product_counter = {}
    if product_dct is None:
        product_dct = {}
    if data is None:
        data = rearrange_stock_based_on_warehouse()

    for dct in stock:
        product = dct["category"]

        if product in product_counter:
            product_counter[product] += 1

        else:
            product_counter[product] = 1

    for key, value in product_counter.items():
        product_dct[counter] = [key, value]
        print(f"{counter}. {key} ({value})")
        counter += 1

    prompt = get_int("Type the number of the category to browse: ")
    print()
    
    
    for key, value in product_dct.items():
        if prompt == key:
            for warehouse_number, product in data.items():
                total = 0
                for dct in product:
                    if value[0] in dct["category"]:
                        print(f'{dct["state"]} {dct["category"]}, Warehouse {warehouse_number}')
                        total += 1
                print(f'- Total {total} amount of {value[0]} in warehouse {warehouse_number}')
                prompt = input('Please press enter for next warehouse : ')
                            
    print()
    print(f"Thank you for your visit, {name}!")
    # print()
    # for key, value in product_dct.items():
    #     if prompt == key:
    #         for dict in stock:
    #             if value[0] in dict["category"]:
    #                 if dict["warehouse"] == 1:
    #                     print(f'{dict["state"]} {dict["category"]}, Warehouse 1')
    #                 else:
    #                     print(f'{dict["state"]} {dict["category"]}, Warehouse 2')
    # print()
    # print(f"Thank you for your visit, {name}!")


def options(name):
    """
    Prompt the user to continuously select one of three options:
    1. List items by warehouse
    2. Search an item and place an order
    3. Quit

    Parameters:
    - name (str): The name of the user.

    Returns:
    None. This function only interacts with the
    user via print statements and input prompts.

    Note:
    This function orchestrates the user's main interactions with the program,
    delegating to other functions based on user choice.
    The function runs in a loop until
    the user decides to quit.
    """
    while True:
        query_for_options = input(
            "What would you like to do?\n1. List items by warehouse\n2. Search an item and place an order\n3. Browse by category\n4. Quit\nType the number of the operation(1\\2\\3\\4): "
        )

        if query_for_options == "4":
            print(f"Thank you for your visit, {name}!")
            break

        if query_for_options not in VALID_MENU_CHOICES:
            print("**************************************************")
            print(f"{query_for_options} is not valid operation")
            print("**************************************************")
            print()
            print(f"Thank you for your visit, {name}!")

        if query_for_options == "1":
            lst_of_items(name)

        elif query_for_options == "2":
            searching_for_item(name)

        elif query_for_options == "3":
            browse_by_category(name, product_counter={})


def main():
    """
    Entry point for the warehouse management program.

    This function performs the following steps:
    1. Fetches the user's name.
    2. Greets the user.
    3. Presents options for interacting with the warehouse system.

    Returns:
    None. The function interacts with the user
    via print statements and input prompts.
    """
    user_name = get_user_name()
    print(greet(user_name))
    options(user_name)


main()
