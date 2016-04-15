#!"E:/Program Files win 7 2nd/Python27/python.exe"

import sys,cookielib,random
import urlparse
import re,os
import mechanize,socket
import urllib,urllib2
from urlparse import urlparse as urlparse2
from os.path import basename
from urlparse import urlsplit
from proxy_checker3_all_function import is_bad_proxy,make_txt_file

print "Content-type: text/html\n"
print ''
print '<pre>'
deftimeout=200
socket.setdefaulttimeout(deftimeout)

def import_mod(**kwargs):
    # import_mod(from_module='sss',from_module2='s')
    from_module_name1=kwargs['from_module']
    try:
        kwargs['from_module2']
        from_module_name2=kwargs['from_module2']
    except:from_module_name2=''

    try:
        kwargs['dir_location']
        CurrentDir=os.path.dirname(os.path.realpath(__file__))
        s=CurrentDir.replace('\\','/')+kwargs['dir_location']
        sys.path.insert(0,s)
    except:pass
    if from_module_name1 in sys.modules:
        print "@@@@@@@@@@@@@@ module already exist  for "+  from_module_name1+' is \n: @@@@@@@@@@@@@@\n\n'
        if from_module_name2=='':
            mod=sys.modules[from_module_name1]
        else:
            mod1=sys.modules[from_module_name1]
            mod = getattr(mod1,from_module_name2)
            print "@@@@@@@@@@@@@@ module already exist  for "+  from_module_name1+'.'+from_module_name2+' is \n: @@@@@@@@@@@@@@\n\n'
    else:
        print "@@@@@@@@@@@@@@ module inserting for "+from_module_name1+"  \n: @@@@@@@@@@@@@@\n\n"
        if from_module_name2=='':
            mod=__import__(from_module_name1)
        else:
            mod1=__import__(from_module_name1)
            mod = getattr(mod1,from_module_name2)
            # mod = getattr(mod1,from_module_name2)
            pass
            print's'
            # mod=mod1[from_module_name2]
    return mod

def url2name(pdf_url):
    if pdf_url.absolute_url is locals():
        url=pdf_url.absolute_url
    else: url=pdf_url
    localName = basename(urlsplit(url)[2])
    # localName=urlparse.urlsplit(pdf_url).path.split('/')[-1]
    req = urllib2.Request(url)
    r = urllib2.urlopen(req)
    if r.info().has_key('Content-Disposition'):
        # If the response has Content-Disposition, we take file name from it
        localName = r.info()['Content-Disposition'].split('filename=')[1]
        if localName[0] == '"' or localName[0] == "'":
            localName = localName[1:-1]
        elif r.url != url:
        # if we were redirected, the real file name we take from the final URL
            localName = url2name(r.url)
        if localFileName:
            # we can force to save the file as specified name
            localName = localFileName
    return localName

def file_rd(path,mode='r',main_data='0'):
    # proxylist = open(path).read().split('\n')
    f = open(path, mode)
    if main_data=='0':
        data=f.read().split('\n')
    else:
        data=f.read()
        # data=f.readlines()
    # print data
    f.close
    return data
def file_save(data,folder_name,pathname):
    f = open(os.path.join(folder_name,pathname), 'wb')
    f.write(data)
    f.close()
    return os.getcwd()+"\\"+os.path.join(folder_name,pathname)

def usr_tag(pip):
    z='--'
    try :
        s=pip.split('USER:'+z)[1].split(":")[0]
        proxy_info = {
            'user' : pip.split('USER:'+z)[1].split(":")[0],
            'pass' : pip.split('USER:'+z)[1].split(z)[0].split(":")[1],
            'user_tag' : pip.split('Form_Tag:'+z)[1].split(":")[0],
            'pass_tag' : pip.split('Form_Tag:'+z)[1].split(z)[0].split(":")[1],
            'submit_tag_name' : pip.split('Submit_tag:'+z)[1].split(":")[0],
            'submit_tag_value' : pip.split('Submit_tag:'+z)[1].split(z)[0].split(":")[1],
            'Form_id': pip.split('Form_id:'+z)[1].split(z)[0],
            'Form_Type': pip.split('Form_Type:'+z)[1].split(z)[0],
            'Log_test': pip.split('Log_test:'+z)[1].split(z)[0].replace('\n', '') # or 8080 or whatever
        }
        # proxy_="http://%(user)s:%(pass)s@%(host)s:%(port)s" % proxy_info
        # proxy_handler = urllib2.ProxyHandler({"http" : "http://%(user)s:%(pass)s@%(host)s:%(port)s" % proxy_info})
    except:
        proxy_info = {
            'Form_Tag' : pip.split('Form_Tag:')[1].replace('\n', '') # or 8080 or whatever
        }
    return  proxy_info
def soap_my(req):
    from BeautifulSoup import BeautifulSoup
    import re
    # soup = BeautifulSoup(file(req).read())
    soup = BeautifulSoup((req))

    for link in soup.findAll('frame', attrs={'src': re.compile("http://ieeexplore.ieee.org/*.pdf")}):
        print link.get('src')

		
