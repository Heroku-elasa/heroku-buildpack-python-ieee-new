

	#-------------------------------------------------------------------+
	#																	|
	#	Prject name:		IP Proxy Scraper     						|
	#	Developer/Author:	Daapii									    |
	#	Website:			http://www.daapii.users.sourceforge.net		|
	#	Email:				devdaapii@gmail.com							|
	#																	|
	#	If you like this tool share it with your friends!				|
	#	You are free to modify and use code of this project,			|
	#	but releasing your own version of IP Proxy Scraper is			|
	#	not allowed. If you want to provide feedback, make suggestions	|
	#	or ask any questions you can do so by contacting me via email.	|
	#																	|
	#	Thanks for using IP Proxy Scraper.								|
	#																	|
	#-------------------------------------------------------------------+

from BeautifulSoup import BeautifulSoup as Soup
from ipwhois import IPWhois
from pprint import pprint
import  urllib
from urlparse import urlparse as urlparse2
import sys

if(sys.version_info[0] != 2 or sys.version_info[1] != 7):
	print("\nSorry this script was created only for Python 2.7.5\nPlease download it at http://python.org/download/releases/2.7.5/ \n")
	sys.exit()
import urllib2
import HTMLParser
import re
import os
from sys import platform as _platform
from time import strftime
import base64
from collections import OrderedDict
from netaddr import IPAddress
import mechanize
import cookielib,random

try:
	from colorama import init, Fore, Back, Style
	init()
except Exception:
	print("You don't have colorama installed! Please download and install it from https://pypi.python.org/pypi/colorama then restart IP Proxy Scraper!")
	sys.exit()
global Html
# globals url_to_check_proxy
Custom_User_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17"
Default_User_agent = "Googlebot/2.1 (+http://www.googlebot.com/bot.html)"
SucceededWebsites = []
NoSuccessWebsites = []
NoSuccessCounter = 0
ScrapedProxies = []
ProxyCounter = 0
TimeOut = 30
OurIP = ""
Html = ""
PROXY_list="..//..//configs//sites_proxy//all_proxies_list//scraped_list.txt"
Proxy_university_checked_by_whois='..//..//configs//sites_proxy//all_proxies_list//Proxy_university_checked_by_whois.txt'
Proxy_on='..//..//configs//sites_proxy//all_proxies_list//Proxy_on.txt'

University_port_checked="..//..//configs//sites_proxy//all_proxies_list//University_port_checked.txt"
university_Proxy_on='..//..//configs//sites_proxy//all_proxies_list//university_Proxy_on.txt'
####################
import thread
import threading
def cdquit(fn_name):
    # print to stderr, unbuffered in Python 2.
    print '{0} took too long'.format(fn_name) #, file=sys.stderr
    sys.stderr.flush() # Python 3 stderr is likely buffered.
    thread.interrupt_main() # raises KeyboardInterrupt

def exit_after(s):
    '''
    use as decorator to exit process if
    function takes longer than s seconds
    '''
    def outer(fn):
        def inner(*args, **kwargs):
            timer = threading.Timer(s, cdquit, fn.__name__)
            timer.start()
            try:
                result = fn(*args, **kwargs)
            finally:
                timer.cancel()
            return result
        return inner
    return outer


########################################


class MECAHNIZM(object):
    def __init__(self, proxy='', User_Pass='', **kwargs):
        global PDF_Dir, Watermarked_PDF_Files_Dir
        if kwargs['cookies']:
            self.cookie3 = kwargs['cookies']
        else:
            self.cookie3 = ''
        if kwargs['url']:
            self.url = kwargs['url']
        else:
            self.url = ''

        self.proxy = proxy
        self.User_Pass = User_Pass
        self.br = self.BROWSER()

    def progressbar(self):
        pass
        # from clint.textui import progress
        # r = requests.get(url, stream=True)
        # with open(path, 'wb') as f:
        #     total_length = int(r.headers.get('content-length'))
        #     for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
        #         if chunk:
        #             f.write(chunk)
        #             f.flush()

    def BROWSER(self, cookie3=''):
        """
        :param url:
        """
        # global br, cj, r, proxy, User_Pass


        br = mechanize.Browser()
        # print br

        # Cookie Jar
        # fo=os.getcwd()+"\\cookies\\"
        # try :
        #     os.mkdir(fo)
        # except:
        #     pass
        # os.chdir(fo)
        # folder=sys.path.insert(0,'/cookies')

        # os.chdir(..)


        # Browser options
        br.set_handle_equiv(True)
        br.set_handle_gzip(True)
        br.set_handle_referer(True)    # no allow everything to be written to
        br.set_handle_robots(False)   # no robots
        # br.set_handle_refresh(True)  # can sometimes hang without this
        # br.set_handle_redirect(True)

        # Follows refresh 0 but not hangs on refresh > 0
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # Want debugging messages?
        #br.set_debug_http(True)
        # br.set_debug_redirects(True)
        #br.set_debug_responses(True)

        # # User-Agent (this is cheating, ok?)
        # br.addheaders = [('User-Agent', 'Mozilla/5.0 (Linux; U; Android 2.3.4; en-us; T-Mobile myTouch 3G Slide Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'),
        #                  ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        #                  ('Accept-Language', 'en-gb,en;q=0.5'),
        #                  ('Accept-Encoding', 'gzip,deflate'),
        #                  ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'),
        #                  ('Keep-Alive', '115'),
        #                  ('Connection', 'keep-alive'),
        #                  ('Cache-Control', 'max-age=0'),
        #                  ('Referer', 'http://yahoo.com')]

        # User-Agent (this is cheating, ok?)
        # br.addheaders = [('User-agent',
        #               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

        br.addheaders = [
            ('User-agent',
             'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'),
            ('Accept',
             'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5;application/json;text/javascript;*/*'),
            ('Accept-Language', 'en,hu;q=0.8,en-us;q=0.5,hu-hu;q=0.3'),
            ('Accept-Encoding', 'gzip, deflate'),
            ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'),
            ('Keep-Alive', '300'),
            ('Connection', 'keep-alive'),
            ('Cache-Control', 'max-age=0'),
            ('Referer', self.url),
            ('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8'),
            ('X-Requested-With', 'XMLHttpRequest')
        ]
        # # If the protected site didn't receive the authentication data you would
        # # end up with a 410 error in your face
        # br.add_password('http://safe-site.domain', 'username', 'password')
        # br.open('http://safe-site.domain')

        # Open some site, let's pick a random one, the first that pops in mind:
        # Proxy and user/password
        #proxy = "61.233.25.166:80"

        # proxy = "202.202.0.163:3128"
        # proxy=self.proxy
        # Proxy
        # dd=re.findall('None:None', proxy)
        if self.proxy != [] and self.proxy != '' and not (re.findall('None', self.proxy)):
            br.proxies = br.set_proxies({"http": self.proxy})
            # br.proxies=br.set_proxies( proxy)

        if self.User_Pass != [] and self.User_Pass != '' and not (re.findall('None:None', self.User_Pass)):
            br.add_proxy_password(self.User_Pass.split(":")[0], self.User_Pass.split(":")[1])

        # if  r!={}:
        # rr = br.open(url)

        # c= cookielib.Cookie(version=0, name='PON', value="xxx.xxx.xxx.111", expires=365, port=None, port_specified=False, domain='xxxx', domain_specified=True, domain_initial_dot=False, path='/', path_specified=True, secure=True, discard=False, comment=None, comment_url=None, rest={'HttpOnly': False}, rfc2109=False)
        # cj.set_cookie(c0)
        if self.cookie3 == '':
            CurrentDir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
            fo = os.path.abspath(os.path.join(CurrentDir, '../..')).replace('\\', '/')
            # pathname = os.path.join("cookies", cookie3)
            # site = urlparse2(self.url).hostname
            site='whois_cookies'
            if not os.path.isdir(fo + "/cookies/" + site): os.mkdir(fo + "/cookies/" + site)
            chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            self.cookie3 = fo + "/cookies/" + site + '/' + ''.join([random.choice(chars) for x in range(5)]) + ".txt"
            self.cj = cookielib.LWPCookieJar()
            opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(self.cj))
            br.set_cookiejar(self.cj)
            self.cj.save(self.cookie3)
        else:
            self.cj = cookielib.LWPCookieJar()
            # self.cj.revert(self.cookie3)
            opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(self.cj))
            br.set_cookiejar(self.cj)
            # self.cj.load(self.cookie3)
            # self.cj.save( self.cookie3, ignore_discard=True, ignore_expires=True)

            # cookiefile=open(self.cookie3,'r')
            # s0=cookiefile.readlines()
            # # print s0
            # for i in range(0,len(s0)):
            #     if re.findall(':',s0[i]):
            #         s2=s0[i].split(':')[1].replace('\n','')
            #         print s2
            #         br.set_cookie(s2)





        # self.cj.save( self.cookie3)

        return br


    # Proxy password
    # br.add_proxy_password("joe", "password")
    # self.dl_acm = "http://dl.acm.org/citation.cfm?id=99977.100000&coll=DL&dl=ACM"


    def speed_download(self, pdf_url, piece_size=1024 * 1024,timeout=12):
        # br2=self.br

        cookiefile = open(self.cookie3, 'r')
        s0 = cookiefile.readlines()
        # print s0
        # for i in range(0,len(s0)):
        #     if re.findall(':',s0[i]):
        #         s2=s0[i].split(':')[1].replace('\n','')
        #         print s2
        #         self.br.set_cookie(s2)
        # socket=import_mod(from_module='socket')
        # socket.setdefaulttimeout(300)
        try:
            openerdirector = self.br.open(pdf_url,timeout=timeout)
        except:
            return '', self.cookie3
        # openerdirector = self.br.open(pdf_url)
        try:
            if (openerdirector._headers.dict['content-type']) == 'application/pdf':
                length = long(openerdirector._headers.dict['content-length'])
                ok = True
            else:
                length = 0
        except:
            length = 0
        dlength = 0
        # piece_size = 4096 # 4 KiB
        # piece_size =1024*1024 # 1MB
        data = ''
        # if True: #openerdirector.getcode() == 200:
			# global Html
			# encoding = openerdirector.headers.getparam('charset')
			# if(encoding):
			# 	Html = openerdirector.read().decode(encoding)
			# else:
			# 	Html = openerdirector.read()
        while True:
            newdata = openerdirector.read(piece_size)
            dlength += len(newdata)
            data += newdata
            if length != 0:
                status = r"%10d [%3.2f%%]" % (dlength, dlength * 100. / length)
                status = status + chr(8) * (len(status) + 1)
                print status
                # pdf_path=PDF_File().file_save(data, "PDF_Files\\", localName.filename)
            # if onprogress:
            #     onprogress(length,dlength)
            if not newdata:
                self.cj.save(self.cookie3)
                break
        return data, self.cookie3 #,pdf_path

    def download_pdf_br(self, pdf_url1):
        class pdf_url():
            abs = 1
            if not ("pdf_url1.absolute_url" is locals()):
                absolute_url = str(pdf_url1)
            else:
                pdf_url = str(pdf_url1)

            def __init__(self):
                self.absolute_url = 2
                if not ("pdf_url1.absolute_url" is locals()):
                    self.absolute_url = str(pdf_url1)
                else:
                    pdf_url = str(pdf_url1)

        # pdf_url = pdf_url1
        # pdf_url.='test'.split()
        # pdf_url2=str(pdf_url1)
        # if not ("pdf_url1.absolute_url" is locals()):
        #     pdf_url.absolute_url = pdf_url2.split()
        # else:
        #     pdf_url = pdf_url1
        if pdf_url.absolute_url.endswith(".pdf") or pdf_url.absolute_url.endswith(".zip"):
            if pdf_url.absolute_url:
                # localName1 = basename(urlsplit(pdf_url.absolute_url)[2])
                # localName = LINK(PDF_Dir=PDF_Dir, Watermarked_PDF_Files_Dir=Watermarked_PDF_Files_Dir).filename(
                #     pdf_url.absolute_url)
                # pathname = os.path.join("PDF_Files", localName.filename)
                # s=get_full_url(pdf_url)
                # req = self.br.click_link(pdf_url.absolute_url)
                # html = self.br.open(req).read()

                f1 = self.br.retrieve(pdf_url.absolute_url, 'test.html')

        else:
            # localName = LINK(PDF_Dir=PDF_Dir, Watermarked_PDF_Files_Dir=Watermarked_PDF_Files_Dir).filename(
            #     pdf_url.absolute_url)
            f1 = self.br.retrieve(pdf_url.absolute_url, 'test.html')
            # f1 = self.br.retrieve(pdf_url, localName.pdf_Folder_filename)

        if f1:
            self.cj.save(self.cookie3)

        return f1[0], self.cookie3 #,pdf_path



        # return os.getcwd()+PDF_File.pdf_Folder_filename,os.getcwd()+PDF_File.W_pdf_Folder_filename
