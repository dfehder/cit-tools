import wosServ_suds, time
from BeautifulSoup import BeautifulStoneSoup

#searcher = "AU = Murray F AND AD = MIT"
#b = wosServ_suds.wos_search(searcher)




print a



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
aa, bb, cc, dd, ee = wosServ_suds.searchIter(se, '2012-08-08')

conn_path = '/home/dcfehder/Dropbox/projects/cit-tools/WoS.db'
f = wosServ_suds.artsDB(aa, conn_path)


outcome = wosServ_suds.search(["AU = Langer R* AND OG = MIT"], conn_path)

print outcome