def getWorkingProxy(proxyList,url='http://www.google.com'):
    k=-1
    i=-1
    index=[]
    sites=[]
    workproxy=[]
    time_diff2=[]
    for j in range(i+1, len(proxyList)):
        currentProxy = proxyList[j]
        # [T_F,site,time_diff]=is_bad_proxy(currentProxy,url)

        [T_F,site,time_diff]=is_bad_proxy_urlib(currentProxy,url)
        # if not is_bad_proxy(currentProxy,url):
        proxy_,proxy_han,user_pass= make_proxy_handler(currentProxy)
        # proxy_=proxy_.split("http://")[1]
        if not T_F:
            k=k+1
            # log("%s is working" % (currentProxy))
            print("%s is working for site " % proxy_ +site+" With Time  "+str(time_diff))
            workproxy.append(currentProxy)
            sites.append(site)
            time_diff2.append(time_diff)
            index.append(j)
            # return currentProxy, j
        else:
            # log("Bad Proxy %s" % (currentProxy))
            make_txt_file("configs//badproxylist.txt",proxy_,site,time_diff)
            print("%s is Bad Proxy for site " % proxy_ + site+" With Time "+str(time_diff))
            # print ("Bad Proxy %s" % (currentProxy))
    return workproxy, index,sites,time_diff2

def proxy_checker(test_url="http://stackoverflow.com",input_file = 'configs//sites_proxy//proxylist.txt',output_file = 'configs//proxy_alive.txt',site_file="configs//sites_proxy//",defaulttimeout=30):
# input_file = 'configs\\proxylist.txt'
# proxy_list = open(input_file, 'r')
# proxy_type = 'http'
# output_file = 'proxy_alive.txt'
# # ip_check_url = 'http://automation.whatismyip.com/n09230945.asp'
# ip_check_url="http://www.icanhazip.com/"
# test_url="http://stackoverflow.com"
# test_url="http://ip.42.pl/raw"
  socket.setdefaulttimeout(defaulttimeout)
# proxyList = getProxiesList()
# for host in open(input_file).readlines():
#  g= host.strip()
  hosts = [host.strip() for host in open(input_file).readlines()]
# pr=['198.27.97.214:3127', '202.202.0.163:3128']
  i=-1
  proxyList=[]
  for j in range(i+1, len(hosts)):
    if ( not re.findall("#",hosts[j])):
        proxyList.append(hosts[j])

  # proxyList=hosts
  # proxy=['151.236.14.48:80@ user:pass For Site:http://stackoverflow.com']
  # sites=['stackowerflow.com']
  proxy, index,sites,time_diff = getWorkingProxy(proxyList,test_url)
  if proxy!=[]:
    # _web = getOpener(proxy)
    # saveAlive = open("configs//proxy_alive.txt", 'wb')
    i=-1
    for j in range(i+1, len(proxy)):
        if  re.findall("For Site:",proxy[j]):
            proxy1=proxy[j].split("For Site:")[0]
            proxy2=proxy[j].split("For Site:")[1]
            if  re.findall(sites[j],proxy2):
                pass
            else:
                # replace("configs//sites_proxy//"+sites[j]+".txt", proxyList[j],proxy1+"For Site:"+proxy2+";"+sites[j])
                make_txt_file(site_file+sites[j]+".txt",proxy1,sites[j],time_diff[j])
                make_txt_file(output_file,proxy1,sites[j],time_diff[j])

        else:
            proxy1=proxy[j]
            make_txt_file(site_file+sites[j]+".txt",proxy1,sites[j],time_diff[j])
            make_txt_file(output_file,proxy1,sites[j],time_diff[j])
    sort_file(site_file+sites[j]+".txt"," Rs_Time ")
    sort_file(output_file," Rs_Time ")



  # return make_returning_proxy(site_file,test_url)

		
def make_proxy_handler(pip=None):
    proxy_handler=[]
    user_pass=[]
    proxy_=[]
    if pip:
        try :
            pip.split('@')[1]

            proxy_info = {
                'user' : pip.split('@')[1].split(":")[0],
                'pass' : pip.split('@')[1].split(":")[1].replace('\n', ''),
                'host' : pip.split('@')[0].split(":")[0],
                'port' : pip.split('@')[0].split(":")[1] # or 8080 or whatever
            }
            user_pass="%(user)s:%(pass)s"% proxy_info
            proxy_="%(host)s:%(port)s" % proxy_info
            proxy_handler = {"http" : "http://%(user)s:%(pass)s@%(host)s:%(port)s" % proxy_info}
        except:
            proxy_info = {
                'host' : pip.split(":")[0],
                'port' : pip.split(":")[1].replace('\n', '') # or 8080 or whatever
            }
            s=pip.split("#")
            ss=re.findall("#",pip)
            if  re.findall("#",pip):
                return False
            else:
            # b="http://%(host)s:%(port)d" % proxy_info
                proxy_="%(host)s:%(port)s" % proxy_info
                proxy_handler = {"http" : "http://%(host)s:%(port)s" % proxy_info}

    return proxy_,proxy_handler,user_pass