def GetSourceCode(url, useragent = Custom_User_agent):
        try:
           global Html
           piece_size=1024*1024*3;
           # Html,cookies = MECAHNIZM('',cookies='',url=url).download_pdf_br(url)
           Html,cookies = MECAHNIZM('', cookies='', url=url).speed_download(url,piece_size)
           return
        except:
           return
		# Se

def GetSourceCode0(url, useragent = Custom_User_agent):
        try:
            global Html
            Html,cookies = MECAHNIZM('',cookies='',url=url).download_pdf_br(url)

        except:
            pass
		# Set the user agent
	try:
		if(useragent == Default_User_agent):
			user_agent = {"User-Agent" : Default_User_agent}
		else:
			user_agent = {"User-Agent" : Custom_User_agent}

		# set the headers
		request = urllib2.Request(url, data=None, headers=user_agent)

		# make the request
		response = urllib2.urlopen(request,timeout=TimeOut)

		# print some debug info if needed
		if(sys.argv[1] == "-d"):
			Log("\n\tResponse from {1}\n\tStatus code: {0}\n\tCharset: {2}\n\tServer: {3}\n".format(response.getcode(), url, response.headers.getparam('charset'), response.info()['server']), "magenta")

	# needed if the argv[1] wasn't specified
	except IndexError:
		print IndexError

		# check if the server returned a positive http code
		if response.getcode() == 200:
			global Html
			encoding = response.headers.getparam('charset')
			if(encoding):
				Html = response.read().decode(encoding)
			else:
				Html = response.read()

			# remove our IP from the sourcecode
			if OurIP in Html:
				Html = Html.replace(OurIP,"")

			# replace some encoded html chars to their real char
			Html = Html.replace("&quot;",'"').replace("&nbsp;"," ").replace("&gt;",">").replace("&lt;","<").replace("&amp;","&")
			return

	except urllib2.URLError:
		print urllib2.URLError
	NoSuccess(url)
	return
@exit_after(11)
def Scrape(url):
	# check for a valid url and fix it if necessary
	url = url.strip().lower()

	if(not url or "facebook" in url):
		return

	if(url.startswith("www.")):
		url = "http://%s" % url

	elif(url.startswith("www.") == False and url.startswith("http://") == False and url.startswith("https://") == False):
		url = "http://%s" % url


	try:
		#______________________________________________________________
		#|-------------------- Obtain sourcecode ---------------------|
		# some websites disallow googlebot as user agent
		if("proxy-list.co.uk" in url):
			GetSourceCode(url, Custom_User_agent)
		else:
			GetSourceCode(url)
		# print "\n htmls is :"+Html +"for this url:\n"+url

		#--------------------------------------------------------------


		#______________________________________________________________
		#|------------------- Encoding recognition --------------------|
		if(Filter(r'(&#?\w{2};?)+', url, "HTML_Encoded")):
			pass
		if(Filter(r"Base64.decode\(('|\").*('|\")", url, "Base64_Encoded")):
			pass
		if(Filter(r"('|\")(%\\w{2}){10,}('|\")", url, "URL_Encoded")):
			pass
		#--------------------------------------------------------------


		#______________________________________________________________
		#|-------------------- Specific websites ----------------------|
		if("proxz.com" in url):
			if(Filter(r'(\d{1,3}\.?){4}:\d{1,5}', url, "None")):
				pass
			else:
				NoSuccess(url)
			return
		if("xroxy.com" in url):
			if(Filter(r'proxy&host=(\d{1,3}\.){3}\d{1,3}&port=\d{1,5}', url, "None")):
				pass
			else:
				NoSuccess(url)
			return
		if("anonymousinet.com" in url or "proxycemetery.com" in url or "proxyforest.com" in url):
			if(Filter(r'\(\d(\,\'\d{1,3}\'){4}', url, "anonminet")):
				pass
			else:
				NoSuccess(url)
			return
		if("gatherproxy.com" in url):
			if(Filter(r'PROXY_IP\":\"(\d{1,3}\.){3}\d{1,3}', url, "gatherproxy")):
				pass
			else:
				NoSuccess(url)
			return
		if("proxylisty.com" in url):
			if(Filter(r"<td><a\shref='.*(L|l)ist'>\d+", url, "proxylisty")):
				pass
			else:
				NoSuccess(url)
			return
		if("proxy-list.co.uk" in url):
			if(Filter(r"rel=\"nofollow\">(\d{1,3}\.){3}\d{1,3}</a>", url, "proxylistdotcodotuk")):
				pass
			else:
				NoSuccess(url)
			return
		if("antipalivo.ru" in url):
			if(Filter(r"decode\(\"(\d+,?)+\"\)", url, "antipalivo")):
				pass
			else:
				NoSuccess(url)
			return
		if("nntime.com" in url):
			if(Filter(r'(\w=\d;){8,10}', url, "nntime")):
				pass
			else:
				NoSuccess(url)
			return
		if("ultraproxies.com" in url):
			if(Filter(r'>\d{2}-(\d{2}-?)+<', url, "ultraproxies")):
				pass
			else:
				NoSuccess(url)
			return
		if("proxynova.com" in url):
			if(Filter(r'decode\(\"\w+\"', url, "proxynova")):
				pass
			else:
				NoSuccess(url)
			return
		if("checkedproxylists.com" in url):
			if(Filter(r"\"loadData\('.+?D'", url, "checkedproxylists")):
				pass
			else:
				NoSuccess(url)
			return
		if("freeproxylists.com" in url):
			if(Filter(r"'dataID',\s'.+'", url, "freeproxylists")):
				pass
			else:
				NoSuccess(url)
			return
		if("cool-proxy.net" in url):
			if(Filter(r"document.write\((\d{1,3}\.){3}\d{1,3}\)", url, "coolproxy")):
				pass
			else:
				NoSuccess(url)
			return
		if("proxylist.ro" in url):
			if(Filter(r"(z\(\d+-\d+\);)+(.|\n)+?(z\(\d+-\d+\);)+", url, "proxylistdotro")):
				pass
			else:
				NoSuccess(url)
			return
		#--------------------------------------------------------------


		#______________________________________________________________
		#|-------------------- General patterns -----------------------|
		# IP:Port,  IP:[Port]
		if("idcloak.com" not in url):
			if(Filter(r'(\d{1,3}\.){3}\d{1,3}:\[?\d{1,5}\]?', url, "None")):
				return
		# IP</td><td>Port
		if(Filter(r'(\d{1,3}\.){3}\d{1,3}</td><td>\d{1,5}', url, "None")):
			return
		# Port</td><td>IP
		if(Filter(r'\d{1,5}</td><td>(\d{1,3}\.){3}\d{1,3}', url, "None")):
			return
		# multiline
		if(Filter(r'<.+?>?(\d{1,3}\.){3}\d{1,3}(.|\n)*?<.+?>\d{1,5}', url, "NewLine")):
			return
		#--------------------------------------------------------------

	# except Exception:
		# pass
	except KeyboardInterrupt:
		pass
	NoSuccess(url)
	return

