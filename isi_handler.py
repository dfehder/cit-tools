#!/usr/bin/env python
# Author: DFehder
# Create Date: 11, 04, 2011
# Purpose: To generate a list of dictionary objects to need isi_parser
import os, random, isi_parser

#first, you want to close any unclosed ISI windows
cmd1 = 'wmctrl -c "Web of Science Home"'
os.system(cmd1)

cmd2 = 'wmctrl -c "Opening savedrecs.txt"'
os.system(cmd2)

cmd3 = 'wmctrl -c "Export Transfer Service"'
os.system(cmd3)


# first, I have to generate a list of all files that are in my save path
lister1 = os.listdir("/home/dcfehder/dev/nbt/download/ISI/")
lister3 = os.listdir("/home/dcfehder/Desktop")
lister1 = lister1 + lister3

# next I generate a list of all the files that I need in that path
filer = open("/home/dcfehder/dev/nbt/citation_list.txt")

lister2 = []
for line in filer: lister2.append(line.strip("\n").strip("\r"))

#lastly, open up the logfile and read each of the lines that have the INFO header
logfile = open("/home/dcfehder/dev/nbt/isi2.log", "r")
logcheck = ""
for line in logfile:
    if line.find("INFO")> -1:
        logcheck = logcheck + line.strip("\n")
    else:
        pass
        


# this is the place where I will store all the random numbers
seed = []

# Generate a set of three DOIs that you can use to query ISI
while len(seed) < 14:
    r = random.randint(0,len(lister2)-1)
    if "cf-" + lister2[r][8:] + ".txt" in lister1:
        pass
    else:
        if logcheck.find(lister2[r]) > -1:
            pass
        else:
            seed.append(lister2[r])

# now package the list into a set of dictionary objects
# no style points on this one, but this is a late night hack
lister = [{"DOI":seed[0]}, {"DOI":seed[1]}, {"DOI":seed[2]}, {"DOI":seed[3]}, {"DOI":seed[4]}, {"DOI":seed[5]}, {"DOI":seed[6]}, {"DOI":seed[7]}, {"DOI":seed[8]}, {"DOI":seed[9]}, {"DOI":seed[10]}, {"DOI":seed[11]}]

          ## {"DOI":seed[12]}, {"DOI":seed[13]}, {"DOI":seed[14]}, {"DOI":seed[15]}, {"DOI":seed[16]}, {"DOI":seed[17]}, {"DOI":seed[18]}, {"DOI":seed[19]}, {"DOI":seed[20]}, {"DOI":seed[21]}, {"DOI":seed[22]}, {"DOI":seed[23]}, {"DOI":seed[24]}, {"DOI":seed[25]}, {"DOI":seed[26]} ]

# now I need to make sure that there is no file called savedrecs.txt on the
# desktop
filer = "/home/dcfehder/Desktop/savedrecs.txt"
#os.path.exists(filer)

# this logic does not allow the process to run if there is a saved recs file
# on the desktop
if os.path.exists(filer):
    os.remove(filer)
else:
    # now I have the list I can feed my other program
    pd = isi_parser.isi_parser()
    pd.article_grabber2(lister)

# note that this logice implies that I will not run the isi_parser if a
# savedrecs file exists on the desktop for that run

cmd = 'wmctrl -c "Web of Science Home"'
os.system(cmd)

cmd = 'wmctrl -c "Mozilla"'
os.system(cmd)

#end of program


