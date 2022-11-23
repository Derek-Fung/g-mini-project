# mini_project_v4.py
"""Mini-project python programme by Derek Tak Yiu Fung. Please run on CLI in this 'src' directory."""
import sys, os, re, ast, shutil
# from dataclasses import dataclass
# Import the txt.py file from directory file_handlers. Do not mix up there is NO file_handlers.txt there!
from file_handlers.txt import TxtFileHelper 
from file_handlers.csv import CsvFileHelper 
from file_handlers.app import AppFileHelper 
from file_handlers.db import DbFileHelper


    
i: int = 0 # for handy list elements
cat = 'category'
cats = 'categories'
main = 'main'
product = 'product'
products = 'products'
courier = 'courier'
couriers = 'couriers'
order = 'order'
orders = 'orders'
body = 'body'
options = 'options'
bottom = 'bottom'

name = "name"
price = "price"
phone = "phone"
price_phone = 'price_phone'
customer_name = "customer_name"
customer_address ="customer_address"
customer_phone = "customer_phone"
courier = "courier"
status = "status"
items = "items"
couriers_name_list = 'couriers_name_list'
products_name_list = 'products_name_list'
orders_name_list   = 'orders_name_list'

txt = 'txt' 
csv = 'csv'
app = 'app'
db = 'db'
table = 'table'
han = 'han'
sto = 'sto'
hlp = 'hlp'

ln = [
    {cat: main, cats: main},
    {cat: product, cats: products, price_phone: price},
    {cat: courier, cats: couriers, price_phone: phone},
    {cat: order, cats: orders},         
]

v = [                  
    ['', '', '', '', ''],  # system input variables fot all menus i.e., v[i][0] = input_filter("Enter something")
    ['', '', '', '', ''],
    ['', '', '', '', ''],
    ['', '', '', '', ''],     
]

handle = {
    txt: './file_handlers/txt.py',
    csv: './file_handlers/csv.py',
    app: './file_handlers/app.py',                        
    db : './db/db.py',                                    
}

storage = {
    txt: {products: '../data/products.txt', couriers: '../data/couriers.txt', orders: '../data/orders.txt'},
    csv:  {products: '../data/products.csv', couriers: '../data/couriers.csv', orders: '../data/orders.csv'},
    app: {products: '../data/products.app', couriers: '../data/couriers.app', orders: '../data/orders.app'},
    db: {products: {db:'mini_project', table:'products'}, couriers: {db:'mini_project', table:'couriers'}, orders: {db:'mini_project', table:'orders'}},    
}

helper_class = {
    txt: TxtFileHelper, # class name inside imported module
    csv: CsvFileHelper,
    app: AppFileHelper,                        
    db : DbFileHelper,          
}

rw = {han: handle[csv], sto: storage[csv], hlp: helper_class[csv]}  # File handles,storage and helper class setting.

data = {}
data[products] = [           # Default data, will be overrided by stored data existed in file or system
    {"name": "Roast Beef Launch", "price": 3.5 },
    {"name": "Roast Chicken Launch", "price": 3.5 },
    {"name": "Chicken & Mushroom Pie", "price": 3.5 },
    {"name": "Stroganoff with Rice", "price": 3.5 },
    {"name": "Sweet & Sour Chicken", "price": 3.5 },
    {"name": "Fisherman's Fish Pie", "price": 3.5 },
    {"name": "Corned Beef Hash", "price": 3.5 },
    {"name": "Cumberland Meat Pie", "price": 3.5 },
    {"name": "Fruity Chicken Curry", "price": 3.5 },
    {"name": "Spaghetti Bolognese", "price": 3.5 },
    {"name": "Cod, Chips & Peas", "price": 3.5 },
    {"name": "Shepherd's Pie", "price": 3.5 },
    {"name": "Cottage Sweet Pie", "price": 3.5 },
    {"name": "Sausages & Mash", "price": 3.5 },
    ]


data[couriers] = [     # Default data, will be overrided by stored data existed in file or system
    {"name": "John", "phone": "07216462393"},
    {"name": "Mary", "phone": "07898878893"},
    {"name": "Peter", "phone": "07568885295"},
    {"name": "Derek", "phone": "07144455595"},
    {"name": "Eliza", "phone": "07766121409"},
    {"name": "Anthony", "phone": "07554896379"},
    {"name": "Winson", "phone": "07555663397"},
    {"name": "Sophia", "phone": "07112223597"},
    {"name": "Olivia", "phone": "07854122291"},
]