def make_returning_proxy(input_file,test_url,proxy_alive='configs//proxy_alive.txt'):
    from urlparse import urlsplit,urlparse
    site= urlparse(test_url).hostname
    l=0
    proxy_handler=[]
    pr_h=[]
    proxy_h=[]
    user_pass_h=[]
    try:
        listhandle = open(input_file+site+".txt").readlines()
        # sort_file(name,text_to_sort)
        for line in listhandle:
            if  re.findall("For Site:",line):
                proxy1=line.split("For Site:")[0]
                proxy2=line.split("For Site:")[1]

                # proxyList.append(proxy1)
                pr,proxy_han,user_pass=make_proxy_handler(proxy1)
                # if pr!=[]:
                pr_h.append(pr)
                # if proxy_han!=[]:
                proxy_h.append(proxy_han)
                # if user_pass!=[]:
                user_pass_h.append(user_pass)
    except:
        listhandle = open(proxy_alive).readlines()
        for line in listhandle:
            if  re.findall(site,line):
                if  re.findall("For Site:",line):
                    proxy1=line.split("For Site:")[0]
                    proxy2=line.split("For Site:")[1]
                    if  re.findall(site,proxy2):
                    # proxyList.append(proxy1)
                        pr,proxy_han,user_pass=make_proxy_handler(proxy1)
                        # if pr!=[]:
                        pr_h.append(pr)
                        # if proxy_han!=[]:
                        proxy_h.append(proxy_han)
                        # if user_pass!=[]:
                        user_pass_h.append(user_pass)
        if pr_h==[]:
            proxy_checker(test_url,input_file+"proxylist.txt",proxy_alive,input_file,30)
            try:
                listhandle = open(input_file+site+".txt").readlines()

                for line in listhandle:
                    if  re.findall("For Site:",line):
                        proxy1=line.split("For Site:")[0]
                        proxy2=line.split("For Site:")[1]

                        # proxyList.append(proxy1)
                        pr,proxy_han,user_pass=make_proxy_handler(proxy1)
                        # if pr!=[]:
                        pr_h.append(pr)
                        # if proxy_han!=[]:
                        proxy_h.append(proxy_han)
                        # if user_pass!=[]:
                        user_pass_h.append(user_pass)
            except:
                pass
        try:
            listhandle = open(input_file+site+".txt").readlines()
        except:
            proxy_checker(test_url,input_file+"proxylist.txt",proxy_alive,input_file,30)
            #             pip=proxy1
            # # if l==1:
            #             try :
            #                 pip.split('@')[1]
            #                 proxy_info = {
            #                     'user' : pip.split('@')[1].split(":")[0],
            #                     'pass' : pip.split('@')[1].split(":")[1].replace('\n', ''),
            #                     'host' : pip.split('@')[0].split(":")[0],
            #                     'port' : pip.split('@')[0].split(":")[1] # or 8080 or whatever
            #                 }
            #                 proxy_handler.append("http://%(user)s:%(pass)s@%(host)s:%(port)s" % proxy_info)
            #             except:
            #                 proxy_info = {
            #                     'host' : pip.split(":")[0],
            #                     'port' : pip.split(":")[1].replace('\n', '') # or 8080 or whatever
            #                 }
            #                 proxy_handler.append("http://%(host)s:%(port)s" % proxy_info)
    return pr_h,proxy_h,user_pass_h
    # proxyList.append( proxy1.split('@')[0])
    # details= proxy1.split('@')
    # email = details[1].split(':')[0]
    # password = details[1].split(':')[1].replace('\n', '')

    # else:
    #     file_string[j]=proxy1+"For Site:"+proxy2+";"+subst

def login_urlib(url,form_data):
    username="%(user)s"%form_data
    password="%(pass)s"%form_data
    user_tag="%(user_tag)s"%form_data
    pass_tag="%(pass_tag)s"%form_data
    Form_id="%(Form_id)s"%form_data
    log_done="%(Log_test)s"%form_data
    submit_tag_name="%(submit_tag_name)s:"%form_data
    submit_tag_value="%(submit_tag_value)s:"%form_data


    login_data=urllib.urlencode({user_tag:username,pass_tag:password,submit_tag_name:submit_tag_value}) # replace username and password with filed name
    # import os
    # os.environ['http_proxy']=''
    req2 = urllib2.urlopen(url,login_data,timeout=44)

    # rsp2 = ClientCookie.urlopen(req2)
    print req2.readlines()
    return req2

