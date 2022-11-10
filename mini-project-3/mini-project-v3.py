# Pop-Up Cafe UI creation #

# PLEASE RUN IN FULL SCREEN #
import sys
import os
import re
import ast
import shutil


main = 'main'
products = 'products'
courier = 'courier'
couriers = 'couriers'
orders = 'orders'
body = 'body'
options = 'options'
bottom = 'bottom'

storage = {
products: 'products.txt',
couriers: 'couriers.txt',
orders: 'orders.txt'
}


data = {
}

data[products] = [           # Default data, will be overrided by stored data existed in file or system.
    "Roast Beef Launch",
    "Roast Chicken Launch",
    "Chicken & Mushroom Pie",
    "Stroganoff with Rice",
    "Sweet & Sour Chicken",
    "Fisherman's Fish Pie",
    "Corned Beef Hash",
    "Cumberland Meat Pie",
    "Fruity Chicken Curry",
    "Spaghetti Bolognese",
    "Cod, Chips & Peas",
    "Shepherd's Pie",
    "Cottage Sweet Pie",
    "Sausages & Mash",
    ]


data[couriers] = [     # Default data, will be overrided by stored data existed in file or system.
    "John",
    "Mary",
    "peter",
    "Derek",
    "Eliza",
    "Anthony",
    "Winson",
    "Sophia",
    "Olivia",
]

data[orders] = [
    {
        "customer_name": "John",
        "customer_address": "26 Sedgeford Rd, Manchester M40 8QL",
        "customer_phone": "0789887334",
        "courier": "Mary",
        "status": "Preparing",
    },
    {
        "customer_name": "Mary",
        "customer_address": "1 Douglas Grn, Salford, Manchester M6 6ES",
        "customer_phone": "0715252177",
        "courier": "Peter",
        "status": "Awaiting Pickup",
    },
    {
        "customer_name": "Sam",
        "customer_address": "71 Blackfriars Rd, Salford, Manchester M3 7GQ",
        "customer_phone": "07411235668",
        "courier": "Eliza",
        "status": "Out-for-Delivery",
    },
]


order_status = ["Preparing", "Awaiting Pickup", "Out-for-Delivery", "Delivered"]

border_chr = ['~~~', '111', '222', '333', '444', '555'] 
# Border characters to ouline the border of menu. Default is single character. But you can increase the border width by increasing the number of characters at the list elements.

padding_chr = ['~', '1', '2', '3', '4', '5'] # Padding character must be single character in f-string. 




menu = {
    main:{},
    products:{},
    couriers:{},
    orders:{},
}

menu_width = 74
menu_half_width = int(menu_width / 2)

menu_header = [
'', # Empty element constructs new line.
'         PPPPP      OOOOO     PPPPP        uu     uu   PPPPP            ',
'         PP  PPP   OO   OO    PP  PPP      uu     uu   PP  PPP          ',
'         PPPPP    OO     OO   PPPPP        uu     uu   PPPPP            ',
'         PP        OO   OO    PP           uu     uu   PP               ',
'         PP         OOOOO     PP             uuuuu     PP               ',
'  Café __________________________________________________________ Café  ',
'',
]

menu[main][body] = [
'MM     MM       A       II   NN    N',
'M M   M M      A A      II   N N   N',
'M  M M  M     A   A     II   N  N  N',
'M   M   M    A A A A    II   N   N N',
'M       M   A       A   II   N    NN',
'',
'', # Empty elements construct new lines.
]

menu[main][options] = [
' [ 0 ]: exit programme',
' [ 1 ]: products menu option',
' [ 2 ]: couriers menu option',
' [ 3 ]: orders menu option',
]

menu[main][bottom] = [
'',
'', # Empty elements construct new lines.
]

menu[products][body] = [
'ppppp   RRRRR     OOOO    DDDD     U     U    CCCCC  TTTTTT   SSSSS ',
'p   pp  R   RR   O    O   D   DD   U     U   CC        TT    SS     ',
'pppp    RRRR    O      O  D    DD  U     U  CC         TT      SSS  ',
'p       R   R    O    O   D   DD   U     U   CC        TT         SS',
'p       R    R    OOOO    DDDD      UUUUU     CCCCC    TT     SSSSS ',
'',
'',
]

