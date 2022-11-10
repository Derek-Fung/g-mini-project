
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



border_chr = ['~~~', '111', '222', '333', '444', '###'] 
# Border characters to ouline the border of menu. Default is single character. But you can increase the border width by increasing the number of characters at the list elements. The last element at [-1] is the default border character in main menu. Sorry I am lazy ^_^.

padding_chr=['~', '1', '2', '3', '4', '#'] # Padding character must be single character in f-string. The last element at [-1] is the default padding character in main menu (Sorry I am lazy again ^_^). Other elements are padding characters of products menu options.


main_menu = [ 
'                                                                        ',
'                     MM   MM     AA     II   NN   N                     ',
'   **********        M M M M    AAAA    II   N NN N        **********   ',
'                     M  M  M   AA  AA   II   N   NN                     ',
'                                                                        ',
'   PPPPPP        OOOOO       PPPPPP         UU        UU    PPPPPP      ',
'   PPPPPPPP    OOO   OOO     PPPPPPPP       UU        UU    PPPPPPPP    ',
'   PP    PPP  OO       OO    PP    PPP      UU        UU    PP    PPP   ',
'   PP  PPPP   OO       OO    PP  PPPP       UU        UU    PP  PPPP    ',
'   PPPPPP     OO       OO    PPPPPP         UU        UU    PPPPPP      ',
'   PPP        OO       OO    PPP            UU        UU    PPP         ',
'   PPP         OOO   OOO     PPP             UUU    UUU     PPP         ',
'   PPP           OOOOO       PPP               UUUUUU       PPP         ',
'                                                                        ',
'                       Pop-Up Café Main Menu                            ',
'                         (main menu option)                             ',
'                                                                        ',
'   [ 0 ]: exit programme            [ 1 ]: product menu option          ',
'                                                                        ',
]

# <---- Both sides at last have one # character to make the border -----> #

# So default menu width is equal to: menu_width = len(main_menu[0]) + 2 
menu_width = len(main_menu[0]) + 2 

product_menu = [
'                                                                        ',
'                      Pop-Up Café Product Menu                          ',
'                        (product menu option)                           ',
'                                                                        ',
'                                                                        ',
'   PPPPPP        OOOOO       PPPPPP         UU        UU    PPPPPP      ',
'   PPPPPPPP    OOO   OOO     PPPPPPPP       UU        UU    PPPPPPPP    ',
'   PP    PPP  OO       OO    PP    PPP      UU        UU    PP    PPP   ',
'   PP  PPPP   OO       OO    PP  PPPP       UU        UU    PP  PPPP    ',
'   PPPPPP     OO       OO    PPPPPP         UU        UU    PPPPPP      ',
'   PPP        OO       OO    PPP            UU        UU    PPP         ',
'   PPP         OOO   OOO     PPP             UUU    UUU     PPP         ',
'   PPP           OOOOO       PPP               UUUUUU       PPP         ',
'                                                                        ',
'                                                                        ',
'   [ 0 ]: return to main menu        [ 1 ]: print product list          ',
'   [ 2 ]: create new product         [ 3 ]: update product name         ',
'   [ 4 ]: delete product                                                ',
'                                                                        ',
]


pd_op = [     #  Products option big-size digit list, each digit conatins 5 list elements.
'     11   ',
'   1111   ',
'     11   ',
'     11   ',
'  11111111',
'    2222  ',
'  22    22',
'      22  ',
'    22    ',
'  22222222',
'  3333333 ',  
'        33',  
'    3333  ', 
'        33', 
'  3333333 ', 
'       44 ', 
'     4444 ', 
'   44  44 ', 
'  44444444',
'       44 ',
]

pdo_chunk_size = 5  # Each big-size digit contains 5 list elements.


pdt_list_chunk_size = 4  # Products list chunk size. The number of list elements to display each line on the screen.

# Please Do Not Modify Below: ################################################

# Start Functions Section ####################################################

def print_main_menu(): # Function prints main menu
    os.system("cls")
    print(f'{border_chr[-1]:{padding_chr[-1]}<{menu_width +len(border_chr[-1])-2}}{border_chr[-1]}')
    for x in range(len(main_menu)):
        print(border_chr[-1] + main_menu[x] + border_chr[-1])
    print(f'{border_chr[-1]:{padding_chr[-1]}<{menu_width +len(border_chr[-1])-2}}{border_chr[-1]}')
    print('') # For nice looking

