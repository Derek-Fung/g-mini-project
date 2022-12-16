# mini_project_v6_oop.py
"""Mini-project python programme by Derek Tak Yiu Fung. Please run on CLI in this 'src' directory."""
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import pymysql, sys, os, random, string, ast, re, time, shutil
from dataclasses import dataclass

mydb = pymysql.connect(
host = 'localhost',
user = 'root',
password = '',
database = 'popup2',
cursorclass=pymysql.cursors.DictCursor
)

cursor = mydb.cursor()

def p(*args, **kwargs): # Alisa to print function
    print(*args, **kwargs)


@dataclass
class Container:
    
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

    report = "report"
    reports = "reports"


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
    data[reports] = []

    tb = {}
    tb[products] = [pid, product_name, product_price, product_stock]
    tb[couriers] = [cid, courier_name, courier_phone]
    tb[orders] = [oid, customer_name, customer_address, customer_phone, products_list, order_total, courier_name, o_status, date]
    tb[orders_status] = [osid, o_status]
    tb[orders_to_pdts] = [opid, oid, pid, product_name, product_price, unixtime, date]

    ln = [
        {cat: main, cats: main},
        {cat: product, cats: products, price_phone: price, prm_key: pid, col_name: product_name, col_phone_price: product_price, col_stock: product_stock},
        {cat: courier, cats: couriers, price_phone: phone, prm_key: cid, col_name: courier_name, col_phone_price: courier_phone, col_stock: ''},
        {cat: order, cats: orders, prm_key: oid, col_name: oid}, 
        {cat: report, cats: report},          
    ]

    v = ['', '', '', '', '']  # system input variables fot all menus i.e., v[0] = input_filter("Enter something")
     

    order_status = ["Preparing", "Awaiting Pickup", "Out-for-Delivery", "Delivered"]

    border_chr = ['~~~', '111', '222', '333', '444', '555'] 
    # Border characters to ouline the border of menu. Default is single character. But you can increase the border width by increasing the number of characters at the list elements.

    padding_chr = ['~', '1', '2', '3', '4', '5'] # Padding character must be single character in f-string. 


    menu = {
        main:{},
        products:{},
        couriers:{},
        orders:{},
        reports:{},
    }
    
    menu_name = list(menu.keys())

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
    ' [ 4 ]: reports menu option',
    ]

    menu[main][bottom] = [
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

    menu[reports][body] = [
    'RRRRR   EEEEEEE  ppppp    OOOO    RRRRR   TTTTTT   SSSSS ',
    'R   RR  E        p   pp  O    O   R   RR    TT    SS     ',
    'RRRR    EEEEEE   pppp   O      O  RRRR      TT      SSS  ',
    'R   R   E        p       O    O   R   R     TT         SS',
    'R    R  EEEEEEE  p        OOOO    R    R    TT     SSSSS ',
    '',
    '',
    ]

    menu[reports][options] = [
    ' [ 0 ]: return to main menu',
    ' [ 1 ]: report on total orders',
    ' [ 2 ]: report on total sales',
    ]

    menu[reports][bottom] = [
    '',
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

    months_name = ['March', 'April', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov']

    months_inv = [('2022-03-01', '2022-03-31'), ('2022-04-01', '2022-04-30'), ('2022-05-01', '2022-05-31'), ('2022-06-01', '2022-06-30'), ('2022-07-01', '2022-07-31'), ('2022-08-01', '2022-08-31'), ('2022-09-01', '2022-09-30'), ('2022-10-01', '2022-10-31'), ('2022-11-01', '2022-11-30')]


    op_elems_no = 5  # Each big-size digit contains 5 list elements.

    op_max_display_no = 4 # Maximun number of big-digits dispaly in vertical. 

    op_total_ht = op_elems_no  * op_max_display_no # Total height to display vertial digits.


###############################################################

@dataclass
class MethodClass():
    
    def check_exist_indb(self, sql_query):
        cursor.execute(sql_query)
        rows = cursor.fetchall()    
        if len(rows) > 0:
            return True
        else:
            return False

    def clear_screen(self): # Function to clear the screen, suitable for winows and linux    
        platform  = sys.platform
        if platform == "win32":
            os.system("clear") # Git bash having "clear" may pretend win32. Howerver it will bypass below "cls" error warning.
            os.system("cls")   # Genuine win32 overrides above "clear" error warning.
        else:
            os.system("clear")

    def dateTimeNow(self)->datetime:
        """return format: 2022-11-19 03:58:05 """
        dateTimeNow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dateTimeNow = datetime.strptime(dateTimeNow, '%Y-%m-%d %H:%M:%S')
        return dateTimeNow 

    def dateTimeToUnix(self, dateTime = None) -> int:
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

    def get_screen_size(self) -> object:
        try:
            screen_size = os.get_terminal_size()
        except:
            screen_size = shutil.get_terminal_size()
        return screen_size

    def input_filter(self, args):
        return re.sub(' +', ' ', input(args).strip())

    def input_option(self, menu_name, main_input):    # Function handles user input on menu
        if main_input != 0:
            # breadcrumb = f"{main} \u25B6 {menu_name}"
            breadcrumb = f"{c.main} > {menu_name}" # use > instead of \u25B6 for compatible of old system.
            
        else:
            breadcrumb = f"{menu_name}"
        while True:
            user_input = self.input_filter(f"{c.c2[0]} {breadcrumb} {c.c2['E']}: Enter option in square brackets [  ]: ")
            if re.match('^([0-9]+)$', user_input):
                user_input = int(user_input)
                if user_input < len(c.menu[menu_name][c.options]):
                    if menu_name == c.main and user_input == 0:
                        self.clear_screen()
                        user_input = -1
                    break # break if user_input < len(menu[menu_name][options]):
        return user_input


    def joint_opts_list(self, menu_name, user_input): # Function joints two options in one line on menu.
        joint_list = []
        cc_count = []  #Colour code count
        cc_length = len(c.cc[user_input]) + len(c.cc["E"]) # Colour code length
        temp_opts = []
        for item in c.menu[menu_name][c.options]: # Assign temp list to prevent polluting the original list.
            temp_opts.append(item)
        if len(temp_opts) % 2 != 0:
            temp_opts.append('') # Prevent colour codes shift. Append 1 empty element if len() is an odd number.
        for x in range(0, len(temp_opts), 2):
            str = ''
            i = 0
            for elm in temp_opts[x:x + 2]: # Join 2 elements to 1 elements
                if user_input != 0 and user_input  == temp_opts.index(elm):
                    elm = f'{c.cc[user_input]}{elm}{c.cc["E"]}'
                    item = f'{elm: <{c.menu_half_width + cc_length}}'
                    i += 1
                else:
                    item = f'{elm: <{c.menu_half_width}}'            
                str += item
            cc_count.append(i)
            joint_list.append(str)
        return [joint_list, cc_count]

    def list_items(self, menu_name, user_input, where_clause, myinput, go_id, dict_key = None, dict_value = None):  # Function prints products listing
        cc_length = (len(c.cc[user_input]) + len(c.cc["E"])) 
        
        prm_key = c.tb[menu_name][0]
        # p('just inside list_items   ', 'go_id[0]:', go_id[0], 'go_id[1]:', go_id[1], 'myinput:', myinput)
        cursor.execute(f'SELECT MAX({prm_key}) as max_id FROM {menu_name} WHERE {where_clause}')
        max_id = cursor.fetchall()
        cursor.execute(f'SELECT  COUNT({prm_key}) as selected_total FROM {menu_name} WHERE {where_clause}')
        selected_total = cursor.fetchall()
        
        
        if max_id[0]["max_id"] is not None:
                
            c.go[c.left_id]  = go_id[0]
            c.go[c.right_id] = go_id[1]
            
            loop_list = c.tb[menu_name]
            
            for item in loop_list:
                c.show[item] = []  # define show[o_status_id], show[prm_key], show[customer_name]...
                c.mx[item] = []

            orderBy = f' order by {prm_key} DESC '
            
            if c.go[c.right_id] > 0 and (myinput == 'd' or myinput == 'D' or myinput == ''):        
                condition = f' {where_clause} AND {prm_key} < {c.go[c.right_id]} {orderBy} LIMIT {c.row_per_page}'
                myinput = str(c.go[c.right_id])
            elif (myinput == 'a' or myinput == 'A'):
                
                if c.go[c.left_id] > 0 :
                    condition = f' {where_clause} AND {prm_key} > {c.go[c.left_id]} order by {prm_key} ASC LIMIT {(c.row_per_page + 1)}'

                else:
                    condition = f' {where_clause} AND {prm_key} >= {max_id[0]["max_id"]} order by {prm_key} ASC LIMIT {(c.row_per_page + 1)}'
                    
                cursor.execute(f'SELECT * FROM {menu_name} WHERE {condition}')  
                rows = cursor.fetchall()
                if len(rows) > 0:
                    c.go[c.right_id] = rows[-1][prm_key] 
                    if len(rows) < c.row_per_page + 1:
                        condition = f' {where_clause} AND {prm_key} <= {c.go[c.right_id]} {orderBy} LIMIT {c.row_per_page}'
                    else:
                        condition = f' {where_clause} AND {prm_key} < {c.go[c.right_id]} {orderBy} LIMIT {c.row_per_page}'
                    myinput = str(c.go[c.right_id])
                else:
                    # condition = f'o_status_id = 0 LIMIT {row_per_page}'
                    condition = f' {where_clause} AND {prm_key} <= {max_id[0]["max_id"]} {orderBy} LIMIT {c.row_per_page}'
                    myinput = str(0)
            else:
                # p('inside last else   ', 'go_id[0]:', go_id[0], 'go_id[1]:', go_id[1], 'myinput:', myinput)
                myinput = str(myinput)
                if re.match('^([0-9]+)$', myinput):
                    myinput = int(myinput)
                    condition = f' {where_clause} AND {prm_key} <= {myinput} {orderBy} LIMIT {c.row_per_page}'
                    myinput = str(myinput)
                else:
                    myinput = max_id[0]["max_id"]
                    condition = f' {where_clause} AND {prm_key} <= {max_id[0]["max_id"]} {orderBy} LIMIT {c.row_per_page}'
                    myinput = str(myinput)
            # p('before re.match inside list_items  ', 'go_id[0]:', go_id[0], 'go_id[1]:', go_id[1], 'myinput:', myinput)
            myinput = str(myinput)        
            if re.match('^([0-9]+)$', myinput):
                myinput = int(myinput)
                
                if (c.go[c.left_id] > 0 or c.go[c.right_id] > 0) and  myinput == 0: # Menually enter 0 will go to last page
                    condition = f' {where_clause} AND {prm_key} > 0 order by {prm_key} ASC LIMIT {(c.row_per_page)+1}'
                    cursor.execute(f'SELECT * FROM {menu_name} WHERE {condition} ')
                    rows = cursor.fetchall()
                    rows[-1][prm_key]
                    condition = f' {where_clause} AND {prm_key} < {rows[-1][prm_key]} order by {prm_key} DESC LIMIT {(c.row_per_page)}'
                    
                # p(condition)
                
                cursor.execute(f'SELECT * FROM {menu_name} WHERE {condition} ')
                rows = cursor.fetchall()
                
                
                # Start Stay at default page if no result found perviously ######################################################
                # print('Just inside Start Stay at default page, len(rows): ', len(rows), 'max_id: ', max_id[0]["max_id"])
                if len(rows) == 0 and max_id[0]["max_id"] > 0:
                    
                    condition = f' {where_clause} AND {prm_key} >= {max_id[0]["max_id"]} order by {prm_key} ASC LIMIT {(c.row_per_page + 1)}'
                    # p(condition)
                    cursor.execute(f'SELECT * FROM {menu_name} WHERE {condition} ')
                    rows = cursor.fetchall()
                    # p('len(rows): ', len(rows))
                    if len(rows) > 0:
                        c.go[c.right_id] = rows[-1][prm_key] 
                        if len(rows) < c.row_per_page + 1:
                            condition = f' {where_clause} AND {prm_key} <= {c.go[c.right_id]} {orderBy} LIMIT {c.row_per_page}'
                        else:
                            condition = f' {where_clause} AND {prm_key} < {c.go[c.right_id]} {orderBy} LIMIT {c.row_per_page}'
                        myinput = str(c.go[c.right_id])
                    else:
                        # condition = f'o_status_id = 0 LIMIT {row_per_page}'
                        condition = f' {where_clause} AND {prm_key} < {c.go[c.right_id]} {orderBy} LIMIT {c.row_per_page}'
                        myinput = str(0)
        
                    # p(condition)
                    cursor.execute(f'SELECT * FROM {menu_name} WHERE {condition} ')
                    rows = cursor.fetchall()
                # End Stay at default page if no result found perviously #########################################################
                
                
                if len(rows) > 0:
                    begin_row = rows[0]
                    final_row = rows[-1]
                    
                    
                    if menu_name == c.orders:
                        for x in range(len(rows)):
                            rows[x][c.products_list] = ast.literal_eval(rows[x][c.products_list]) 
                            rows[x][c.products_list] = [rows[x][c.products_list][i][0] for i in range(len(rows[x][c.products_list]))]
                            # rows[x][products_list][i][0] is prodcut id inside tuple e.g. [(6, "Fisherman's Fish Pie", 7.5), (3, 'Chicken & Mushroom Pie', 5.5)]
                            sql = f'''SELECT c.courier_name, s.o_status FROM orders as o 
                                        LEFT JOIN orders_status as s ON o.o_status_id = s.osid 
                                        LEFT JOIN couriers as c ON o.courier_id = c.cid
                                        WHERE o.oid = {rows[x][c.oid]}'''
                            cursor.execute(sql)
                            res = cursor.fetchall()
                            rows[x][c.courier_name] = res[0][c.courier_name]
                            rows[x][c.o_status] = res[0][c.o_status]
                        
                        
                        
                    for x in range(len(rows)):
                        
                        for item in loop_list:
                            c.show[item].append(str(rows[x][item]))

                    for item in loop_list:
                        c.show[item].append(item)
                    
                    for item in loop_list:
                        c.mx[item] = len(max(list(x for x in c.show[item]), key=len)) + 1 #add 1 spaceing for easing feeling.

                    screen_size = self.get_screen_size()
                    p("")     
                    for x in range(len(rows)):
                        temp = ''
                        header = ''
                        for item in loop_list:
                            if x == 0:
                                header += f'{str(item): <{c.mx[item]}}'
                            temp += f'{str(rows[x][item]): <{c.mx[item]}}'
                        if x == 0:
                            header = f'{c.cc[user_input]}{header}{c.cc["E"]}'
                            p(f'{header: ^{screen_size.columns - 1 + cc_length}}') 
                            
                        if rows[x][loop_list[0]] == int(myinput):
                            temp = f'{c.c3["VIOLETBG"]}{temp}{c.c3["E"]}'
                            p(f'{temp: ^{screen_size.columns - 1 + cc_length}}')
                        else:
                            p(f'{temp: ^{screen_size.columns - 1}}')
                        
                    p("")      
                    pager = f'{c.cc[user_input]}Top Page [T]{c.cc["E"]} | [{begin_row[prm_key]} <<<- {c.cc[user_input]}Previous Page [A]{c.cc["E"]}  {menu_name} ID [{c.c3["BLINK"]}{rows[0][prm_key]}{c.c3["E"]}]  {c.cc[user_input]}[D] Next Page{c.cc["E"]} ->>> {final_row[prm_key]}] | {c.cc[user_input]}[0] Last Page {c.cc["E"]} | [MAX ID: {max_id[0]["max_id"]}] | [{selected_total[0]["selected_total"]} Records]'
                    p(f'{pager:*^{screen_size.columns - 1 + 5 * cc_length}}')
                    p("")
                    c.go[c.right_id] = final_row[prm_key]
                    c.go[c.left_id] = begin_row[prm_key]
                else:
                    c.go[c.right_id] = 0
                    c.go[c.left_id]  = 0

            return [c.go[c.left_id], c.go[c.right_id]]
        else:
            return [0,0]


    def list_options(self, menu_name, user_input):  # Function prints options listing
        cc_length = (len(c.cc[user_input]) + len(c.cc["E"])) 
    
        # check order status
        
        id_number = []
        temp_data = []
        for item in c.data[menu_name]:
            for x, y in item.items():
                id_number.append(x)
                temp_data.append(y)


        search_terms = ''
        cc_length_factor = 0
        
        if len(temp_data) > 0:
            screen_size = self.get_screen_size()
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
                    colour_number = f"{c.cc[user_input]}{id_number[id_loop]}{c.cc['E']}"
                    id_loop += 1
                    colour_string = f"( {colour_number} ){search_terms}: {item_name}"
                    if item_number > len(temp) - loop_times:
                        items_string += f"{item_name: <{pedding_length}}"
                    else:
                        items_string += f"{colour_string: <{pedding_length}}"
                p(f'{items_string: ^{screen_size.columns + display_chunk_size * cc_length}}')   
            p(" ") # For nice looking


            
    def print_menu(self, menu_name, user_input): # Function prints products menu
        self.clear_screen()
        # print(f'user_input: {user_input}') # For debug use
        menu_list = []
        cc_count = []
        opts_list = self.joint_opts_list(menu_name, user_input)

        border = c.border_chr[user_input]
        cc_length = len(c.cc[user_input]) + len(c.cc["E"])

        menu_list.append(f'{border:{c.padding_chr[user_input]}<{c.menu_width +len(border)}}{border}')
        cc_count.append(0)
        for elm in c.menu_header:
            elm = f'{c.cc[user_input]}{elm}{c.cc["E"]}'
            menu_list.append(f'{border}{elm: ^{c.menu_width + cc_length}}{border}')
            cc_count.append(1)
        for elm in c.menu[menu_name][c.body]:
            menu_list.append(f'{border}{elm: ^{c.menu_width}}{border}')
            cc_count.append(0)
        for x, elm in enumerate(opts_list[0]):
            menu_list.append(f'{border}{elm: ^{c.menu_width}}{border}')
            cc_count.append(opts_list[1][x] if opts_list[1][x] > 0 else 0)
        for elm in c.menu[menu_name][c.bottom]:
            menu_list.append(f'{border}{elm: ^{c.menu_width}}{border}')
            cc_count.append(0)
        menu_list.append(f'{border:{c.padding_chr[user_input]}<{c.menu_width +len(border)}}{border}')
        cc_count.append(0)

        op_start_pos = (user_input - 1) * c.op_elems_no
        # print(f'op_start_pos: {op_start_pos}') # For debug use
        digit_print_pos = op_start_pos % c.op_total_ht

        for x in range(len(menu_list)):
            if op_start_pos >= 0 and x in range(digit_print_pos, digit_print_pos + c.op_elems_no):
                menu_list[x] = (menu_list[x] + f'{c.cc[user_input]}{c.op_list[x % c.op_elems_no + op_start_pos]}{c.cc["E"]}')
                cc_count[x] += 1
            else:
                menu_list[x] = (menu_list[x] + f'{c.op_list[-1]}')

        screen_size = self.get_screen_size()
        for x in range(len(menu_list)):
            spacer = cc_count[x] * (cc_length)
            print(f'{menu_list[x]: ^{screen_size.columns + spacer}}')

            
    

    def m_1_opt_1(self, m_name, user_input):
        arr = [0,0]
        myinput = 0
        while True:
            self.print_menu(m_name, user_input)
            arr = self.list_items(m_name, user_input, 1, myinput, arr) 
            myinput = input(f'Enter ID to Search: {c.cc[user_input]}Spacebar to Pass{c.cc["E"]}: ')
            if myinput in c.bypass_list:
                self.print_menu(m_name, 0) # Default menu 
                break
            
    def m_1_opt_2(self, m_name, user_input):
        
        i = c.menu_name.index(m_name)
        while True:
            while True:
                c.v[0] = self.input_filter(f"Enter new {c.ln[i][c.cat]} name: ")
                if c.v[0] == "":
                    break                  
                elif self.check_exist_indb(f'SELECT {c.ln[i][c.col_name]} FROM {c.ln[i][c.cats]} WHERE {c.ln[i][c.col_name]} = "{c.v[0]}" '):
                    p(f"{c.v[0]} already exist, please try again.")
                else:
                    break
            
            while True:
                c.v[1] = self.input_filter(f"Enter {c.ln[i][c.cat]} {c.ln[i][c.price_phone]}  : ")
                if  c.v[1] == "":
                    break
                if i == 1:
                    if re.match('^([0-9]*)(\\.){0,1}([0-9]*)$', c.v[1]): # match 0 or 1 dot in digit string. 
                        c.v[1] = round(float(c.v[1]), 2)
                        break
                    else:
                        p(f"Please enter valid number. ")
                elif i == 2:
                    if len(c.v[1]) != 11:
                        p(f"Please enter valid phone number. ") 
                    elif re.match('^([0-9]+)$', c.v[1]):
                        break
                    else:
                        p(f"Please enter valid phone number. ")              

            if c.v[0] == "" or c.v[1] == "":
                self.print_menu(c.ln[i][c.cats], 0) # Reset to default menu after enter new product name.
                break
            else:
                if i == 1:
                    insert = f"""INSERT INTO {c.ln[i][c.cats]} ({c.ln[i][c.col_name]}, {c.ln[i][c.col_phone_price]}, {c.ln[i][c.col_stock]}) values (%s, %s, %s)"""
                    cursor.execute(insert, (c.v[0], c.v[1], 100)) # product stock defualt value 100                                 
                elif i == 2:
                    insert = f"""INSERT INTO {c.ln[i][c.cats]} ({c.ln[i][c.col_name]}, {c.ln[i][c.col_phone_price]}) values (%s, %s)"""
                    cursor.execute(insert, (c.v[0], c.v[1]))
                mydb.commit()
                insert_id = cursor.lastrowid                          
                self.print_menu(c.ln[i][c.cats], 0) # Reset to default menu after enter new product name.
                self.list_items(c.ln[i][c.cats], user_input, 1, insert_id, [0,0]) 
                p(f"( {c.cc[user_input]}{insert_id}{c.cc['E']} ): {c.v[0]} : added to {c.ln[i][c.cats]} record")
                break

    def m_1_opt_3(self, m_name, user_input):
        i = c.menu_name.index(m_name)
        arr = [0,0]
        myinput = 0
        while True:
            self.print_menu(c.ln[i][c.cats], user_input)
            arr = self.list_items(c.ln[i][c.cats], user_input, 1, myinput, arr) 
            myinput = input(f'Enter ID to Search: {c.cc[user_input]}Spacebar to Pass{c.cc["E"]}: ')
            if myinput in c.bypass_list:
                break
    
        while True:
            index_input = self.input_filter(f"Enter {c.ln[i][c.cat]} ID to update: ")
            if index_input == "":
                self.print_menu(c.ln[i][c.cats], 0) # Reset to default menu after enter to escape
                break
            elif re.match('^([0-9]+)$', index_input):
                index_input = int(index_input)
                
                if self.check_exist_indb(f'SELECT {c.ln[i][c.prm_key]} FROM {c.ln[i][c.cats]} WHERE {c.ln[i][c.prm_key]} = {index_input}'):
                    p(" ") # For nice looking
                    p(f"Edit {c.ln[i][c.cats]} ( {c.cc[user_input]}{index_input}{c.cc['E']} ) ")
                    cursor.execute(f'SELECT * FROM {c.ln[i][c.cats]} WHERE {c.ln[i][c.prm_key]} = {index_input}')  
                    rows = cursor.fetchall()
                    elm_max_length = len(max(list(x for x in rows[0]), key=len))
                    for key, value, in rows[0].items():
                        
                        print(f'{key: <{elm_max_length}} : {value}')
                        
                        if key == c.ln[i][c.col_name]:
                            while True:
                                c.v[0] = self.input_filter(f'{key: <{elm_max_length}} : ')
                                if c.v[0] == "":
                                    break 
                                elif self.check_exist_indb(f'SELECT {c.ln[i][c.prm_key]} FROM {c.ln[i][c.cats]} WHERE {c.ln[i][c.col_name]} = "{c.v[0]}"'):
                                    p(f"{c.v[0]} already exist, please try again.")
                                else:
                                    cursor.execute(f'UPDATE {c.ln[i][c.cats]} SET {c.ln[i][c.col_name]} = "{c.v[0]}" WHERE {c.ln[i][c.prm_key]} = {index_input}') 
                                    mydb.commit() 
                                    break                                      
                        elif key == c.ln[i][c.col_phone_price]:
                            while True:
                                c.v[1] = self.input_filter(f'{key: <{elm_max_length}} : ')
                                if  c.v[1] == "":
                                    break
                                if i == 1:
                                    if re.match('^([0-9]*)(\\.){0,1}([0-9]*)$', c.v[1]): # match 0 or 1 dot in digit string. 
                                        c.v[1] = round(float(c.v[1]), 2)
                                        cursor.execute(f'UPDATE {c.ln[i][c.cats]} SET {c.ln[i][c.col_phone_price]} = {c.v[1]} WHERE {c.ln[i][c.prm_key]} = {index_input}') 
                                        mydb.commit() 
                                        break
                                    else:
                                        p(f"Please enter valid number. ")
                                elif i == 2:
                                    if len(c.v[1]) != 11:
                                        p(f'Please enter valid phone umber.') 
                                    elif re.match('^([0-9]+)$', c.v[1]):
                                        cursor.execute(f'UPDATE {c.ln[i][c.cats]} SET {c.ln[i][c.col_phone_price]} = "{c.v[1]}" WHERE {c.ln[i][c.prm_key]} = {index_input}') 
                                        mydb.commit() 
                                        break
                                    else:
                                        p(f"Please enter valid phone number. ") 
                        elif key == c.ln[i][c.col_stock]:
                            while True:
                                c.v[2] = self.input_filter(f'{key: <{elm_max_length}} : ')
                                if c.v[2] == "":
                                    break 
                                else:
                                    if re.match('^([0-9]+)$', c.v[2]):
                                        cursor.execute(f'UPDATE {c.ln[i][c.cats]} SET {c.ln[i][c.col_stock]} = {c.v[2]} WHERE {c.ln[i][c.prm_key]} = {index_input}') 
                                        mydb.commit() 
                                        break    
                                    else:
                                        p(f"Please enter valid phone number. ")
                            
                    self.print_menu(c.ln[i][c.cats], 0)                    
                    self.list_items(c.ln[i][c.cats], user_input, 1, index_input, [0,0])
                    cursor.execute(f'SELECT * FROM {c.ln[i][c.cats]} WHERE {c.ln[i][c.prm_key]} = {index_input}')  
                    rows = cursor.fetchall()
                    p(f"Successfully updated {c.ln[i][c.cat]} ( {c.cc[user_input]}{index_input}{c.cc['E']} ): {rows[0][c.ln[i][c.col_name]]}")
            break # beak to outer while loop
    
    
    def m_1_opt_4(self, m_name, user_input):
        i = c.menu_name.index(m_name)
        arr = [0,0]
        myinput = 0
        while True:
            self.print_menu(c.ln[i][c.cats], user_input)
            arr = self.list_items(c.ln[i][c.cats], user_input, 1, myinput, arr) 
            myinput = input(f'Enter ID to Search: {c.cc[user_input]}Spacebar to Pass{c.cc["E"]}: ')
            if myinput in c.bypass_list:
                break
        
        while True:
            index_input = self.input_filter(f"Enter {c.ln[i][c.cat]} ID to delete: ")
            if index_input == "":
                self.print_menu(c.ln[i][c.cats], 0) # Reset to default menu after enter to escape
                break
            elif re.match('^([0-9]+)$', index_input):
                index_input = int(index_input)
                if self.check_exist_indb(f'SELECT {c.ln[i][c.prm_key]} FROM {c.ln[i][c.cats]} WHERE {c.ln[i][c.prm_key]} = {index_input}'):
                    p(" ") # For nice looking
                    cursor.execute(f'SELECT * FROM {c.ln[i][c.cats]} WHERE {c.ln[i][c.prm_key]} = {index_input}')  
                    rows = cursor.fetchall()
                    c.v[0] = self.input_filter(f"Delete {c.ln[i][c.cat]} ( {c.cc[user_input]}{index_input}{c.cc['E']} ): {rows[0][c.ln[i][c.col_name]]} \nConfirm delete: y/n? ")
                    if c.v[0] == 'y' or c.v[0].upper() == 'Y':
                        cursor.execute(f'DELETE FROM {c.ln[i][c.cats]} WHERE {c.ln[i][c.prm_key]} = {index_input}') 
                        mydb.commit()
                        self.print_menu(c.ln[i][c.cats], 0)
                        self.list_items(c.ln[i][c.cats], user_input, 1, index_input, [0,0])
                        p(f"Successfully deleted. Previously ( {c.cc[user_input]}{index_input}{c.cc['E']} ): {rows[0][c.ln[i][c.col_name]]}")
                        p(" ") # For nice looking
                        break
                    else:
                        self.print_menu(c.ln[i][c.cats], 0)
                        break
            p("")
            user_input = self.input_option(c.ln[i][c.cats], i)
            if user_input == 0:
                main_input = 0
                break
    
    def m_3_opt_1(self, m_name, user_input):
        orders  = m_name
        
        arr = [0,0]
        myinput = 0
        while True:
            self.print_menu(orders, user_input)
            arr = self.list_items(orders, user_input, 1, myinput, arr) 
            myinput = input(f'Enter ID to Search: {c.cc[user_input]}Spacebar to Pass{c.cc["E"]}: ')
            if myinput in c.bypass_list:
                break

        while True:
            cursor.execute(f'SELECT * FROM orders_status WHERE 1')  
            rows = cursor.fetchall()
            # print(rows)
            status_list=''
            for row in rows:
                status_list += f"[{c.cc[user_input]}{row[c.osid]}{c.cc['E']}] {row[c.o_status]}, "
            p(status_list.rstrip(', '))
            p(" ") # For nice looking

            status_input = self.input_filter(f"Choose status number [ ]: ")
            if status_input == "":
                break
            elif re.match('^([0-9]+)$', status_input):
                status_input = int(status_input)
                if True in set(str(status_input) in str(dic[c.osid]) for dic in rows):
                    arr = [0,0]
                    myinput = 0
                    while True:
                        self.print_menu(orders, user_input)
                        where_clause = f'{c.o_status_id} = {status_input}'
                        arr = self.list_items(orders, user_input, where_clause, myinput, arr) 
                        myinput = input(f'Enter ID to Search: {c.cc[user_input]}Spacebar to Pass{c.cc["E"]}: ')
                        if myinput in c.bypass_list:
                            break

        while True:
            cursor.execute(f'SELECT * FROM couriers WHERE 1')  
            rows = cursor.fetchall()
            p("")
            couriers_list=''
            for row in rows:
                couriers_list += f"[{c.cc[user_input]}{row[c.cid]}{c.cc['E']}] {row[c.courier_name]}, "
            p(couriers_list.rstrip(', '))
            p(" ") # For nice looking
            get_input = self.input_filter(f"Choose courier number [ ]: ")
            p("")                        
            if get_input == "":
                
                break
            elif re.match('^([0-9]+)$', get_input):
                get_input = int(get_input)
                if True in set(str(get_input) in str(dic[c.cid]) for dic in rows):
                    self.print_menu(orders, user_input)
                    arr = [0,0]
                    myinput = 0
                    while True:
                        self.print_menu(orders, user_input)
                        where_clause = f'{c.courier_id} = {get_input}'
                        arr = self.list_items(orders, user_input, where_clause, myinput, arr) 
                        myinput = input(f'Enter ID to Search: {c.cc[user_input]}Spacebar to Pass{c.cc["E"]}: ')
                        if myinput in c.bypass_list:
                            break
                    
        self.print_menu(orders, 0)

                    
    def m_3_opt_2(self, m_name, user_input):
        
        orders = m_name
        
        self.print_menu(orders, user_input)
        p(" ") # For nice looking
        while True:
            cust_name = self.input_filter("Enter new order customer name: ")
            cust_address = self.input_filter("Enter new order customer address: ")
            while True:
                cust_phone = self.input_filter("Enter new order customer phone: ")
                if cust_phone != '' and len(cust_phone) != 11:
                    p(f'Please enter valid phone umber.')                
                elif re.match('^([0-9]+)$', cust_phone) or cust_phone == '':
                    break
                else:
                    p(f'Please enter valid phone umber.')                    
            if cust_name == "" or cust_address == "" or cust_phone == "":
                self.print_menu(orders, 0) # Reset to default menu after no input.
                break
            else:
                cursor.execute(f'SELECT pid, product_name, product_price FROM products WHERE 1')  
                rows = cursor.fetchall()
                c.data[c.products_name_list] = [{dic[c.pid]:  f'{dic[c.product_name]} £{dic[c.product_price]}'}for dic in rows]
                pid_list = [dic[c.pid] for dic in rows]
                price_list = [dic[c.product_price] for dic in rows]


                p("Products items choices: ")
                self.list_options(c.products_name_list, user_input)
                item_string = ''
                item_list =[]
                total_price = 0
                while True:
                    
                    bypass_input = input(f"( {c.cc[user_input]}{item_string[:-2]}{c.cc['E']} ) {c.cc[user_input]}£{round(total_price, 2)}{c.cc['E']}: Choose number, e/E Esacpe, {c.cc[user_input]}Spacebar to Confirm{c.cc['E']}: ")
                    
                    input_order = re.sub(' +', ' ', bypass_input.strip())
                    
                    if input_order == "e":
                        self.print_menu(orders, 0) # Reset to default menu after escape
                        break
                    elif bypass_input in c.bypass_list:
                        break
                    elif re.match('^([0-9]+)$', input_order):
                        input_order = int(input_order)
                        if True in set(str(input_order) in str(dic[c.pid]) for dic in rows):
                            total_price += price_list[pid_list.index(input_order)]
                            item_string += f'{input_order}, '
                            item_list.append(input_order)
                if input_order != 'E' and input_order != 'e':
                    cursor.execute(f'SELECT cid, courier_name, courier_phone FROM couriers WHERE 1')  
                    rows = cursor.fetchall()
                    c.data[c.couriers_name_list] = [{dic[c.cid]: f'{dic[c.courier_name]} - {dic[c.courier_phone]}'} for dic in rows]
                    p("Courier choices: ")
                    self.list_options(c.couriers_name_list, user_input)
                    while True:
                        courier_input = self.input_filter(f"Choose courier number (   ): Enter e/E to esacpe: ")
                        p("")
                        if courier_input == "e":
                            self.print_menu(orders, 0) # Reset to default menu after escape
                            break
                        elif re.match('^([0-9]+)$', courier_input):
                            courier_input = int(courier_input)
                            if True in set(str(courier_input) in str(dic[c.cid]) for dic in rows):
                                pdt_list = []
                                for item in item_list:
                                    cursor.execute(f'SELECT pid, product_name, product_price FROM products WHERE pid = {item}')
                                    rows = cursor.fetchall()
                                    pdt_list.append(rows[0])
                                    
                                products_tuple =[ (x[1], y[1], z[1]) for x, y, z in (dic.items() for dic in pdt_list)]
                                products_string = str(products_tuple)
                                insert = f"""INSERT INTO orders (customer_name, customer_address, customer_phone, products_list, order_total, courier_id, o_status_id, unixtime, date) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                                
                                cursor.execute(insert, (cust_name, cust_address, cust_phone, products_string, total_price, courier_input, 1, self.dateTimeToUnix(), self.dateTimeNow()))
                                mydb.commit()  
                                last_oid = cursor.lastrowid
                        
                                for dic in pdt_list:
                                    insert = f"""INSERT INTO orders_to_pdts (oid, pid, product_name, product_price, unixtime, date) values (%s, %s, %s, %s, %s, %s)"""
                                    cursor.execute(insert, (last_oid, dic[c.pid], dic[c.product_name], dic[c.product_price], self.dateTimeToUnix(), self.dateTimeNow()))
                                    mydb.commit() 
                
                                self.print_menu(orders, 0) # Reset to default menu after adding order
                                self.list_items(orders, user_input, 1, last_oid, [0,0])
                                p(f"Added new order ( {c.cc[user_input]}{last_oid}{c.cc['E']} ): ")
                                break                                    
            break # break the outer while loop       
    def m_3_opt_3(self, m_name, user_input):
        orders = m_name
        arr = [0,0]
        myinput = 0
        while True:
            self.print_menu(orders, user_input)
            arr = self.list_items(orders, user_input, 1, myinput, arr) 
            myinput = input(f'Enter ID to Search: {c.cc[user_input]}Spacebar to Pass{c.cc["E"]}: ')
            if myinput in c.bypass_list:
                break
        while True:
            index_input = self.input_filter("Enter order (  ) to update: ")
            if index_input == "":
                self.print_menu(orders, 0) # Reset to default menu after enter to escape
                break
            elif re.match('^([0-9]+)$', index_input):
                index_input = int(index_input)
                if self.check_exist_indb(f'SELECT oid FROM orders WHERE oid = {index_input}'):
                    cursor.execute(f'SELECT s.o_status, o.* FROM orders as o INNER JOIN orders_status as s ON o.o_status_id = s.osid WHERE o.oid = {index_input}')  
                    order_rows = cursor.fetchall()
                    p(" ") # For nice looking
                    p(f"Order ( {index_input} ) status: [{order_rows[0][c.o_status_id]}] {order_rows[0][c.o_status]}")
                    
                    cursor.execute(f'SELECT * FROM orders_status WHERE 1')  
                    status_rows = cursor.fetchall()
                    osid_list = [dic["osid"] for dic in status_rows]
                    o_status_list = [dic["o_status"] for dic in status_rows]
                    # p(osid_list)
                    # p(o_status_list)
                    p(" ") # For nice looking
                    status_list="Status choices: "
                    for row in status_rows:
                        status_list += f"[{c.cc[user_input]}{row[c.osid]}{c.cc['E']}] {row[c.o_status]}, "
                    p(status_list.rstrip(', '))
                    p(" ") # For nice looking

                    while True:
                        edit_order = self.input_filter(f"Choose status number [ ]: ")
                        if edit_order == "":
                            self.print_menu(orders, 0) # Reset to default menu after edit orders name
                            break
                        elif re.match('^([0-9]+)$', edit_order):
                            edit_order = int(edit_order)
                            if self.check_exist_indb(f'SELECT osid FROM orders_status WHERE osid = {edit_order}'):
                                cursor.execute(f'UPDATE orders SET o_status_id = {edit_order} WHERE oid = {index_input}') 
                                mydb.commit() 
                                self.print_menu(orders, 0) # Reset to default menu after edit orders name
                                self.list_items(orders, user_input, 1, index_input, [0,0])
                                p(f"Successfully updated. Order ( {c.cc[user_input]}{index_input}{c.cc['E']} ) status: {edit_order} - {o_status_list[osid_list.index(edit_order)]}")
                                break
                    break # break the outer while loop
    def m_3_opt_4(self, m_name, user_input):
        orders = m_name
        arr = [0,0]
        myinput = 0
        while True:
            self.print_menu(orders, user_input)
            arr = self.list_items(orders, user_input, 1, myinput, arr) 
            myinput = input(f'Enter ID to Search: {c.cc[user_input]}Spacebar to Pass{c.cc["E"]}: ')
            if myinput in c.bypass_list:
                break                    
        while True:
            index_input = self.input_filter("Enter order (  ) to update: ")
            if index_input == "":
                self.print_menu(orders, 0) # Reset to default menu after enter to escape
                break
            elif re.match('^([0-9]+)$', index_input):
                index_input = int(index_input)
                if self.check_exist_indb(f'SELECT oid FROM orders WHERE oid = {index_input}'):
                    sql = f'''SELECT c.courier_name, c.courier_phone, s.o_status, o.* FROM orders as o 
                                LEFT JOIN orders_status as s ON o.o_status_id = s.osid 
                                LEFT JOIN couriers as c ON o.courier_id = c.cid
                                WHERE o.oid = {index_input}'''
                    cursor.execute(sql)  
                    order_rows = cursor.fetchall()
                    order_rows[0]["products_list"] = ast.literal_eval(order_rows[0]["products_list"])                                
                    # column_name_list = [key for key, value in rows[0].items()]
                    p(" ") # For nice looking
                    p(f"Edit order ( {c.cc[user_input]}{index_input}{c.cc['E']} ) ")
                    update_column_list = ['customer_name', 'customer_address', 'customer_phone', 'products_list', 'courier_id', 'o_status_id']
                    elm_max_length = len(max(update_column_list, key=len))
                    
                    for x in update_column_list:
                        if x == c.customer_name or x == c.customer_address or x == c.customer_phone:
                            p(f'{x: <{elm_max_length}} : {order_rows[0][x]}')
                            if x == c.customer_phone:
                                while True:
                                    edit_order = self.input_filter(f'{x: <{elm_max_length}} : ')
                                    if edit_order != '' and len(edit_order) != 11:
                                        p(f'Please enter valid phone umber.') 
                                    elif re.match('^([0-9]+)$', edit_order) or edit_order == '':
                                            break
                                    else:
                                        p(f'Please enter valid phone umber.') 
                            else:
                                edit_order = self.input_filter(f'{x: <{elm_max_length}} : ')
                                
                            if edit_order != "":
                                cursor.execute(f'UPDATE orders SET {x} = "{edit_order}" WHERE oid = {index_input}') 
                                mydb.commit() 

                        elif x == c.products_list:
                            p(" ")
                            
                            order_pid_list = [x[0] for x in order_rows[0][c.products_list]]
                            p(f'{x: <{elm_max_length}} : {order_pid_list}')
                            cursor.execute(f'SELECT pid, product_name, product_price FROM products WHERE 1')  
                            rows = cursor.fetchall()
                            c.data[c.products_name_list] = [{dic[c.pid]:  f'{dic[c.product_name]} £{dic[c.product_price]}'}for dic in rows]
                            pid_list = [dic[c.pid] for dic in rows]
                            price_list = [dic[c.product_price] for dic in rows]
                            self.list_options(c.products_name_list, user_input)
                            item_string = ''
                            item_list = []
                            total_price = 0
                            escape_outer = False
                            while True:
                                
                                bypass_input = input(f"( {c.cc[user_input]}{item_string[:-2]}{c.cc['E']} ) {c.cc[user_input]}£{round(total_price, 2)}{c.cc['E']}: Choose number, e/E Esacpe, {c.cc[user_input]}Spacebar to Confirm{c.cc['E']}: ")
                                
                                input_order = re.sub(' +', ' ', bypass_input.strip())
                                
                                if input_order == "e":
                                    escape_outer = True
                                    break
                                elif bypass_input in c.bypass_list:
                                    if len(item_list) > 0:
                                        pdt_list = []
                                        for item in item_list:
                                            cursor.execute(f'SELECT pid, product_name, product_price FROM products WHERE pid = {item}')
                                            rows = cursor.fetchall()
                                            pdt_list.append(rows[0])   
                                        products_tuple =[ (x[1], y[1], z[1]) for x, y, z in (dic.items() for dic in pdt_list)]
                                        products_string = str(products_tuple)
                                        products_string = products_string.replace("'", r"\'")
                                        products_string = products_string.replace('"', r'\"')                                        
                                        cursor.execute(f'UPDATE orders SET products_list = "{products_string}",  order_total = {total_price} WHERE oid = {index_input}') 
                                        mydb.commit()
                                        cursor.execute(f'DELETE FROM orders_to_pdts WHERE oid = {index_input}')
                                        mydb.commit()
                                        for dic in pdt_list:
                                            insert = f"""INSERT INTO orders_to_pdts (oid, pid, product_name, product_price, unixtime, date) values (%s, %s, %s, %s, %s, %s)"""
                                            cursor.execute(insert, (index_input, dic[c.pid], dic[c.product_name], dic[c.product_price], self.dateTimeToUnix(), self.dateTimeNow()))
                                            mydb.commit()
                                                
                                    break
                                
                                elif re.match('^([0-9]+)$', input_order):
                                    input_order = int(input_order)
                                    if True in set(str(input_order) in str(dic[c.pid]) for dic in rows):
                                        total_price += price_list[pid_list.index(input_order)]
                                        item_string += f'{input_order}, '
                                        item_list.append(input_order)
                            
                            if escape_outer == True:
                                break # break the outer while loop           
                            
                        elif x == c.courier_id:
                            p(" ")                                       
                            cursor.execute(f'SELECT cid, courier_name, courier_phone FROM couriers WHERE 1')  
                            rows = cursor.fetchall()
                            c.data[c.couriers_name_list] = [{dic[c.cid]: f'{dic[c.courier_name]} - {dic[c.courier_phone]}'} for dic in rows]
                            p(f'{x: <{elm_max_length}} : ( {order_rows[0][c.courier_id]} ): {order_rows[0][c.courier_name]} - {order_rows[0][c.courier_phone]}')
                            self.list_options(c.couriers_name_list, user_input)

                            while True:
                                edit_order = self.input_filter(f"Choose courier number (   ): ")
                                p("")
                                if edit_order == "":
                                    break
                                elif re.match('^([0-9]+)$', edit_order):
                                    edit_order = int(edit_order)
                                    if True in set(str(edit_order) in str(dic[c.cid]) for dic in rows):  
                                        cursor.execute(f'UPDATE orders SET courier_id = {edit_order} WHERE oid = {index_input}') 
                                        mydb.commit()
                                        break
                        
                        elif x == c.o_status_id:
                            cursor.execute(f'SELECT * FROM orders_status WHERE 1')  
                            rows = cursor.fetchall()
                            c.data[c.order_status_list] = [{dic[c.osid]: f'{dic[c.o_status]}'} for dic in rows]
                            p(f'{x: <{elm_max_length}} : ( {order_rows[0][c.o_status_id]} ): {order_rows[0][c.o_status]}')
                            self.list_options(c.order_status_list, user_input)  
                            while True:
                                edit_order = self.input_filter(f"Choose status number (  ): ")
                                if edit_order == "":
                                    break
                                elif re.match('^([0-9]+)$', edit_order):
                                    edit_order = int(edit_order)
                                    if True in set(str(edit_order) in str(dic[c.osid]) for dic in rows):
                                        cursor.execute(f'UPDATE orders SET o_status_id = {edit_order} WHERE oid = {index_input}') 
                                        mydb.commit()
                                        break

                    self.print_menu(orders, 0) # Reset to default menu after edit orders name
                    self.list_items(orders, user_input, 1, index_input, [0,0])
                    p(f"Updated order ( {c.cc[user_input]}{index_input}{c.cc['E']} ):")                            
                    break # break the outer while loop

    def m_3_opt_5(self, m_name, user_input):
        p('m_3_opt_5')
        pass
    
    def m_4_opt_1(self, m_name, user_input):
        
        reports = m_name
        
        past_month_num_orders = []
        for i in range(len(c.months_inv)):
            sql = f'''SELECT COUNT(oid) as res FROM orders WHERE date > DATE("{c.months_inv[i][0]}") AND date < DATE("{c.months_inv[i][1]}")'''
            cursor.execute(sql)
            num_of_orders = cursor.fetchall()
            past_month_num_orders.append(num_of_orders[0]["res"])
        # p(past_month_num_orders)


        graph_title = 'Pop Up Cafe Monthly Orders'
        grapg_label = 'Order Numbers'

        x_pos = np.arange(len(c.months_name))
        fig, ax = plt.subplots()
        ax.bar(x_pos, past_month_num_orders, align='center', alpha=0.5)
        ax.set_ylabel(grapg_label)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(c.months_name)
        ax.set_title(graph_title)
        ax.yaxis.grid(True)
        plt.tight_layout()
        plt.show()

        self.print_menu(reports, 0) # Default menu 

    def m_4_opt_2(self, m_name, user_input):
        reports = m_name
        past_month_result = []
        for i in range(len(c.months_inv)):
            sql = f'''SELECT SUM(order_total) as res FROM orders WHERE date > DATE("{c.months_inv[i][0]}") AND date < DATE("{c.months_inv[i][1]}")'''
            cursor.execute(sql)
            result = cursor.fetchall()
            past_month_result.append(result[0]["res"])
        # p(past_month_result)


        graph_title = 'Pop Up Cafe Monthly Sales £'
        grapg_label = 'Order Sales £'

        x_pos = np.arange(len(c.months_name))
        fig, ax = plt.subplots()
        ax.bar(x_pos, past_month_result, align='center', alpha=0.5)
        ax.set_ylabel(grapg_label)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(c.months_name)
        ax.set_title(graph_title)
        ax.yaxis.grid(True)
        plt.tight_layout()
        plt.show()

        self.print_menu(reports, 0) # Default menu 
        
        
    def m_4_opt_3(self, m_name, user_input):
        p('m_4_opt_3')
        pass
    def m_4_opt_4(self, m_name, user_input):
        p('m_4_opt_4')
        pass

           
    def menu_option_selected(self, m_name, user_input):
        
        c.menu_name = list(c.menu.keys())
        
        func_name = {
            c.menu_name[1]: ['', self.m_1_opt_1, self.m_1_opt_2, self.m_1_opt_3, self.m_1_opt_4],
            c.menu_name[2]: ['', self.m_1_opt_1, self.m_1_opt_2, self.m_1_opt_3, self.m_1_opt_4], # c.menu_name[1] and c.menu_name[2] share same function
            c.menu_name[3]: ['', self.m_3_opt_1, self.m_3_opt_2, self.m_3_opt_3, self.m_3_opt_4, self.m_1_opt_4],
            c.menu_name[4]: ['', self.m_4_opt_1, self.m_4_opt_2, self.m_4_opt_3, self.m_1_opt_4],
        }
        
        if m_name in func_name and user_input > 0:
            func_name[m_name][user_input](m_name, user_input)
        

    
    
def main():
    
    m = MethodClass()
        
    menu_index = 0
    user_input = 0
    display_path = c.menu_name[0]
    while True:
        
        m.print_menu(c.menu_name[menu_index], user_input)

        m.menu_option_selected(c.menu_name[menu_index], user_input)
        
        user_input = input(f'{c.c2[0]} {display_path} {c.c2["E"]} Enter option in square brackets [  ]: ')
        

        if re.match('^([0-9]+)$', user_input):
            user_input = int(user_input)
    
            if menu_index >= len(c.menu[c.main][c.options]):
                menu_index = 0
            
            elif user_input >= len(c.menu[c.menu_name[menu_index]][c.options]):
                user_input = 0

            elif menu_index == 0 and user_input == 0:
                os.system("cls")
                break
            elif menu_index == 0 and user_input > 0:
                display_path = f'{c.menu_name[0]} > {c.menu_name[user_input]}'
                menu_index = user_input
                user_input = 0
            elif menu_index > 0 and user_input > 0:
                display_path = f'{c.menu_name[0]} > {c.menu_name[menu_index]}'          
            elif menu_index > 0 and user_input == 0:
                display_path = f'{c.menu_name[0]}' 
                menu_index = 0
            else:
                display_path = f'{c.menu_name[0]}'
                menu_index = 0  
                user_input = 0
        else:
            display_path = f'{c.menu_name[0]}' 
            user_input = 0
        

if __name__ == "__main__":
    c = Container()
    main()

        