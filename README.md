# Functions

## Topics covered

Functions, arguments & parameters, scope, recursion and decorators.

## Goal achieved

By the end of the exercise you will have a better structured code that will be easier to maintain and further improve. You will also add some more features to your command line query tool.

More specifically, you will add the following features:

- Unlimited warehouses
- Extended sessions
- User system

## Data

For the new features you will need some new data, so that you can test your code.

Replace your file `cli/data.py` with the one at [sample/data.py](sample/data.py).

> You may want to do the refactoring first, before doing this.

This file now has a list of items from 4 different warehouses.

It also has a list with the user names and passwords of the employees. This is a nested list of dictionaries and it may change with time. You don't know how many nesting levels may the list hold.


## Description

The script you created so far in this project has become very useful to the warehouse employees, and they are requesting to have additional functionalities developed.

But the code starts to get big and some of these new features are becoming difficult to implement. Thankfully, you have just learned about functions and are ready to improve the readability and structure of the code to make it easier to add these requested features.

### Refactor the code

Again, you will be refactoring the code, this time to use functions. The code is not extremely huge, but it is starting to be a bit complex to manage already and converting this into meaningful functions may not always be easy.

To do this, look at your file and identify big chunks of code that are used for a particular task. In your case, this is not extremely complex as you have a menu you can use to identify these first big groups of instructions. Additionally, you have to ask the user name, greet them and make them chose an operation. So, you will need, at least, a function for each of the following tasks:

- Get the user name
- Greet the user
- Get the operation selected
- Print the list of items
- Search and order an item
- Browse by category

A way to approach this is to make the changes on the same file. Create the first function on the top and replace the appropriate code in your script with this new function (you can often copy/paste big parts of the code and adapt it when needed). Leave the rest as it is. Check if the tool still works the same way as before. Create the second function and replace the related code. Check again. And so on.

When you finish all the functions in the previous list, explore each one of the functions to see if they are already readable enough or are still too complex.

Refactor again the function that searches and places orders, it is too complex. If you need it, keep the main logic in the "search and order" function but put the rest of the instructions in three other functions:

- Search an item
- Print the search results
- Order an item

Refactor now the function that prints the search results. If you look at it you will see two blocks of code that look exactly the same except that one uses the `warehouse1` list and the other one uses `warehouse2`. This is a clear pattern for a function.

Once you are done, your main script (the code outside any function) should look similar to this:

```
# Get the user name
user_name = get_user_name()
greet_user()

# Get the user selection
operation = get_selected_operation()

print()

# Execute the operation
if operation == "1":
    list_items_by_warehouse()

elif operation == "2":
    search_and_order_item()

elif operation == "3":
    browse_by_category()

elif operation == "4":
    pass

else:
    print("*" * 50)
    print(operation, "is not a valid operation.")
    print("*" * 50)

# Finish
print()
print(f"Thank you for your visit, {user_name}!")
```

You can chose to create additional functions for the error message and finishing the script.

### New features

The warehouse management and employees have requested the following list of features:

**Unlimited number of warehouses**

The tool is only working well for warehouses 1 and 2, but we just opened two more and the business is expanding fast, so we may need to add even more warehouses any time soon.

The data is already structured in a way that lets us add items from other warehouses. Each item has a property warehouse and the new item will simply have the value 3 (or 4,...).

But the functions are not prepared for this. They wouldn't make the tool crash and items from a third warehouse would still appear in search results, but they would be grouped and counted as being in one of the other 2 warehouses.

The tool should be able to work properly with any number of warehouses in the data, so the functions need to be adapted.

> **Hint:** remove any variable and argument named warehouse1 and warehouse2, then find another way to do the same without writing 1 variable or 1 argument for each warehouse.

**More than one operation in a session**

Every time an employee finishes using the tool, it stops running. Very often they want to perform additional queries, so they have to execute again the tool, type again the name and then do the new operation.

They want you to add an option that, every time an operation finishes, lets them go back to the menu and chose another operation without stopping the tool.

So, whenever the script finishes running any operation (except quit), the script should ask the user if they want to perform another operation. If they decline, then the script should stop running. If they accept, then the initial menu should show up again and ask to pick a choice (without asking again for the user name).

This should happen indefinitely until the user declines performing a new operation.

Once this is working, there is an additional requirement for this feature. At the end of the session (when the user declines performing another operation), the tool should print a list of the actions taken during that session and they should appear in the order they were performed.

Example:

```
Thank you for your visit, Example!
In this session you have:
        1. Listed 5000 items.
        2. Searched a Cheap tablet.
        3. Browsed the category Headphones.
```

> **Hint**: Each of the main functions for each one of the 3 operations should return a string with the description of the action taken. You may also need to use recursion for this feature.

**User system**

The tool has become so popular that the warehouse management has decided to let visitors use it also on the front desk. The problem is, visitors should only be allowed to list, search and browse, and they should not be able to order items straight from the tool. The placing of orders should only be allowed to employees in the `personnel` list of the `data.py` file.

The tool should still ask the name to everyone. Only when the user wants to place an order, the tool will ask for a valid password and then will try to match the user name and password against the previous list.

> **Hint:** If you have a function that starts the order (after the user answers yes to placing the order) you can apply a decorator that checks for a variable in the global scope indicating whether the user is already validated. The decorator will override the function with a prompt for the password, or will call the function normally if the user is already validated.

If there is no employee with such name and password, it should say so and should allow the user to change the name and type again the password. This should happen indefinitely until the user declines trying again or succeeds authenticating and finishes the order.

> This can be done easier within the decorator to keep the code cleaner and make it easier to implement this feature.

Any of the employees, of any level, in the personnel list is allowed to place orders.

The next time the user tries to place an order during the same session, if the user has already authenticated before, it should remember and not ask for the password again.
