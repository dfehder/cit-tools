"""
Author: D. Fehder
Date: 8/13/2012
"""
import mechanize, cookielib, re, logging
from bs4 import BeautifulSoup
#BeautifulSoup(markup, html5lib)

"""

1. Error Logging Configuration

""" 

#logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('suds.client')
logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.INFO)

# create file handler which logs even debug messages
fh = logging.FileHandler('/home/dcfehder/Dropbox/projects/cit-tools/wosScrap.log')
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

2. functions to control website

""" 

def getBrowser():
   # Browser
    br = mechanize.Browser()

    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # Want debugging messages?
    #br.set_debug_http(True)
    #br.set_debug_redirects(True)
    #br.set_debug_responses(True)

    # User-Agent (this is cheating, ok?)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    return br

def getSID(browser):
    #br = getBrowser()
    url = "http://libraries.mit.edu/get/webofsci"
    r = browser.open(url)
    newurl = r.geturl()
    
    m = re.match(r".*&SID=(?P<sid>.*?)&", newurl)
    s = m.group('sid')

    return s

def getQID(url):
    m = re.match(r".*&qid=(?P<qid>[0-9]+)", url)
    s = m.group('qid')

    return s
    

def getUID(uid):
    br = getBrowser()
    sid = getSID(br)
    url1 = "http://apps.webofknowledge.com.libproxy.mit.edu/OneClickSearch.do?product=WOS&search_mode=OneClickSearch&colName=WOS&SID=%s&field=UT&value=%s"%(str(sid),str(uid))
    temp = br.open(url1)

    url2 = temp.geturl()

    qid = getQID(url2)

    url3 = "http://apps.webofknowledge.com.libproxy.mit.edu/full_record.do?product=WOS&search_mode=OneClickSearch&qid=%s&SID=%s&page=1&doc=1"%(str(qid),str(sid))

    temp2 = br.open(url3)
    #filename = "/home/dcfehder/Dropbox/projects/cit-tools/tester.html"
    #out = open(filename, "w")
    #print >> out, temp2.read()
    #out.close()
    soup = BeautifulSoup(temp2.read(), "html5lib") 
    
    return soup




"""
Everything below here is for script development
"""

    