menu[products][options] = [
' [ 0 ]: return to main menu',
' [ 1 ]: print product list',
' [ 2 ]: create new product',
' [ 3 ]: update product name',
' [ 4 ]: delete product',
]

menu[products][bottom] = [
'',
]


menu[couriers][body] = [
'  CCCCC    OOOO    U     U  RRRRR   II  EEEEEEE   SSSSS ',
' CC       O    O   U     U  R   RR  II  EE       SS     ',
'CC       O      O  U     U  RRRR    II  EEEEE      SSS  ',
' CC       O    O   U     U  R   R   II  EE            SS',
'  CCCCC    OOOO     UUUUU   R    R  II  EEEEEEE   SSSSS ',
'',
'',
]

menu[couriers][options] = [
' [ 0 ]: return to main menu',
' [ 1 ]: print couriers list',
' [ 2 ]: create new courier',
' [ 3 ]: update courier name',
' [ 4 ]: delete courier',
]

menu[couriers][bottom] = [
'',
]




menu[orders][body] = [
'  OOOO    RRRRR    DDDD      EEEEEEE   RRRRR     SSSSS ',
' O    O   R   RR   D   DD    E         R   RR   SS     ',
'O      O  RRRR     D    DD   EEEEEE    RRRR       SSS  ',
' O    O   R   R    D   DD    E         R   R         SS',
'  OOOO    R    R   DDDD      EEEEEEE   R    R    SSSSS ',
'',
'',
]

menu[orders][options] = [
' [ 0 ]: return to main menu',
' [ 1 ]: print orders dictionary',
' [ 2 ]: create new order',
' [ 3 ]: update order status',
' [ 4 ]: update order',
' [ 5 ]: delete order',
]

menu[orders][bottom] = [
'',
]


cc = { # color code dictionary
    0: '\033[1;32m',   
    1: '\033[1;32m',
    2: '\033[1;33m',
    3: '\033[1;36m',
    4: '\033[1;35m',
    5: '\033[1;31m',
    'E': '\033[m',
}


op_list = [     #  Options big-size digit list, each digit conatins 5 list elements.
'    11   ',
'  1111   ',
'    11   ',
'    11   ',
' 11111111',
'   2222  ',
' 22    22',
'     22  ',
'   22    ',
' 22222222',
' 3333333 ',  
'       33',  
'   3333  ', 
'       33', 
' 3333333 ', 
'      44 ', 
'    4444 ', 
'  44  44 ', 
' 44444444',
'      44 ',
' 55555555', 
' 55      ', 
' 55555555', 
'       55',
' 55555555',
'         ',  # last elements op_list[-1] used for default padding
]



op_elems_no = 5  # Each big-size digit contains 5 list elements.

op_max_display_no = 4 # Maximun number of big-digits dispaly in vertical. 

op_total_ht = op_elems_no  * op_max_display_no # Total height to display vertial digits.


# Please Do Not Modify Below: ################################################

# Start Functions Section ####################################################

def init_file_data(file_name, default_data): # Function initilizes data, use default data if stroage data not exist
    with open(file_name, 'a') as f: # create file if not exist
        pass
    with open(file_name, 'r+') as f: # read the fil, use r+, do not erase existing data
        f_list = f.readlines()
        f_list[:] = [x.replace("\n", "").strip() for x in f_list if x.replace("\n", "").strip()]
        if len(f_list) == 0:      # if no content, write the defualt data into the file
            for item in default_data:
                f.write(f'{item}\n')            
        else:                            # if aleady have content, override the default data
            default_data[:] = f_list
    return default_data 


def update_storage(name): # Function upates data storage 
    if name in storage and name in data:
        with open(storage[name], 'w+') as f: # Use w+, erase existing data and write whole new set of data    
             [f.write(f'{item}\n') for item in data[name]]



def clear_screen(): # Function to clear the screen, suitable for winows and linux    
    platform  = sys.platform
    if platform == "win32":
        os.system("clear") # Git bash having "clear" may pretend win32. Howerver it will bypass below "cls" error warning.
        os.system("cls")   # Genuine win32 overrides above "clear" error warning.
    else:
        os.system("clear")

