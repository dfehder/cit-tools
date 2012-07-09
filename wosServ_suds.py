#Author: Daniel Fehder
# Last modified: 4/12/2012
# Purpose: to provide a suds client to ISI Web of Science Lite web services
import suds,logging, time
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)


#this establishes the auth
def wos_auth(auth_url, proxy):
    client = suds.client.Client(auth_url)
    #d = dict(http='host:1080', https='host:1080')
    #client.set_options(proxy=d)
    session_id =  client.service.authenticate()
    return session_id



def wos_search(search_text):
    url = "http://search.isiknowledge.com/esti/wokmws/ws/WOKMWSAuthenticate?wsdl"
    serv_url = "http://search.isiknowledge.com/esti/wokmws/ws/WokSearchLite?wsdl"
    
    a = wos_auth(url, 1)
    time.sleep(1)

    #now try to ping the main service server
    try:
        search_client = suds.client.Client(serv_url)
        #set the required headers for the http
        search_client.set_options(headers={'content-type':'text/xml; charset=utf-8'})
        search_client.set_options(headers={'Cookie':'SID=%s'%a})
        #set the http proxy
        #d = dict(http='host:1080', https='host:1080')
        #search_client.set_options(proxy=d)
        #now create the query parameters object
    except:
        return "wos_search ERROR: CONNECTION ERROR"

    #now create the search request object
    try:
        qp = search_client.factory.create('')
        #now populate it with the data
        qp.userQuery = search_text
        qp.databaseID = "WOS"
        qp.queryLanguage = "en"

        #now create the annoyting
        ed1 = search_client.factory.create('queryParameters.editions')
        ed2 = search_client.factory.create('queryParameters.editions')

        ed1.collection = 'WOS'
        ed1.edition = 'SSCI'

        ed2.collection = 'WOS'
        ed2.edition = 'SCI'

        qp.editions = [ed1, ed2]

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
        res =  search_client.service.citingArticles(queryParameters= qp, retrieveParameters = rt)
        #bb =  search_client.last_sent()
        #print bb
        
    except:
        return "wosServ ERROR: request error"

    return res


def wos_UID(muid, edition, endDate, a):
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
        #set the http proxy
        #d = dict(http='host:1080', https='host:1080')
        #search_client.set_options(proxy=d)
        #now create the query parameters object
        #this is to select the return value as a xml doc
        search_client.set_options(retxml=bool(1))
    except:
        return "wos_search ERROR: CONNECTION ERROR"

    #now create the search request object
    try:
        
        #now create the editions
        ed1 = search_client.factory.create('editionDesc')
        ed1.collection = 'WOS'
        ed1.edition = edition
        
        ed2 = search_client.factory.create('editionDesc')
        ed2.collection = 'WOS'
        ed2.edition = 'SSCI'

        eds = [ed1, ed2]

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
        res =  search_client.service.citingArticles(databaseId = woos, uid = muid, editionDesc = ed1, timeSpan = ts, queryLanguage = 'en', retrieveParameters = rt)
        #bb =  search_client.last_sent()
        #print bb
        
    except:
        return "wosServ ERROR: request error"

    return res