def AddToSuccessCounter(matchesCount, url):
	global ProxyCounter
	ProxyCounter += matchesCount
	SucceededWebsites.append(url)
	return

def Log(msg, color = ""):
	if(color == "black"):
		print(Fore.BLACK + msg + Fore.RESET)
		return
	elif(color == "magenta"):
		print(Fore.MAGENTA + msg + Fore.RESET)
		return
	elif(color == "red"):
		print(Fore.RED + msg + Fore.RESET)
		return
	elif(color == "blue"):
		print(Fore.BLUE + msg + Fore.RESET)
		return
	elif(color == "yellow"):
		print(Fore.YELLOW + msg + Fore.RESET)
		return
	elif(color == "green"):
		print(Fore.GREEN + msg + Fore.RESET)
		return
	elif(color == "white" or color == "reset"):
		print(Fore.RESET + msg)
		return
	elif(color == "cyan"):
		print(Fore.CYAN + msg + Fore.RESET)
		return
	else:
		print(msg)
	return

def NoSuccess(url):
	global NoSuccessCounter
	NoSuccessCounter += 1
	global NoSuccessWebsites
	NoSuccessWebsites.append(url)
	return

def StatusReport():

	try:
		if(ProxyCounter <= 0):
			print("\nNo proxies found!\n")
		else:
			print("\n\n\t---------------------------------------\n\tEstimated Proxies: %d\n\n" % ProxyCounter )

			exportToFile = raw_input("\tExport to file? (Y/n): ");
			if("N" in exportToFile or "n" in exportToFile):
				pass
			else:
				SaveFile()

			# prompt to view the list of results
			if(NoSuccessCounter > 0):
				viewList = raw_input( "\n\tView website statistics? (y/N): ");
				if("y" in viewList or "Y" in viewList):
					global SucceededWebsites
					global NoSuccessWebsites
					# remove duplicate entries from the lists
					uniqueSW = list(OrderedDict.fromkeys(SucceededWebsites))
					uniqueNW = list(OrderedDict.fromkeys(NoSuccessWebsites))

					print("\n\tWebsites without proxies:\n\t---------------------------------------\n")
					for url in uniqueNW:
						Log("\t" + url,"red")

					print("\n\n\tWebsites with proxies:\n\t---------------------------------------\n")
					for url in uniqueSW:
						Log("\t" + url,"green")

					exportToFile = raw_input("\n\tExport succeeded websites to file? (y/N): ")
					if(exportToFile == "Y" or exportToFile == "y"):
						with open("output/Succeeded websites.txt","w+") as f:
							urlList = []
							# read all lines from the file (if it exists)
							for urlFromFile in f.readlines():
								urlList.append(urlFromFile)
							# append all succeeded websites to the list
							for sucUrl in uniqueSW:
								urlList.append(sucUrl)

							unique = list(OrderedDict.fromkeys(urlList))
							for url in unique:
								f.write(url + os.linesep)

						print("\n\tFile has been saved!\n\tYou can find it under 'output/Succeeded websites.txt'\n")

			# wait until we hit enter to continue because the call to Menu will clear the screen
		raw_input("\n\tHit enter to return to the main menu...")
	except KeyboardInterrupt:
		sys.exit()
	Menu()
	return

def SaveFile():
	try:
		fileName = raw_input("\tFilename: ~> ");

	except KeyboardInterrupt:
		sys.exit()
		return

	#check if we have the directory 'output', if not create it.
	if(os.path.isdir("output") == False):
		os.makedirs("output")

	#if we accidently press enter or don't provide a filename, set a default one
	if(fileName == ""):
		print("\tUsing default filename...")
		fileName = strftime("{0} Proxies - %d.%b.%Y %H%M%S").format(ProxyCounter) + ".txt"

	with open("output/" + fileName,'w') as file:
		for lines in ScrapedProxies:
			file.write(lines + os.linesep) # linesep securily makes a new line

	print("\n\tFile saved!\n\tYou can find it under 'output/%s'\n" % fileName)
	return

def Filter(regexPattern, url, Encryption):

	global Html
	matchesCount = len(list(re.finditer(regexPattern, Html)))
	matches = re.finditer(regexPattern, Html)

	if(Encryption is "None"):
		if(matchesCount > 0):
			for match in matches:
				Dump(match.group())

			AddToSuccessCounter(matchesCount, url)
			return True
	elif(Encryption is "HTML_Encoded"):
		# Are HTML encoded characters in the source code?
		if(matchesCount > 0):
			Html = HtmlDecoder()
			return True
	elif(Encryption is "Base64_Encoded"):
		# Are Base64 encrypted strings in the source code?
		if(matchesCount > 0):
			for match in matches:
				Html = Html.replace(match.group() ,Base64Decoder(match.group().replace("Base64.decode(\"", "")))
			return True
	elif(Encryption is "URL_Encoded"):
		# Are URL-Encoded strings in the source code?
		if(matchesCount > 0):
			for match in matches:
				Html = Html.replace(match, URLDecoder(match))
			return True
	elif(Encryption is "NewLine"):
		if(matchesCount > 0):
			for match in matches:
				Dump(match.group())

			AddToSuccessCounter(matchesCount, url)
			return True
	elif(Encryption is "anonminet"):
		if("anonymousinet.com" in url or "proxyforest.com" in url):
			matches = re.finditer(r'\(\d(\,\'\d{1,3}\'){4}\,\d{1,5}\);', Html)
			matchesCount = len(list(matches))
			if(matchesCount > 0):
				matches = re.finditer(r'\(\d(\,\'\d{1,3}\'){4}\,\d{1,5}\);', Html)
				AnonymouseInetFilter(matches, True)
				AddToSuccessCounter(matchesCount, url)
				return True
		else:
			matches = re.finditer(r'\(\d(\,\'\d{1,3}\'){4}', Html)
			matchesCount = len(list(matches))
			if(matchesCount > 0):
				AnonymouseInetFilter(matches, False)
				AddToSuccessCounter(matchesCount, url)
				return True
	elif(Encryption is "gatherproxy"):
		if(matchesCount > 0):
			GatherproxyFilter(matches)
			AddToSuccessCounter(matchesCount, url)
			return True
	elif(Encryption is "proxylisty"):
		if(matchesCount > 0):
			ProxyListyFilter(matches)
			AddToSuccessCounter(matchesCount, url)
			return True
	elif(Encryption is "proxylistdotcodotuk"):
		if(matchesCount > 0):
			ProxyListDotcoDotuk(matches)
			AddToSuccessCounter(matchesCount, url)
			return True
	elif(Encryption is "antipalivo"):
		if(matchesCount > 0):
			AntipalivoFilter(matches)
			AddToSuccessCounter(matchesCount, url)
			return True
	elif(Encryption is "ultraproxies"):
		if(matchesCount > 0):
			UltraproxiesFilter(matches)
			AddToSuccessCounter(matchesCount, url)
			return True
	elif(Encryption is "nntime"):
		match = re.search(regexPattern, Html)
		if(matchesCount > 0):
			NnTimeFilter(match, url)
			return True
	elif(Encryption is "proxynova"):
		print("matchesCount = {0}".format(matchesCount))
		if(matchesCount > 0):
			print(matchesCount)
			ProxyNovaFilter(matches)
			AddToSuccessCounter(matchesCount, url)
			return True
	elif(Encryption is "checkedproxylists"):
		if("checkedproxylists.com/proxylist" in url):
			match = re.search(r"'dataID',\s'.+?'", Html)
			if(match):
				CheckedproxyListsFilter(match, url, False)
				# AddToSuccessCounter is in function
				return True
		elif(url.endswith("checkedproxylists.com/") or url.endswith("checkedproxylists.com")):
			match = re.search(r"'shortID',\s'.+?'", Html)
			if(match):
				CheckedproxyListsFilter(match, url, True)
				# AddToSuccessCounter is in function
				return True
	elif(Encryption is "freeproxylists"):
		# make the 'matches' to a single match object
		match = re.search(regexPattern, Html)
		if(url == "freeproxylists.com" or url == "freeproxylists.com/"):
				return False
		if(match):
			if("freeproxylists.com/load" in url):
				#isRaw = true
				FreeproxyListsFilter(match, url, True)
				return True
			elif("freeproxylists.com/" in url):
				# isRaw = false
				FreeproxyListsFilter(match, url, False)
				return True
	elif(Encryption is "coolproxy"):
		if(matchesCount > 0):
			CoolproxyFilter(matches)
			AddToSuccessCounter(matchesCount, url)
			return True
	elif(Encryption is "proxylistdotro"):
		if(matchesCount > 0):
			ProxyListdotRoFilter(matches)
			AddToSuccessCounter(matchesCount, url)
			return True


	return False

