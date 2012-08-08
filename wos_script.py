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
conn_path = '/home/dcfehder/Dropbox/projects/cit-tools/WoS.db'

outcome = wosServ_suds.artsDB(arts, conn_path)

print outcome


#note that the WoS api bugs out whenever there are @ symbols in the SID, so you will need to fix that (like don't look up anything with that SID)


#this tests out the search option
se = "AU = Langer R* AND OG = MIT"
se = "AU = Murray F* AND OG = MIT"

#aa is the arts dict, bb is the uts, cc is qid, dd is recs, ee is a
aa, bb, cc, dd, ee = wosServ_suds.searchIter(se, '2012-07-12')

#now try the
srt = 1101
ff = wosServ_suds.wos_retrieve(cc, srt, ee)
uts1 = wosServ_suds.utExtract(ff)
arts1 = wosServ_suds.shortExtract(ff)

inter = range(101,dd,100)


