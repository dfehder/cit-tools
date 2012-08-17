#Author: Daniel Fehder
# Last modified: 8/15/2012
# Purpose: to provide a suds client to ISI Web of Science Lite web services
import suds,logging, time, sqlite3
from BeautifulSoup import BeautifulStoneSoup


"""

1. Error Logging Configuration

""" 

#logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('suds.client')
logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.INFO)

# create file handler which logs even debug messages
fh = logging.FileHandler('/home/dcfehder/Dropbox/projects/cit-tools/wosAPI.log')
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

2. SOAP functions for direct interaction with API

"""



#this establishes the auth
def wos_auth(auth_url, proxy):
    w = 0
    while w < 1:
        client = suds.client.Client(auth_url)
        session_id =  client.service.authenticate()
        session_id  = str(session_id)

        if session_id.find("@") < 0:
            w = 2
        else:
            pass

        time.sleep(1)
            

    return session_id



def wos_search(search_text, endDate, a):
    serv_url = "http://search.isiknowledge.com/esti/wokmws/ws/WokSearchLite?wsdl"
        
    #now try to ping the main service server
    try:
        search_client = suds.client.Client(serv_url)
        #set the required headers for the http
        search_client.set_options(headers={'content-type':'text/xml; charset=utf-8'})
        search_client.set_options(headers={'Cookie':'SID=%s'%a})
        #to get xml
        search_client.set_options(retxml=bool(1))
    except:
        return "wos_search ERROR: CONNECTION ERROR"

    #now create the search request object
    try:
        qp = search_client.factory.create('queryParameters')
        #now populate it with the data
        qp.userQuery = search_text
        qp.databaseID = "WOS"
        qp.queryLanguage = "en"

        #now create the 
        ed1 = search_client.factory.create('queryParameters.editions')
        ed2 = search_client.factory.create('queryParameters.editions')
        ed3 = search_client.factory.create('queryParameters.editions')
        ed4 = search_client.factory.create('queryParameters.editions')
        ed5 = search_client.factory.create('queryParameters.editions')
        ed6 = search_client.factory.create('queryParameters.editions')
        ed7 = search_client.factory.create('queryParameters.editions')

        ed1.collection = 'WOS'
        ed1.edition = 'SSCI'

        ed2.collection = 'WOS'
        ed2.edition = 'SCI'

        ed3.collection = 'WOS'
        ed3.edition = 'AHCI'

        ed4.collection = 'WOS'
        ed4.edition = 'IC'

        ed5.collection = 'WOS'
        ed5.edition = 'CCR'

        ed6.collection = 'WOS'
        ed6.edition = 'ISTP'

        ed7.collection = 'WOS'
        ed7.edition = 'ISSHP'

        qp.editions = [ed1, ed2, ed3, ed6, ed7]

        ts = search_client.factory.create('timeSpan')
        ts.begin = '1900-01-01'
        ts.end = endDate
        qp.timeSpan = ts
        

    except:
        return "wosServ ERROR: Search request object error"

    try:
        #now create the return parameters object I will eventually want to add to the results if it is over 100
        rt = search_client.factory.create('retrieveParameters')
        rt.count = 100
        rt.firstRecord = 1
    except:
        return "wosServ ERROR: response request object error"

    try:
        #this is the actual request to the server
        res =  search_client.service.search(queryParameters= qp, retrieveParameters = rt)
        
    except:
        return "wosServ ERROR: request error"

    return res


def wos_UID(muid, endDate, a):
    url = "http://search.isiknowledge.com/esti/wokmws/ws/WOKMWSAuthenticate?wsdl"
    serv_url = "http://search.isiknowledge.com/esti/wokmws/ws/WokSearchLite?wsdl"
    
    #a = wos_auth(url, 1)
    time.sleep(1)

    #now try to ping the main service server
    try:
        search_client = suds.client.Client(serv_url)
        #set the required headers for the http
        search_client.set_options(headers={'content-type':'text/xml; charset=utf-8'})
        search_client.set_options(headers={'Cookie':'SID=%s'%a})

        #this is to select the return value as a xml doc
        search_client.set_options(retxml=bool(1))
    except:
        return "wos_search ERROR: CONNECTION ERROR"

    #now create the search request object
    try:
        
        #now create the editions
        ed1 = search_client.factory.create('editionDesc')
        ed1.collection = 'WOS'
        ed1.edition = 'SCI'
        
        ed2 = search_client.factory.create('editionDesc')
        ed2.collection = 'WOS'
        ed2.edition = 'SSCI'

        ed3 = search_client.factory.create('editionDesc')
        ed3.collection = 'WOS'
        ed3.edition = 'AHCI'

        ed4 = search_client.factory.create('editionDesc')
        ed4.collection = 'WOS'
        ed4.edition = 'ISTP'

        ed5 = search_client.factory.create('editionDesc')
        ed5.collection = 'WOS'
        ed5.edition = 'ISSHP'
        

        eds = [ed1, ed2, ed3, ed4, ed5]

        ts = search_client.factory.create('timeSpan')
        ts.begin = '1900-01-01'
        ts.end = endDate

        

    except:
        return "wosServ ERROR: Search request object error"

    try:
        #now create the return parameters object I will eventually want to add to the results if it is over 100
        rt = search_client.factory.create('retrieveParameters')
        rt.count = 100
        rt.firstRecord = 1
    except:
        return "wosServ ERROR: response request object error"

    try:
        #this is the actual request to the server
        woos = "WOS"
        res =  search_client.service.citingArticles(databaseId = woos, uid = muid, editionDesc = eds, timeSpan = ts, queryLanguage = 'en', retrieveParameters = rt)
        #bb =  search_client.last_sent()
        #print bb
        
    except:
        return "wosServ ERROR: request error"

    return res

def wos_retrieve(quid, srtRec, a):
    url = "http://search.isiknowledge.com/esti/wokmws/ws/WOKMWSAuthenticate?wsdl"
    serv_url = "http://search.isiknowledge.com/esti/wokmws/ws/WokSearchLite?wsdl"
    
    #a = wos_auth(url, 1)
    time.sleep(1)

    #now try to ping the main service server
    try:
        search_client = suds.client.Client(serv_url)
        #set the required headers for the http
        search_client.set_options(headers={'content-type':'text/xml; charset=utf-8'})
        search_client.set_options(headers={'Cookie':'SID=%s'%a})

        #this is to select the return value as a xml doc
        search_client.set_options(retxml=bool(1))
    except:
        return "wos_search ERROR: CONNECTION ERROR"

    
    try:
        #now create the return parameters object 
        rt = search_client.factory.create('retrieveParameters')
        rt.count = 100
        rt.firstRecord = srtRec
    except:
        return "wosServ ERROR: response request object error"

    try:
        #this is the actual request to the server
        res =  search_client.service.retrieve(queryId = str(quid), retrieveParameters = rt)
        
    except:
        return "wosServ ERROR: request error"

    return res




def utExtract(xml):
    """ this function extracts all of the UTs from a returned record xml document from the WoS searchlit api"""
    retlist = []

    try:
        soup = BeautifulStoneSoup(xml)
        bb = soup.findAll('records')
        for i in range(len(bb)):
            """ no we will remove the ut for each record """
            try:
                ccc = bb[i].find('ut')
                if len(ccc.contents) == 1:
                    """ make sure that there is only one entry or else don't add it to the list"""
                    ccc = ccc.contents[0]
                    retlist.append(ccc)
                else:
                    pass
            except:
                pass
    except:
        pass

    if len(bb) == len(retlist):
        return retlist
    else:
        return "error"