def Dump(proxy):
	if(proxy):
		# exclude our own ip if it exists
		# get the ip from the filtered proxy entry which could contain stuff we don't want
		ip = re.search(r'(\d{1,3}\.){3}\d{1,3}', proxy)
		# delete the ip from the string
		proxy = proxy.replace(ip.group(),"")
		# search for the port
		port = re.search(r'\d{1,5}', proxy)
		if(ip.group() is not None and port.group() is not None):
			print("\t%s:%s" %(ip.group(),port.group()))

			ScrapedProxies.append("%s:%s" %(ip.group(),port.group()))
	        f= open(PROXY_list, "a+b");
        if(ip.group() is not None and port.group() is not None):
            fr= open(PROXY_list, "r");data=fr.read();fr.close();
            if re.search("%s:%s" %(ip.group(),port.group())+'\n',data):
                pass;
                f.close()
            else:
                # f.writelines("%s:%s" %(ip.group(),port.group())+'\n');
                t= "%s:%s" %(ip.group(),port.group())+'\n'
                f.writelines(str(t))
                # print "%s:%s" %(ip.group(),port.group())+'\n'
                f.close()
        return ScrapedProxies

def Clear():
	"""
	Linux (2.x and 3.x)_____'linux2'
	Windows_________________'win32'
	Windows/Cygwin__________'cygwin'
	Mac OS X _______________'darwin'
	"""
	if(_platform == "linux" or _platform == "linux2" or _platform == "darwin" or _platform == "cygwin"):
		os.system('clear')
	# Clear screen for windows
	elif(_platform == "win32" or _platform == "nt" or _platform ==  "dos" or _platform ==  "ce"):
		os.system('cls')
	return

def ResetStats():
	# reset all stats
	global SucceededWebsites
	SucceededWebsites = []
	global NoSuccessWebsites
	NoSuccessWebsites = []
	global NoSuccessCounter
	NoSuccessCounter = 0
	global ProxyCounter
	ProxyCounter = 0
	global Html
	global ScrapedProxies
	ScrapedProxies = []
	global TimeOut
	TimeOut = timeout
	return

def Menu():

	ResetStats()
	Clear()

	# print our sweet logo :)
	print(Fore.CYAN)
	print("\t ___ ____    ____                      ")
	print("\t|_ _|  _ \  |  _ \ _ __ _____  ___   _ ")
	print("\t | || |_) | | |_) | '__/ _ \ \/ / | | |")
	print("\t | ||  __/  |  __/| | | (_) >  <| |_| |")
	print("\t|___|_|     |_|   |_|  \___/_/\_\\__,  |")
	print("\t                                 |___/ ")
	print("\t ____                                 ")
	print("\t/ ___|  ___ _ __ __ _ _ __   ___ _ __ ")
	print("\t\___ \ / __| '__/ _` | '_ \ / _ \ '__|")
	print("\t ___) | (__| | | (_| | |_) |  __/ |   ")
	print("\t|____/ \___|_|  \__,_| .__/ \___|_|   ")
	print("\t                     |_|            ")
	print(Fore.RESET)
	Log("\n\t---------------------------------------\n")
	Log("\t1. Import from file")
	Log("\t2. Specify URLs")
	Log("\n\t3. Quit")
	Log("\n\t---------------------------------------\n\n")
	try:
		answer = raw_input("\tInput method: ~> ");

		#end the program?
		if(answer is not "1" and answer is not "2"):
			Log("\n\tAborting IP Proxy Scraper...\n", "cyan")
			sys.exit()

		# Import from file?
		elif(answer is "1"):
			ImportFromFile()

		# type manualy?
		elif(answer is "2"):
			urls = raw_input("\n\tYour URLs: ~> ");
			split = urls.split(",")
			if(len(split) >= 1 and "," not in urls):
				try:
					split = urls.split(' ')
				except Exception:
					Log("\tPlease seperate your URLs with a comma!\n\tExample: www.example.com, www.example2.com, ...\n\n")
					sys.exit()
				except KeyboardInterrupt:
					pass
			Log("\n\tStarting scrape process...\n\n","cyan")
			Log("\n\t---------------------------------------\n")
			# try to scrape all provided urls
			for url in split:
				Scrape(url.strip())

		if(ProxyCounter > 0):
			StatusReport()
		else:
			Log("\n\tNo proxies found!\n\n","red")
			raw_input("\n\tHit enter to return to the main menu...");
			Menu()

	except KeyboardInterrupt:
		sys.exit()

	return

def ImportFromFile():
	try:
		path = raw_input("\n\tSource of the file: ~> ");

		# remove leading and trailing quotes when a file is dragged in
		if(path.startswith("\"") or path.endswith("\"")):
			path = path.replace("\"","")

		with open(path) as file:
			websites = file.readlines()

		if(len(list(websites)) > 0):
			Log("\n\tStarting scrape process...\n\n","cyan")
			Log("\n\t---------------------------------------\n")
			for url in websites:
				try:
					if(url):
						Scrape(url)

				except KeyboardInterrupt:
					break
					sys.exit()
		else:
			Log("red", "\tThis file is empty, please provide a file which contains URLs!\n")
			ImportFromFile()

	except KeyboardInterrupt:
		sys.exit()

	# except:
		# Log("\n\tFile not found, please try again!\n","red")
		# ImportFromFile()
	return

def HtmlDecoder():
	# try:
		# global Html
		# p = HTMLParser.HTMLParser()
		# unescaped = p.unescape(Html)
		# return unescaped.contents
	# except Exception:
		# return Html
	# except KeyboardInterrupt:
		# pass
	return Html

def Base64Decoder(match):
	decoded = base64.b64decode(match).decode('utf-8', errors='ignore')
	return decoded

def URLDecoder(match):
	cleanedMatch = match.group().replace("'","").replace("\"","")
	return urllib2.unquote(cleanedMatch).decode('utf8', errors='ignore')

def AnonymouseInetFilter(matches, withPorts):

	ipList = []
	portList = []

	for encodedProxy in matches:
		splitter = encodedProxy.group().split(',')
		mode = splitter[0].replace("(","")
		arg1 = splitter[1].replace("'","")
		arg2 = splitter[2].replace("'","")
		arg3 = splitter[3].replace("'","")
		arg4 = splitter[4].replace("'","")
		if(withPorts):
			port = splitter[5].replace(");","")
			finalProxy = "";
			if(mode == "1"):
				finalProxy = "{0}.{1}.{2}.{3}:{4}".format(arg1,arg2,arg3,arg4,port)
				Dump(finalProxy)
			elif(mode == "2"):
				finalProxy = "{0}.{1}.{2}.{3}:{4}".format(arg4,arg1,arg2,arg3,port)
				Dump(finalProxy)
			elif(mode == "3"):
				finalProxy = "{0}.{1}.{2}.{3}:{4}".format(arg3,arg4,arg1,arg2,port)
				Dump(finalProxy)
			elif(mode == "4"):
				finalProxy = "{0}.{1}.{2}.{3}:{4}".format(arg2,arg3,arg4,arg1,port)
				Dump(finalProxy)
		else:
			finalIP = "";
			if(mode == "1"):
				finalIP = "{0}.{1}.{2}.{3}:{4}".format(arg1,arg2,arg3,arg4)
				ipList.append(finalIP)
			elif(mode == "2"):
				finalIP = "{0}.{1}.{2}.{3}:{4}".format(arg4,arg1,arg2,arg3)
				ipList.append(finalIP)
			elif(mode == "3"):
				finalIP = "{0}.{1}.{2}.{3}:{4}".format(arg3,arg4,arg1,arg2)
				ipList.append(finalIP)
			elif(mode == "4"):
				finalIP = "{0}.{1}.{2}.{3}:{4}".format(arg2,arg3,arg4,arg1)
				ipList.append(finalIP)

	if(withPorts):
		return

	portCollector = re.finditer("<TD></TD>(.|\n)+?<TD>\d{1,5}</TD>", Html)
	for match in portCollector:
		portExtractor = re.search(r"\d{1,5}")
		portList.append(portExtractor.group())

	for i in range(0, len(list(portCollector))):
		Dump("{0}:{1}".format(ipList[i], portList[i]))
	return

