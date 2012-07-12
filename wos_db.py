import sqlite3, xls_util, sys

#create the path and the connection to the db
conn_path = '/home/dcfehder/Dropbox/projects/cit-tools/WoS.db'
conn = sqlite3.connect(conn_path)

c = conn.cursor()

# write the crate sql code and then create the table
sqlcmd = 'CREATE TABLE article (UT text PRIMARY KEY ASC, AU text, TI text, SO text, PD text, PY text, DI text, AF text, LA text, DT text, DE text, ID text, AB text, C1 text, RP text, EM text, FU text, FX text, CR text, NR integer, TC integer, PU text, WC text, SC text)'

c.execute(sqlcmd)

#close it all up
conn.commit()
c.close()

#now I want to load some data into the database
#first I create the list object
pp = "/home/dcfehder/Dropbox/projects/cit-tools/nbtest.xls"
aa = xls_util.xlsList(pp, "UT", "AU", "TI", "SO", "PD", "PY", "DI", "AF", "LA", "DT", "DE", "ID", "AB", "C1", "RP", "EM", "FU", "FX", "CR", "NR", "TC", "PU", "WC", "SC")

xls_util.listInsTable(conn_path, 'article', aa)