def login_to_site(url,form_data,proxy=[],User_Pass=[]):
    username="%(user)s"%form_data
    password="%(pass)s"%form_data
    user_tag="%(user_tag)s"%form_data
    pass_tag="%(pass_tag)s"%form_data
    Form_id="%(Form_id)s"%form_data
    log_done="%(Log_test)s"%form_data
    br = mechanize.Browser(factory=mechanize.RobustFactory())
    # Browser options
    br.set_handle_robots(False)
    br.set_handle_referer(True)
    br.set_handle_refresh(True)

    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)



    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    cookie3=''.join([random.choice(chars) for x in range(5)])+".txt"
    cj = cookielib.LWPCookieJar()
    # cj.revert(cookie3)
    opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cj))

    br.set_cookiejar(cj)
    try :
        fo=os.getcwd()
        os.chdir(fo)
        os.mkdir(fo+"\\cookies\\")
    except:
        pass
    pathname = os.path.join("cookies", cookie3)
    cj.save(pathname)
    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # Want debugging messages?
    # User-Agent (this is cheating, ok?)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    # txheaders = {
    #     'Accept':'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
    #     'Accept-Language':'en,hu;q=0.8,en-us;q=0.5,hu-hu;q=0.3',
    #     'Accept-Encoding': 'gzip, deflate',
    #     'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    #     'Keep-Alive': '300',
    #     'Connection': 'keep-alive',
    #     'Cache-Control': 'max-age=0',
    # }
    #
    # req = urllib2.Request(url, txheaders)
    # req2 = urllib2.urlopen(req)
    # print req2





    if proxy != [] and not(re.findall('None:None', proxy)):
        br.proxies=br.set_proxies({"http": proxy})
        # br.proxies=br.set_proxies( proxy)

    if User_Pass!= [] and not(re.findall('None:None', User_Pass)):
        br.add_proxy_password(User_Pass.split(":")[0],User_Pass.split(":")[1])

    try:
        br.open(url)
    except urllib2.HTTPError, e:
       print "Got error code", e.code
       try:
           br.open(url)
       except urllib2.HTTPError, e:
           print "Got error code", e.code
    except urllib2.URLError, e:
        print "Got error code", e.code

    # os.environ['http_proxy']=''

    if br.forms():
        print [form for form in br.forms()]
        # br.select_form(name="USER")
        # [f.id for f in br.forms()]
        formcount=done=0
        for form in br.forms():
            if form.attrs['id'] == Form_id:
                br.form = form
                done=1
            if done==0:formcount=formcount+1

        formcount=0
        for frm in br.forms():
            if str(frm.attrs["id"])==Form_id:
                done=1
            if done==0:formcount=formcount+1

        br.select_form(nr=formcount)
        # br.select_form(nr = 0)
        br[user_tag] = username
        br[pass_tag] = password
        br.submit()

    print br.response().get_data()
    # print current url
    print "We are now at:", br.geturl()
    # print error
    if br.geturl() == url:
        print "Login Failed"
    else: print "Successfully logged in"

    if log_done in br.response().get_data():
        print ("You are logged on to the Public Access to Court Electronic "
              "Records (PACER) Case Search website as "+ username + ". All costs "
                                                                 "will be billed to this account.")
        for link in br.links():
            print "<li><a>"
            print (link)
            print "</a></li>"
            print "<li><a>"
            print link.base_url
            print "</a></li>"

    else:
        raise ValueError("Could not login to PACER Case Search. Check your "
                         "username and password")
    return br
def download_mechanize():
    browser = mechanize.Browser(factory=mechanize.RobustFactory())
    browser.set_handle_robots(False)
    url="http://164.100.247.17/"
    browser.open(url)
    # browser.follow_link(text="Package Index", nr=0)
    # for form in browser.forms():
    #     if form.attrs['id'] == 'password':
    #         browser.form = form
    d= browser.select_form(nr=0)
    browser["user"] = self.username
    browser["passwd"] = self.password
    browser.submit()

    browser.select_form(name="password")
    browser.select_form(name="user")
    browser.select_form(name="searchform")
    browser.form["term"] = "mechanize"
    browser.submit()
    browser.follow_link(text_regex="mechanize-?(.*)")
    link = browser.find_link(text_regex=r"\.tar\.gz")
    filename = os.path.basename(urlparse.urlsplit(link.url)[2])
    if os.path.exists(filename):
        sys.exit("%s already exists, not grabbing" % filename)
    browser.retrieve(link.url, filename)

def twill_work(url):
    import twill
    import twill.commands
    # from twill import get_browser
    # b = get_browser()
    # b.go(url)
    # print b.result.page
    import os
    os.environ['http_proxy'] = 'http://222.66.115.233:80'

    t_com = twill.commands
    ## get the default browser
    t_brw = t_com.get_browser()
    ## open the url
    # url = 'http://google.com'
    t_brw.go(url)
    print t_brw.result.page
    ## get all forms from that URL
    all_forms = t_brw.get_all_forms()         ## this returns list of form objects
    print "Forms:"
    t_brw.showforms()

    ## now, you have to choose only that form, which is having POST method

    for each_frm in all_forms:

        attr = each_frm.attrs             ## all attributes of form
    if each_frm.method == 'post':
        ctrl = each_frm.controls    ## return all control objects within that form (all html tags as control inside form)
        for ct in ctrl:
            if ct.type == 'text':     ## i did it as per my use, you can put your condition here
                ct._value = "twill"
                t_brw.clicked(each_frm,ct.attrs['name'])            ## clicked takes two parameter, form object and button name to be clicked.
                t_brw.submit()

    ## you might write the output (submitted page) to any file using content = t_brw.get_html()
    ## dont forget to reset the browser and putputs.

    try:
        from twill.commands import go, showforms, formclear, fv, show, submit
        # Force try using the first form found on a page.
        t_com.formclear('1')
        t_com.fv("1", "usern", "test_name")
        t_com.fv("1", "passw", "test_pass")
        t_com.submit('0')
        content = t_com.show()
        print 'debug twill post content:', content

    except urllib2.HTTPError, e:
        sys.exit("%d: %s" % (e.code, e.msg))
    except IOError, e:
        print e
    except:
        pass
    t_com.reset_browser
    t_com.reset_output