def joint_opts_list(menu_name, option_value): # Function joints two options in one line on menu.
    joint_list = []
    cc_count = []  #Colour code count
    cc_length = len(cc[option_value]) + len(cc["E"]) # Colour code length
    temp_opts = []
    for item in menu[menu_name][options]: # Assign temp list to prevent polluting the original list.
        temp_opts.append(item)
    if len(temp_opts) % 2 != 0:
        temp_opts.append('') # Prevent colour codes shift. Append 1 empty element if len() is an odd number.
    for x in range(0, len(temp_opts), 2):
        str = ''
        i = 0
        for elm in temp_opts[x:x + 2]: # Join 2 elements to 1 elements
            if option_value != 0 and option_value  == temp_opts.index(elm):
                elm = f'{cc[option_value]}{elm}{cc["E"]}'
                item = f'{elm: <{menu_half_width + cc_length}}'
                i += 1
            else:
                item = f'{elm: <{menu_half_width}}'            
            str += item
        cc_count.append(i)
        joint_list.append(str)
    return [joint_list, cc_count]


def print_menu(menu_name, option_value): # Function prints products menu
    clear_screen()
    # print(f'option_value: {option_value}') # For debug use
    menu_list = []
    cc_count = []
    opts_list = joint_opts_list(menu_name, option_value)

    border = border_chr[option_value]
    cc_length = len(cc[option_value]) + len(cc["E"])

    menu_list.append(f'{border:{padding_chr[option_value]}<{menu_width +len(border)}}{border}')
    cc_count.append(0)
    for elm in menu_header:
        elm = f'{cc[option_value]}{elm}{cc["E"]}'
        menu_list.append(f'{border}{elm: ^{menu_width + cc_length}}{border}')
        cc_count.append(1)
    for elm in menu[menu_name][body]:
        menu_list.append(f'{border}{elm: ^{menu_width}}{border}')
        cc_count.append(0)
    for x, elm in enumerate(opts_list[0]):
        menu_list.append(f'{border}{elm: ^{menu_width}}{border}')
        cc_count.append(opts_list[1][x] if opts_list[1][x] > 0 else 0)
    for elm in menu[menu_name][bottom]:
        menu_list.append(f'{border}{elm: ^{menu_width}}{border}')
        cc_count.append(0)
    menu_list.append(f'{border:{padding_chr[option_value]}<{menu_width +len(border)}}{border}')
    cc_count.append(0)

    op_start_pos = (option_value - 1) * op_elems_no
    # print(f'op_start_pos: {op_start_pos}') # For debug use
    digit_print_pos = op_start_pos % op_total_ht

    for x in range(len(menu_list)):
        if op_start_pos >= 0 and x in range(digit_print_pos, digit_print_pos + op_elems_no):
            menu_list[x] = (menu_list[x] + f'{cc[option_value]}{op_list[x % op_elems_no + op_start_pos]}{cc["E"]}')
            cc_count[x] += 1
        else:
            menu_list[x] = (menu_list[x] + f'{op_list[-1]}')

    screen_size = shutil.get_terminal_size()
    for x in range(len(menu_list)):
        spacer = cc_count[x] * (cc_length)
        print(f'{menu_list[x]: ^{screen_size.columns + spacer - len(op_list[-1]) - 2 * len(border)}}')



def input_option(menu_name):    # Function handles user input on menu
    while True:
        user_input = input("Enter option in square brackets [  ]: ").strip()
        if re.match('^([0-9]+)$', user_input):
            user_input = int(user_input)
            if user_input < len(menu[menu_name][options]):
                if menu_name == main and user_input == 0:
                    clear_screen()
                    quit()
                break # break if user_input < len(menu[menu_name][options]):
    return user_input


