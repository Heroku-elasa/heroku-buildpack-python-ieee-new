from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup
from random import randint
dots ='..............................................................................?..'
print'Python 2.7.7'
print'                       Welcome to Python Proxy Scraper'
print'                             Type "Help" for Help'
print'                             14 User-Agent Edition'
print(dots)
cL = ['view user agents', 'help', 'credits', 'command list', 'start',]
userAgents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)',
    'Mozilla/4.0 (compatible; MSIE 7.0; America Online Browser 1.1; Windows NT 5.1; (R1 1.5); .NET CLR 2.0.50727; InfoPath.1)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1) Gecko/20061026 BonEcho/2.0',
    'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.12pre) Gecko/20080103 BonEcho/2.0.0.12pre',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.9) Gecko/20071113 BonEcho/2.0.0.9',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)',
    'Mozilla/4.0 (compatible; MSIE 4.01; AOL 4.0; Windows 98)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Acoo Browser; InfoPath.2; .NET CLR 2.0.50727; Alexa Toolbar)',
    'Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02',
    'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; SV1; TheWorld)',
    ]
mainUrl = ('http://free-proxy-list.net/') # Target web page.
mainLoop = True
searchLoop = False
searchLoop = False
myInt1 = (0) # I've used this as a counter for later, once it reaches a certain number it will reset. 
myInt2 = (0) # That Certain number is the pattern location for the proxies within a table, example.. there is a proxy every 8 cells.
while mainLoop:
    userInput = raw_input('<>< ')
    if userInput ==(cL[0]): # view agents
        for x in range(0, (len(userAgents))):
            print(dots)
            print(x, userAgents[x])
            print(dots)
    elif userInput ==(cL[1]): # help
        print('<>< Version 1.0')
        print('<>< Compatible with Python 2.7.7, maybe unstable on other versions.')
        print('<>< Type command list for a list of commands..')
        print('<>< Feel free to edit/tweak my script give credit where needed if repost.')
        print(dots)
        print('<>< In order to get this to work you might need to tweak some veriables in the code sorry skids...')
        print('<>< Default Target http://free-proxy-list.net.')
        print('<>< This script will scrape proxies from mainUrl.')
        print('<>< The script will then use BeautifulSoup to isolate the table containing the proxies and ports.')
        print('<>< The script will then remove any unwanted characters and spaces and present you a nicely formated list of proxies')
        print(dots)
    elif userInput ==(cL[2]): # credits
        print('<>< Kopuz 2014')
        print('<>< Feel free to edit/tweak my script give credit where needed if repost.')
        print(dots)
    elif userInput ==(cL[3]): # command list
        print(dots)
        print(cL)
        print(dots)
    elif userInput ==(cL[4]): # start
        searchLoop = True
        while searchLoop:
            try:
                agentSelect = randint(0, 14)
                webReq = urllib2.Request(mainUrl)
                print('<>< Starting Proxy Scrape At ' + mainUrl)
                webReq.add_unredirected_header('User-Agent', userAgents[agentSelect])
                print('<>< Agent: ' + userAgents[agentSelect])
                thePage = urlopen(webReq)
                theText = thePage.read()
                print('<>< Raw data gathered, would you like to sort and view? y/n')
                userInput = raw_input('<>< ')
                if userInput == ("y"):
                    soup = BeautifulSoup(theText)
                    rawProx = soup.find('tbody') # Key world to isolate proxy table in HTML document.
                    tableD = rawProx.findAll('td') # To furth isolate the table cells.
                    for x in xrange(len(tableD)):
                        myInt1 += 1
                        myInt2 += 1
                        if myInt1 == 8: # Every 8 cell is a proxy.
                            myInt = myInt2 +1 # Assuming the port is in the next cell.
                            strBuilder = (tableD[myInt2],":",tableD[myInt])
                            theString = str(strBuilder)
                            noSpace = theString.replace(" ", "")
                            noComma = noSpace.replace(",", "")
                            noTd = noComma.replace("<td>", "")
                            noCtd = noTd.replace("</td>", "")
                            noSQ = noCtd.replace("'", "")
                            noBo = noSQ.replace("(", "")
                            noBc = noBo.replace(")", "")
                            print (noBc)
                            myInt1 = 0
                        searchLoop = False
                elif userInput == ("n"):
                    searchLoop = False    
            except Exception:
                continue
    else:
        print'<>< Unknown Command'