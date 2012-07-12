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


#note that the WoS api bugs out whenever there are @ symbols in the SID, so you will need to fix that (like don't look up anything with that SID)


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
            
                

        
        
        
        
    
    
    