def list_items(menu_name, option_value):  # Function prints products listing
    if len(data[menu_name]) > 0:
        screen_size = shutil.get_terminal_size()
        cc_length = len(cc[option_value]) + len(cc["E"])
        temp=[]
        for item in data[menu_name]:
            temp.append(str(item))  # Convert the list elements to string for display purpose.
        elm_max_length = len(max(temp, key=len)) + len(str(len(temp))) + len('(  ): ')
        # elm_max_length = the max text element length in list + text length of number of elemets in list (e.g. 23 is length 2, 645 is length 3) + text length of '(  ): '        
        chunk_no =  screen_size.columns / elm_max_length
        display_chunk_size = 1 if chunk_no < 1 else int(chunk_no)
        pedding_length = 0 if display_chunk_size == 1 else elm_max_length + cc_length

        item_number = 0
        print(" ") # For nice looking
        for i in range(0, len(temp), display_chunk_size):        
            items_string = ''
            for item_name in temp[i:i + display_chunk_size]:
                item_number += 1
                colour_number = f"{cc[option_value]}{item_number}{cc['E']}"
                colour_string = f"( {colour_number} ): {item_name}"
                items_string += f"{colour_string: <{pedding_length}}"
            print(items_string)
        print(" ") # For nice looking


# End Functions Section ######################################################

# Initialize data, use default data if storage data not exist.
data = {key:init_file_data(storage[key], data[key]) for key in storage}

for x in range(len(data[orders])):
    if type(data[orders][x]) is str: # dictonary read from file is str, need to convert back to dict
        data[orders][x] = ast.literal_eval(data[orders][x]) # change str back to dict


main_input = 0