def listString(lister, delim):
    """ this function converts the contents of a list into a string
    delimited with the specified delim"""
    retstr = ""
    for i in range(len(lister)): retstr = retstr + lister[i] + delim

    retstr = retstr.rstrip(";")

    return retstr
        
   
def rmValuesTag(lister):
    """
    This function removes the values tags from a beautiful soup results set
    """
    retlist = []
    for elem in lister:
        ee = elem.contents[0]
        retlist.append(ee)

    return retlist

def shortExtract(xml):
    """
    this function extracts the title, authors, pubdate, and keywords from the xml feed of the article
    """
    try:
        retlist = []
        soup = BeautifulStoneSoup(xml)
        bb = soup.findAll('records')
        for i in range(len(bb)):
            """ no we will remove the info for each record """
            indict = {}
            try:
                #ut
                ut = bb[i].find('ut')
                ut = ut.contents[0]
                indict['UT'] = ut
                
                #authors
                author = bb[i].find('authors')
                authors = author.findAll('values')
                authors = rmValuesTag(authors)
                authors = listString(authors, ";")
                indict['AU'] = authors

                #keywords (same design as authors)
                #except for the fact that not everyone has keywords
                try:
                    key1 = bb[i].find('keywords')
                    keys = key1.findAll('values')
                    keys = rmValuesTag(keys)
                    keys = listString(keys, ";")
                    indict['DE'] = keys
                except:
                    indict['DE'] = ""

                #title
                tit1 = bb[i].find(text = 'Title')
                inttag = tit1.parent
                nexter = inttag.nextSibling
                titler = nexter.contents[0]
                indict['TI'] = titler

                #pub year
                py1 = bb[i].find(text = 'Published.BiblioYear')
                inttag = py1.parent
                nexter = inttag.nextSibling
                py = nexter.contents[0]
                indict['PY'] = int(py)

                #pub title
                pt1 = bb[i].find(text = 'SourceTitle')
                inttag = pt1.parent
                nexter = inttag.nextSibling
                pt = nexter.contents[0]
                indict['SO'] = pt
                

                retlist.append(indict)
                
            except:
                pass
    except:
        pass

    if len(retlist) == len(bb):
        return retlist
    else:
        return "error"
            
             
