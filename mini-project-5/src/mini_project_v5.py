# mini_project_v5.py
"""Mini-project python programme by Derek Tak Yiu Fung. Please run on CLI in this 'src' directory."""

from datetime import datetime
import pymysql, sys, os, random, string, ast, re, time, shutil
# from dataclasses import dataclass
# Import the txt.py file from directory file_handlers. Do not mix up there is NO file_handlers.txt there!
from file_handlers.txt import TxtFileHelper 
from file_handlers.csv import CsvFileHelper 
from file_handlers.app import AppFileHelper 
from file_handlers.db import DbFileHelper

mydb = pymysql.connect(
host = 'localhost',
user = 'root',
password = '',
database = 'popup2',
cursorclass=pymysql.cursors.DictCursor
)
cursor = mydb.cursor()

row_per_page = 15          

bypass_list = [" ", "  ", "   ", "    "]
    
# Start: words in mysql table ############3
orders_to_pdts = "orders_to_pdts"
opid = "opid"
oid = "oid"
pid = "pid"
product_name = "product_name"
product_price = "product_price"
date = "date"
unixtime = "unixtime"

products = "products"
pid = "pid"
product_name = "product_name"
product_price = "product_price"
product_stock = "product_stock"

orders_status = "orders_status"
osid = "osid"
o_status = "o_status"

orders = "orders"
oid = "oid"
customer_name = "customer_name"
customer_name = "customer_name"
customer_address ="customer_address"
customer_phone = "customer_phone"
products_list = "products_list"
order_total = "order_total"
courier_id = "courier_id"
o_status_id = "o_status_id"
unixtime = "unixtime"
date = "date"

couriers = "couriers"
cid = "cid"
courier_name = "courier_name"
courier_phone = "courier_phone"

customers = "customers"
cusid = 'cusid'
customer_name = "customer_name"
customer_address = "customer_address"
customer_phone = "customer_phone"
left_id = "left_id"
right_id = "right_id"

prm_key="prm_key"
col_name = "col_name"
col_phone_price = "col_phone_price"
col_stock = "col_stock"
 
go = {} # direction left and right in row display
go[left_id] = 0
go[right_id] = 0
show = {} # show the results on screen
mx = {} # max length of each show column

minute1 = 60 # seconds
hour1 = 60*minute1 # seconds
day1 = 24*hour1*minute1 # seconds
# End: words in mysql table ############


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
order_status_list = 'order_status_list'
orders_name_list   = 'orders_name_list'


data = {}

data[products] = []
data[couriers] = []
data[orders] = []

tb = {}
tb[products] = [pid, product_name, product_price, product_stock]
tb[couriers] = [cid, courier_name, courier_phone]
tb[orders] = [oid, customer_name, customer_address, customer_phone, products_list, order_total, courier_id, o_status_id, date]
tb[orders_status] = [osid, o_status]
tb[orders_to_pdts] = [opid, oid, pid, product_name, product_price, unixtime, date]

ln = [
    {cat: main, cats: main},
    {cat: product, cats: products, price_phone: price, prm_key: pid, col_name: product_name, col_phone_price: product_price, col_stock: product_stock},
    {cat: courier, cats: couriers, price_phone: phone, prm_key: cid, col_name: courier_name, col_phone_price: courier_phone, col_stock: ''},
    {cat: order, cats: orders},         
]

v = [                  
    ['', '', '', '', ''],  # system input variables fot all menus i.e., v[i][0] = input_filter("Enter something")
    ['', '', '', '', ''],
    ['', '', '', '', ''],
    ['', '', '', '', ''],     
]

txt = 'txt' 
csv = 'csv'
app = 'app'
db = 'db'
table = 'table'
han = 'han'
sto = 'sto'
hlp = 'hlp'

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
    2: '\033[1;93m',
    3: '\033[1;92m',
    4: '\033[1;96m',
    5: '\033[1;91m',
    'E': '\033[m',
}

c2 = { # color code dictionary 2
    0: '\033[1;45m',   
    1: '\033[1;42m',
    2: '\033[1;43m',
    3: '\033[1;42m',
    4: '\033[1;46m',
    5: '\033[1;41m',
    'E': '\033[m',
}