while True:

    if main_input == 0:
        print_menu(main, main_input)
        print(" ") # For nice looking
        main_input = input_option(main)
    
    ######################################################
    # Products menu
    if main_input == 1:

        user_input = 0
        while True:
            if user_input == 0:
                print_menu(products, 0) # Default menu       
            if user_input == 1:
                print_menu(products, user_input)
                list_items(products, user_input)  # ------- Print products list action ------------ #
                index_input = input(f"{cc[user_input]}Press Enter to continue:{cc['E']} ").strip()
                print_menu(products, 0) # Reset to default menu after enter to continue
                
            elif user_input == 2:
                print_menu(products, user_input)
                print(" ") # For nice looking
                while True:
                    new_product = input("Enter new product name: ").strip()
                
                    if new_product == "":
                        print_menu(products, 0) # Reset to default menu after enter new product name.
                        break
                    elif new_product in data[products]:
                        print(f"{new_product} already exist, please try again.")
                    elif new_product not in data[products]:
                        data[products].append(new_product)  # ------- Add product action ------------ #
                        update_storage(products)
                        print_menu(products, 0) # Reset to default menu after enter new product name.
                        list_items(products, user_input)
                        print(f"( {cc[user_input]}{len(data[products])}{cc['E']} ): {new_product} : added to products list")
                        break
                
            elif user_input == 3:
                print_menu(products, user_input)
                list_items(products, user_input)
                while True:
                    index_input = input("Enter product (  ) to update: ").strip()
                    if index_input == "":
                        print_menu(products, 0) # Reset to default menu after enter to escape
                        break
                    elif re.match('^([0-9]+)$', index_input):
                        index_input = int(index_input)
                        if index_input >=1 and index_input <= len(data[products]):
                            print(" ") # For nice looking
                            edit_product = input(f"Edit product ( {cc[user_input]}{index_input}{cc['E']} ): {data[products][index_input-1]} : ").strip()
                           
                            if edit_product == "":
                                print_menu(products, 0) # Reset to default menu after escape
                                break
                            elif edit_product in data[products]:
                                print(f"{edit_product} already exist, please try again.")
                            elif edit_product not in data[products]:
                                data[products][index_input-1]=edit_product  # ------- Edit action ------------ #
                                update_storage(products)
                                print_menu(products, 0) # Reset to default menu after edit product name
                                list_items(products, user_input)
                                print(f"Successfully updated product ( {cc[user_input]}{index_input}{cc['E']} ): {data[products][index_input-1]}")
                                break        
            elif user_input == 4:
                print_menu(products, user_input)
                list_items(products, user_input)
                while True:
                    index_input = input("Enter product (  ) to delete: ").strip()
                    if index_input == "":
                        print_menu(products, 0) # Reset to default menu after enter to escape
                        break
                    elif re.match('^([0-9]+)$', index_input):
                        index_input = int(index_input)
                        if index_input >=1 and index_input <= len(data[products]):
                            print(" ") # For nice looking
                            del_product = input(f"Delete product ( {cc[user_input]}{index_input}{cc['E']} ): {data[products][index_input-1]} \nConfirm delete: y/n? ").strip()
                            print_menu(products, 0) # Reset to default menu after delete product.
                            if del_product == 'y' or del_product.upper() == 'Y':
                                deleted_name = data[products][index_input-1] 
                                del data[products][index_input-1]   # ------- Delete action ------------ #
                                update_storage(products)
                                list_items(products, user_input)
                                print(f"Successfully deleted. Previously ( {cc[user_input]}{index_input}{cc['E']} ): {deleted_name}")
                                break
                            else:
                                break

            print(" ") # For nice looking
            user_input = input_option(products)
            if user_input == 0:
                main_input = 0
                break
    
    
    
    # Couriers menu
    elif main_input == 2:    
    
        user_input = 0
        while True:
            if user_input == 0:
                print_menu(couriers, 0) # Default menu       
            if user_input == 1:
                print_menu(couriers, user_input)
                list_items(couriers, user_input)  # ------- Print couriers list action ------------ #
                index_input = input(f"{cc[user_input]}Press Enter to continue:{cc['E']} ").strip()
                print_menu(couriers, 0) # Reset to default menu after enter to continue
                
            elif user_input == 2:
                print_menu(couriers, user_input)
                print(" ") # For nice looking
                while True:
                    new_courier = input("Enter new courier name: ").strip()

                    if new_courier == "":
                        print_menu(couriers, 0) # Reset to default menu after enter new product name.
                        break
                    elif new_courier in data[couriers]:
                        print(f"{new_courier} already exist, please try again.")
                    elif new_courier not in data[couriers]:
                        data[couriers].append(new_courier)  # ------- Add product action ------------ #
                        update_storage(couriers)
                        print_menu(couriers, 0) # Reset to default menu after enter new product name.
                        list_items(couriers, user_input)
                        print(f"( {cc[user_input]}{len(data[couriers])}{cc['E']} ): {new_courier} : added to couriers list")
                        break
                
            elif user_input == 3:
                print_menu(couriers, user_input)
                list_items(couriers, user_input)
                while True:
                    index_input = input("Enter courier (  ) to update: ").strip()
                    if index_input == "":
                        print_menu(couriers, 0) # Reset to default menu after enter to escape
                        break
                    elif re.match('^([0-9]+)$', index_input):
                        index_input = int(index_input)
                        if index_input >=1 and index_input <= len(data[couriers]):
                            print(" ") # For nice looking
                            edit_courier= input(f"Edit courier ( {cc[user_input]}{index_input}{cc['E']} ): {data[couriers][index_input-1]} : ").strip()
                            
                            if edit_courier == "":
                                print_menu(couriers, 0) # Reset to default menu after edit product name
                                break
                            elif edit_courier in data[couriers]:
                                print(f"{edit_courier} already exist, please try again.")
                            elif edit_courier not in data[couriers]:
                                data[couriers][index_input-1]=edit_courier  # ------- Edit action ------------ #
                                update_storage(couriers)
                                print_menu(couriers, 0) # Reset to default menu after edit product name
                                list_items(couriers, user_input)
                                print(f"Successfully updated courier ( {cc[user_input]}{index_input}{cc['E']} ): {data[couriers][index_input-1]}")
                                break        
            elif user_input == 4:
                print_menu(couriers, user_input)
                list_items(couriers, user_input)
                while True:
                    index_input = input("Enter courier (  ) to delete: ").strip()
                    if index_input == "":
                        print_menu(couriers, 0) # Reset to default menu after enter to escape
                        break
                    elif re.match('^([0-9]+)$', index_input):
                        index_input = int(index_input)
                        if index_input >=1 and index_input <= len(data[couriers]):
                            print(" ") # For nice looking
                            del_product = input(f"Delete courier ( {cc[user_input]}{index_input}{cc['E']} ): {data[couriers][index_input-1]} \nConfirm delete: y/n? ").strip()
                            print_menu(couriers, 0) # Reset to default menu after delete product.
                            if del_product == 'y' or del_product.upper() == 'Y':
                                deleted_name = data[couriers][index_input-1] 
                                del data[couriers][index_input-1]   # ------- Delete action ------------ #
                                update_storage(couriers)
                                list_items(couriers, user_input)
                                print(f"Successfully deleted. Previously ( {cc[user_input]}{index_input}{cc['E']} ): {deleted_name}")
                                break
                            else:
                                break

            print(" ") # For nice looking
            user_input = input_option(couriers)
            if user_input == 0:
                main_input = 0
                break 
   
    
    # Orders menu
    elif main_input == 3:

        user_input = 0
        while True:
            if user_input == 0:
                print_menu(orders, 0) # Default menu       
            if user_input == 1:
                print_menu(orders, user_input)
                list_items(orders, user_input)  # ------- Print orders list action ------------ #
                index_input = input(f"{cc[user_input]}Press Enter to continue:{cc['E']} ").strip()
                print_menu(orders, 0) # Reset to default menu after enter to continue
                
            elif user_input == 2:
                print_menu(orders, user_input)
                print(" ") # For nice looking
                while True:
                    cust_name = input("Enter new order customer name: ").strip()
                    cust_address = input("Enter new order customer address: ").strip()
                    cust_phone = input("Enter new order customer phone: ").strip()
                    

                    if cust_name == "" or cust_address == "" or cust_phone == "":
                        print_menu(orders, 0) # Reset to default menu after no input.
                        break
                    else:
                        
                        print(" ") # For nice looking
                        courier_list="Courier choices: "
                        for x in range(len(data[couriers])):
                            courier_list += f"[{x}] {data[couriers][x]}, "
                        print(courier_list)
                        print(" ") # For nice looking

                        while True:
                            edit_order = input(f"Choose courier number [ ]: Enter e to esacpe: ").strip()
                            if edit_order == "e":
                                print_menu(orders, 0) # Reset to default menu after escape
                                break
                            elif re.match('^([0-9]+)$', edit_order):
                                edit_order = int(edit_order)
                                if edit_order < len(data[couriers]):                                   
                                    new_order = {
                                        "customer_name": cust_name,
                                        "customer_address": cust_address,
                                        "customer_phone": cust_phone,
                                        "courier": data[couriers][edit_order],
                                        "status": order_status[0],
                                    }
                                    data[orders].append(new_order)  # ------- Add order action ------------ #
                                    update_storage(orders)
                                    print_menu(orders, 0) # Reset to default menu after adding order
                                    list_items(orders, user_input)
                                    print(f"Added new order ( {cc[user_input]}{len(data[orders])}{cc['E']} ): {new_order}")
                                    break                                    
                    break # break the outer while loop                
                
            elif user_input == 3:
                print_menu(orders, user_input)
                list_items(orders, user_input)
                while True:
                    index_input = input("Enter order (  ) to update: ").strip()
                    if index_input == "":
                        print_menu(orders, 0) # Reset to default menu after enter to escape
                        break
                    elif re.match('^([0-9]+)$', index_input):
                        index_input = int(index_input)
                        if index_input >=1 and index_input <= len(data[orders]):
                            print(" ") # For nice looking                      
                            print(f"Order ( {cc[user_input]}{index_input}{cc['E']} ) status: {data[orders][index_input-1]['status']}")
                            print(" ") # For nice looking
                            status_list="Status choices: "
                            for x in range(len(order_status)):
                                status_list += f"[{x}] {order_status[x]}, "
                            print(status_list.rstrip(', '))
                            print(" ") # For nice looking

                            while True:
                                edit_order = input(f"Choose status number [ ]: ").strip()
                                if edit_order == "":
                                    print_menu(orders, 0) # Reset to default menu after edit orders name
                                    break
                                elif re.match('^([0-9]+)$', edit_order):
                                    edit_order = int(edit_order)
                                    if edit_order < len(order_status):
                                        data[orders][index_input-1]['status'] = order_status[edit_order]  # ------- Edit action ------------ #
                                        update_storage(orders)
                                        print_menu(orders, 0) # Reset to default menu after edit orders name
                                        list_items(orders, user_input)
                                        print(f"Successfully updated. Order ( {cc[user_input]}{index_input}{cc['E']} ) status: {data[orders][index_input-1]['status']}")
                                        break
                            break # break the outer while loop
  
            elif user_input == 4:
                print_menu(orders, user_input)
                list_items(orders, user_input)
                while True:
                    index_input = input("Enter order (  ) to update: ").strip()
                    if index_input == "":
                        print_menu(orders, 0) # Reset to default menu after enter to escape
                        break
                    elif re.match('^([0-9]+)$', index_input):
                        index_input = int(index_input)
                        if index_input >=1 and index_input <= len(data[orders]):
                            print(" ") # For nice looking
                            print(f"Edit order ( {cc[user_input]}{index_input}{cc['E']} ) ")
                            elm_max_length = len(max(list(x for x in data[orders][index_input-1]), key=len))
                            for x, y, in data[orders][index_input-1].items():
                                if x != 'status' and x != courier:
                                    print(f'{x: <{elm_max_length}} : {y}')
                                    edit_order = input(f'{x: <{elm_max_length}} : ').strip()
                                    if edit_order == "":
                                        pass
                                    else:
                                        data[orders][index_input-1][x] = edit_order # ------- Edit action ------------ #
                                        update_storage(orders)
                                elif x == courier:
                                    print(f'{x: <{elm_max_length}} : {y}')          
                                    courier_list=f'{x: <{elm_max_length}} : '
                                    for x in range(len(data[couriers])):
                                        courier_list += f"[{x}] {data[couriers][x]}, "
                                    print(courier_list.rstrip(', '))
                                    print(" ") # For nice looking

                                    while True:
                                        edit_order = input(f"Choose courier number [ ]: ").strip()
                                        if edit_order == "":
                                            break
                                        elif re.match('^([0-9]+)$', edit_order):
                                            edit_order = int(edit_order)
                                            if edit_order < len(data[couriers]):
                                                data[orders][index_input-1][courier] = data[couriers][edit_order]  # ------- Edit action ------------ #
                                                update_storage(orders)
                                                break
                                
                                elif x == 'status':
                                    print(" ") # For nice looking
                                    print(f'{x: <{elm_max_length}} : {y}')
                                    status_list=f'{x: <{elm_max_length}} : '
                                    for x in range(len(order_status)):
                                        status_list += f"[{x}] {order_status[x]}, "
                                    print(status_list.rstrip(', '))
                                    print(" ") # For nice looking

                                    while True:
                                        edit_order = input(f"Choose status number [ ]: Enter e to escape: ").strip()
                                        if edit_order == "e":
                                            break
                                        elif re.match('^([0-9]+)$', edit_order):
                                            edit_order = int(edit_order)
                                            if edit_order < len(order_status):
                                                data[orders][index_input-1]['status'] = order_status[edit_order]  # ------- Edit action ------------ #
                                                update_storage(orders)
                                                print_menu(orders, 0) # Reset to default menu after edit orders name
                                                list_items(orders, user_input)
                                                print(f"Updated order ( {cc[user_input]}{index_input}{cc['E']} ): {data[orders][index_input-1]}")
                                                break
                            break # break the outer while loop

            elif user_input == 5:
                print_menu(orders, user_input)
                list_items(orders, user_input)
                while True:
                    index_input = input("Enter order (  ) to delete: ").strip()
                    if index_input == "":
                        print_menu(orders, 0) # Reset to default menu after enter to escape
                        break
                    elif re.match('^([0-9]+)$', index_input):
                        index_input = int(index_input)
                        if index_input >=1 and index_input <= len(data[orders]):
                            print(" ") # For nice looking
                            del_order = input(f"Delete order ( {cc[user_input]}{index_input}{cc['E']} ): {data[orders][index_input-1]} \nConfirm delete: y/n? ").strip()
                            print_menu(orders, 0) # Reset to default menu after delete order.
                            if del_order == 'y' or del_order.upper() == 'Y':
                                deleted_name = data[orders][index_input-1] 
                                del data[orders][index_input-1]   # ------- Delete action ------------ #
                                update_storage(orders)
                                list_items(orders, user_input)
                                print(f"Successfully deleted. Previously ( {cc[user_input]}{index_input}{cc['E']} ): {deleted_name}")
                                break
                            else:
                                break

            print(" ") # For nice looking
            user_input = input_option(orders)
            if user_input == 0:
                main_input = 0
                break
    
    else:
        main_input = 0