def GatherproxyFilter(matches):
	IPList = []
	PortList = []

	for m in matches:
		IPList.append(m.group().replace("PROXY_IP\":\"",""))

	portMatches = re.finditer("PROXY_PORT\":\"\\d{1,5}", Html)
	for p in portMatches:
		PortList.append(p.group().replace("PROXY_PORT\":\"",""))

	for i in range(0, len(PortList)):
		Dump("{0}:{1}".format(IPList[i],PortList[i]))

	return

def ProxyListyFilter(Portmatches):
	IPList = []
	PortList = []
	ourIP = ""

	IPMatches = re.finditer(r"(\d{1,3}\.){3}\d{1,3}", Html)

	for ip in IPMatches:
		IPList.append(ip.group())

	for port in Portmatches:
		PortList.append(port.group()[:(port.group().rfind(">"))].replace(">",""))

	for i in range(0, len(PortList)):
		Dump("{0}:{1}".format(IPList[i], PortList[i]))
	return

def ProxyListDotcoDotuk(matches):
	IPList = []
	PortList = []

	for m in matches:
		IPList.append(m.group().replace("rel=\"nofollow\">","").replace("</a>",""))

	PortMatches = re.finditer(r"class=\"port_td\">\d{1,5}</td>", Html)

	for p in PortMatches:
		PortList.append(p.group().replace("class=\"port_td\">","").replace("</td>",""))

	for i in range(0, len(PortList)):
		Dump("{0}:{1}".format(IPList[i], PortList[i]))

	return

def AntipalivoFilter(matches):
	IPList = []
	PortList = []

	# chr(97) = Convert.toChar()
	for port in matches:
		cleanedPort = port.group().replace("decode(","").replace("\"","").replace(")","")
		# decoding logic of the website
		a = cleanedPort.split(',')
		r = ""

		for i in range(0, len(a)):
			r+= chr(int(a[i]) - 1)

		PortList.append(r)
	IPMatches = re.finditer("(\d{1,3}\.){3}\d{1,3}", Html)
	for ip in IPMatches:
		IPList.append(ip.group())

	for i in range(0, len(PortList)):
		Dump("{0}:{1}".format(IPList[i], PortList[i]))
	return

def UltraproxiesFilter(matches):
	IPList = []
	PortList = []

	a = 22
	b = 28
	c = 2
	x = (((b/c + a)/c - 1)*-1)
	for m in matches:
		digit = m.group().replace(">","").replace("<","").split("-")
		port = ""
		for i in range(0, len(digit)):
			port += chr(int(digit[i]) + x)
		PortList.append(port)

	IPMatches = re.finditer(r"(\d{1,3}\.){3}\d{1,3}", Html)
	for ip in IPMatches:
		IPList.append(ip.group())

	for i in range(0, len(PortList)):
		Dump("{0}:{1}".format(IPList[i], PortList[i]))
	return

def NnTimeFilter(match, url):
	PortList = []
	IPList = []
	try:
		splitter = match.group().split(';')
		# removes empty strings from the list
		splitter = filter(None, splitter)

		if(len(splitter) == 10):
			keyOne = splitter[0][0]
			decodeOne = splitter[0][2]

			keyTwo = splitter[1][0]
			decodeTwo = splitter[1][2]

			keyThree = splitter[2][0]
			decodeThree = splitter[2][2]

			keyFour = splitter[3][0]
			decodeFour = splitter[3][2]

			keyFive = splitter[4][0]
			decodeFive = splitter[4][2]

			keySix = splitter[5][0]
			decodeSix = splitter[5][2]

			keySeven = splitter[6][0]
			decodeSeven = splitter[6][2]

			keyEight = splitter[7][0]
			decodeEight = splitter[7][2]

			keyNine = splitter[8][0]
			decodeNine = splitter[8][2]

			keyTen = splitter[9][0]
			decodeTen = splitter[9][2]

			PortFilter = re.finditer(r"write\(((\":\")?\+\w){1,5}\)", Html)
			for port in PortFilter:
				cleanedPort = port.group().replace("write(\":\"","").replace(")","").replace("+","")
				decodedPort = cleanedPort.replace(keyTen, decodeTen).replace(keyNine, decodeNine).replace(keyEight, decodeEight).replace(keySeven, decodeSeven).replace(keySix, decodeSix).replace(keyFive, decodeFive).replace(keyFour, decodeFour).replace(keyThree, decodeThree).replace(keyTwo, decodeTwo).replace(keyOne, decodeOne)
				PortList.append(decodedPort)

		elif(len(splitter) == 9):
			keyOne = splitter[0][0]
			decodeOne = splitter[0][2]

			keyTwo = splitter[1][0]
			decodeTwo = splitter[1][2]

			keyThree = splitter[2][0]
			decodeThree = splitter[2][2]

			keyFour = splitter[3][0]
			decodeFour = splitter[3][2]

			keyFive = splitter[4][0]
			decodeFive = splitter[4][2]

			keySix = splitter[5][0]
			decodeSix = splitter[5][2]

			keySeven = splitter[6][0]
			decodeSeven = splitter[6][2]

			keyEight = splitter[7][0]
			decodeEight = splitter[7][2]

			keyNine = splitter[8][0]
			decodeNine = splitter[8][2]

			matches = re.finditer(r"write\(((\":\")?\+\w){1,5}\)", Html)
			for port in matches:
				cleanedPort = port.group().replace("write(\":\"","").replace(")","").replace("+","")
				decodedPort = cleanedPort.replace(keyNine, decodeNine).replace(keyEight, decodeEight).replace(keySeven, decodeSeven).replace(keySix, decodeSix).replace(keyFive, decodeFive).replace(keyFour, decodeFour).replace(keyThree, decodeThree).replace(keyTwo, decodeTwo).replace(keyOne, decodeOne)
				PortList.append(decodedPort)

		IPMatches = re.finditer(r"<td>(\d{1,3}\.){3}\d{1,3}<", Html)
		for ip in IPMatches:
			IPList.append(ip.group().replace("<td>","").replace("<",""))
		for i in range(0, len(PortList)):
			Dump("{0}:{1}".format(IPList[i],PortList[i]))
	except Exception:
		NoSuccess(url)
	else:
		AddToSuccessCounter(len(IPList), url)
	return

def ProxyNovaFilter(matches):
	IPList = []
	PortList = []

	for encodedChunk in matches:
		cleanedIP = encodedChunk.group().replace("decode(","").replace("\"","")
		keyMatcher = re.search(r"var\sletters\s=\s\".+\"", Html)

		letters = list(keyMatcher.group().replace("var letters = \"","").replace("\"",""))

		for letter in range(0, len(letters)):
			novaFilter = re.finditer(letters[letter],cleanedIP)
			for match in novaFilter:
				cleanedIP = cleanedIP.replace(match.group(), str(letter))

		ip = int(cleanedIP)
		t = [ip >> 24,ip >> 16 & 0xFF, ip >> 8 & 0xFF, ip & 0xFF]

		IPList.append("{0}.{1}.{2}.{3}".format(t[0], t[1], t[2], t[3]))
	PortMatches = re.finditer(r"\d{2,5}(</a>)?\s+</span>", Html)

	for port in PortMatches:
		trashFilter = re.search(r"\d{2,5}",port.group())
		PortList.append(trashFilter.group())

	for i in range(0, len(IPList)):
		Dump("{0}:{1}".format(IPList[i], PortList[i]))
	return

def CheckedproxyListsFilter(match, url, isMainSite):
	global Html
	pCounter = 0
	baseURL = "http://www.checkedproxylists.com/"

	if(isMainSite):
		grabSLink = match.group().replace("shortID', ","").replace("'","").strip()
		GetSourceCode(baseURL+grabSLink)

		pFilter = re.finditer(r"(\d{1,3}\.?){4}:\d{1,5}", Html)
		for proxy in pFilter:
			Dump(proxy.group())
			pCounter += 1

		AddToSuccessCounter(pCounter, url)
		return
	else:
		resList = match.group().replace("dataID', ","").replace("'","").strip()
		GetSourceCode(baseURL+resList)

		proxyFilter = re.finditer(r"(\d{1,3}\.?){4}<.+?>\d{1,5}", Html)
		for proxy in proxyFilter:
			trashFilter = re.search("<.+?>", proxy.group())
			Dump(proxy.group().replace(trashFilter.group(), ":"))
			pCounter += 1
		AddToSuccessCounter(pCounter, url)
	return

def FreeproxyListsFilter(match, url, isRaw):
	# simmilar to checkedproxylistsFilter
	if(isRaw):
		pass
	else:
		rawUrl = match.group().replace("'dataID', ","").replace("'","")
		GetSourceCode("http://www.freeproxylists.com"+rawUrl)

	HtmlDecoder()
	proxyFilter = re.finditer(r"(\d{1,3}\.?){4}</td><td>\d{1,5}", Html)
	pCounter = 0
	for p in proxyFilter:
		Dump(p.group().replace("<td>","").replace("</td>",":"))
		pCounter += 1
	AddToSuccessCounter(pCounter, url)
	return

