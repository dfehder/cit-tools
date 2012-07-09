import wosServ_suds, time

#searcher = "AU = Murray F AND AD = MIT"
#b = wosServ_suds.wos_search(searcher)

url = "http://search.isiknowledge.com/esti/wokmws/ws/WOKMWSAuthenticate?wsdl"
a = wosServ_suds.wos_auth(url, 1)

print a


time.sleep(1)

muid = '000084170700023'
b = wosServ_suds.wos_UID(muid, 'SCI', '2012-05-16', a)

#print b['recordsFound']

#author = b['records'][0]['authors'][0]['values']
#print author
#print b
