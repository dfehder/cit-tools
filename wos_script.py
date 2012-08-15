import wosAPI, time, random
from BeautifulSoup import BeautifulStoneSoup
from xls_util import xlsList


docpath = "/home/dcfehder/Dropbox/projects/cit-tools/docs/ohchan-pubquery-3.xls"
alist = xlsList(docpath, "wosSearch")
#Since there is only one column of data, it will be in the second place in the list
wosSearches = alist[1]
wosSearchesSub = random.sample(wosSearches,5)

#now run the searches
#conn_path = '/home/dcfehder/dev/WoS.db'
conn_path = '/home/dcfehder/Dropbox/projects/cit-tools/WoS-MITFac.db'
outcome = wosAPI.search(wosSearchesSub, conn_path, 8)

#now populate the utRegister table
wosAPI.utRegPop(conn_path)
wosAPI.utRegCheck(conn_path, "article_short")
wosAPI.utRegCheck(conn_path, "citedBy")

#now generate a list of articles that are missing citedBy entries
#utList = wosAPI.utListGen(conn_path)
#utListShort = random.sample(utList,3)

#result = wosAPI.citedBy(utList, conn_path)
#wosAPI.utRegCheck(conn_path, "citedBy")



"""
Everything below is test-bed for making sure evryting works
"""