def CoolproxyFilter(matches):
	# base64
	IPList = []
	PortList = []
	#Base64Decoder not required, will be done because of the structure of scrape

	for ip in matches:
		IPList.append(ip.group().replace("Base64.decode(","").replace("\"",""))

	PortFilter = re.finditer(r"<td>\d{1,5}</td>", Html)
	for port in PortFilter:
		PortList.append(port.group().replace("/","").replace("<td>",""))

	for i in range(0, len(IPList)):
		Dump("{0}:{1}".format(IPList[i], PortList[i]))

	return

def ProxyListdotRoFilter(matches):
	EncodedIPList = []
	DecodedIPList = []

	EncodedPortList = []
	DecodedPortList = []

	for match in matches:
		filterEncodedData = re.finditer(r"(z\(\d+-\d+\);)+", match.group())
		filteredList = list(filterEncodedData)

		EncodedIPList.append(filteredList[0])
		EncodedPortList.append(filteredList[1])

	for encodedIP in EncodedIPList:
		cleanedString = encodedIP.group().replace("z(","").replace(")","").strip()

		splitter = cleanedString.split(';')
		decodedIP = ""

		for splitted in splitter:
			if(splitted):
				part = splitted.split('-')
				decodedIP += chr(int(part[0]) - int(part[1]))

		DecodedIPList.append(decodedIP)

	for encodedPort in EncodedPortList:
		cleanedString = encodedPort.group().replace("z(","").replace(")","").strip()
		splitter = cleanedString.split(';')
		decodedPort = ""

		for splitted in splitter:
			if(splitted):
				part = splitted.split('-')
				decodedPort += chr(int(part[0]) - int(part[1]))

		DecodedPortList.append(decodedPort)

	for i in range(0, len(DecodedPortList)):
		Dump("{0}:{1}".format(DecodedIPList[i], DecodedPortList[i]))

	return


def GetOurOwnIP():
	try:
		# get our own public IP to exclude it from the sourcecode
		ip = urllib2.urlopen("http://icanhazip.com")
		response = ip.read()
		match = re.search("(\d{1,3}\.){3}\d{1,3}", response)
		return match.group()
	except Exception:
		import ipgetter
        IP = ipgetter.myip()
        return IP
	return
def get_proxy_list(pr_site_list='..//..//configs//sites_proxy//all_proxies_list//Sites_to_get_proxylist.txt'):
    hosts = [host.strip() for host in open(pr_site_list).readlines()]

    siteList = [];proxies_list=[]
    i=-1
    for j in range(i + 1, len(hosts)):
        if ( not re.findall("#", hosts[j]) and hosts[j] != '' ):
            siteList.append(hosts[j])
            print hosts[j]+'\n'
    for j in range(0, len(siteList)):

            proxies=Scrape(str(siteList[j]))
            if proxies==None:
                proxies = [line.rstrip('\n') for line in open(PROXY_list)]
                #print proxies
            try:
                if ( not re.findall("#", proxies[j]) and proxies[j] != '' ):
                   # proxies_list.append(proxies[j])
                    proxies_list=proxies
            except:
                print "Proxies are not found in :\n"+PROXY_list+' \nfile'

            if True:
                proxies=None
                if proxies==None:
                    proxies = [line.rstrip('\n') for line in open(PROXY_list)]
                    #print proxies

            try:
                if ( not re.findall("#", proxies[j]) and proxies[j] != '' ):
                   # proxies_list.append(proxies[j])
                    proxies_list=proxies
            except:
                print "Proxies are not found in :\n"+PROXY_list+' \nfile'

                # print '\n proxies is emptry:'+str(proxies)
                # return []

    return proxies_list



from grab import Grab, GrabError
def get_valid_proxy(proxy_list): #format of items e.g. '128.2.198.188:3124'
    g = Grab()
    for proxy in proxy_list:
        g.setup(proxy=proxy, proxy_type='http', connect_timeout=timeout, timeout=timeout)
        try:
            g.go(url_to_check_proxy)
        except GrabError:
            #logging.info("Test error")
            pass
        else:
            yield proxy
#s=get_valid_proxy(proxy_list)
#
# from grab.spider import Spider, Task
# import logging
#
# class ExampleSpider(Spider):
#     def task_generator(self):
#         for lang in ('python', 'ruby', 'perl'):
#             url = 'https://www.google.com/search?q=%s' % lang
#             yield Task('search', url=url, lang=lang)
#
#     def task_search(self, grab, task):
#         print('%s: %s' % (task.lang,
#                           grab.doc('//div[@class="s"]//cite').text()))


#logging.basicConfig(level=logging.DEBUG)
# bot = ExampleSpider()
# bot.run()
def xgoogle_search(text="quick and dirty"):
    import os
    fo = os.getcwd().replace('\\','/')
    CurrentDir=os.path.dirname(os.path.realpath(__file__))
    Parent_Dir=os.path.abspath(os.path.join(CurrentDir, 'x_google'))
    # os.chdir(Parent_Dir)
    fo1 = Parent_Dir.replace('\\','/')
    import sys
    sys.path.insert(0, fo1)

    from xgoogle.search import GoogleSearch, SearchError
    site_list=[]
    try:
        gs = GoogleSearch(text)
        gs.results_per_page = 50
        results = gs.get_results()
        for res in results:
            print res.title.encode("utf8")
            print res.desc.encode("utf8")
            print res.url.encode("utf8")
            print
            pip=res.url.encode("utf8")
            site_list.append(str(pip))
            # fr= open(university_Proxy_on.split('.txt')[0]+'_working_for_url.txt', "r");data=fr.read();fr.close()
            # if re.search("%s" %(pip.replace('\n','')),data):
            #     print pip.replace('\n','')+"is repeated" ;
            #     # fr.close()
            # else:
            #     fr= open(university_Proxy_on.split('.txt')[0]+'_working_for_url.txt', "a+b");
            #     fr.writelines("%s" %(pip.replace('\n',''))+ u3_2+ '\n');
            #     fr.close()
    except SearchError, e:
            print "Search failed: %s" % e
    return site_list

# xgoogle_search('university proxy ip')
#
def pygoogle_1(text='free proxy list'):
    from pygoogle import pygoogle
    g = pygoogle(text)
    g.pages = 100
    print '*Found %s results*'%(g.get_result_count())
    proxy_sites=g.get_urls()
    pr_list=[str(x) for x in proxy_sites]
    return pr_list




import urllib2
import socket

