from data import stock, personnel
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
        str: Text indicating that the user has displayed a list of all items.

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

    return f"Listed {len(stock)} items"


def ask_for_max(name, total, item_name):
    """
    Prompt to order up to the maximum quantity available.
    Parameters:
    - name (str): The name of the user.
    - total (int): The total available quantity of the item.
    - item_name (str): The name of the item user is interested in.

    Returns:
    bool: Returns False if the user selects 'n', and True if 'y'.

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
            return False
        elif ask_again.lower() == "y":
            print(f"{total} {item_name} have been ordered")
            print()
            print(f"Thank you for your visit, {name}")
            return True


def validate_user(func):
    """
    A decorator to validate the user's credentials before allowing them to order a product.

    Parameters:
    - func (function): The original function being decorated.

    Notes:
    - This is a decorator with three inner functions:
        1. `authenticate()`: Validates the user's credentials against a provided list.
        2. `prompt_username_password()`: Prompts the user for their username and password.
        3. `wrapped_func()`: The main wrapper function which integrates the above two functions
           and checks authentication before calling the original function.

    The decorator will repeatedly prompt for credentials until the user either authenticates
    successfully or chooses to exit. If authenticated, the original function (`func`) is executed.
    """

    def authenticate(personnel_lst, p_user_name, p_password):
        for dct in personnel_lst:
            if dct["user_name"] == p_user_name and dct["password"] == p_password:
                return True
            elif "head_of" in dct:
                if authenticate(dct["head_of"], p_user_name, p_password):
                    return True
        return False

    def prompt_username_password():
        p_user_name = input("*** Enter the user name ***: ")
        p_password = input("*** Enter your password ***: ")

        return p_user_name, p_password

    def wrapped_func(name, total, item_name, username_password=[]):
        authenticated = False

        while not authenticated:
            if len(username_password) == 0:
                username_password = list(prompt_username_password())

            authenticated = authenticate(
                personnel, username_password[0], username_password[1]
            )
            if authenticated:
                result = func(name, total, item_name)
                return result
            else:
                print(f"Authentication failed!")
                try_again = input("Press 'q' to exit or any other key to try again:")
                if try_again.lower() == "q":
                    return
                username_password.clear()

    return wrapped_func


@validate_user
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

    while True:
        ask_for_amount = get_int("How many would you like?: ")

        if ask_for_amount <= 0:
            print("Nothing has been ordered")
            print()
            print(f"Thank you for your visit, {name}!")
            return False

        if ask_for_amount > total:
            print("**************************************************")
            print(
                f"There are not this many available. The maximum amount that can be ordered is {total}"
            )
            print("**************************************************")
            result = ask_for_max(name, total, item_name)
            if result:
                return True
            return False

        elif total >= ask_for_amount > 0:
            print(f"{ask_for_amount} {item_name} have been ordered")
            print()
            print(f"Thank you for your visit, {name}")
            return True


def rearrange_stock_based_on_warehouse(grouped_by_warehouse=None):
    """
    Organizes the list of dictionaries by warehouse number.

    Parameters:
    - grouped_by_warehouse (dict, optional): A dictionary with items grouped by
                                            warehouse number. If not provided,
                                            an empty dictionary is initialized.

    Returns:
    dict: A dictionary with items grouped by their respective warehouse numbers.

    Note:
    This function ensures proper handling of data with any number of warehouses..
    """
    if grouped_by_warehouse is None:
        grouped_by_warehouse = {}

    for dict in stock:
        key = dict["warehouse"]

        if key not in grouped_by_warehouse:
            grouped_by_warehouse[key] = []

        grouped_by_warehouse[key].append(dict)

    return grouped_by_warehouse


def searching_for_item(name, data=None, continue_loop=True):
    """
    Search item and validate the amount of the item in each any number of warehouse.

    Parameters:
    - name (str): The name of the user.
    - data (dict, optional): A dictionary of items
                            organized by warehouses. If not provided,
                            it defaults to the output of the function
                            `rearrange_stock_based_on_warehouse()`.
    Returns:
        str: The item the user has searched.

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
            return f"Searched {looking_for_item.capitalize()} but nothing found"
            # break

        else:
            while continue_loop:
                ask_for_order = input("Would you like to order this item?(y/n): ")

                if ask_for_order.lower() not in YES_OR_NO:
                    print(
                        f"{ask_for_order} is not a valid operation. please try again."
                    )
                    continue

                if ask_for_order.lower() == "n":
                    print(f"Thank you for your visit, {name}!")
                    # continue_loop = False
                    return f"Searched a {looking_for_item.capitalize()}"
                elif ask_for_order.lower() == "y":
                    order_placed = ask_for_placing_order(
                        name, total_amount, looking_for_item
                    )
                    if order_placed:
                        return f"Ordered a {looking_for_item.capitalize()}"
                    else:
                        return f"Searched a {looking_for_item.capitalize()}"


