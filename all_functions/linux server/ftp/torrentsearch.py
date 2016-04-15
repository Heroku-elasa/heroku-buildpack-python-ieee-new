print """Pirate Bay Torrent Downloader - Command Line Interface

        Program Written by: Daniel Folkes
        website: http://danfolkes.com
        email: danfolkes @t gmail dot c0m
		
		--- Usage  ---
	-a[n]      =  auto downloads first [n] results (default:10)
	-o[/path/] =  points to the folder where .torrent's go
"""

import urllib2
import sys
autoprint = 0
outgoing = "./"
searchFor = []
for arg in sys.argv[1:]:
	print "|"+arg+"|"
	if arg[:2] == "-a":
		autoprint = int(arg[2:len(arg)])
	elif arg[:2] == "-o":
		outgoing = arg[2:len(arg)]
	else:
		searchFor.append(arg)
	
print "Searching The Pirate Bay for: " + str(searchFor)

url = 'http://thepiratebay.org/search.php?q='
o = 0;
for ar in searchFor:
	if o != 0:
		url+="%20"	
	url+=str(ar)
	o +=1
print "URL: " + url
req = urllib2.Request(url)
response = urllib2.urlopen(req)
the_page = response.read()
results = 15
i=0
listing = []
for line in the_page.split("<td>"):
	if i < results:
		if line.count(".torrent"):
			strippedLine = line[9:line.find(".torrent")+8]
			if autoprint == 0:
				print i, strippedLine[15:]
			listing.append(strippedLine)
			i+=1
if autoprint==0:
	download = raw_input("Which ones to download?(sep by commas) :").split(',')
else:
	download = range(0,autoprint)
print download

for j in download:
        g = int(j)
        if (g < results) and (g >=0):
		
		#--- Strip Characters Off
		localPath = listing[g]
		for c in ".:/%!@#$^&*()_-=+~`[]{}|;',.":
		        localPath = localPath.replace(c,"")
		localPath = localPath[(len(localPath)/2):]
		localPath += ".torrent"
		if outgoing:
			localPath = outgoing+localPath
		#---
		print "Downloading: "+ listing[g] + " -> " + str(localPath)
		open(localPath, 'wb').write(urllib2.urlopen(listing[g]).read())
		#import os 			#if you want to use wget and have progress bar (remove line before)
		#os.system("wget "+listing[g]) 	#if you want to use wget and have progress bar

print "...Download Complete"