class TWILL_Browser(object):
       def __init__(self, url="http://www.slashdot.org",form_data=None):

            self.a=twill.commands
            try:
                [self.proxy,self.proxy_h,self.prx_pass]=make_returning_proxy('configs//sites_proxy//',url,'configs//proxy_alive.txt')
            except:
                pass
            self.url=url
            self.username="%(user)s"%form_data
            self.password="%(pass)s"%form_data
            self.user_tag="%(user_tag)s"%form_data
            self.pass_tag="%(pass_tag)s"%form_data
            self.Form_id="%(Form_id)s"%form_data
            self.submit_tag_name="%(submit_tag_name)s"%form_data
            self.submit_tag_value="%(submit_tag_value)s"%form_data
            self.Form_Type="%(Form_Type)s"%form_data
            self.log_done="%(Log_test)s"%form_data
            self.a.config("readonly_controls_writeable", 1)
            self.b = self.a.get_browser()
            self.b.set_agent_string("Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14")
            self.b.clear_cookies()

       def slashdot(self):
          self.b.go(self.url)
          t_brw=self.b
          print t_brw.result.page
          ## get all forms from that URL
          all_forms = t_brw.get_all_forms()         ## this returns list of form objects
          print "Forms:"
          t_brw.showforms()
          formnumberr=1
          for each_frm in all_forms:
              attr = each_frm.attrs             ## all attributes of form
              if each_frm.method == 'POST' and each_frm.attrs['id']==self.Form_id:

                  f = self.b.get_form(formnumberr)
              regexp = re.compile(self.submit_tag_value)
              link = self.b.find_link(regexp)
              if link:
                self.b.follow_link(link)
                f=self.b.get_form(self.Form_id)
                f[self.user_tag] = self.username
                f[self.pass_tag] = self.password
                self.a.fv("2", self.submit_tag_name, self.submit_tag_value)
              formnumberr=formnumberr+1


          return self

       def twill_work_form(self):

           # from twill import get_browser
           # b = get_browser()
           # b.go(url)
           # print b.result.page

           try:
               os.environ['http_proxy'] = 'http://'+''.join(self.proxy)
               # os.environ['http_proxy'] = 'http://222.66.115.233:80'
           except:
               pass



           t_com = twill.commands
           t_com.reset_browser
           t_com.reset_output
           t_com = twill.commands
           ## get the default browser
           t_brw = t_com.get_browser()
           ## open the url
           # url = 'http://google.com'
           t_brw.go(url)
           html=t_brw.result.page
           print html
           # print fill_login_form(url, html, "john", "secret")

           ## get all forms from that URL
           all_forms = t_brw.get_all_forms()         ## this returns list of form objects
           print "Forms:"
           t_brw.showforms()

           ## now, you have to choose only that form, which is having POST method

           self.formnumber=0
           formnumber=1
           for each_frm in all_forms:
               self.formnumber=1+self.formnumber
               attr = each_frm.attrs             ## all attributes of form
               try:
                   form_id=each_frm.attrs['id']
               except:
                   form_id=''

               if each_frm.method == 'POST' and (form_id==self.Form_id ) :


                   t_com.formclear(formnumber)
                   t_com.fv(self.formnumber, self.user_tag, self.username)
                   t_com.fv(self.formnumber, self.pass_tag, self.password)
                   all_forms = t_brw.get_all_forms()         ## this returns list of form objects
                   print "Forms:"
                   t_brw.showforms()
                   # t_com.submit(self.formnumber)
                   # t_brw.submit(self.submit_tag_name)
                   t_com.submit(self.submit_tag_name)
                   #
                   content = t_com.show()
                   print 'debug twill post content:', content
                   t_com.save_cookies(cookies)
                   t_brw.load_cookies(cookies)

               if each_frm.method == 'POST' and each_frm.attrs['id']==self.Form_id:


                   t_com.formclear(formnumber)
                   t_com.fv(self.formnumber, self.user_tag, self.username)
                   t_com.fv(self.formnumber, self.pass_tag, self.password)
                   all_forms = t_brw.get_all_forms()         ## this returns list of form objects
                   print "Forms:"
                   t_brw.showforms()
                   # t_com.submit(self.formnumber)
                   # t_brw.submit(self.submit_tag_name)
                   t_com.submit(self.submit_tag_name)
                   #
                   content = t_com.show()
                   print 'debug twill post content:', content
                   t_com.save_cookies(cookies)
                   t_brw.load_cookies(cookies)

                   t_brw.go('http://johnny.heliohost.org:2082/frontend/x3/index.phpcp')
                   print t_brw.find_link('http://64.62.211.131:2082/frontend/x3/mail/fwds.html')
                   print t_com.show_extra_headers()
                   print t_com.show_cookies()
                   print t_com.showlinks()
                   print t_brw.result.page

                   each_frm=t_brw.get_form(self.Form_id)
                   ctrl = each_frm.controls    ## return all control objects within that form (all html tags as control inside form)
                   for ct in ctrl:

                       if ct.attrs['name']==self.user_tag and ct.type=='text':     ## i did it as per my use, you can put your condition here
                           ct._value = self.username
                           # t_brw.clicked(each_frm,ct.attrs['name'])            ## clicked takes two parameter, form object and button name to be clicked.
                           # each_frm2=t_brw.get_form(1)
                           # t_com.fv(ct, self.user_tag, self.username)


                       if ct.attrs['name']==self.pass_tag and ct.type=='password':     ## i did it as per my use, you can put your condition here
                           ct._value = self.password
                           # t_com.fv(formnumber, self.pass_tag, self.password)
                           # t_brw.clicked(each_frm,ct.attrs['name'])            ## clicked takes two parameter, form object and button name to be clicked.

                       if ct.type == self.Form_Type and ct.attrs['name']==self.submit_tag_name:
                           t_brw.clicked(each_frm,self.submit_tag_name)
                           t_brw.submit(formnumber)
                       formnumber=formnumber+1
                       all_forms = t_brw.get_all_forms()         ## this returns list of form objects
                       print "Forms:"
                       t_brw.showforms()

                       # t_com.fv(self.formnumber, self.user_tag, self.username)
                       # t_com.fv(self.formnumber, self.pass_tag, self.password)
                       # t_brw.clicked(each_frm,ct.attrs['name'])            ## clicked takes two parameter, form object and button name to be clicked.
                       # t_brw.get_form_field(each_frm,'login')
                       # t_com.formvalue()
                       # t_brw.submit(3)
                   html=t_brw.get_html()
                   print html
                   content = t_com.show()
                   print 'debug twill post content:', content
                   # print t_brw.go('http://127.0.0.1/trash/test/elec-lab.tk%20Mover-201312290438/fa/admin/config')
                   t_brw.go('http://64.62.211.131:2082/frontend/x3/mail/fwds.html')
                   print t_brw.find_link('http://64.62.211.131:2082/frontend/x3/mail/fwds.html')
                   print t_com.show_extra_headers()
                   print t_com.show_cookies()
                   print t_brw.result.page

           ## you might write the output (submitted page) to any file using content = t_brw.get_html()
           ## dont forget to reset the browser and putputs.
           print t_brw.find_link(text="Full Text as PDF",url_regex=re.compile("/stamp/stamp.jsp?tp=&arnumber"))


           try:
               from twill.commands import go, showforms, formclear, fv, show, submit
               # Force try using the first form found on a page.
               t_com.formclear('1')
               t_com.fv("1", "usern", "test_name")
               t_com.fv("1", "passw", "test_pass")
               t_com.submit('0')
               content = t_com.show()
               print 'debug twill post content:', content

           except urllib2.HTTPError, e:
               sys.exit("%d: %s" % (e.code, e.msg))
           except IOError, e:
               print e
           except:
               pass
           t_com.reset_browser
           t_com.reset_output

       def twill_work(self):

            # from twill import get_browser
            # b = get_browser()
            # b.go(url)
            # print b.result.page

            try:
                os.environ['http_proxy'] = 'http://'+''.join(self.proxy)
                # os.environ['http_proxy'] = 'http://222.66.115.233:80'
            except:
                pass



            t_com = twill.commands
            t_com.reset_browser
            t_com.reset_output
            t_com = twill.commands
            ## get the default browser
            t_brw = t_com.get_browser()
            ## open the url
            # url = 'http://google.com'
            t_brw.go(url)
            html=t_brw.result.page
            print html
            links=t_brw.find_link('Full Text as PDF')
            print links
            t_com = twill.commands
            t_com.reset_browser
            t_com.reset_output
            t_com = twill.commands
            t_brw.go(links.absolute_url)
            file=t_brw.result.page
            print file

            links=t_brw.find_link('frameborder="0" src="http://ieeexplore.ieee.org/')
            [l2,l3]= t_com.showlinks()

            links=soap_my(file)
            print links
            t_com = twill.commands
            t_com.reset_browser
            t_com.reset_output
            t_com = twill.commands
            t_brw.go(l3.absolute_url)
            file=t_brw.result.page
            print file
            # files=t_brw.follow_link(links)
            # print files
            # url2name=basename(urlsplit(l3)[2])
            pathname = os.path.join("PDF_Files", url2name(l3.absolute_url))

            file_save(file,"PDF_Files",pathname)
            # from loginform import fill_login_form
            # import requests
            # # url = "https://github.com/login"
            # r = requests.get(url)
            # fill_login_form(url, r.text, "john", "secret")
            # print fill_login_form(url, html, "john", "secret")

           ## get all forms from that URL
            all_forms = t_brw.get_all_forms()         ## this returns list of form objects
            print "Forms:"
            t_brw.showforms()

            ## now, you have to choose only that form, which is having POST method

            self.formnumber=0
            formnumber=1
            for each_frm in all_forms:
                 self.formnumber=1+self.formnumber
                 attr = each_frm.attrs             ## all attributes of form
                 if each_frm.method == 'POST' and each_frm.attrs['id']==self.Form_id:


                        t_com.formclear(formnumber)
                        t_com.fv(self.formnumber, self.user_tag, self.username)
                        t_com.fv(self.formnumber, self.pass_tag, self.password)
                        all_forms = t_brw.get_all_forms()         ## this returns list of form objects
                        print "Forms:"
                        t_brw.showforms()
                        # t_com.submit(self.formnumber)
                        # t_brw.submit(self.submit_tag_name)
                        t_com.submit(self.submit_tag_name)
                        #
                        content = t_com.show()
                        print 'debug twill post content:', content
                        t_com.save_cookies(cookies)
                        t_brw.load_cookies(cookies)

                        t_brw.go('http://johnny.heliohost.org:2082/frontend/x3/index.phpcp')
                        print t_brw.find_link('http://64.62.211.131:2082/frontend/x3/mail/fwds.html')
                        print t_com.show_extra_headers()
                        print t_com.show_cookies()
                        print t_com.showlinks()
                        print t_brw.result.page

                        each_frm=t_brw.get_form(self.Form_id)
                        ctrl = each_frm.controls    ## return all control objects within that form (all html tags as control inside form)
                        for ct in ctrl:

                            if ct.attrs['name']==self.user_tag and ct.type=='text':     ## i did it as per my use, you can put your condition here
                                ct._value = self.username
                                # t_brw.clicked(each_frm,ct.attrs['name'])            ## clicked takes two parameter, form object and button name to be clicked.
                                # each_frm2=t_brw.get_form(1)
                                # t_com.fv(ct, self.user_tag, self.username)


                            if ct.attrs['name']==self.pass_tag and ct.type=='password':     ## i did it as per my use, you can put your condition here
                                ct._value = self.password
                                # t_com.fv(formnumber, self.pass_tag, self.password)
                                # t_brw.clicked(each_frm,ct.attrs['name'])            ## clicked takes two parameter, form object and button name to be clicked.

                            if ct.type == self.Form_Type and ct.attrs['name']==self.submit_tag_name:
                                t_brw.clicked(each_frm,self.submit_tag_name)
                                t_brw.submit(formnumber)
                            formnumber=formnumber+1
                            all_forms = t_brw.get_all_forms()         ## this returns list of form objects
                            print "Forms:"
                            t_brw.showforms()

                            # t_com.fv(self.formnumber, self.user_tag, self.username)
                            # t_com.fv(self.formnumber, self.pass_tag, self.password)
                            # t_brw.clicked(each_frm,ct.attrs['name'])            ## clicked takes two parameter, form object and button name to be clicked.
                            # t_brw.get_form_field(each_frm,'login')
                            # t_com.formvalue()
                            # t_brw.submit(3)
                        html=t_brw.get_html()
                        print html
                        content = t_com.show()
                        print 'debug twill post content:', content
                        # print t_brw.go('http://127.0.0.1/trash/test/elec-lab.tk%20Mover-201312290438/fa/admin/config')
                        t_brw.go('http://64.62.211.131:2082/frontend/x3/mail/fwds.html')
                        print t_brw.find_link('http://64.62.211.131:2082/frontend/x3/mail/fwds.html')
                        print t_com.show_extra_headers()
                        print t_com.show_cookies()
                        print t_brw.result.page

            ## you might write the output (submitted page) to any file using content = t_brw.get_html()
            ## dont forget to reset the browser and putputs.
            print t_brw.find_link(text="Full Text as PDF",url_regex=re.compile("/stamp/stamp.jsp?tp=&arnumber"))


            try:
                from twill.commands import go, showforms, formclear, fv, show, submit
                # Force try using the first form found on a page.
                t_com.formclear('1')
                t_com.fv("1", "usern", "test_name")
                t_com.fv("1", "passw", "test_pass")
                t_com.submit('0')
                content = t_com.show()
                print 'debug twill post content:', content

            except urllib2.HTTPError, e:
                 sys.exit("%d: %s" % (e.code, e.msg))
            except IOError, e:
                print e
            except:
                 pass
            t_com.reset_browser
            t_com.reset_output
       def splinter(self):
            from splinter import Browser

            with Browser('firefox') as browser:
                browser.visit(self.url)
                browser.find_by_name('element_name').click()