def artsDB(artlist, dbPath):
    """
    This function takes the return value of the shortExtract function
    and puts it into the article_short table
    """
    
    try:
        conn = sqlite3.connect(dbPath)
        c = conn.cursor()
        sql_insert = 'insert into article_short (UT, AU, TI, PY, SO, DE) values (:UT, :AU, :TI, :PY, :SO, :DE)'

        sql_check = 'SELECT * FROM article_short WHERE UT = :UT'

        for elem in artlist:
            c.execute(sql_check, elem)
            allit = c.fetchall()
            if len(allit) > 0:
                pass
            else:
                c.execute(sql_insert, elem)
                conn.commit()

        return 1

    except:
        return 0

def wosSearchDB(searcher, utList, dbPath):
    """
    This function inserts the resulting UTs from a search into an entry into
    wosSearch table
    """
    #first check for the fact that it is a list
    if type(utList) is list:
        pass
    else:
        return 0
    
    try:
        conn = sqlite3.connect(dbPath)
        c = conn.cursor()

        resStr = listString(utList, ";")
        resDic = {'search':searcher, 'results':resStr}
        

        sql_insert = 'insert into wosSearch (search, results) values (:search, :results)'

        sql_check = 'SELECT * FROM wosSearch WHERE search = :search'

        c.execute(sql_check, resDic)
        allit = c.fetchall()
        if len(allit) > 0:
            pass
        else:
            c.execute(sql_insert, resDic)
            conn.commit()

        return 1

    except:
        return 0

def citedByDB(utfoc, utList, dbPath):
    """
    This function inserts the resulting UTs from a search into an entry into
    wosSearch table
    """
    #first check for the fact that it is a list
    if type(utList) is list:
        pass
    else:
        return 0
    
    try:
        conn = sqlite3.connect(dbPath)
        c = conn.cursor()

        resStr = listString(utList, ";")
        resDic = {'UT':utfoc, 'forwCites':resStr}
        

        sql_insert = 'insert into citedBy (UT, forwCites) values (:UT, :forwCites)'

        sql_check = 'SELECT * FROM citedBy WHERE UT = :UT'

        c.execute(sql_check, resDic)
        allit = c.fetchall()
        if len(allit) > 0:
            pass
        else:
            c.execute(sql_insert, resDic)
            conn.commit()

        return 1

    except:
        return 0



