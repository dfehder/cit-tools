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

arts = wosServ_suds.shortExtract(b)
uts = wosServ_suds.utExtract(b)

def artsDB(artlist, dbPath):
    """
    This function takes the return value of the shortExtract function
    and puts it into the article_short table
    """
    #first check for the fact that it is a list
    if type(artlist) is list:
        pass
    else:
        return 0
    
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
        

#now to test the above function
conn_path = '/home/dcfehder/Dropbox/projects/cit-tools/WoS.db'

outcome = artsDB(arts, conn_path)


#note that the WoS api bugs out whenever there are @ symbols in the SID, so you will need to fix that (like don't look up anything with that SID)