c3 = { # color code dictionary 3
    "BLINK": '\033[1;5m',   
    "BLINK2": '\033[1;6m',
    "VIOLETBG": '\033[1;45m',
    "BLUEBG": '\033[1;44m',
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

def check_exist_indb(sql_query):
    cursor.execute(sql_query)
    rows = cursor.fetchall()    
    if len(rows) > 0:
        return True
    else:
        return False

def clear_screen(): # Function to clear the screen, suitable for winows and linux    
    platform  = sys.platform
    if platform == "win32":
        os.system("clear") # Git bash having "clear" may pretend win32. Howerver it will bypass below "cls" error warning.
        os.system("cls")   # Genuine win32 overrides above "clear" error warning.
    else:
        os.system("clear")

def dateTimeNow()->datetime:
    """return format: 2022-11-19 03:58:05 """
    dateTimeNow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dateTimeNow = datetime.strptime(dateTimeNow, '%Y-%m-%d %H:%M:%S')
    return dateTimeNow 

def dateTimeToUnix(dateTime = None) -> int:
    """ 2022-11-19 04:19:13 -> 1668831553 """
    if type(dateTime) is datetime and dateTime >= datetime(1970, 1, 1):
        unixtime = int(datetime.timestamp(dateTime))
    elif type(dateTime) is str and re.match('^((\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}))$', dateTime) and datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S') >= datetime(1970, 1, 1):
        dateTime = datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S')
        unixtime = int(datetime.timestamp(dateTime))
    elif dateTime is None:
        dateTimeNow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dateTimeNow = datetime.strptime(dateTimeNow, '%Y-%m-%d %H:%M:%S')
        unixtime = int(datetime.timestamp(dateTimeNow))
    else:
        unixtime = 0
    return unixtime

def get_screen_size() -> object:
    try:
        screen_size = os.get_terminal_size()
    except:
        screen_size = shutil.get_terminal_size()

    return screen_size
    
def init_file_data(file_name, default_data): # Function initilizes data, use default data if stroage data not exist
    helper = rw[hlp]() # helper object created from Class rw[hlp]
    return helper.get_filecontents(file_name, default_data)

def input_filter(args):
    return re.sub(' +', ' ', input(args).strip())
        
def input_option(menu_name, main_input):    # Function handles user input on menu
    if main_input != 0:
        # breadcrumb = f"{main} \u25B6 {menu_name}"
        breadcrumb = f"{main} > {menu_name}" # use > instead of \u25B6 for compatible of old system.
  
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

def list_items(menu_name, option_value, where_clause, myinput, go_id, dict_key = None, dict_value = None):  # Function prints products listing
    cc_length = (len(cc[option_value]) + len(cc["E"])) 
    
    prm_key = tb[menu_name][0]
    # p('just inside list_items   ', 'go_id[0]:', go_id[0], 'go_id[1]:', go_id[1], 'myinput:', myinput)
    cursor.execute(f'SELECT MAX({prm_key}) as max_id FROM {menu_name} WHERE {where_clause}')
    max_id = cursor.fetchall()
    cursor.execute(f'SELECT  COUNT({prm_key}) as selected_total FROM {menu_name} WHERE {where_clause}')
    selected_total = cursor.fetchall()
    
    
    if max_id[0]["max_id"] is not None:
            
        go[left_id]  = go_id[0]
        go[right_id] = go_id[1]
        
        loop_list = tb[menu_name]
        
        for item in loop_list:
            show[item] = []  # define show[o_status_id], show[prm_key], show[customer_name]...
            mx[item] = []

        orderBy = f' order by {prm_key} DESC '
        
        if go[right_id] > 0 and (myinput == 'd' or myinput == 'D' or myinput == ''):        
            condition = f' {where_clause} AND {prm_key} < {go[right_id]} {orderBy} LIMIT {row_per_page}'
            myinput = str(go[right_id])
        elif (myinput == 'a' or myinput == 'A'):
            
            if go[left_id] > 0 :
                condition = f' {where_clause} AND {prm_key} > {go[left_id]} order by {prm_key} ASC LIMIT {(row_per_page + 1)}'

            else:
                condition = f' {where_clause} AND {prm_key} >= {max_id[0]["max_id"]} order by {prm_key} ASC LIMIT {(row_per_page + 1)}'
                
            cursor.execute(f'SELECT * FROM {menu_name} WHERE {condition}')  
            rows = cursor.fetchall()
            if len(rows) > 0:
                go[right_id] = rows[-1][prm_key] 
                if len(rows) < row_per_page + 1:
                    condition = f' {where_clause} AND {prm_key} <= {go[right_id]} {orderBy} LIMIT {row_per_page}'
                else:
                    condition = f' {where_clause} AND {prm_key} < {go[right_id]} {orderBy} LIMIT {row_per_page}'
                myinput = str(go[right_id])
            else:
                # condition = f'o_status_id = 0 LIMIT {row_per_page}'
                condition = f' {where_clause} AND {prm_key} <= {max_id[0]["max_id"]} {orderBy} LIMIT {row_per_page}'
                myinput = str(0)
        else:
            # p('inside last else   ', 'go_id[0]:', go_id[0], 'go_id[1]:', go_id[1], 'myinput:', myinput)
            myinput = str(myinput)
            if re.match('^([0-9]+)$', myinput):
                myinput = int(myinput)
                condition = f' {where_clause} AND {prm_key} <= {myinput} {orderBy} LIMIT {row_per_page}'
                myinput = str(myinput)
            else:
                myinput = max_id[0]["max_id"]
                condition = f' {where_clause} AND {prm_key} <= {max_id[0]["max_id"]} {orderBy} LIMIT {row_per_page}'
                myinput = str(myinput)
        # p('before re.match inside list_items  ', 'go_id[0]:', go_id[0], 'go_id[1]:', go_id[1], 'myinput:', myinput)
        myinput = str(myinput)        
        if re.match('^([0-9]+)$', myinput):
            myinput = int(myinput)
            
            if (go[left_id] > 0 or go[right_id] > 0) and  myinput == 0: # Menually enter 0 will go to last page
                condition = f' {where_clause} AND {prm_key} > 0 order by {prm_key} ASC LIMIT {(row_per_page)+1}'
                cursor.execute(f'SELECT * FROM {menu_name} WHERE {condition} ')
                rows = cursor.fetchall()
                rows[-1][prm_key]
                condition = f' {where_clause} AND {prm_key} < {rows[-1][prm_key]} order by {prm_key} DESC LIMIT {(row_per_page)}'
                
            # p(condition)
            
            cursor.execute(f'SELECT * FROM {menu_name} WHERE {condition} ')
            rows = cursor.fetchall()
            
            
            # Start Stay at default page if no result found perviously ######################################################
            # print('Just inside Start Stay at default page, len(rows): ', len(rows), 'max_id: ', max_id[0]["max_id"])
            if len(rows) == 0 and max_id[0]["max_id"] > 0:
                
                condition = f' {where_clause} AND {prm_key} >= {max_id[0]["max_id"]} order by {prm_key} ASC LIMIT {(row_per_page + 1)}'
                # p(condition)
                cursor.execute(f'SELECT * FROM {menu_name} WHERE {condition} ')
                rows = cursor.fetchall()
                # p('len(rows): ', len(rows))
                if len(rows) > 0:
                    go[right_id] = rows[-1][prm_key] 
                    if len(rows) < row_per_page + 1:
                        condition = f' {where_clause} AND {prm_key} <= {go[right_id]} {orderBy} LIMIT {row_per_page}'
                    else:
                        condition = f' {where_clause} AND {prm_key} < {go[right_id]} {orderBy} LIMIT {row_per_page}'
                    myinput = str(go[right_id])
                else:
                    # condition = f'o_status_id = 0 LIMIT {row_per_page}'
                    condition = f' {where_clause} AND {prm_key} < {go[right_id]} {orderBy} LIMIT {row_per_page}'
                    myinput = str(0)
     
                # p(condition)
                cursor.execute(f'SELECT * FROM {menu_name} WHERE {condition} ')
                rows = cursor.fetchall()
            # End Stay at default page if no result found perviously #########################################################
            
            
            if len(rows) > 0:
                begin_row = rows[0]
                final_row = rows[-1]
                
                for x in range(len(rows)):
                    if menu_name == orders:
                        rows[x][products_list] = ast.literal_eval(rows[x][products_list]) 
                        rows[x][products_list] = [rows[x][products_list][i][0] for i in range(len(rows[x][products_list]))]
                        # rows[x][products_list][i][0] is prodcut id inside tuple e.g. [(6, "Fisherman's Fish Pie", 7.5), (3, 'Chicken & Mushroom Pie', 5.5)]
                    
                    for item in loop_list:
                        show[item].append(str(rows[x][item]))

                for item in loop_list:
                    show[item].append(item)
                
                for item in loop_list:
                    mx[item] = len(max(list(x for x in show[item]), key=len)) + 1 #add 1 spaceing for easing feeling.

                screen_size = get_screen_size()
                p("")     
                for x in range(len(rows)):
                    temp = ''
                    header = ''
                    for item in loop_list:
                        if x == 0:
                            header += f'{str(item): <{mx[item]}}'
                        temp += f'{str(rows[x][item]): <{mx[item]}}'
                    if x == 0:
                        header = f'{cc[user_input]}{header}{cc["E"]}'
                        p(f'{header: ^{screen_size.columns - 1 + cc_length}}') 
                        
                    if rows[x][loop_list[0]] == int(myinput):
                        temp = f'{c3["VIOLETBG"]}{temp}{c3["E"]}'
                        p(f'{temp: ^{screen_size.columns - 1 + cc_length}}')
                    else:
                        p(f'{temp: ^{screen_size.columns - 1}}')
                    
                p("")      
                pager = f'{cc[user_input]}Top Page [T]{cc["E"]} | [{begin_row[prm_key]} <<<- {cc[user_input]}Previous Page [A]{cc["E"]}  {menu_name} ID [{c3["BLINK"]}{rows[0][prm_key]}{c3["E"]}]  {cc[user_input]}[D] Next Page{cc["E"]} ->>> {final_row[prm_key]}] | {cc[user_input]}Last Page [0]{cc["E"]} | [MAX ID: {max_id[0]["max_id"]}] | [{selected_total[0]["selected_total"]} Records]'
                p(f'{pager:*^{screen_size.columns - 1 + 5 * cc_length}}')
                p("")
                go[right_id] = final_row[prm_key]
                go[left_id] = begin_row[prm_key]
            else:
                go[right_id] = 0
                go[left_id]  = 0

        return [go[left_id], go[right_id]]
    else:
        return [0,0]
    
    


def list_options(menu_name, option_value):  # Function prints options listing
    cc_length = (len(cc[option_value]) + len(cc["E"])) 
  
    # check order status
    
    id_number = []
    temp_data = []
    for item in data[menu_name]:
        for x, y in item.items():
            id_number.append(x)
            temp_data.append(y)


    search_terms = ''
    cc_length_factor = 0
    
    if len(temp_data) > 0:
        screen_size = get_screen_size()
        temp=[]
        for item in temp_data:
            temp.append(str(item))  # Convert the list elements to string for display purpose.
        elm_max_length = len(max(temp, key=len)) + len(str(len(temp))) + len('(  ): ')
        # elm_max_length = the max text element length in list + text length of number of elemets in list (e.g. 23 is length 2, 645 is length 3) + text length of '(  ): '        
        chunk_no =  screen_size.columns / elm_max_length
        display_chunk_size = 1 if chunk_no < 1 or len(temp) < 2 else int(chunk_no)
        # pedding_length = 0 if display_chunk_size == 1 else elm_max_length + cc_length
        pedding_length = elm_max_length + len(search_terms) + cc_length
        
        item_number = 0
        id_loop = 0
        # if display_chunk_size > 1:
        residual = len(temp) % display_chunk_size
        if residual != 0:
            loop_times = display_chunk_size - residual
            for i in range(loop_times):
                temp.append("")
                id_number.append("")
                
        else:
            loop_times = 0
        
        p(" ") # For nice looking      
        for i in range(0, len(temp), display_chunk_size):        
            items_string = ''
            for item_name in temp[i:i + display_chunk_size]:
                item_number += 1
                colour_number = f"{cc[option_value]}{id_number[id_loop]}{cc['E']}"
                id_loop += 1
                colour_string = f"( {colour_number} ){search_terms}: {item_name}"
                if item_number > len(temp) - loop_times:
                    items_string += f"{item_name: <{pedding_length}}"
                else:
                    items_string += f"{colour_string: <{pedding_length}}"
            p(f'{items_string: ^{screen_size.columns + display_chunk_size * cc_length}}')   
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

    screen_size = get_screen_size()
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

# Establish a database connection #############################################


if __name__ == "__main__":
            
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
                    
                    arr = [0,0]
                    myinput = 0
                    while True:
                        print_menu(ln[i][cats], user_input)
                        arr = list_items(ln[i][cats], user_input, 1, myinput, arr) 
                        myinput = input(f'Enter ID to Search: {cc[user_input]}Spacebar to Pass{cc["E"]}: ')
                        if myinput in bypass_list:
                            print_menu(ln[i][cats], 0) # Default menu 
                            break

                elif user_input == 2:
                    print_menu(ln[i][cats], user_input)
                    list_items(ln[i][cats], user_input, 1, 0, [0,0]) 

                    while True:
                        
                        while True:
                            v[i][0] = input_filter(f"Enter new {ln[i][cat]} name: ")
                            if v[i][0] == "":
                                break                  
                            elif check_exist_indb(f'SELECT {ln[i][col_name]} FROM {ln[i][cats]} WHERE {ln[i][col_name]} = "{v[i][0]}" '):
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

                        if v[i][0] == "" or v[i][1] == "":
                            print_menu(ln[i][cats], 0) # Reset to default menu after enter new product name.
                            break
                        else:
                            if main_input == 1:
                                insert = f"""INSERT INTO {ln[i][cats]} ({ln[i][col_name]}, {ln[i][col_phone_price]}, {ln[i][col_stock]}) values (%s, %s, %s)"""
                                cursor.execute(insert, (v[i][0], v[i][1], 100)) # product stock defualt value 100                                 
                            elif main_input == 2:
                                insert = f"""INSERT INTO {ln[i][cats]} ({ln[i][col_name]}, {ln[i][col_phone_price]}) values (%s, %s)"""
                                cursor.execute(insert, (v[i][0], v[i][1]))
                            mydb.commit()
                            insert_id = cursor.lastrowid                          
                            print_menu(ln[i][cats], 0) # Reset to default menu after enter new product name.
                            list_items(ln[i][cats], user_input, 1, insert_id, [0,0]) 
                            p(f"( {cc[user_input]}{insert_id}{cc['E']} ): {v[i][0]} : added to {ln[i][cats]} record")
                            break
                    
                elif user_input == 3:                 
                    arr = [0,0]
                    myinput = 0
                    while True:
                        print_menu(ln[i][cats], user_input)
                        arr = list_items(ln[i][cats], user_input, 1, myinput, arr) 
                        myinput = input(f'Enter ID to Search: {cc[user_input]}Spacebar to Pass{cc["E"]}: ')
                        if myinput in bypass_list:
                            break
                        
                    while True:
                        index_input = input_filter(f"Enter {ln[i][cat]} ID to update: ")
                        if index_input == "":
                            print_menu(ln[i][cats], 0) # Reset to default menu after enter to escape
                            break
                        elif re.match('^([0-9]+)$', index_input):
                            index_input = int(index_input)
                            
                            if check_exist_indb(f'SELECT {ln[i][prm_key]} FROM {ln[i][cats]} WHERE {ln[i][prm_key]} = {index_input}'):
                                p(" ") # For nice looking
                                p(f"Edit {ln[i][cats]} ( {cc[user_input]}{index_input}{cc['E']} ) ")
                                cursor.execute(f'SELECT * FROM {ln[i][cats]} WHERE {ln[i][prm_key]} = {index_input}')  
                                rows = cursor.fetchall()
                                elm_max_length = len(max(list(x for x in rows[0]), key=len))
                                for key, value, in rows[0].items():
                                    
                                    print(f'{key: <{elm_max_length}} : {value}')
                                    
                                    if key == ln[i][col_name]:
                                        while True:
                                            v[i][0] = input_filter(f'{key: <{elm_max_length}} : ')
                                            if v[i][0] == "":
                                                break 
                                            elif check_exist_indb(f'SELECT {ln[i][prm_key]} FROM {ln[i][cats]} WHERE {ln[i][col_name]} = "{v[i][0]}"'):
                                                p(f"{v[i][0]} already exist, please try again.")
                                            else:
                                                cursor.execute(f'UPDATE {ln[i][cats]} SET {ln[i][col_name]} = "{v[i][0]}" WHERE {ln[i][prm_key]} = {index_input}') 
                                                mydb.commit() 
                                                break                                      
                                    elif key == ln[i][col_phone_price]:
                                        while True:
                                            v[i][1] = input_filter(f'{key: <{elm_max_length}} : ')
                                            if  v[i][1] == "":
                                                break
                                            if main_input == 1:
                                                if re.match('^([0-9]*)(\\.){0,1}([0-9]*)$', v[i][1]): # match 0 or 1 dot in digit string. 
                                                    v[i][1] = round(float(v[i][1]), 2)
                                                    cursor.execute(f'UPDATE {ln[i][cats]} SET {ln[i][col_phone_price]} = {v[i][1]} WHERE {ln[i][prm_key]} = {index_input}') 
                                                    mydb.commit() 
                                                    break
                                                else:
                                                    p(f"Please enter valid number. ")
                                            elif main_input == 2:
                                                if re.match('^([0-9]+)$', v[i][1]):
                                                    cursor.execute(f'UPDATE {ln[i][cats]} SET {ln[i][col_phone_price]} = "{v[i][1]}" WHERE {ln[i][prm_key]} = {index_input}') 
                                                    mydb.commit() 
                                                    break
                                                else:
                                                    p(f"Please enter valid phone number. ") 
                                    elif key == ln[i][col_stock]:
                                        while True:
                                            v[i][2] = input_filter(f'{key: <{elm_max_length}} : ')
                                            if v[i][2] == "":
                                                break 
                                            else:
                                                if re.match('^([0-9]+)$', v[i][2]):
                                                    cursor.execute(f'UPDATE {ln[i][cats]} SET {ln[i][col_stock]} = {v[i][2]} WHERE {ln[i][prm_key]} = {index_input}') 
                                                    mydb.commit() 
                                                    break    
                                                else:
                                                    p(f"Please enter valid phone number. ")
                                        
                                print_menu(ln[i][cats], 0)                    
                                list_items(ln[i][cats], user_input, 1, index_input, [0,0])
                                cursor.execute(f'SELECT * FROM {ln[i][cats]} WHERE {ln[i][prm_key]} = {index_input}')  
                                rows = cursor.fetchall()
                                p(f"Successfully updated {ln[i][cat]} ( {cc[user_input]}{index_input}{cc['E']} ): {rows[0][ln[i][col_name]]}")
                        break # beak to outer while loop
                elif user_input == 4:
                    arr = [0,0]
                    myinput = 0
                    while True:
                        print_menu(ln[i][cats], user_input)
                        arr = list_items(ln[i][cats], user_input, 1, myinput, arr) 
                        myinput = input(f'Enter ID to Search: {cc[user_input]}Spacebar to Pass{cc["E"]}: ')
                        if myinput in bypass_list:
                            break
                    
                    while True:
                        index_input = input_filter(f"Enter {ln[i][cat]} ID to delete: ")
                        if index_input == "":
                            print_menu(ln[i][cats], 0) # Reset to default menu after enter to escape
                            break
                        elif re.match('^([0-9]+)$', index_input):
                            index_input = int(index_input)
                            if check_exist_indb(f'SELECT {ln[i][prm_key]} FROM {ln[i][cats]} WHERE {ln[i][prm_key]} = {index_input}'):
                                p(" ") # For nice looking
                                cursor.execute(f'SELECT * FROM {ln[i][cats]} WHERE {ln[i][prm_key]} = {index_input}')  
                                rows = cursor.fetchall()
                                v[i][0] = input_filter(f"Delete {ln[i][cat]} ( {cc[user_input]}{index_input}{cc['E']} ): {rows[0][ln[i][col_name]]} \nConfirm delete: y/n? ")
                                if v[i][0] == 'y' or v[i][0].upper() == 'Y':
                                    cursor.execute(f'DELETE FROM {ln[i][cats]} WHERE {ln[i][prm_key]} = {index_input}') 
                                    mydb.commit()
                                    print_menu(ln[i][cats], 0)
                                    list_items(ln[i][cats], user_input, 1, index_input, [0,0])
                                    p(f"Successfully deleted. Previously ( {cc[user_input]}{index_input}{cc['E']} ): {rows[0][ln[i][col_name]]}")
                                    p(" ") # For nice looking
                                    break
                                else:
                                    print_menu(ln[i][cats], 0)
                                    break
                p("")
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
                    arr = [0,0]
                    myinput = 0
                    while True:
                        print_menu(orders, user_input)
                        arr = list_items(orders, user_input, 1, myinput, arr) 
                        myinput = input(f'Enter ID to Search: {cc[user_input]}Spacebar to Pass{cc["E"]}: ')
                        if myinput in bypass_list:
                            break
                    
                    while True:
                        cursor.execute(f'SELECT * FROM {orders_status} WHERE 1')  
                        rows = cursor.fetchall()
                        # print(rows)
                        status_list=''
                        for row in rows:
                            status_list += f"[{cc[user_input]}{row[osid]}{cc['E']}] {row[o_status]}, "
                        p(status_list.rstrip(', '))
                        p(" ") # For nice looking
  
                        status_input = input_filter(f"Choose status number [ ]: ")
                        if status_input == "":
                            break
                        elif re.match('^([0-9]+)$', status_input):
                            status_input = int(status_input)
                            if True in set(str(status_input) in str(dic[osid]) for dic in rows):
                                arr = [0,0]
                                myinput = 0
                                while True:
                                    print_menu(orders, user_input)
                                    where_clause = f'{o_status_id} = {status_input}'
                                    arr = list_items(orders, user_input, where_clause, myinput, arr) 
                                    myinput = input(f'Enter ID to Search: {cc[user_input]}Spacebar to Pass{cc["E"]}: ')
                                    if myinput in bypass_list:
                                        break

                    while True:
                        cursor.execute(f'SELECT * FROM {couriers} WHERE 1')  
                        rows = cursor.fetchall()
                        p("")
                        couriers_list=''
                        for row in rows:
                            couriers_list += f"[{cc[user_input]}{row[cid]}{cc['E']}] {row[courier_name]}, "
                        p(couriers_list.rstrip(', '))
                        p(" ") # For nice looking
                        get_input = input_filter(f"Choose courier number [ ]: ")
                        p("")                        
                        if get_input == "":
                            
                            break
                        elif re.match('^([0-9]+)$', get_input):
                            get_input = int(get_input)
                            if True in set(str(get_input) in str(dic[cid]) for dic in rows):
                                print_menu(orders, user_input)
                                arr = [0,0]
                                myinput = 0
                                while True:
                                    print_menu(orders, user_input)
                                    where_clause = f'{courier_id} = {get_input}'
                                    arr = list_items(orders, user_input, where_clause, myinput, arr) 
                                    myinput = input(f'Enter ID to Search: {cc[user_input]}Spacebar to Pass{cc["E"]}: ')
                                    if myinput in bypass_list:
                                        break
                                
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
                            cursor.execute(f'SELECT pid, product_name, product_price FROM {products} WHERE 1')  
                            rows = cursor.fetchall()
                            data[products_name_list] = [{dic[pid]:  f'{dic[product_name]} £{dic[product_price]}'}for dic in rows]
                            pid_list = [dic[pid] for dic in rows]
                            price_list = [dic[product_price] for dic in rows]


                            p("Products items choices: ")
                            list_options(products_name_list, user_input)
                            item_string = ''
                            item_list =[]
                            total_price = 0
                            while True:
                                
                                bypass_input = input(f"( {cc[user_input]}{item_string[:-2]}{cc['E']} ) {cc[user_input]}£{round(total_price, 2)}{cc['E']}: Choose number, e/E Esacpe, {cc[user_input]}Spacebar to Confirm{cc['E']}: ")
                                
                                input_order = re.sub(' +', ' ', bypass_input.strip())
                                
                                if input_order == "e":
                                    print_menu(orders, 0) # Reset to default menu after escape
                                    break
                                elif bypass_input in bypass_list:
                                    break
                                elif re.match('^([0-9]+)$', input_order):
                                    input_order = int(input_order)
                                    if True in set(str(input_order) in str(dic[pid]) for dic in rows):
                                        total_price += price_list[pid_list.index(input_order)]
                                        item_string += f'{input_order}, '
                                        item_list.append(input_order)
                            if input_order != 'E' and input_order != 'e':
                                cursor.execute(f'SELECT cid, courier_name, courier_phone FROM {couriers} WHERE 1')  
                                rows = cursor.fetchall()
                                data[couriers_name_list] = [{dic[cid]: f'{dic[courier_name]} - {dic[courier_phone]}'} for dic in rows]
                                p("Courier choices: ")
                                list_options(couriers_name_list, user_input)
                                while True:
                                    courier_input = input_filter(f"Choose courier number (   ): Enter e/E to esacpe: ")
                                    p("")
                                    if courier_input == "e":
                                        print_menu(orders, 0) # Reset to default menu after escape
                                        break
                                    elif re.match('^([0-9]+)$', courier_input):
                                        courier_input = int(courier_input)
                                        if True in set(str(courier_input) in str(dic[cid]) for dic in rows):
                                            pdt_list = []
                                            for item in item_list:
                                                cursor.execute(f'SELECT pid, product_name, product_price FROM {products} WHERE pid = {item}')
                                                rows = cursor.fetchall()
                                                pdt_list.append(rows[0])
                                                
                                            products_tuple =[ (x[1], y[1], z[1]) for x, y, z in (dic.items() for dic in pdt_list)]
                                            products_string = str(products_tuple)
                                            insert = f"""INSERT INTO {orders} ({customer_name}, {customer_address}, {customer_phone}, {products_list}, {order_total}, {courier_id}, {o_status_id}, {unixtime}, {date}) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                                            
                                            cursor.execute(insert, (cust_name, cust_address, cust_phone, products_string, total_price, courier_input, 1, dateTimeToUnix(), dateTimeNow()))
                                            mydb.commit()  
                                            last_oid = cursor.lastrowid
                                   
                                            for dic in pdt_list:
                                                insert = f"""INSERT INTO {orders_to_pdts} (oid, pid, product_name, product_price, unixtime, date) values (%s, %s, %s, %s, %s, %s)"""
                                                cursor.execute(insert, (last_oid, dic[pid], dic[product_name], dic[product_price], dateTimeToUnix(), dateTimeNow()))
                                                mydb.commit() 
                           
                                            print_menu(orders, 0) # Reset to default menu after adding order
                                            list_items(orders, user_input, 1, last_oid, [0,0])
                                            p(f"Added new order ( {cc[user_input]}{last_oid}{cc['E']} ): ")
                                            break                                    
                        break # break the outer while loop                
                    
                elif user_input == 3:
                    arr = [0,0]
                    myinput = 0
                    while True:
                        print_menu(orders, user_input)
                        arr = list_items(orders, user_input, 1, myinput, arr) 
                        myinput = input(f'Enter ID to Search: {cc[user_input]}Spacebar to Pass{cc["E"]}: ')
                        if myinput in bypass_list:
                            break
                    while True:
                        index_input = input_filter("Enter order (  ) to update: ")
                        if index_input == "":
                            print_menu(orders, 0) # Reset to default menu after enter to escape
                            break
                        elif re.match('^([0-9]+)$', index_input):
                            index_input = int(index_input)
                            if check_exist_indb(f'SELECT oid FROM orders WHERE oid = {index_input}'):
                                cursor.execute(f'SELECT s.o_status, o.* FROM orders as o INNER JOIN orders_status as s ON o.o_status_id = s.osid WHERE o.oid = {index_input}')  
                                order_rows = cursor.fetchall()
                                p(" ") # For nice looking
                                p(f"Order ( {index_input} ) status: [{order_rows[0][o_status_id]}] {order_rows[0][o_status]}")
                                
                                cursor.execute(f'SELECT * FROM orders_status WHERE 1')  
                                status_rows = cursor.fetchall()
                                osid_list = [dic["osid"] for dic in status_rows]
                                o_status_list = [dic["o_status"] for dic in status_rows]
                                # p(osid_list)
                                # p(o_status_list)
                                p(" ") # For nice looking
                                status_list="Status choices: "
                                for row in status_rows:
                                    status_list += f"[{cc[user_input]}{row[osid]}{cc['E']}] {row[o_status]}, "
                                p(status_list.rstrip(', '))
                                p(" ") # For nice looking

                                while True:
                                    edit_order = input_filter(f"Choose status number [ ]: ")
                                    if edit_order == "":
                                        print_menu(orders, 0) # Reset to default menu after edit orders name
                                        break
                                    elif re.match('^([0-9]+)$', edit_order):
                                        edit_order = int(edit_order)
                                        if check_exist_indb(f'SELECT osid FROM orders_status WHERE osid = {edit_order}'):
                                            cursor.execute(f'UPDATE orders SET o_status_id = {edit_order} WHERE oid = {index_input}') 
                                            mydb.commit() 
                                            print_menu(orders, 0) # Reset to default menu after edit orders name
                                            list_items(orders, user_input, 1, index_input, [0,0])
                                            p(f"Successfully updated. Order ( {cc[user_input]}{index_input}{cc['E']} ) status: {edit_order} - {o_status_list[osid_list.index(edit_order)]}")
                                            break
                                break # break the outer while loop
    
                elif user_input == 4:
                    arr = [0,0]
                    myinput = 0
                    while True:
                        print_menu(orders, user_input)
                        arr = list_items(orders, user_input, 1, myinput, arr) 
                        myinput = input(f'Enter ID to Search: {cc[user_input]}Spacebar to Pass{cc["E"]}: ')
                        if myinput in bypass_list:
                            break                    
                    while True:
                        index_input = input_filter("Enter order (  ) to update: ")
                        if index_input == "":
                            print_menu(orders, 0) # Reset to default menu after enter to escape
                            break
                        elif re.match('^([0-9]+)$', index_input):
                            index_input = int(index_input)
                            if check_exist_indb(f'SELECT oid FROM orders WHERE oid = {index_input}'):
                                sql = f'''SELECT c.courier_name, c.courier_phone, s.o_status, o.* FROM orders as o 
                                            LEFT JOIN orders_status as s ON o.o_status_id = s.osid 
                                            LEFT JOIN couriers as c ON o.courier_id = c.cid
                                            WHERE o.oid = {index_input}'''
                                cursor.execute(sql)  
                                order_rows = cursor.fetchall()
                                order_rows[0]["products_list"] = ast.literal_eval(order_rows[0]["products_list"])                                
                                # column_name_list = [key for key, value in rows[0].items()]
                                p(" ") # For nice looking
                                p(f"Edit order ( {cc[user_input]}{index_input}{cc['E']} ) ")
                                update_column_list = ['customer_name', 'customer_address', 'customer_phone', 'products_list', 'courier_id', 'o_status_id']
                                elm_max_length = len(max(update_column_list, key=len))
                                
                                for x in update_column_list:
                                    if x == customer_name or x == customer_address or x == customer_phone:
                                        p(f'{x: <{elm_max_length}} : {order_rows[0][x]}')
                                        if x == customer_phone:
                                            while True:
                                                edit_order = input_filter(f'{x: <{elm_max_length}} : ')
                                                if re.match('^([0-9]+)$', edit_order) or edit_order == '':
                                                        break
                                                else:
                                                    p(f'Please enter vaild phone umber.') 
                                        else:
                                            edit_order = input_filter(f'{x: <{elm_max_length}} : ')
                                            
                                        if edit_order != "":
                                            cursor.execute(f'UPDATE orders SET {x} = "{edit_order}" WHERE oid = {index_input}') 
                                            mydb.commit() 
    
                                    elif x == products_list:
                                        p(" ")
                                        
                                        order_pid_list = [x[0] for x in order_rows[0][products_list]]
                                        p(f'{x: <{elm_max_length}} : {order_pid_list}')
                                        cursor.execute(f'SELECT pid, product_name, product_price FROM {products} WHERE 1')  
                                        rows = cursor.fetchall()
                                        data[products_name_list] = [{dic[pid]:  f'{dic[product_name]} £{dic[product_price]}'}for dic in rows]
                                        pid_list = [dic[pid] for dic in rows]
                                        price_list = [dic[product_price] for dic in rows]
                                        list_options(products_name_list, user_input)
                                        item_string = ''
                                        item_list = []
                                        total_price = 0
                                        escape_outer = False
                                        while True:
                                            
                                            bypass_input = input(f"( {cc[user_input]}{item_string[:-2]}{cc['E']} ) {cc[user_input]}£{round(total_price, 2)}{cc['E']}: Choose number, e/E Esacpe, {cc[user_input]}Spacebar to Confirm{cc['E']}: ")
                                            
                                            input_order = re.sub(' +', ' ', bypass_input.strip())
                                            
                                            if input_order == "e":
                                                escape_outer = True
                                                break
                                            elif bypass_input in bypass_list:
                                                if len(item_list) > 0:
                                                    pdt_list = []
                                                    for item in item_list:
                                                        cursor.execute(f'SELECT pid, product_name, product_price FROM products WHERE pid = {item}')
                                                        rows = cursor.fetchall()
                                                        pdt_list.append(rows[0])   
                                                    products_tuple =[ (x[1], y[1], z[1]) for x, y, z in (dic.items() for dic in pdt_list)]
                                                    products_string = str(products_tuple)
                                                    cursor.execute(f'UPDATE orders SET products_list = "{products_string}",  order_total = {total_price} WHERE oid = {index_input}') 
                                                    mydb.commit()
                                                    cursor.execute(f'DELETE FROM orders_to_pdts WHERE oid = {index_input}')
                                                    mydb.commit()
                                                    for dic in pdt_list:
                                                        insert = f"""INSERT INTO orders_to_pdts (oid, pid, product_name, product_price, unixtime, date) values (%s, %s, %s, %s, %s, %s)"""
                                                        cursor.execute(insert, (index_input, dic[pid], dic[product_name], dic[product_price], dateTimeToUnix(), dateTimeNow()))
                                                        mydb.commit()
                                                            
                                                break
                                            
                                            elif re.match('^([0-9]+)$', input_order):
                                                input_order = int(input_order)
                                                if True in set(str(input_order) in str(dic[pid]) for dic in rows):
                                                    total_price += price_list[pid_list.index(input_order)]
                                                    item_string += f'{input_order}, '
                                                    item_list.append(input_order)
                                        
                                        if escape_outer == True:
                                            break # break the outer while loop           
                                        
                                    elif x == courier_id:
                                        p(" ")                                       
                                        cursor.execute(f'SELECT cid, courier_name, courier_phone FROM {couriers} WHERE 1')  
                                        rows = cursor.fetchall()
                                        data[couriers_name_list] = [{dic[cid]: f'{dic[courier_name]} - {dic[courier_phone]}'} for dic in rows]
                                        p(f'{x: <{elm_max_length}} : ( {order_rows[0][courier_id]} ): {order_rows[0][courier_name]} - {order_rows[0][courier_phone]}')
                                        list_options(couriers_name_list, user_input)
 
                                        while True:
                                            edit_order = input_filter(f"Choose courier number (   ): ")
                                            p("")
                                            if edit_order == "":
                                                break
                                            elif re.match('^([0-9]+)$', edit_order):
                                                edit_order = int(edit_order)
                                                if True in set(str(edit_order) in str(dic[cid]) for dic in rows):  
                                                    cursor.execute(f'UPDATE orders SET courier_id = {edit_order} WHERE oid = {index_input}') 
                                                    mydb.commit()
                                                    break
                                    
                                    elif x == o_status_id:
                                        cursor.execute(f'SELECT * FROM {orders_status} WHERE 1')  
                                        rows = cursor.fetchall()
                                        data[order_status_list] = [{dic[osid]: f'{dic[o_status]}'} for dic in rows]
                                        p(f'{x: <{elm_max_length}} : ( {order_rows[0][o_status_id]} ): {order_rows[0][o_status]}')
                                        list_options(order_status_list, user_input)  
                                        while True:
                                            edit_order = input_filter(f"Choose status number (  ): ")
                                            if edit_order == "":
                                                break
                                            elif re.match('^([0-9]+)$', edit_order):
                                                edit_order = int(edit_order)
                                                if True in set(str(edit_order) in str(dic[osid]) for dic in rows):
                                                    cursor.execute(f'UPDATE orders SET o_status_id = {edit_order} WHERE oid = {index_input}') 
                                                    mydb.commit()
                                                    break

                                print_menu(orders, 0) # Reset to default menu after edit orders name
                                list_items(orders, user_input, 1, index_input, [0,0])
                                p(f"Updated order ( {cc[user_input]}{index_input}{cc['E']} ):")                            
                                break # break the outer while loop

                elif user_input == 5:
                    arr = [0,0]
                    myinput = 0
                    while True:
                        print_menu(orders, user_input)
                        arr = list_items(orders, user_input, 1, myinput, arr) 
                        myinput = input(f'Enter ID to Search: {cc[user_input]}Spacebar to Pass{cc["E"]}: ')
                        if myinput in bypass_list:
                            break
                    while True:
                        index_input = input_filter("Enter order (  ) to delete: ")
                        if index_input == "":
                            print_menu(orders, 0) # Reset to default menu after enter to escape
                            break
                        elif re.match('^([0-9]+)$', index_input):
                            index_input = int(index_input)
                            cursor.execute(f'SELECT * FROM orders WHERE oid = {index_input}')  
                            rows = cursor.fetchall()
                            if True in set(str(index_input) in str(dic[oid]) for dic in rows):
                                p(" ") # For nice looking
                                del_order = input_filter(f"Delete order ( {cc[user_input]}{index_input}{cc['E']} ): Confirm delete: y/n? ")
                                if del_order == 'y' or del_order.upper() == 'Y':
                                    cursor.execute(f'DELETE FROM orders WHERE oid = {index_input}') 
                                    mydb.commit()
                                    cursor.execute(f'DELETE FROM orders_to_pdts WHERE oid = {index_input}')
                                    mydb.commit()
                                    print_menu(orders, 0) # Reset to default menu after delete order or escape.
                                    list_items(orders, user_input, 1, index_input, [0,0])
                                    p(f"Successfully deleted. Previously ( {cc[user_input]}{index_input}{cc['E']} ):")
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




