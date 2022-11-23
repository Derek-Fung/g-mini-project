# test_mini_project_v4.py
import pytest, sys, os, builtins
from pytest import MonkeyPatch

from src.file_handlers.txt import *
from src.file_handlers.csv import *
from src.file_handlers.app import *
from src.file_handlers.db import *
from src.mini_project_v4 import *


#### Start programme data used in pytest ###########################################

i: int = 0 # for handy list elements of this class iterates outside this class
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

#### End programme data used in pytest ###########################################

#### Start test ############################

def test_get_filecontents():
    assert CsvFileHelper.get_filecontents(CsvFileHelper, '../data/pytest_products.csv', data[products]) == data[products]

def test_write_filecontents():
    assert CsvFileHelper.write_filecontents(CsvFileHelper, '../data/pytest_products.csv', data[products]) == data[products]    

def test_clear_screen(monkeypatch):
    monkeypatch.setattr('mini_project_v4.clear_screen', lambda: None) 
    assert  clear_screen() == None

def test_init_file_data():
    assert init_file_data('../data/pytest_products.csv', data[products]) == data[products]


def test_input_filter(mocker):
    mocker.patch.object(builtins, 'input', lambda _: '   Derek     Tak      Yiu      ')
    assert  input_filter('Enter anything') == 'Derek Tak Yiu'
    mocker.patch.object(builtins, 'input', lambda _: 'Somebody Name')
    assert  input_filter('Enter anything') != 'Derek Tak Yiu'
    

def test_input_option(mocker):
    # Do not try the main menu 0 option, it will force the programme quit!
    # mocker.patch.object(builtins, 'input', lambda _: '0') 
    # assert input_option(main, 0) == 0
    mocker.patch.object(builtins, 'input', lambda _: '1')
    assert input_option(main, 0) == 1
    mocker.patch.object(builtins, 'input', lambda _: '2')
    assert input_option(main, 0) == 2
    mocker.patch.object(builtins, 'input', lambda _: '3')
    assert input_option(main, 0) == 3
    for x in range(len(menu[products][options])):
        mocker.patch.object(builtins, 'input', lambda _: str(x))    
        assert input_option(products, 1) == x
    for x in range(len(menu[couriers][options])):
        mocker.patch.object(builtins, 'input', lambda _: str(x))    
        assert input_option(couriers, 2) == x 
    for x in range(len(menu[orders][options])):
        mocker.patch.object(builtins, 'input', lambda _: str(x))    
        assert input_option(orders, 3) == x 

def test_joint_opts_list():
    assert joint_opts_list(products, 1) != joint_opts_list(orders, 1)
    

def test_list_items():
    assert list_items(products, 1) == None
    assert list_items(couriers, 1) == None
    assert list_items(orders, 1) == None

def test_p():
    assert p("print anything") == print("print anything")

def test_print_menu():
    assert print_menu(products, 1) == None
    assert print_menu(couriers, 1) == None
    assert print_menu(orders, 1) == None

def test_update_storage():
    assert update_storage(orders) == None


#### End test ############################