if __name__ == "__main__":
    site_list_form='configs/sites_form_user.txt'
    cookies='configs/cookies'

    url="http://164.100.247.17/"

    # url='http://johnny.heliohost.org:2082/login/'
    url='http://64.62.211.131:2082/'
    # url='http://207.211.9.100:80/'
    # url='http://31.170.167.5:80/'
    # url='http://free-papers.tk/cpanel'
    # url='http://johnny.heliohost.org:2082/login/'
    # url='http://127.0.0.1/trash/test/elec-lab.tk%20Mover-201312290438/'
    url='http://ieeexplore.ieee.org/ielx5/8981/28518/01274437.pdf?tp=&arnumber=1274437&isnumber=28518'
    url='http://ieeexplore.ieee.org/xpl/login.jsp?tp=&arnumber=1274437&url=http%3A%2F%2Fieeexplore.ieee.org%2Fxpls%2Fabs_all.jsp%3Farnumber%3D1274437'
    url='http://cpanel.1freehosting.com/'
    url='http://lib.just.edu.jo/login?url='
    proxy_checker3_all_function=import_mod(from_module='proxy_checker3_all_function')
    try:
        [proxy,proxy_h,prx_pass] = proxy_checker3_all_function.make_returning_proxy("configs//sites_proxy//", url)
        proxy='http://'+''.join(proxy)
        os.environ['http_proxy'] = proxy
        # os.environ['http_proxy'] = 'http://222.66.115.233:80'
    except:
        pass
    # [proxy,proxy_h,prx_pass]=proxy_checker3_all_function.make_returning_proxy('configs//sites_proxy//',url,'configs//proxy_alive.txt')



    listform=file_rd(site_list_form,'r')
    # file_input='configs/sites_proxy'
    host= urlparse2(url).hostname

    #timeout in seconds see http://docs.python.org/library/socket.html#socket.setdefaulttimeout
    socket.setdefaulttimeout(100)
    # os.environ['http_proxy']=''
    # import requests
    # content = requests.get(url)
    # print content

    # Navigate to Google
    for line in listform:
        if line.find(host)!=-1:
            form_data=usr_tag(line)
            # html=login_to_site(url,form_data)
            import twill.commands
            # t1=TWILL_Browser(url,form_data).splinter()
            # twill_work(url)
            # t=TWILL_Browser(url,form_data).slashdot()
            # tt=TWILL_Browser(url,form_data).twill_work()
            tt=TWILL_Browser(url,form_data).twill_work_form()
    try:

        txheaders = {
            'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
            'Accept-Language':'en,hu;q=0.8,en-us;q=0.5,hu-hu;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
            'Keep-Alive': '300',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Host':	'johnny.heliohost.org:2082',
            'Referer':'http://johnny.heliohost.org:2082/frontend/x3/index.phpcp',
            'X-Requested-With':	'XMLHttpRequest',
            'Cookie':'	cprelogin=no; cpsession=soheilsa%3aZTw6vgajGklrpoKSKboU0Rj0SRJvL65dK4Qgx22qJNe1mrrLeAOB5uil3gRLDK6V; _jsuid=2121790376; langedit=; lang='
            }

        y={'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
           'Connection': 'keep-alive',
           'Host': 'johnny.heliohost.org:2082',
           'Accept-Language': 'en,hu;q=0.8,en-us;q=0.5,hu-hu;q=0.3',
           'Accept-Encoding': 'gzip, deflate',
           'Cache-Control': 'max-age=0',
           'Referer': 'http://johnny.heliohost.org:2082/frontend/x3/index.phpcp',
           'X-Requested-With': 'XMLHttpRequest',
           'Keep-Alive': '300',
           'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5'}
        # req = urllib2.Request(url, None,txheaders)
        # req2 = urllib2.urlopen(req)
        # print req2

        # req=urllib2.urlopen(urllib2.Request(url))
        # print req.headers.headers
        # print req

    except urllib2.HTTPError, e:
        print e.headers
        print e.headers.has_key('WWW-Authenticate')
    try :
        # p = urllib2.HTTPPasswordMgrWithDefultRealm()
        req=urllib2.Request(url)
        handler = urllib2.HTTPBasicAuthHandler()
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        # page = urllib2.urlopen(req).read()
        print page
    except:
        pass

    # req2 = urllib2.urlopen(url)
    # print req2

    for line in listform:
        if line.find(host)!=-1:
            form_data=usr_tag(line)
            html=login_to_site(url,form_data)
            # html=login_to_site(url,form_data,'127.0.0.1:8580')
            # print html.response().read()
            # html2=login_urlib(url,"%(user)s"%form_data,"%(pass)s"%form_data,"%(user_tag)s"%form_data,"%(pass_tag)s"%form_data,"%(submit_tag_name)s:"%form_data,"%(submit_tag_value)s:"%form_data)
            # html2=login_urlib(url,form_data)
            # print html2

    # html=login_to_site(url,'jnu', 'jnulib')
    # print html.submit()
    # download_mechanize()
    print '</pre>'