def is_bad_proxy(pip):
    global url_to_check_proxy
    url=[]
    if re.findall('.txt',url_to_check_proxy):
        d = open (url_to_check_proxy,'r');ul=d.readlines();d.close();
        for u in ul:
            url.append(u.replace('\n',''))
    elif len (url_to_check_proxy)>2:
        for u2 in url_to_check_proxy:
            url.append(u2.replace('\n',''))
    else:
        url.append(url_to_check_proxy)
    test=0
    for u3 in url:
        try:
            proxy_handler = urllib2.ProxyHandler({'http': pip})
            opener = urllib2.build_opener(proxy_handler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib2.install_opener(opener)
            req=urllib2.Request(u3)  # change the URL to test here
            sock=urllib2.urlopen(req)
            test=test+1;
            u3_2=u3.split('http://')[1].split("/")[0]
            fr= open(university_Proxy_on.split('.txt')[0]+'_working_for_url.txt', "r");data=fr.read();fr.close()
            if re.search("%s" %(pip.replace('\n','')),data):
                print pip.replace('\n','')+"is repeated" ;
                # fr.close()
            else:
                fr= open(university_Proxy_on.split('.txt')[0]+'_working_for_url.txt', "a+b");
                fr.writelines("%s" %(pip.replace('\n',''))+ u3_2+ '\n');
                fr.close()
        except urllib2.HTTPError, e:
            print "for:"+u3+"\n"
            print 'Error code: ', e.code

            # return e.code
        except Exception, detail:
            print "for:"+u3+"\n"
            print "ERROR:", detail
            if re.findall('<urlopen error timed out>',str(detail)):
                try:
                    socket.setdefaulttimeout(10*timeout)
                    proxy_handler = urllib2.ProxyHandler({'http': pip})
                    opener = urllib2.build_opener(proxy_handler)
                    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                    urllib2.install_opener(opener)
                    req=urllib2.Request(u3)  # change the URL to test here
                    sock=urllib2.urlopen(req)
                    test=test+1;
                    u3_2=u3.split('http://')[1].split("/")[0]
                    fr= open(university_Proxy_on.split('.txt')[0]+'_working_for_url.txt', "r");data=fr.read();fr.close()
                    if re.search("%s" %(pip.replace('\n','')),data):
                        pass;
                        # fr.close()
                    else:
                        fr= open(university_Proxy_on.split('.txt')[0]+'_working_for_url.txt', "a+b");
                        fr.writelines("%s" %(pip.replace('\n',''))+' '*10+ u3_2+ '\n');
                        fr.close()
                except:
                        print 'failur for '+u3+'in:'+'\n'+pip+'\n timeout:  '+str(5*timeout)+'   Seconds'


            # return True
    socket.setdefaulttimeout(timeout)
    if test>=1:
        return False
    else:
        return True

def ipRange(start_ip, end_ip):
   start = list(map(int, start_ip.split(".")))
   end = list(map(int, end_ip.split(".")))
   temp = start
   ip_range = []

   ip_range.append(start_ip)
   while temp != end:
      start[3] += 1
      for i in (3, 2, 1):
         if temp[i] == 256:
            temp[i] = 0
            temp[i-1] += 1
      ip_range.append(".".join(map(str, temp)))

   return ip_range

def find_on_proxy_range(Proxy_university_checked_by_whois='',university_Proxy_on=''):
    global prot_range,timeout
    socket.setdefaulttimeout(timeout)

    # two sample proxy IPs
    print "find_on_proxy_range for whois checked by this file\n"+Proxy_university_checked_by_whois+'\nand saving in :\n'+university_Proxy_on
    proxyList = [line.rstrip('\n') for line in open(Proxy_university_checked_by_whois ,'a+')]
    #d=open(university_Proxy_on ,'a+');
    # ports=['80','8080','1080','3128','8888','8123','8118','8081','6588','4444','9999','443','8121','7004','8118','6903'];
    ports=prot_range
    if re.findall('all',str(ports)):
        for p_range in range(1,1025):
            ports.append(str(p_range));

    for currentProxy in proxyList:
        k=currentProxy.replace('\n','').split(':')[0];
        try:
            whosi=whois(k);
            dd=whosi['nets']

            # range_=dd[0];
            #range1=range.items()
            #print range1

            range2=dd[0].keys()
            range_value=dd[0].values()
            if 'range' in range2:
                i = range2.index('range')
                #print players.name('range')
            print '\n'+str(i)+'\n'
            print range2[i]
            print range_value[i]
            range_12=range_value[i];
            range_1=range_12.split('-')[0].replace(' ','');
            range_2=range_12.split('-')[1].replace(' ','')
            ip_range = ipRange(range_1, range_2)
            for ip in ip_range:
                print(ip)
            for ip in ip_range:
                #ip_existance_cheker=ipaddress.ip_address(ip)
                ip2 = IPAddress(ip)
                if ip2.is_unicast() and not ip2.is_private():
                #if  ip_existance_cheker:

                    for port in ports:
                        currentProxy=ip;
                        currentProxy=currentProxy.split(':')[0]+':'+port;
                        if is_bad_proxy(currentProxy):
                            print "\nBad Proxy %s" % (currentProxy)
                        else:
                            print "\n%s is working" % (currentProxy)
                            #proxies_on = [line.rstrip('\n') for line in open(Proxy_on ,'a+')]
                            #proxies_on.append(currentProxy)
                            d=open(university_Proxy_on ,'a+');dr=d.read();
                            if re.search (dr,currentProxy):
                                d.writelines(currentProxy+'\n');
                                d.close()
                            else:
                                print '\n'+currentProxy +"is repeated"

                                d.close()
        except:
            print "\n"+"bad proxy:"+currentProxy
            pass
    #d.close()


def find_on_proxy(proxyList='',Proxy_on=''):

    socket.setdefaulttimeout(timeout)

    # two sample proxy IPs
    # proxyList = proxy_list
    d=open(proxyList ,'a+');proxyList_1=d.readlines();d.close();

    for currentProxy in proxyList_1:
        if is_bad_proxy(currentProxy.replace('\n','')):
            print "Bad Proxy %s" % (currentProxy.replace('\n',''))
            fr= open(Proxy_on, "r");data=fr.read();fr.close()
            if re.search("%s" %(currentProxy.replace('\n',''))+'\n',data):
                fr= open(Proxy_on, "w+");
                data_2=data.replace(currentProxy,'');data_2=data_2.split("\n")[0]
                fr.write(data_2+'\n');
                fr.close()
            else:
                fr.close()
        else:
            #print "%s is working" % (currentProxy)
            print "is working %s" % (currentProxy.replace('\n',''))
            #proxies_on = [line.rstrip('\n') for line in open(Proxy_on ,'a+')]
            #proxies_on.append(currentProxy)
            fr= open(Proxy_on, "r");data=fr.read();fr.close()
            if re.search("%s" %(currentProxy.replace('\n',''))+'\n',data):
                pass;
                # fr.close()
            else:
                fr= open(Proxy_on, "a+b");
                fr.writelines("%s" %(currentProxy.replace('\n',''))+'\n');
                fr.close()

            # d.writelines(currentProxy.replace('\n','')+'\n');
    # d.close()
def search(dictionary, substr):
    result = []
    for key in dictionary:
        if substr in key:
            result.append((key, dictionary[key]))
    return result
# @exit_after(11)
def whois(pr):

    obj = IPWhois(pr.split(':')[0])
    #
    try:
        results = obj.lookup(get_referral=True)
        # results = obj.lookup()
        return results
    except:
        return {}
def university(PROXY_list,Proxy_university_checked_by_whois):
            repeated=0
            import dpath
            proxies = [line.rstrip('\n') for line in open(PROXY_list)]
            #print proxies
            j=-1
            # proxies_un = [line.rstrip('\n') for line in open(Proxy_university_checked_by_whois ,'a+')]
            for k1 in proxies:
              j=j+1
              try:
               if ( not re.findall("#", proxies[j]) and proxies[j] != '' ) :#and not (is_bad_proxy(proxies[j])):
               # proxies_list.append(proxies[j])


                k=k1.replace('\n','');
                url='http://www.whois.com/whois/'+k.split(':')[0]

                # CurrentDir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
                # cookies=CurrentDir+"/cookies_whois.txt"
                whosi, cookies = MECAHNIZM('', cookies="", url=url).speed_download(url)
                os.remove(cookies)
                # whosi=whois(k);
                #print whosi
               if whosi!={}:
                   try:
                        dd=whosi['nets']
                   except:
                       dd=whosi
                   t=search(whosi, 'edu')
                   print "\n"+' '*60;
                   print '\n'+' edu searching in  proxy find is:'+str(t)+'for'+k1+'\n';
                   print "\n"+' '*60
                   #result = [(key, value) for key, value in whosi.iteritems() if re.search("edu",key)]

                   #s=dpath.util.search(whosi, 'univ*')
                   #if dpath.util.search(whosi, 'univ*')!={} or dpath.util.search(whosi, 'cll*')!={} or dpath.util.search(whosi, 'edu*')!={} or  re.findall('edu',str(dd)) :
                   repeated=0
                   if  re.findall('univ',str(dd))  or  re.findall('coll',str(dd)) or  re.findall('edu',str(dd)):
                       print "\n"+'@'*60;print '\n'+' University proxy find is:'+k1+'\n';print '@'*60
                       proxies_un = [line.rstrip('\n') for line in open(Proxy_university_checked_by_whois ,'a+')]
                       if proxies_un!=[]:
                         for l in proxies_un:
                           if re.search(k,l):
                               repeated=1
                       if repeated!=1:
                          proxies_un.append(k1)
                          d=open(Proxy_university_checked_by_whois ,'a+');
                          if True:
                              d.writelines(k1+'\n');
                              d.close();
                       else:print "\nproxy :\n"+k +'is repeated in:\n'+Proxy_university_checked_by_whois
               else:
                    print '\n'+'error in :'+ proxies[j]+'proxy whois not work\n'
              except:
                  print '\n'+'error in :'+ proxies[j]+'proxy whois not work\n'
def url_proxy_scraper(url):
    document = urllib.urlopen(url)
    tree = Soup(document.read())
    regex  = re.compile(r'^(\d{3}).(\d{1,3}).(\d{1,3}).(\d{1,3}):(\d{2,4})')

    proxylist = tree.findAll(attrs = {"class":"Apple-style-span", "style": "color: black;"}, text = regex)
    data = proxylist[0]
    for x in data.split('\n'):
            print x
    #if __name__ == '__main__':

#OurIP = GetOurOwnIP()
# Menu()
url='http://free-proxy-list.net/'
url='http://www.proxz.com/proxy_list_anonymous_us_0.html'
url ='http://www.proxz.com/proxy_list_cn_ssl_0.html'
#proxies=Scrape(url)
#pr=get_proxy_list();proxy_list=pr

#find_on_proxy(Proxy_on)

try:
        pass
        # university(PROXY_list)
except:
        pass
try:
        # university(Proxy_on)
        pass
except:

        pass
# find_on_proxy_range(University_port_checked,university_Proxy_on)
#mains()
#cd /var/lib/openshift/55cda3827628e1f4a200002d/app-root/runtime/repo/www/all_functions/configs/proxy_scraper
# cd ~/app-root/runtime/repo/diy/all_functions/configs/proxy_scraper
#nohup sh -c " ~/app-root/runtime/srv/python/bin/python     IPProxyScraper.py --mode=5  "> $OPENSHIFT_LOG_DIR/35python_modules_install3.log /dev/null 2>&1 &
# bash -i -c 'tail -f  $OPENSHIFT_LOG_DIR/35python_modules_install3.log'


#nohup sh -c " ~/app-root/runtime/srv/python/bin/python     IPProxyScraper.py  "> $OPENSHIFT_LOG_DIR/1python_modules_install3.log /dev/null 2>&1 &
#tail -f  $OPENSHIFT_LOG_DIR/1python_modules_install3.log

if __name__ == '__main__':

    print("Content-type: text/html")
    # print data
    page = """
    <html>
    <head>
    <title>Hello World Page!</title>
    </head>
    <body>
    <p>Hello World</p>
    </body>
    </html>
    """
    print (page)
    from optparse import OptionParser

    parser = OptionParser(description=__doc__)
    help1 = 'Address url file name to be checked for proxy testing like:"www.google.com"\n' + \
            "Please make attention 'www.google.com' is risky use  only with" + '"blabla"'
    parser.add_option('-u', '--url', type='string', dest='url', help=help1,
                      default='..//..//configs//sites_proxy//all_proxies_list//site_list.txt')
    parser.add_option('-U', '--url_to_scap_proxy', type='string', dest='url_to_scap_proxy', help='\n Url to scrap proxy and ips like :http://hide-my-ass.com',
                      default='..//..//configs//sites_proxy//all_proxies_list//Sites_to_get_proxylist.txt')
    parser.add_option('-p','--proxy_on_list', dest='proxy_on_list', help=' proxy setting for url file name to be download like:.//proxy_on.txt',
                      default='..//..//configs//sites_proxy//all_proxies_list//Proxy_on.txt')
    # parser.add_option('-s','--user', dest='proxy_list', help='user & password of proxy setting')
    parser.add_option('-i','--prot_range', dest='prot_range', help='port_range for scrapping proxy example='+"""['80','8080','1080','3128','8888','8123','8118','8081','6588','4444','9999','443','8121','7004','8118','6903'] or =all for 1 to 1025"""
                      , default=['80','8080','1080','3128','8888','8123','8118','8081','6588','4444','9999','443','8121','7004','8118','6903'])
    parser.add_option('-w','--proxy_un_all', dest='proxy_un_all', help='get whois for all scraped proxy ip in this file defualt is =..//..//configs//sites_proxy//all_proxies_list//Proxy_university_checked_by_whois.txt',
                      default='..//..//configs//sites_proxy//all_proxies_list//Proxy_university_checked_by_whois.txt')

    parser.add_option('-l', '--scraped_list', dest='scraped_list',
                      help='list file  proxy for checkig via url like =..//..//configs//sites_proxy//all_proxies_list//scraped_list.txt',
                      default='..//..//configs//sites_proxy//all_proxies_list//scraped_list.txt')
    parser.add_option('-v', '--University_port_checked', dest='University_port_checked',
                      help='list file  proxy for writing alive university proxy via url like =..//..//configs//sites_proxy//all_proxies_list//University_port_checked.txt',
                      default='..//..//configs//sites_proxy//all_proxies_list//University_port_checked.txt')
    parser.add_option('-V', '--university_Proxy_on', dest='university_Proxy_on',
                      help='list file  proxy for writing alive proxy based of hosts via url like =..//..//configs//sites_proxy//all_proxies_list//university_Proxy_on.txt',
                      default='..//..//configs//sites_proxy//all_proxies_list//university_Proxy_on.txt')
    parser.add_option('-t', '--time', dest='timeout', help='default timeout to end connection=10', default=20)
    parser.add_option('-m', '--mode', dest='mode', help='mode:1 for scraping proxy from url.txt\n'
                                                        '\n mode2:find working proxy from scraped_list.txt'
                                                        '\n Mode3:find university ip by whois form  Proxy_on.txt or scraped_list.txt'
                                                        '\n Mode4:find onlive university proxy from University_port_checked.txt '
                                                        '\n Mode5:find university proxy in range given and saving in university_Proxy_on.txt '
                                                        '\n Mode6:Doing  all step in one mode 1 to 5 in 6 ')
    # parser.add_option('-o', dest='outdir', help='outputdir used with option -d', default='tmp')
    options, args = parser.parse_args()
    if options.url:
        url_to_check_proxy=options.url
        # proxy_checker(options.url, options.list, options.alive, options.alive_host, options.timeout)

    if options.timeout:
        timeout=int(options.timeout)
    if options.proxy_on_list:
        Proxy_on=options.proxy_on_list
    else:
        Proxy_on='..//..//configs//sites_proxy//all_proxies_list//Proxy_on.txt'
    if options.prot_range:
        prot_range=options.prot_range
    if options.proxy_un_all:
        Proxy_university_checked_by_whois=options.proxy_un_all
    else:
        Proxy_university_checked_by_whois='..//..//configs//sites_proxy//all_proxies_list//Proxy_university_checked_by_whois.txt'

    if options.scraped_list:
        PROXY_list=options.scraped_list
    else:
        PROXY_list="..//..//configs//sites_proxy//all_proxies_list//scraped_list.txt"

    if options.University_port_checked:
        University_port_checked=options.University_port_checked
        # find_on_proxy_range(University_port_checked,university_Proxy_on)
    else:
        University_port_checked="..//..//configs//sites_proxy//all_proxies_list//University_port_checked.txt"

    if options.university_Proxy_on:
        university_Proxy_on=options.university_Proxy_on
    else:
        university_Proxy_on='..//..//configs//sites_proxy//all_proxies_list//university_Proxy_on.txt'
    # options.mode='3'

    try:
        if options.mode==None:
            options.mode='1'
            # options.url_to_scap_proxy='http://proxyrox.com/inactive-proxies?p=1'
    except:
        pass
    if options.mode=='1':
        # if not re.findall('http',options.url_to_scap_proxy):
        #     f=open(options.scraped_list,'w+');f.close();
        #     pr=get_proxy_list(options.url_to_scap_proxy);
        #     proxy_list=pr
        # else:
        #     proxies=Scrape(options.url_to_scap_proxy)
        if not re.findall('http',options.url_to_scap_proxy):
            f=open(options.scraped_list,'w+');f.close();
            f=open(options.url_to_scap_proxy,'r');data=f.readlines();f.close();
            # uniqlines = set(open(options.url_to_scap_proxy).readlines())
            # bar = open(options.url_to_scap_proxy, 'w').writelines(set(uniqlines))
            # bar.close();
            # data=set(data);
            data = list(set(data))
            fr= open(options.url_to_scap_proxy, "w+");
            data_new=data
            fr.writelines(data_new)
            fr.close()
            pip0=xgoogle_search('free proxy list')
            # pip0=pygoogle_1('free proxy list')

            for x in range(len(pip0),0,-1):
                fr= open(options.url_to_scap_proxy, "r");
                data=fr.read();
                fr.close();
                pip=pip0[x-1]
                if re.search("%s" %(pip.replace('\n','')),data):
                    print pip.replace('\n','')+" is repeated" ;
                    # fr.close()
                else:
                    fr= open(options.url_to_scap_proxy, "w+");
                    data_new=pip.replace('\n','')+'\n'+data
                    fr.writelines(data_new)
                    # fr.writelines("%s" %(pip.replace('\n',''))+ '\n');
                    fr.close()

            f=open(options.url_to_scap_proxy,'r');websites=f.readlines();f.close();
            # for url in websites:
				# if True:
				# 	if(url):
				# 		print '%'*60+'proxy find from this url :\n'+url.replace('\n','')
				# 		Scrape(url.replace('\n',''))

            for url in websites:
                try:
                    print '%'*60+'proxy find from this url :\n'+url.replace('\n','')
                    Scrape(url.replace('\n',''))
                except:
                    pass
            print("\n\tFile has been saved!\n\tYou can find it under "+options.scraped_list+"\n")
            # pr=get_proxy_list(options.url_to_scap_proxy);
            # proxy_list=pr
        else:
            print '%'*60+'proxy find from this url :\n'+options.url_to_scap_proxy.replace('\n','')
            proxies=Scrape(options.url_to_scap_proxy)
        if True:
                f=open(options.scraped_list,'r');
                data=f.readlines();
                f.close();
                # uniqlines = set(open(options.url_to_scap_proxy).readlines())
                # bar = open(options.url_to_scap_proxy, 'w').writelines(set(uniqlines))
                # bar.close();
                # data=set(data);
                data = list(set(data))
                fr= open(options.scraped_list, "w+");
                data_new=data
                fr.writelines(data_new)
                fr.close()
    elif options.mode=='2':
        find_on_proxy(PROXY_list,Proxy_on)
    elif options.mode=='3':#whois for finding university and save in Proxy_university_checked_by_whois
        university(PROXY_list,Proxy_university_checked_by_whois)
    elif options.mode=='4':
        find_on_proxy(Proxy_university_checked_by_whois,university_Proxy_on)
    elif options.mode=='5':
        find_on_proxy_range(Proxy_university_checked_by_whois,university_Proxy_on)
    elif options.mode=='6':
        if not re.findall('http',options.url_to_scap_proxy):
            f=open(options.scraped_list,'w+');f.close();
            f=open(options.url_to_scap_proxy,'r');websites=f.readlines();f.close();
            for url in websites:
				if True:
					if(url):
						Scrape(url.replace('\n',''))
            # pr=get_proxy_list(options.url_to_scap_proxy);
            # proxy_list=pr
        else:
            proxies=Scrape(options.url_to_scap_proxy)
        find_on_proxy(PROXY_list,Proxy_on)#2
        university(PROXY_list,Proxy_university_checked_by_whois)#3
        find_on_proxy(Proxy_university_checked_by_whois,university_Proxy_on)#4
        find_on_proxy_range(Proxy_university_checked_by_whois,university_Proxy_on)#5

    else:
        parser.print_help()
        pass