def product_amount_counter(product_amount=None):
    """
    Count the total amount for each product category from the `stock` list.

    Parameters:
    - product_amount (dict, optional): A dictionary to start with, if available.
                                      Keys represent product categories, and values
                                      represent the count of each product category.
                                      If not provided, an empty dictionary is initialized.

    Returns:
    dict: A dictionary with product categories as keys and their respective counts as values.

    Notes:
    This function processes the `stock` list of dictionary to derive the counts for each product category.
    """

    if product_amount is None:
        product_amount = {}

    for dct in stock:
        key = dct["category"]
        if key in product_amount:
            product_amount[key] += 1
        else:
            product_amount[key] = 1

    return product_amount


def numeric_product_amount(counter=1, data=None, product_dct=None):
    """
    Map each product category to a numeric value and its respective amount.

    Parameters:
    - counter (int, default=1): The starting number for numeric mapping.
    - data (dict, optional): The dictionary containing product categories and
                             their respective counts. If not provided, it defaults
                             to the output of `product_amount_counter()`.
    - product_dct (dict, optional): A starting dictionary for numeric mapping.
                                    If not provided, an empty dictionary is initialized.

    Returns:
    dict: A dictionary where keys are numeric values and values are lists containing
          the product category and its count.

    Notes:
    This function assigns a numeric value to each product category for easier reference.
    """
    if data is None:
        data = product_amount_counter()
    if product_dct is None:
        product_dct = {}

        for number, product_amount in data.items():
            product_dct[counter] = [number, product_amount]
            counter += 1

    return product_dct


def browse_by_category(
    name, counter=1, product_counter=None, product_dct=None, data=None, total_amount=0
):
    """
    Display a menu of available product categories.
    Upon selecting a category number, it prints products of each page of
    warehouse. Pressing enter leads to next page of warehouse.

    Parameters:
    - name (str): The name of the user.
    - counter (int, default = 1): a numeric code for the categories
    - product_counter (dict): A dictionary mapping product names
                            to their stock counts.
    - product_dct (dict): A dictionary with numeric keys mapping to product
                            names and their respective amounts
    - data (dict, optional): A dictionary of items
                            organized by warehouses. If not provided,
                            it defaults to the output of the function
                            `rearrange_stock_based_on_warehouse()`.
    - total_amount (int, default = 0):  Total number of products
                                        within each category.

    Returns:
        str: The category the user has browsed.

    Note:
    This function is intended to be called after 'option()'.
    This function is executed if the user selects number 3 in option().

    """
    # if product_counter is None:
    product_counter = product_amount_counter()
    if product_dct is None:
        product_dct = numeric_product_amount()
    if data is None:
        data = rearrange_stock_based_on_warehouse()

    for key, value in product_counter.items():
        print(f"{counter}. {key} ({value})")
        counter += 1

    prompt = get_int("Type the number of the category to browse: ")
    print()

    for key, value in product_dct.items():
        if prompt == key:
            selected_category = value[0]
            for warehouse_number, product in data.items():
                total = 0
                state_category = {}
                for dct in product:
                    key = dct["state"] + " " + dct["category"]
                    if value[0] in dct["category"]:
                        if key in state_category:
                            state_category[key] += 1
                        else:
                            state_category[key] = 1
                        total += 1
                        total_amount += 1
                for product_name, amount in state_category.items():
                    print(
                        f"{product_name}, in amount ({amount}) in warehouse {warehouse_number}"
                    )
                print(
                    f"- Total of ({total}) {value[0]} in warehouse {warehouse_number}"
                )
                input("Please press enter for next warehouse : ")
    print(f"- Total of ({total_amount}) in all warehouses")
    print(f"Thank you for your visit, {name}!")
    return f"Browsed the category {selected_category}."


def options(name, actions_taken=[]):
    """
    Prompt the user to continuously select one of three options:
    1. List items by warehouse
    2. Search an item and place an order
    3. Quit

    Parameters:
    - name (str): The name of the user.
    - actions_taken (lst): Log actions taken during the session.

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
            action = lst_of_items(name)
            actions_taken.append(action)
        elif query_for_options == "2":
            action = searching_for_item(name)
            actions_taken.append(action)
        elif query_for_options == "3":
            action = browse_by_category(name, product_counter={})
            actions_taken.append(action)
    print("In this session you have:")
    for idx, done in enumerate(actions_taken, start=1):
        print(f"{idx}. {done}")


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
