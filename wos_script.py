import wosAPI, time
from BeautifulSoup import BeautifulStoneSoup
from xls_util import xlsList


docpath = "/home/dcfehder/Dropbox/projects/cit-tools/search_template.xls"
alist = xlsList(docpath, "wosSearch")
#Since there is only one column of data, it will be in the second place in the list
wosSearches = alist[1]


#now run the searches
conn_path = '/home/dcfehder/Dropbox/projects/cit-tools/WoS.db'

outcome = wosAPI.search(wosSearches, conn_path)


muid = '000084170700023'
muid2 = '000084170700024'
muid3 = '000165188900010'
url = "http://search.isiknowledge.com/esti/wokmws/ws/WOKMWSAuthenticate?wsdl"


a = wosAPI.wos_auth(url, 1)
aa, bb, cc, dd, ee = wosAPI.utIter(muid3, '2012-08-09')


b = wosAPI.wos_UID(muid2, '2012-07-12', a)



arts = wosAPI.shortExtract(b)
uts = wosAPI.utExtract(b)
mm = wosAPI.listString(uts, ";")



#now to test the above function


print outcome




