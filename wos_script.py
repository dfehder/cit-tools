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
b = wosServ_suds.wos_UID(muid2, 'SCI', '2012-07-12', a)

arts = wosServ_suds.shortExtract(b)
uts = wosServ_suds.utExtract(b)


#now to test the above function


print outcome


#note that the WoS api bugs out whenever there are @ symbols in the SID, so you will need to fix that (like don't look up anything with that SID)


#this tests out the search option
se = "AU = Langer R* AND OG = MIT"
se = "AU = Murray F* AND OG = MIT"

#aa is the arts dict, bb is the uts, cc is qid, dd is recs, ee is a
aa, bb, cc, dd, ee = wosAPI.searchIter(se, '2012-08-08')

conn_path = '/home/dcfehder/Dropbox/projects/cit-tools/WoS.db'
f = wosAPI.artsDB(aa, conn_path)


outcome = wosAPI.search(["AU = Langer R* AND OG = MIT"], conn_path)

print outcome


result = wosAPI.wosSearchDB("AU = Murray F* AND OG = MIT", bb, conn_path)


testy = ["AU = Azoulay P* AND OG = MIT AND PY = 2011", "AU = Utterback J* AND OG = MIT AND PY = 1997"]

conn_path = '/home/dcfehder/Dropbox/projects/cit-tools/WoS.db'

outcome = wosAPI.search(testy, conn_path)



