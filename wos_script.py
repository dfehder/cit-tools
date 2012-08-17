import wosAPI, time, random, logging
from BeautifulSoup import BeautifulStoneSoup
from xls_util import xlsList


"""

1. Error Logging Configuration

""" 

#logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('wosAPI.script')
logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.INFO)

# create file handler which logs even debug messages
fh = logging.FileHandler('/home/dcfehder/Dropbox/projects/cit-tools/wosAPI2.log')
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


"""

2. Run searches from xls file

""" 



docpath = "/home/dcfehder/Dropbox/projects/cit-tools/docs/ohchan-pubquery-3.xls"
alist = xlsList(docpath, "wosSearch")
#Since there is only one column of data, it will be in the second place in the list
wosSearches = alist[1]
wosSearchesSub = random.sample(wosSearches,900)

#now run the searches
#conn_path = '/home/dcfehder/dev/WoS.db'
conn_path = '/home/dcfehder/Dropbox/projects/cit-tools/WoS-MITFac.db'
outcome = wosAPI.search(wosSearchesSub, conn_path, 0.632, 20000)
logger.info(outcome)

"""

3. Log added rows of data

""" 



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