def recCount(souper):
    #takes an xml file parsed by soup and gets number of records
    ret = 0
    ee = souper.find('recordsfound')
    ret = int(ee.contents[0])

    return ret

def queryID(souper):
    #takes parsed xml and gives query id
    ret = 0
    ee = souper.find('queryid')
    ret = int(ee.contents[0])

    return ret
    


def searchIter(search_text, endDate, a):
    
    c = wos_search(search_text, endDate, a)

    #now create the data for the insertion into db
    soup = BeautifulStoneSoup(c)
    arts = shortExtract(c)
    uts = utExtract(c)
    qid = queryID(soup)
    print qid
    recs = recCount(soup)
    print recs
        
    #below is the logic for searches which return more than 100 results
    if recs < 100:
        pass
    else:
        for i in range(101,recs,100):
            nXML = wos_retrieve(qid, i, a)
            narts = shortExtract(nXML)
            nuts = utExtract(nXML)

            #now combine the records

            arts = arts + narts
            uts = uts + nuts

            time.sleep(5)

    return arts, uts, qid, recs, a

def utIter(uid, endDate, a):
    #url = "http://search.isiknowledge.com/esti/wokmws/ws/WOKMWSAuthenticate?wsdl"
    #a = wos_auth(url, 1)

    #time.sleep(2)

    #now we will get the xml from the server
    try:
        c = wos_UID(uid, endDate, a)
        
        #now create the data for the insertion into db
        soup = BeautifulStoneSoup(c)
        arts = shortExtract(c)
        uts = utExtract(c)
        qid = queryID(soup)
        print qid
        recs = recCount(soup)
        print recs
        
    except:
        return "FAILED: wos_uid1", 0, 0, 0, 0

    #below is the logic for searches which return more than 100 results
    try:
        if recs < 100:
            pass
        else:
            for i in range(101,recs,100):
                nXML = wos_retrieve(qid, i, a)
                narts = shortExtract(nXML)
                nuts = utExtract(nXML)

                #now combine the records

                arts = arts + narts
                uts = uts + nuts

                time.sleep(1)
                
    except:
        return "FAILED: wos_uid2", 0, 0, 0, 0

    return arts, uts, qid, recs, a


   
def search(lsSearch, dbPath, delay, catchLim):
    """
    This function takes the list of search string and implements the searches
    it then puts the search results into the dbs
    """
    f = [0,0,0]
    currentDate = time.strftime("%Y-%m-%d", time.gmtime())
    srtTime = time.time()

    url = "http://search.isiknowledge.com/esti/wokmws/ws/WOKMWSAuthenticate?wsdl"
    a = wos_auth(url, 1)

    time.sleep(2)

    #define var for tracking data downloaded
    caught = 0

    #clean up list to remove entries in db
    def listClean(lsSearcher):
        sql_check = "SELECT * FROM wosSearch WHERE search = :search"
        conn = sqlite3.connect(dbPath)
        c = conn.cursor()
        retlist = []

        for elem in lsSearcher:
            check_dic = {"search":elem}
            c.execute(sql_check, check_dic)
            allit = c.fetchall()
            if len(allit) > 0:
                pass
            else:
                retlist.append(elem)

        return retlist

    lsSearch2 = listClean(lsSearch)   
    
    try:
        for elem in lsSearch2:
            #first execute the search
            print elem
                        
            print caught

            if caught > catchLim:
                pass
            else:
                #
                arts1, utsLs, q, rec, a = searchIter(elem, currentDate, a)
                logger.debug(str(type(arts1)))
                caught = caught + len(utsLs)
                
                f[0] = f[0] + artsDB(arts1, dbPath)
                f[1] = f[1] + wosSearchDB(elem, utsLs, dbPath)
                

 
            time.sleep(delayCalc(srtTime, caught, delay))
                
        
        logger.info(caught)
        return f

    except:
        return f
            