data[orders] = [
    {
        "customer_name": "John",
        "customer_address": "26 Sedgeford Rd, Manchester M40 8QL",
        "customer_phone": "07898873344",
        "items": "1, 2, 3, 4, 5, 6",
        "courier": 0,
        "status": "Delivered",
        
    },
    {
        "customer_name": "Mary",
        "customer_address": "1 Douglas Grn, Salford, Manchester M6 6ES",
        "customer_phone": "07152521727",
        "items": "2, 3, 3, 4, 1, 0",
        "courier": 0,
        "status": "Preparing",
        
    },
    {
        "customer_name": "Sam",
        "customer_address": "71 Blackfriars Rd, Salford, Manchester M3 7GQ",
        "customer_phone": "07411235668",
        "items": "5, 4, 0, 2, 1, 5",
        "courier": 1,
        "status": "Preparing",
    },
    {
        "customer_name": "Martin",
        "customer_address": "23 Rose Garden Road, Manchester M1 8DL",
        "customer_phone": "07712377859",
        "items": "3, 3, 2, 4, 5",
        "courier": 2,
        "status": "Out-for-Delivery",
    },
    {
        "customer_name": "Harry",
        "customer_address": "5 Sandy Road, Manchester M4 4RF",
        "customer_phone": "07456231567",
        "items": "4, 1",
        "courier": 2,
        "status": "Out-for-Delivery",
    },
    {
        "customer_name": "Susan",
        "customer_address": "71 Memory Sweet, Manchester M2 8HG",
        "customer_phone": "07512489653",
        "items": "4, 1",
        "courier": 0,
        "status": "Out-for-Delivery",
    },
    {
        "customer_name": "Isabella",
        "customer_address": "121 Happy Day Road, Manchester M3 9MN",
        "customer_phone": "07451236859",
        "items": "1, 3, 4, 3",
        "courier": 3,
        "status": "Awaiting Pickup",
    },                         
]

data[orders_name_list] =[ (x[1], y[1], z[1] ,s[1] ,t[1], w[1]) for x, y, z, s, t, w  in (dic.items() for dic in data[orders])]

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
'                                                                        ',
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
' [ 1 ]: print products list',
' [ 2 ]: create new product',
' [ 3 ]: update product name',
' [ 4 ]: delete product',
]

menu[products][bottom] = [
'',
]


menu[couriers][body] = [
'  CCCCC    OOOO    U     U  RRRRR   II   EEEEEEE   SSSSS ',
' CC       O    O   U     U  R   RR  II   EE       SS     ',
'CC       O      O  U     U  RRRR    II   EEEEE      SSS  ',
' CC       O    O   U     U  R   R   II   EE            SS',
'  CCCCC    OOOO     UUUUU   R    R  II   EEEEEEE   SSSSS ',
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
    0: '\033[1;45m',   
    1: '\033[1;92m',
    2: '\033[1;92m',
    3: '\033[1;93m',
    4: '\033[1;96m',
    5: '\033[1;91m',
    'E': '\033[m',
}

c2 = { # color code dictionary 2
    0: '\033[1;45m',   
    1: '\033[1;42m',
    2: '\033[1;42m',
    3: '\033[1;43m',
    4: '\033[1;46m',
    5: '\033[1;41m',
    'E': '\033[m',
}


op_list = [     #  Options big-size digit list, each digit conatins 5 list elements.
'    11    ',
'  1111    ',
'    11    ',
'    11    ',
' 11111111 ',
'   2222   ',
' 22    22 ',
'     22   ',
'   22     ',
' 22222222 ',
' 3333333  ',  
'       33 ',  
'   3333   ', 
'       33 ', 
' 3333333  ', 
'      44  ', 
'    4444  ', 
'  44  44  ', 
' 44444444 ',
'      44  ',
' 55555555 ', 
' 55       ', 
' 55555555 ', 
'       55 ',
' 55555555 ',
' 66666666 ', 
' 66       ', 
' 66666666 ', 
' 66    66 ',
' 66666666 ',
' 77777777 ', 
'       77 ', 
'     77   ', 
'    77    ',
'   77     ',
'          ',  # last elements op_list[-1] used for default padding
]

op_elems_no = 5  # Each big-size digit contains 5 list elements.

op_max_display_no = 4 # Maximun number of big-digits dispaly in vertical. 

op_total_ht = op_elems_no  * op_max_display_no # Total height to display vertial digits.




######## Start functoins in alphabetical orders ###################################################################

def clear_screen(): # Function to clear the screen, suitable for winows and linux    
    platform  = sys.platform
    if platform == "win32":
        os.system("clear") # Git bash having "clear" may pretend win32. Howerver it will bypass below "cls" error warning.
        os.system("cls")   # Genuine win32 overrides above "clear" error warning.
    else:
        os.system("clear")
        
def init_file_data(file_name, default_data): # Function initilizes data, use default data if stroage data not exist
    helper = rw[hlp]() # helper object created from Class rw[hlp]
    return helper.get_filecontents(file_name, default_data)

