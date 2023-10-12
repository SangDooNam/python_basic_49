
from data import stock

def rearrange_stock_based_on_warehouse(grouped_by_warehouse= None):
    
    if grouped_by_warehouse is None:
        
        grouped_by_warehouse = {}
        
    for dict in stock:
        
        key = dict['warehouse']
        
        if key not in grouped_by_warehouse:
            
            grouped_by_warehouse[key] = []
        
        
            
        grouped_by_warehouse[key].append(dict)
    
    return grouped_by_warehouse
            

data = rearrange_stock_based_on_warehouse()


# print(data)
# for key, value in data.items():
    
#     print(f'Items in warehouse {key}:')
#     for dct in value:
        
#         print(dct['state'] + ' ' + dct['category'])

# product_counter = {}

# for dct in stock:
    
#     amount_of_product_in_each_warehouse = dct['warehouse']
    
#     if amount_of_product_in_each_warehouse in product_counter:
        
#         product_counter[amount_of_product_in_each_warehouse] += 1
    
#     else:
#         product_counter[amount_of_product_in_each_warehouse] = 1
        
# print(product_counter)

# product_counter = {}

# for key, value in data.items():

#     for dct in value:
        
#         amount_each_warehouse = dct['warehouse']
        
#         if amount_each_warehouse in product_counter:
            
#             product_counter[amount_each_warehouse] += 1
#         else:
            
#             product_counter[amount_each_warehouse] = 1
            
# print(product_counter)

# print(len(stock))
# total_items_in_data = sum(len(v) for v in data.values())
# print(total_items_in_data)

amount_displaying_page = 100

index = 0 

for key, value in data.items():
    
    print(len(value))
    start_idx = index * amount_displaying_page
    end_idx = index + amount_displaying_page