def citedBy(lsSearch, dbPath):
    """
    This function takes the list of search string and implements the searches
    it then puts the search results into the dbs
    """
    f = [0,0,0]
    currentDate = time.strftime("%Y-%m-%d", time.gmtime())
    
    print currentDate

    url = "http://search.isiknowledge.com/esti/wokmws/ws/WOKMWSAuthenticate?wsdl"
    a = wos_auth(url, 1)

    time.sleep(2)



    try:
        for elem in lsSearch:
            #first execute the search
            print elem

            arts1, utsLs, q, rec, a = utIter(elem, currentDate, a)
            print type(arts1)
            print type(utsLs)

            if type(arts1) is list:
                #now execute the insertion to the DB
                f[0] = artsDB(arts1, dbPath)
                
            else:
                f[0] = f[0] + -1

            if type(utsLs) is list:
                #execute into wosSearch
                f[1] = citedByDB(elem, utsLs, dbPath)
                

            else:
                f[1] = f[1] + -1


            time.sleep(8)
                


        return f

    except:
        return f


#####
"""
This section will provide the functions which ensures that the tables all have data they should, starting with the wosSearch table.
"""
#####

def utRegPop(dbPath):
    """
    This function reads the wosSearch table and makes sure that every ut in all of the searches is contained in the utRegister table
    """

    conn = sqlite3.connect(dbPath)
    c = conn.cursor()

    currentDate = time.strftime("%Y-%m-%d", time.gmtime())
    sql_check = "SELECT * FROM utRegister WHERE UT = :UT"
    sql_insert = "INSERT INTO utRegister (UT, wosSearch) values (:UT, :wosSearch)"

    utList = []
    for elem in c.execute('SELECT results FROM wosSearch'):
        utList1 = elem[0].split(";")

        for ut in utList1:
            utList.append(ut)
            
            
            #utDict = {"UT":ut, "wosSearch":currentDate}
            
    for ut in utList:
        utDict = {"UT":ut, "wosSearch":currentDate}
        d = conn.cursor()
        d.execute(sql_check, utDict)
        #print ut
        allit = d.fetchall()
        if len(allit) > 0:
            pass
        else:
            d.execute(sql_insert, utDict)
            conn.commit()


def utRegCheck(dbPath, col):
    """
    This function checks all of the entries of the utRegister to see if the ut is in the table refered to in the columns name
    """
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    currentDate = time.strftime("%Y-%m-%d", time.gmtime())
    utDict = []
    sql_check = "SELECT * FROM %s WHERE UT = :UT" % (col)
    sql_up = "UPDATE utRegister set %s = :%s WHERE UT = :UT" % (col, col)
    

    for elem in c.execute('SELECT UT, %s from utRegister' % (col)):
        utDict.append(elem)

    for elem in utDict:
        if elem[1] > 0:
            pass
        else:
            utDict = {"UT":elem[0], "%s"%(col):currentDate}
            c.execute(sql_check, utDict)
            allit = c.fetchall()
            if len(allit) > 0:
                c.execute(sql_up, utDict)
                conn.commit()
            else:
                pass
        

        
        
def utListGen(dbPath):
    """
    This function creates a list of ut's to search for
    """
    utList = []

    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    sql = "SELECT UT FROM utRegister WHERE citedBy is NULL"
    for elem in c.execute(sql):
        utList.append(elem[0])

    return utList
        

def delayCalc(startTime, recordsCaught, throttle):
    """
    Function returns the number of seconds to sleep given number of records caught to maintain under threshold. throttle here is seconds/record. suggested throttle is .632 which is roughly 60s/95 records
    """
    diff = time.time() - startTime
    wait = throttle*recordsCaught - diff

    if wait > 0:
        return wait
    else:
        return 0
    

        

