# Pop-Up Cafe UI creation #

# PLEASE RUN IN FULL SCREEN #

import os
import re

products_list=[
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

order_status = ["Preparing", "Awaiting Pickup", "Out-for-Delivery", "Delivered"]

orders_list =[
{
    "customer_name": "John",
    "customer_address": "26 Sedgeford Rd, Manchester M40 8QL",
    "customer_phone": "0789887334",
    "status": "Preparing",
},
{
    "customer_name": "Mary",
    "customer_address": "1 Douglas Grn, Salford, Manchester M6 6ES",
    "customer_phone": "0715252177",
    "status": "Awaiting Pickup",
},
{
    "customer_name": "Sam",
    "customer_address": "71 Blackfriars Rd, Salford, Manchester M3 7GQ",
    "customer_phone": "07411235668",
    "status": "Out-for-Delivery",
},
{
    "customer_name": "Peter",
    "customer_address": "451 Liverpool St., Salford, Manchester M6 5QQ",
    "customer_phone": "0789887334",
    "status": "Delivered",
},
{
    "customer_name": "Eliza",
    "customer_address": "48 Heys Rd, Prestwich, Manchester M25 1JZ",
    "customer_phone": "0777888555",
    "status": "Delivered",
},
]



border_chr = ['~~~', '111', '222', '333', '444', '555'] 
# Border characters to ouline the border of menu. Default is single character. But you can increase the border width by increasing the number of characters at the list elements.

padding_chr = ['~', '1', '2', '3', '4', '5'] # Padding character must be single character in f-string. 

menu_header = [
'                                                                        ',
'         PPPPP      OOOOO     PPPPP        uu     uu   PPPPP            ',
'         PP  PPP   OO   OO    PP  PPP      uu     uu   PP  PPP          ',
'         PPPPP    OO     OO   PPPPP        uu     uu   PPPPP            ',
'         PP        OO   OO    PP           uu     uu   PP               ',
'         PP         OOOOO     PP             uuuuu     PP               ',
'  Café __________________________________________________________ Café  ',
'                                                                        ',
]


main_max_opts = 2
main_menu = [
'                 MM     MM       A       II   NN    N                   ',
'                 M M   M M      A A      II   N N   N                   ',
'                 M  M M  M     A   A     II   N  N  N                   ',
'                 M   M   M    A A A A    II   N   N N                   ',
'                 M       M   A       A   II   N    NN                   ',
'                                                                        ',
'                                                                        ',
'   [ 0 ]: exit programme            [ 1 ]: products menu option         ',
'   [ 2 ]: orders menu option                                            ',
'                                                                        ',
'                                                                        ',
]

products_max_opts = 4
products_menu = [
'  ppppp   RRRRR     OOOO    DDDD     U     U    CCCCC  TTTTTT   SSSSS   ',
'  p   pp  R   RR   O    O   D   DD   U     U   CC        TT    SS       ',
'  pppp    RRRR    O      O  D    DD  U     U  CC         TT      SSS    ',
'  p       R   R    O    O   D   DD   U     U   CC        TT         SS  ',
'  p       R    R    OOOO    DDDD      UUUUU     CCCCC    TT     SSSSS   ',
'                                                                        ',
'                                                                        ',
'   [ 0 ]: return to main menu        [ 1 ]: print product list          ',
'   [ 2 ]: create new product         [ 3 ]: update product name         ',
'   [ 4 ]: delete product                                                ',
'                                                                        ',
]



orders_max_opts = 5
orders_menu = [
'           OOOO    RRRRR    DDDD      EEEEEEE   RRRRR     SSSSS         ',
'          O    O   R   RR   D   DD    E         R   RR   SS             ',
'         O      O  RRRR     D    DD   EEEEEE    RRRR       SSS          ',
'          O    O   R   R    D   DD    E         R   R         SS        ',
'           OOOO    R    R   DDDD      EEEEEEE   R    R    SSSSS         ',
'                                                                        ',
'                                                                        ',
'   [ 0 ]: return to main menu        [ 1 ]: print orders dictionary     ',
'   [ 2 ]: create new order           [ 3 ]: update order status         ',
'   [ 4 ]: update order               [ 5 ]: delete order                ',
'                                                                        ',
]


# <---- Both sides at last have one # character to make the border -----> #

# So default menu width is equal to: menu_width = len(main_menu[0]) + 2 
menu_width = len(menu_header[0]) + 2 

cd = { # color dictionary
    'E': '\033[m',   
    'G': '\033[32m',
    'Y': '\033[33m',
    'B': '\033[34m',
    'M': '\033[35m',
    'C': '\033[36m',
    'BG':'\033[1;32;40m',
}

op_list = [     #  Options big-size digit list, each digit conatins 5 list elements.
cd['G'] + '     11   ' + cd['E'],
cd['G'] + '   1111   ' + cd['E'],
cd['G'] + '     11   ' + cd['E'],
cd['G'] + '     11   ' + cd['E'],
cd['G'] + '  11111111' + cd['E'],
cd['Y'] + '    2222  ' + cd['E'],
cd['Y'] + '  22    22' + cd['E'],
cd['Y'] + '      22  ' + cd['E'],
cd['Y'] + '    22    ' + cd['E'],
cd['Y'] + '  22222222' + cd['E'],
cd['C'] + '  3333333 ' + cd['E'],  
cd['C'] + '        33' + cd['E'],  
cd['C'] + '    3333  ' + cd['E'], 
cd['C'] + '        33' + cd['E'], 
cd['C'] + '  3333333 ' + cd['E'], 
cd['M'] + '       44 ' + cd['E'], 
cd['M'] + '     4444 ' + cd['E'], 
cd['M'] + '   44  44 ' + cd['E'], 
cd['M'] + '  44444444' + cd['E'],
cd['M'] + '       44 ' + cd['E'],
cd['B'] + ' 555555555' + cd['E'], 
cd['B'] + ' 55       ' + cd['E'], 
cd['B'] + ' 555555555' + cd['E'], 
cd['B'] + '        55' + cd['E'],
cd['B'] + ' 555555555' + cd['E'],
]



op_elems_no = 5  # Each big-size digit contains 5 list elements.

op_max_display_no = 4 # Maximun number of big-digits dispaly in vertical. 

op_total_ht = op_elems_no  * op_max_display_no # Total height to display vertial digits.

display_chunk_size = 4  # display chunk size. The number of elements to display each line on the screen.

# Please Do Not Modify Below: ################################################

# Start Functions Section ####################################################

def print_menu(menu_name, option_value): # Function prints products menu
    os.system("cls")
    # print(f'option_value: {option_value}') # For debug use
    menu_list = menu_header + menu_name # Two lists join together

    menu = []
    menu.append(f'{border_chr[option_value]:{padding_chr[option_value]}<{menu_width +len(border_chr[option_value])-2}}{border_chr[option_value]}')
    
    for x in range(len(menu_list)):
        menu.append(border_chr[option_value] + menu_list[x] + border_chr[option_value])
    menu.append(f'{border_chr[option_value]:{padding_chr[option_value]}<{menu_width +len(border_chr[option_value])-2}}{border_chr[option_value]}')
    
    op_start_pos = (option_value - 1) * op_elems_no
    # print(f'op_start_pos: {op_start_pos}') # For debug use
    letter_print_position = op_start_pos % op_total_ht
    for x in range(len(menu)):
        if op_start_pos >= 0 and x in range(letter_print_position, letter_print_position + op_elems_no):
            print(menu[x] + op_list[x % op_elems_no + op_start_pos])
        else:
            print(menu[x])




def input_main_options(max_opts_num):    # Function handles user input on main menu
    while True:
        user_input = input("Enter option in square brackets [  ]: ")
        if re.match('^([0-9]+)$', user_input):
            user_input = int(user_input)
            if user_input <= max_opts_num:
                if user_input == 0:
                    os.system("cls")
                    quit()
                break
    return user_input

def input_option(max_opts_num): # Function handles user input options on other menus
    while True:
        user_input = input("Enter option in square brackets [  ]: ")
        if re.match('^([0-9]+)$', user_input):
            user_input = int(user_input)
            if user_input <= max_opts_num:
                break
    return user_input

def list_products():  # Function prints products listing
    if len(products_list) > 0:
        item_number = 0
        print(" ") # For nice looking
        for i in range(0, len(products_list), display_chunk_size):        
            items_string = ''
            for item_name in products_list[i:i + display_chunk_size]:
                item_number += 1
                items_string += f"( {cd['BG']}{item_number}{cd['E']} ): {item_name} \t"
            print(items_string)
        print(" ") # For nice looking

def list_orders():  # Function prints orders listing
    if len(orders_list) > 0:
        item_number = 0
        print(" ") # For nice looking
        for i in range(0, len(orders_list), display_chunk_size):        
            items_string = ''
            for item_name in orders_list[i:i + display_chunk_size]:
                item_number += 1
                items_string += f"( {cd['BG']}{item_number}{cd['E']} ): {item_name} \t"
            print(items_string)
        print(" ") # For nice looking


# End Functions Section ######################################################




main_input = 0

while True:

    if main_input == 0:
        print_menu(main_menu, main_input)
        print(" ") # For nice looking
        main_input = input_main_options(main_max_opts)
    
    ######################################################
    # Products menu
    if main_input == 1:

        user_input = 0
        while True:
            if user_input == 0:
                print_menu(products_menu, 0) # Default menu       
            if user_input == 1:
                print_menu(products_menu, user_input)
                list_products()  # ------- Print products list action ------------ #
                index_input = input("Press Enter to continue: ")
                print_menu(products_menu, 0) # Reset to default menu after enter to continue
                
            elif user_input == 2:
                print_menu(products_menu, user_input)
                print(" ") # For nice looking
                while True:
                    new_product = input("Enter new product name: ")
                    print_menu(products_menu, 0) # Reset to default menu after enter new product name.
                    if new_product == "":
                        break
                    elif new_product:
                        products_list.append(new_product)  # ------- Add product action ------------ #
                        list_products()
                        print(f"( {len(products_list)} ): {new_product} : added to products list")
                        break
                
            elif user_input == 3:
                print_menu(products_menu, user_input)
                list_products()
                while True:
                    index_input = input("Enter product (  ) to update: ")
                    if index_input == "":
                        print_menu(products_menu, 0) # Reset to default menu after enter to escape
                        break
                    elif re.match('^([0-9]+)$', index_input):
                        index_input = int(index_input)
                        if index_input >=1 and index_input <= len(products_list):
                            print(" ") # For nice looking
                            edit_product = input(f"Edit product ( {index_input} ): {products_list[index_input-1]} : ")
                            print_menu(products_menu, 0) # Reset to default menu after edit product name
                            if edit_product == "":
                                break
                            elif edit_product:
                                products_list[index_input-1]=edit_product  # ------- Edit action ------------ #
                                list_products()
                                print(f"Successfully updated product ( {index_input} ): {products_list[index_input-1]}")
                                break        
            elif user_input == 4:
                print_menu(products_menu, user_input)
                list_products()
                while True:
                    index_input = input("Enter product (  ) to delete: ")
                    if index_input == "":
                        print_menu(products_menu, 0) # Reset to default menu after enter to escape
                        break
                    elif re.match('^([0-9]+)$', index_input):
                        index_input = int(index_input)
                        if index_input >=1 and index_input <= len(products_list):
                            print(" ") # For nice looking
                            del_product = input(f"Delete product ( {index_input} ): {products_list[index_input-1]} : y/n? ")
                            print_menu(products_menu, 0) # Reset to default menu after delete product.
                            if del_product == 'y' or del_product.upper() == 'Y':
                                deleted_name = products_list[index_input-1] 
                                del products_list[index_input-1]   # ------- Delete action ------------ #
                                list_products()
                                print(f"Successfully deleted. Previously ( {index_input} ): {deleted_name}")
                                break
                            else:
                                break

            print(" ") # For nice looking
            user_input = input_option(products_max_opts)
            if user_input == 0:
                main_input = 0
                break
    
    # Orders menu
    elif main_input == 2:

        user_input = 0
        while True:
            if user_input == 0:
                print_menu(orders_menu, 0) # Default menu       
            if user_input == 1:
                print_menu(orders_menu, user_input)
                list_orders()  # ------- Print orders list action ------------ #
                index_input = input("Press Enter to continue: ")
                print_menu(orders_menu, 0) # Reset to default menu after enter to continue
                
            elif user_input == 2:
                print_menu(orders_menu, user_input)
                print(" ") # For nice looking
                while True:
                    cust_name = input("Enter new order customer name: ")
                    cust_address = input("Enter new order customer address: ")
                    cust_phone = input("Enter new order customer phone: ")
                    print_menu(orders_menu, 0) # Reset to default menu after enter new product name.

                    if cust_name == "" or cust_address == "" or cust_phone == "":
                        break
                    else:
                        new_order = {
                            "customer_name": cust_name,
                            "customer_address": cust_address,
                            "customer_phone": cust_phone,
                            "status": order_status[0],
                        }
                        orders_list.append(new_order)  # ------- Add order action ------------ #
                        list_orders()
                        print(f"Added new order ( {len(orders_list)} ): {new_order}")
                        break
                
            elif user_input == 3:
                print_menu(orders_menu, user_input)
                list_orders()
                while True:
                    index_input = input("Enter order (  ) to update: ")
                    if index_input == "":
                        print_menu(orders_menu, 0) # Reset to default menu after enter to escape
                        break
                    elif re.match('^([0-9]+)$', index_input):
                        index_input = int(index_input)
                        if index_input >=1 and index_input <= len(orders_list):
                            print(" ") # For nice looking
                            status_list="Available status: "
                            for x in range(len(order_status)):
                                status_list += f"[{x}] {order_status[x]}, "
                            print(status_list)
                            print(" ") # For nice looking
                            print(f"Order ( {index_input} ) hase status [{order_status.index(orders_list[index_input-1]['status'])}] {orders_list[index_input-1]['status']} :")
                            print(" ") # For nice looking
                            while True:
                                edit_order = input(f"Choose status number [ ]: ")
                                if edit_order == "":
                                    print_menu(orders_menu, 0) # Reset to default menu after edit orders name
                                    break
                                elif re.match('^([0-9]+)$', edit_order):
                                    edit_order = int(edit_order)
                                    if edit_order < len(order_status):
                                        orders_list[index_input-1]['status'] = order_status[edit_order]  # ------- Edit action ------------ #
                                        print_menu(orders_menu, 0) # Reset to default menu after edit orders name
                                        list_orders()
                                        print(f"Successfully updated. Order ( {index_input} ) has status [{order_status.index(orders_list[index_input-1]['status'])}] {orders_list[index_input-1]['status']}")
                                        break
                            break # break the outer while loop
  
            elif user_input == 4:
                print_menu(orders_menu, user_input)
                list_orders()
                while True:
                    index_input = input("Enter order (  ) to update: ")
                    if index_input == "":
                        print_menu(orders_menu, 0) # Reset to default menu after enter to escape
                        break
                    elif re.match('^([0-9]+)$', index_input):
                        index_input = int(index_input)
                        if index_input >=1 and index_input <= len(orders_list):
                            print(" ") # For nice looking
                            max_length = len(max(list(x for x in orders_list[index_input-1]), key=len))
                            for x, y, in orders_list[index_input-1].items():
                                if x != 'status':
                                    print(f'{x: <{max_length}} : {y}')
                                    edit_order = input(f'{x: <{max_length}} : ')
                                    if edit_order == "":
                                        pass
                                    else:
                                        orders_list[index_input-1][x] = edit_order # ------- Edit action ------------ #
                                else:
                                    status_num = order_status.index(orders_list[index_input-1]['status'])
                                    print(f'{x: <{max_length}} : [{status_num}] {y}')
                                    print(" ") # For nice looking
                                    status_list=f'{x: <{max_length}} : '
                                    for x in range(len(order_status)):
                                        status_list += f"[{x}] {order_status[x]}, "
                                    print(status_list)
                                    print(" ") # For nice looking

                                    while True:
                                        edit_order = input(f"Choose status number [ ]: ")
                                        if edit_order == "":
                                            pass
                                        elif re.match('^([0-9]+)$', edit_order):
                                            edit_order = int(edit_order)
                                            if edit_order < len(order_status):
                                                orders_list[index_input-1]['status'] = order_status[edit_order]  # ------- Edit action ------------ #
                                                print_menu(orders_menu, 0) # Reset to default menu after edit orders name
                                                list_orders()
                                                print(f"Updated order ( {index_input} ): {orders_list[index_input-1]}")
                                                break
                            break # break the outer while loop

            elif user_input == 5:
                print_menu(orders_menu, user_input)
                list_orders()
                while True:
                    index_input = input("Enter order (  ) to delete: ")
                    if index_input == "":
                        print_menu(orders_menu, 0) # Reset to default menu after enter to escape
                        break
                    elif re.match('^([0-9]+)$', index_input):
                        index_input = int(index_input)
                        if index_input >=1 and index_input <= len(orders_list):
                            print(" ") # For nice looking
                            del_order = input(f"Delete order ( {index_input} ): {orders_list[index_input-1]} : y/n? ")
                            print_menu(orders_menu, 0) # Reset to default menu after delete order.
                            if del_order == 'y' or del_order.upper() == 'Y':
                                deleted_name = orders_list[index_input-1] 
                                del orders_list[index_input-1]   # ------- Delete action ------------ #
                                list_orders()
                                print(f"Successfully deleted. Previously ( {index_input} ): {deleted_name}")
                                break
                            else:
                                break

            print(" ") # For nice looking
            user_input = input_option(orders_max_opts)
            if user_input == 0:
                main_input = 0
                break