def input_filter(args):
    return re.sub(' +', ' ', input(args).strip())
        
def input_option(menu_name, main_input):    # Function handles user input on menu
    if main_input != 0:
        breadcrumb = f"{main} \u25B6 {menu_name}"
    else:
        breadcrumb = f"{menu_name}"
    while True:
        user_input = input_filter(f"{c2[0]} {breadcrumb} {c2['E']}: Enter option in square brackets [  ]: ")
        if re.match('^([0-9]+)$', user_input):
            user_input = int(user_input)
            if user_input < len(menu[menu_name][options]):
                if menu_name == main and user_input == 0:
                    clear_screen()
                    user_input = -1
                break # break if user_input < len(menu[menu_name][options]):
    return user_input

def joint_opts_list(menu_name, option_value): # Function joints two options in one line on menu.
    joint_list = []
    cc_count = []  #Colour code count
    cc_length = len(c2[option_value]) + len(c2["E"]) # Colour code length
    temp_opts = []
    for item in menu[menu_name][options]: # Assign temp list to prevent polluting the original list.
        temp_opts.append(item)
    if len(temp_opts) % 2 != 0:
        temp_opts.append(' ') # Prevent colour codes shift. Append 1 empty element if len() is an odd number.
    for x in range(0, len(temp_opts), 2):
        str = ''
        i = 0
        for elm in temp_opts[x:x + 2]: # Join 2 elements to 1 elements
            if option_value != 0 and option_value  == temp_opts.index(elm):
                # elm = f'{c2[option_value]}{elm}{c2["E"]}'
                elm = f'{c2[option_value]}' + f'{elm: <{menu_half_width - 1}}' + f'{c2["E"]}'
                item = f'{elm: <{menu_half_width + cc_length}}'
                i += 1
            else:
                item = f'{elm: <{menu_half_width}}'            
            str += item
        cc_count.append(i)
        joint_list.append(str)
    return [joint_list, cc_count]

def list_items(menu_name, option_value, dict_key = None, dict_value = None):  # Function prints products listing
    cc_length = (len(cc[option_value]) + len(cc["E"])) 
    # check order status
    if menu_name == orders and dict_key == status and dict_value != None:
        temp_data = [data[menu_name][key] for key, val in enumerate([dic[dict_key] for dic in data[menu_name]]) if val == dict_value]
        temp_data[::] = [ (x[1], y[1], z[1] ,s[1] ,t[1], w[1]) for x, y, z, s, t, w  in (dic.items() for dic in temp_data)]
        search_terms = f' {c2[option_value]}{dict_value}{c2["E"]}'
        cc_length_factor = 1
    # check order courier
    elif menu_name == orders and dict_key == courier and dict_value != None:            
        temp_data = [data[menu_name][key] for key, val in enumerate([dic[dict_key] for dic in data[menu_name]]) if val == dict_value-1]
        temp_data[::] = [ (x[1], y[1], z[1] ,s[1] ,t[1], w[1]) for x, y, z, s, t, w  in (dic.items() for dic in temp_data)]
        search_terms = f' {c2[option_value]}{data[couriers][dict_value-1][name]}{c2["E"]}'
        cc_length_factor = 1        
    else:
        temp_data = data[menu_name]
        search_terms = ''
        cc_length_factor = 0
    
    if len(temp_data) > 0:
        screen_size = shutil.get_terminal_size()
        temp=[]
        for item in temp_data:
            temp.append(str(item))  # Convert the list elements to string for display purpose.
        elm_max_length = len(max(temp, key=len)) + len(str(len(temp))) + len('(  ): ')
        # elm_max_length = the max text element length in list + text length of number of elemets in list (e.g. 23 is length 2, 645 is length 3) + text length of '(  ): '        
        chunk_no =  screen_size.columns / elm_max_length
        display_chunk_size = 1 if chunk_no < 1 or len(temp) < 2 else int(chunk_no)
        # pedding_length = 0 if display_chunk_size == 1 else elm_max_length + cc_length
        pedding_length = elm_max_length + len(search_terms) + cc_length

        p(" ") # For nice looking
        item_number = 0
        # if display_chunk_size > 1:
        residual = len(temp) % display_chunk_size
        if residual != 0:
            loop_times = display_chunk_size - residual
            for i in range(loop_times):
                temp.append("")
        else:
            loop_times = 0
            
        for i in range(0, len(temp), display_chunk_size):        
            items_string = ''
            for item_name in temp[i:i + display_chunk_size]:
                item_number += 1
                colour_number = f"{cc[option_value]}{item_number}{cc['E']}"
                colour_string = f"( {colour_number} ){search_terms}: {item_name}"
                if item_number > len(temp) - loop_times:
                    items_string += f"{item_name: <{pedding_length}}"
                else:
                    items_string += f"{colour_string: <{pedding_length}}"
            p(f'{items_string: ^{screen_size.columns + display_chunk_size * cc_length + cc_length_factor * cc_length}}')   
        # else:
        #     for x in range(len(temp)):
        #         item_number += 1
        #         colour_number = f"{cc[option_value]}{item_number}{cc['E']}"
        #         temp[x] = f"( {colour_number} ){search_terms}: {temp[x]}"                    
        #         temp[x] = f'{temp[x]: <{pedding_length}}'
        #     for x in range(len(temp)):
        #         p(f'{temp[x]: ^{screen_size.columns}}')
        p(" ") # For nice looking