def print_products_menu(option_value): # Function prints products menu
    os.system("cls")
    menu_arr = []
    menu_arr.append(f'{border_chr[option_value]:{padding_chr[option_value]}<{menu_width +len(border_chr[option_value])-2}}{border_chr[option_value]}')
    for x in range(len(product_menu)):
        menu_arr.append(border_chr[option_value] + product_menu[x] + border_chr[option_value])
    menu_arr.append(f'{border_chr[option_value]:{padding_chr[option_value]}<{menu_width +len(border_chr[option_value])-2}}{border_chr[option_value]}')
    letter_printing_position = (option_value - 1) * pdo_chunk_size
    for x in range(len(menu_arr)):
        if x in range(letter_printing_position, letter_printing_position + pdo_chunk_size):
            print(menu_arr[x] + pd_op[x])
        else:
            print(menu_arr[x])

def input_main_options():    # Function handles user input on main menu
    while True:
        main_input = input("[  ]: Enter menu option in square brackets: ")
        if main_input == '0':
            os.system("cls")
            quit()
        elif main_input == '1':
            break

def input_product_option(): # Function handles user input on products menu
    while True:
        user_input = input("[  ]: Enter products option in square brackets: ")
        if re.match('^([0-9]+)$', user_input):
            user_input = int(user_input)
            if user_input <= 4: #Products menu has 0 to 4 options
                break
    return user_input

def list_products():  # Function prints products listing
    if len(products_list) > 0:
        item_number = 0
        print(" ") # For nice looking
        for i in range(0, len(products_list), pdt_list_chunk_size):        
            items_string = ''
            for item_name in products_list[i:i + pdt_list_chunk_size]:
                item_number += 1
                items_string += f"( {item_number} ): {item_name} \t"
            print(items_string)
        print(" ") # For nice looking

# End Functions Section ######################################################



user_input=0

while True:

    if user_input == 0:
        print_main_menu()
        input_main_options()
        print_products_menu(user_input)
        
    elif user_input == 1:
        print_products_menu(user_input)
        list_products()  # ------- Print products list action ------------ #
        index_input = input("Press Enter to continue: ")
        print_products_menu(0) # Reset to default menu after enter to continue
        
    elif user_input == 2:
        print_products_menu(user_input)
        print(" ") # For nice looking
        while True:
            new_product = input("Enter new product name: ")
            print_products_menu(0) # Reset to default menu after enter new product name.
            if new_product == "":
                break
            elif new_product:
                products_list.append(new_product)  # ------- Add product action ------------ #
                list_products()
                print(f"( {len(products_list)} ): {new_product} : added to products list")
                break
        
    elif user_input == 3:
        print_products_menu(user_input)
        list_products()
        while True:
            index_input = input("(   ): Enter number in parenthesis to update: ")
            if index_input == "":
                print_products_menu(0) # Reset to default menu after enter to escape
                break
            elif re.match('^([0-9]+)$', index_input):
                index_input = int(index_input)
                if index_input >=1 and index_input <= len(products_list):
                    print(" ") # For nice looking
                    edit_product = input(f"Edit product name ( {index_input} ): {products_list[index_input-1]} : ")
                    print_products_menu(0) # Reset to default menu after edit product name
                    if edit_product == "":
                        break
                    elif edit_product:
                        products_list[index_input-1]=edit_product  # ------- Edit action ------------ #
                        list_products()
                        print(f"Successfully updated ( {index_input} ): {products_list[index_input-1]}")
                        break        
    elif user_input == 4:
        print_products_menu(user_input)
        list_products()
        while True:
            index_input = input("(   ): Enter number in parenthesis to delete: ")
            if index_input == "":
                print_products_menu(0) # Reset to default menu after enter to escape
                break
            elif re.match('^([0-9]+)$', index_input):
                index_input = int(index_input)
                if index_input >=1 and index_input <= len(products_list):
                    print(" ") # For nice looking
                    del_product = input(f"Delete product ( {index_input} ): {products_list[index_input-1]} : y/n? ")
                    print_products_menu(0) # Reset to default menu after delete product.
                    if del_product == 'y' or del_product.upper() == 'Y':
                        deleted_name = products_list[index_input-1] 
                        del products_list[index_input-1]   # ------- Delete action ------------ #
                        list_products()
                        print(f"Successfully deleted. Previously ( {index_input} ): {deleted_name}")
                        break
                    else:
                        break
    

    print(" ") # For nice looking
    user_input = input_product_option()



