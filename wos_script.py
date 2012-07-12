import wosServ_suds, time
from BeautifulSoup import BeautifulStoneSoup

#searcher = "AU = Murray F AND AD = MIT"
#b = wosServ_suds.wos_search(searcher)

url = "http://search.isiknowledge.com/esti/wokmws/ws/WOKMWSAuthenticate?wsdl"
a = wosServ_suds.wos_auth(url, 1)

print a


time.sleep(2)

muid = '000084170700023'
b = wosServ_suds.wos_UID(muid, 'SCI', '2012-05-16', a)

arts = wosServ_suds.shortExtract(b)
uts = wosServ_suds.utExtract(b)

#note that the WoS api bugs out whenever there are @ symbols in the SID, so you will need to fix that (like don't look up anything with that SID)