def p(*args, **kwargs): # Alisa to print function
    print(*args, **kwargs)

def print_menu(menu_name, option_value): # Function prints menu
    clear_screen()
    # p(f'option_value: {option_value}') # For debug use
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
    # p(f'op_start_pos: {op_start_pos}') # For debug use
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
        p(f'{menu_list[x]: ^{screen_size.columns + spacer}}')

def update_storage(name): # Function upates data storage 
    if name in rw[sto] and name in data:
        helper = rw[hlp]() # helper object created from Class rw[hlp]
        helper.write_filecontents(rw[sto][name], data[name])
        if name == orders:
            data[orders_name_list] =[ (x[1], y[1], z[1] ,s[1] ,t[1], w[1]) for x, y, z, s, t, w  in (dic.items() for dic in data[orders])]
            
        
######## End functoins in alphabetical orders #########################################################################

if __name__ == "__main__":
            
    ###### Start Initialize data, use default data if storage data not exist. ##########
    data = {key:init_file_data(rw[sto][key], data[key]) for key in rw[sto]}

    for data_key_name in data.keys():
        for x in range(len(data[data_key_name])):
            if type(data[data_key_name][x]) is str: # dictonary read from file is str, need to convert back to dict
                data[data_key_name][x] = ast.literal_eval(data[data_key_name][x]) # change str back to dict

    # Convert data back to porper type after data retrieved from files #####################
    for i, dic in enumerate(data[orders]):
        for x, y in dic.items():
            if x == courier:
                data[orders][i][courier] = int(data[orders][i][courier])
                               
    for i, dic in enumerate(data[products]):
        for x, y in dic.items():
            if x == price:
                data[products][i][price] = float(data[products][i][price])
    
    data[orders_name_list] =[ (x[1], y[1], z[1] ,s[1] ,t[1], w[1]) for x, y, z, s, t, w  in (dic.items() for dic in data[orders])]            
    ####### End Initialize data ###########################################################                           
                
    main_input = 0

    while True:

        if main_input == 0:
            print_menu(main, main_input)
            p(" ") # For nice looking
            main_input = input_option(main, main_input) # return -1 if user press 0 option in main menu
            if main_input == -1: 
                clear_screen()
                break # Break to exit the while loop i.e. end the programme
        #######################################################
        # Products menu and Couriers menu
        if main_input == 1 or main_input == 2:

            user_input = 0
            while True:
                i = main_input
                if user_input == 0:
                    print_menu(ln[i][cats], 0) # Default menu       
                if user_input == 1:
                    print_menu(ln[i][cats], user_input)
                    list_items(ln[i][cats], user_input)  # ------- Print products list action ------------ #
                    # index_input = input_filter(f"{cc[user_input]}Press Enter to continue:{cc['E']} ")
                    # print_menu(ln[i][cats], 0) # Reset to default menu after enter to continue
                    
                elif user_input == 2:
                    print_menu(ln[i][cats], user_input)
                    list_items(ln[i][cats], user_input) 

                    while True:
                        
                        while True:
                            v[i][0] = input_filter(f"Enter new {ln[i][cat]} name: ")
                            if v[i][0] == "":
                                break 
                            
                  
                            elif True in set(v[i][0].lower() in dic[name].lower() for dic in data[ln[i][cats]]):
                                p(f"{v[i][0]} already exist, please try again.")
                            else:
                                break
                        
                        while True:
                            v[i][1] = input_filter(f"Enter {ln[i][cat]} {ln[i][price_phone]}  : ")
                            if  v[i][1] == "":
                                break
                            if main_input == 1:
                                if re.match('^([0-9]*)(\\.){0,1}([0-9]*)$', v[i][1]): # match 0 or 1 dot in digit string. 
                                    v[i][1] = round(float(v[i][1]), 2)
                                    break
                                else:
                                    p(f"Please enter valid number. ")
                            elif main_input == 2:
                                if re.match('^([0-9]+)$', v[i][1]):
                                    break
                                else:
                                    p(f"Please enter valid phone number. ")              
                            else:
                                p(f"Error, main_input value error = {main_input} at user_input == 1 or 2. Please enter to exit: ")
                                exit_programme = input_filter(f"Press enter to exit programme: ")
                                quit() 
                                
                        
                        if v[i][0] == "" or v[i][1] == "":
                            print_menu(ln[i][cats], 0) # Reset to default menu after enter new product name.
                            break
                        else:
                            new_product = {
                                name: v[i][0],     
                                ln[i][price_phone]:v[i][1],  
                            }
                            data[ln[i][cats]].append(new_product)  # ------- Add product action ------------ #
                            update_storage(ln[i][cats])
                            print_menu(ln[i][cats], 0) # Reset to default menu after enter new product name.
                            list_items(ln[i][cats], user_input)
                            p(f"( {cc[user_input]}{len(data[ln[i][cats]])}{cc['E']} ): {v[i][0]} : added to {ln[i][cats]} list")
                            break
                    
                elif user_input == 3:
                    print_menu(ln[i][cats], user_input)
                    list_items(ln[i][cats], user_input)
                    while True:
                        index_input = input_filter(f"Enter {ln[i][cat]} (  ) to update: ")
                        if index_input == "":
                            print_menu(ln[i][cats], 0) # Reset to default menu after enter to escape
                            break
                        elif re.match('^([0-9]+)$', index_input):
                            index_input = int(index_input)
                            if index_input >=1 and index_input <= len(data[ln[i][cats]]):
                                p(" ") # For nice looking
                                p(f"Edit product ( {cc[user_input]}{index_input}{cc['E']} ) ")
                                elm_max_length = len(max(list(x for x in data[ln[i][cats]][index_input-1]), key=len))
                                for key, value, in data[ln[i][cats]][index_input-1].items():
                                    
                                    print(f'{key: <{elm_max_length}} : {value}')
                                    
                                    if key == name:
                                        while True:
                                            v[i][0] = input_filter(f'{key: <{elm_max_length}} : ')
                                            if v[i][0] == "":
                                                break 
                                            elif True in set(v[i][0].lower() in dic[name].lower() for dic in data[ln[i][cats]]):
                                                p(f"{v[i][0]} already exist, please try again.")
                                            else:
                                                data[ln[i][cats]][index_input-1][key] = v[i][0] # ------- Edit action ------------ #
                                                update_storage(ln[i][cats])
                                                break                                    
                                    else:
                                        while True:
                                            v[i][1] = input_filter(f'{key: <{elm_max_length}} : ')
                                            if  v[i][1] == "":
                                                break
                                            if main_input == 1:
                                                if re.match('^([0-9]*)(\\.){0,1}([0-9]*)$', v[i][1]): # match 0 or 1 dot in digit string. 
                                                    v[i][1] = round(float(v[i][1]), 2)
                                                    data[ln[i][cats]][index_input-1][key] = v[i][1] # ------- Edit action ------------ #
                                                    update_storage(ln[i][cats])
                                                    break
                                                else:
                                                    p(f"Please enter valid number. ")
                                            elif main_input == 2:
                                                if re.match('^([0-9]+)$', v[i][1]):
                                                    data[ln[i][cats]][index_input-1][key] = v[i][1] # ------- Edit action ------------ #
                                                    update_storage(ln[i][cats])                                                    
                                                    break
                                                else:
                                                    p(f"Please enter valid phone number. ")              
                                            else:
                                                p(f"Error, main_input value error = {main_input} at user_input == 3. Please enter to exit: ")
                                                exit_programme = input_filter(f"Press enter to exit programme: ")
                                                quit()                                             
   
                                                    
                                print_menu(ln[i][cats], 0) # Reset to default menu after edit product name
                                list_items(ln[i][cats], user_input)
                                p(f"Successfully updated {ln[i][cat]} ( {cc[user_input]}{index_input}{cc['E']} ): {data[ln[i][cats]][index_input-1]}")                               
                                break    
        
                elif user_input == 4:
                    print_menu(ln[i][cats], user_input)
                    list_items(ln[i][cats], user_input)
                    while True:
                        index_input = input_filter(f"Enter {ln[i][cat]} (  ) to delete: ")
                        if index_input == "":
                            print_menu(ln[i][cats], 0) # Reset to default menu after enter to escape
                            break
                        elif re.match('^([0-9]+)$', index_input):
                            index_input = int(index_input)
                            if index_input >=1 and index_input <= len(data[ln[i][cats]]):
                                p(" ") # For nice looking
                                v[i][0] = input_filter(f"Delete {ln[i][cat]} ( {cc[user_input]}{index_input}{cc['E']} ): {data[ln[i][cats]][index_input-1]} \nConfirm delete: y/n? ")
                                print_menu(ln[i][cats], 0) # Reset to default menu after delete product.
                                if v[i][0] == 'y' or v[i][0].upper() == 'Y':
                                    deleted_name = data[ln[i][cats]][index_input-1] 
                                    del data[ln[i][cats]][index_input-1]   # ------- Delete action ------------ #
                                    update_storage(ln[i][cats])
                                    list_items(ln[i][cats], user_input)
                                    p(f"Successfully deleted. Previously ( {cc[user_input]}{index_input}{cc['E']} ): {deleted_name}")
                                    break
                                else:
                                    break

                p(" ") # For nice looking
                user_input = input_option(ln[i][cats], main_input)
                if user_input == 0:
                    main_input = 0
                    break
        
        # Orders menu #######################################################
        elif main_input == 3:

            user_input = 0
            while True:
                if user_input == 0:
                    print_menu(orders, 0) # Default menu       
                if user_input == 1:
                    print_menu(orders, user_input)
                    list_items(orders_name_list, user_input)  # ------- Print orders list action ------------ #
                    # index_input = input_filter(f"{cc[user_input]}Press Enter to continue:{cc['E']} ")
                    # print_menu(orders, 0) # Reset to default menu after enter to continue
                    
                    while True:
                        status_list=''
                        for x in range(len(order_status)):
                            status_list += f"[{cc[user_input]}{x}{cc['E']}] {order_status[x]}, "
                        p(status_list.rstrip(', '))
                        p(" ") # For nice looking
                        
                        status_input = input_filter(f"Choose status number [ ]: ")
                        if status_input == "":
                            
                            break
                        elif re.match('^([0-9]+)$', status_input):
                            status_input = int(status_input)
                            if status_input < len(order_status):
                                print_menu(orders, user_input)
                                list_items(orders, user_input, dict_key = status, dict_value = order_status[status_input])

                    while True:
                        couriers_list=''
                        data[couriers_name_list] = [ x[1] for x, y in (dic.items() for dic in data[couriers])]
                        list_items(couriers_name_list, user_input)
                        get_input = input_filter(f"Choose courier number [ ]: ")                        
                        if get_input == "":
                            
                            break
                        elif re.match('^([0-9]+)$', get_input):
                            get_input = int(get_input)
                            if get_input >= 1 and get_input <= len(data[couriers]):
                                print_menu(orders, user_input)
                                list_items(orders, user_input, dict_key = courier, dict_value = get_input)
                                
                    print_menu(orders, 0)
                    
                elif user_input == 2:
                    print_menu(orders, user_input)
                    p(" ") # For nice looking
                    while True:
                        cust_name = input_filter("Enter new order customer name: ")
                        cust_address = input_filter("Enter new order customer address: ")
                        while True:
                            cust_phone = input_filter("Enter new order customer phone: ")                    
                            if re.match('^([0-9]+)$', cust_phone) or cust_phone == '':
                                break
                            else:
                                p(f'Please enter vaild phone umber.')                    
                        if cust_name == "" or cust_address == "" or cust_phone == "":
                            print_menu(orders, 0) # Reset to default menu after no input.
                            break
                        else:
                            
                            data[products_name_list] = [ x[1] for x, y in (dic.items() for dic in data[products])]
                            p("Products items choices: ")
                            list_items(products_name_list, user_input)
                            items_list = '' # Showing items choosen in format 1,2,3,4
                            index_list = '' # items list string
                            while True:
                                
                                input_order = input_filter(f"( {cc[user_input]}{items_list[:-2]}{cc['E']} ): Choose number / e Esacpe /{c2[user_input]} f{cc['E']} Finish: ")
                                if input_order == "e":
                                    print_menu(orders, 0) # Reset to default menu after escape
                                    break
                                elif input_order == "f":
                                    break
                                elif re.match('^([0-9]+)$', input_order):
                                    input_order = int(input_order)
                                    if input_order >=1 and input_order <= len(data[products]):
                                        items_list += f'{input_order}, '
                                        index_list += f'{input_order-1}, '
                                            
                            if input_order != 'e':
                                data[couriers_name_list] = [ x[1] for x, y in (dic.items() for dic in data[couriers])]
                                p("Courier choices: ")
                                list_items(couriers_name_list, user_input)
                                while True:
                                    input_order = input_filter(f"Choose courier number (   ): Enter e to esacpe: ")
                                    if input_order == "e":
                                        print_menu(orders, 0) # Reset to default menu after escape
                                        break
                                    elif re.match('^([0-9]+)$', input_order):
                                        input_order = int(input_order)
                                        if input_order >=1 and input_order <= len(data[couriers]):                                   
                                            new_order = {
                                                customer_name: cust_name,
                                                customer_address: cust_address,
                                                customer_phone: cust_phone,
                                                items: index_list[:-2],
                                                courier: input_order - 1,
                                                status: order_status[0],
                                            }
                                            data[orders].append(new_order)  # ------- Add order action ------------ #
                                            update_storage(orders)
                                            print_menu(orders, 0) # Reset to default menu after adding order
                                            list_items(orders_name_list, user_input)
                                            p(f"Added new order ( {cc[user_input]}{len(data[orders])}{cc['E']} ): {new_order}")
                                            break                                    
                        break # break the outer while loop                
                    
                elif user_input == 3:
                    print_menu(orders, user_input)
                    list_items(orders_name_list, user_input)
                    while True:
                        index_input = input_filter("Enter order (  ) to update: ")
                        if index_input == "":
                            print_menu(orders, 0) # Reset to default menu after enter to escape
                            break
                        elif re.match('^([0-9]+)$', index_input):
                            index_input = int(index_input)
                            if index_input >=1 and index_input <= len(data[orders]):
                                p(" ") # For nice looking
                                status_name = data[orders][index_input-1][status]                      
                                p(f"Order ( {cc[user_input]}{index_input}{cc['E']} ) status: [{order_status.index(status_name)}] {status_name}")
                                p(" ") # For nice looking
                                status_list="Status choices: "
                                for x in range(len(order_status)):
                                    status_list += f"[{cc[user_input]}{x}{cc['E']}] {order_status[x]}, "
                                p(status_list.rstrip(', '))
                                p(" ") # For nice looking

                                while True:
                                    edit_order = input_filter(f"Choose status number [ ]: ")
                                    if edit_order == "":
                                        print_menu(orders, 0) # Reset to default menu after edit orders name
                                        break
                                    elif re.match('^([0-9]+)$', edit_order):
                                        edit_order = int(edit_order)
                                        if edit_order < len(order_status):
                                            data[orders][index_input-1][status] = order_status[edit_order]  # ------- Edit action ------------ #
                                            update_storage(orders)
                                            print_menu(orders, 0) # Reset to default menu after edit orders name
                                            list_items(orders_name_list, user_input)
                                            p(f"Successfully updated. Order ( {cc[user_input]}{index_input}{cc['E']} ) status: {data[orders][index_input-1][status]}")
                                            break
                                break # break the outer while loop
    
                elif user_input == 4:
                    print_menu(orders, user_input)
                    list_items(orders_name_list, user_input)
                    while True:
                        index_input = input_filter("Enter order (  ) to update: ")
                        if index_input == "":
                            print_menu(orders, 0) # Reset to default menu after enter to escape
                            break
                        elif re.match('^([0-9]+)$', index_input):
                            index_input = int(index_input)
                            if index_input >=1 and index_input <= len(data[orders]):
                                p(" ") # For nice looking
                                p(f"Edit order ( {cc[user_input]}{index_input}{cc['E']} ) ")
                                elm_max_length = len(max(list(x for x in data[orders][index_input-1]), key=len))
                                for x, y, in data[orders][index_input-1].items():
                                    if x != status and x != courier and x != items:
                                        p(f'{x: <{elm_max_length}} : {y}')
                                        if x == phone:
                                            while True:
                                                edit_order = input_filter(f'{x: <{elm_max_length}} : ')
                                                if re.match('^([0-9]+)$', edit_order) or edit_order == '':
                                                        break
                                                else:
                                                    p(f'Please enter vaild phone umber.') 
                                        else:
                                            edit_order = input_filter(f'{x: <{elm_max_length}} : ')
                                            
                                        if edit_order != "":
                                            data[orders][index_input-1][x] = edit_order # ------- Edit action ------------ #
                                            update_storage(orders)
    
                                    elif x == items:
                                        p(" ")
                                        string = ''
                                        for elm in y.split(', '):
                                            string += f'{int(elm) + 1}, '
                                        # y = f"( {', '.join([f'{(elm + 1)}' for elm in y])} )" if type(y) is list else y
                                        p(f'{x: <{elm_max_length}} : {string[:-2]}')
                                        data[products_name_list] = [ x[1] for x, y in (dic.items() for dic in data[products])]
                                        list_items(products_name_list, user_input)
                                        items_list = '' # Showing items choosen in format 1 2 3 4
                                        index_list = '' # items list string
                                        escape_outer = False
                                        while True:
                                            
                                            input_order = input_filter(f"( {cc[user_input]}{items_list[:-2]}{cc['E']} ): Choose number / e Esacpe /{c2[user_input]} f{cc['E']} Finish: ")
                                            if input_order == "e":
                                                escape_outer = True
                                                break
                                            elif input_order == "f":
                                                if len(index_list) > 0:
                                                    data[orders][index_input-1][items] = index_list[:-2]  # ------- Edit action ------------ #
                                                    update_storage(orders)
                                                break
                                            
                                            elif re.match('^([0-9]+)$', input_order):
                                                input_order = int(input_order)
                                                if input_order >=1 and input_order <= len(data[products]):
                                                    items_list += f'{input_order}, '
                                                    index_list += f'{input_order-1}, '
                                        
                                        if escape_outer == True:
                                            break # break the outer while loop           
                                        
                                    elif x == courier:
                                        p(" ")
                                        # if type(y) is dict:
                                        #     lst = [key for key, val in enumerate([y[name] for  y in data[couriers]]) if val == y[name]]
                                        #     # Finding all occurring key in list of dict elements which have y['name'] key value pair. We just take the first occurance key i.e. lst[0] in [2, 4] is 2, as 2 is the first occurring key of the list with dict elements match the key value pair y['name'] e.g value pair 'name': 'Peter' in order is at index position 2 in couriers list. Using index method .index() will rise error if the element is not exist in the list. Such as ["foo", "bar", "baz"].index("barxx") will rise error.
                                        #     string = f'( {lst[0]+1} ): {y[name]}' if len(lst) > 0 else y # Display position needs +1
                                        # else:
                                        
                                        string1 = y + 1 if type(y) is int else ''
                                        string2 = f'{data[couriers][y][name]}' if type(y) is int else ''
                                        p(f'{x: <{elm_max_length}} : ( {string1} ): {string2}')
                                        data[couriers_name_list] = [ x[1] for x, y in (dic.items() for dic in data[couriers])]
                                        list_items(couriers_name_list, user_input)
 
                                        while True:
                                            edit_order = input_filter(f"Choose courier number (   ): ")
                                            if edit_order == "":
                                                break
                                            elif re.match('^([0-9]+)$', edit_order):
                                                edit_order = int(edit_order)
                                                if edit_order >=1 and edit_order <= len(data[couriers]):  
                                                    data[orders][index_input-1][courier] = edit_order - 1 # ------- Edit action ------------ #
                                                    update_storage(orders)
                                                    break
                                    
                                    elif x == status:
                                        p(" ") # For nice looking
                                        p(f'{x: <{elm_max_length}} : [{order_status.index(y)}] {y}')
                                        status_list=f'{x: <{elm_max_length}} : '
                                        for x in range(len(order_status)):
                                            status_list += f"[{cc[user_input]}{x}{cc['E']}] {order_status[x]}, "
                                        p(status_list.rstrip(', '))
                                        p(" ") # For nice looking

                                        while True:
                                            edit_order = input_filter(f"Choose status number [ ]: ")
                                            if edit_order == "":
                                                break
                                            elif re.match('^([0-9]+)$', edit_order):
                                                edit_order = int(edit_order)
                                                if edit_order < len(order_status):
                                                    data[orders][index_input-1][status] = order_status[edit_order]  # ------- Edit action ------------ #
                                                    update_storage(orders)
                                                    break

                                print_menu(orders, 0) # Reset to default menu after edit orders name
                                list_items(orders_name_list, user_input)
                                p(f"Updated order ( {cc[user_input]}{index_input}{cc['E']} ): {data[orders][index_input-1]}")                            
                                break # break the outer while loop

                elif user_input == 5:
                    print_menu(orders, user_input)
                    list_items(orders_name_list, user_input)
                    while True:
                        index_input = input_filter("Enter order (  ) to delete: ")
                        if index_input == "":
                            print_menu(orders, 0) # Reset to default menu after enter to escape
                            break
                        elif re.match('^([0-9]+)$', index_input):
                            index_input = int(index_input)
                            if index_input >=1 and index_input <= len(data[orders]):
                                p(" ") # For nice looking
                                del_order = input_filter(f"Delete order ( {cc[user_input]}{index_input}{cc['E']} ): {data[orders][index_input-1]} \nConfirm delete: y/n? ")
                                print_menu(orders, 0) # Reset to default menu after delete order or escape.
                                if del_order == 'y' or del_order.upper() == 'Y':
                                    deleted_name = data[orders][index_input-1] 
                                    del data[orders][index_input-1]   # ------- Delete action ------------ #
                                    update_storage(orders)
                                    list_items(orders_name_list, user_input)
                                    p(f"Successfully deleted. Previously ( {cc[user_input]}{index_input}{cc['E']} ): {deleted_name}")
                                    break
                                else:
                                    break

                p(" ") # For nice looking
                user_input = input_option(orders, main_input)
                if user_input == 0:
                    main_input = 0
                    break
        
        else:
            main_input = 0




