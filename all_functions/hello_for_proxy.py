#!"E:/Program Files win 7 2nd/python27/python.exe"
#!/usr/bin/python
__author__ = 's'
import socket,os
import urllib2
import threading
import sys
import Queue,re,time
import socket,urlparse
from urlparse import urlparse as urlparse2

import cgi

print "Content-type: text/html\n"
print ''
print '<pre>'

socket.setdefaulttimeout(7)

print "Bobng's proxy checker. Using %s second timeout"%(socket.getdefaulttimeout())

#input_file = sys.argv[1]
#proxy_type = sys.argv[2] #options: http,s4,s5
#output_file = sys.argv[3]
input_file = "configs/proxylist.txt"
proxy_type = 'http'
output_file = "configs/proxy_alive.txt"
sites_list="configs/sites_list.txt"

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

proxylist = file_rd(input_file,'r')
# print "proxylist is:"+''.join(proxylist)+'\n'

defaulttimeout=20
url = "www.seemyip.com" # Don't put http:// in here, or any /'s

check_queue = Queue.Queue()
output_queue = Queue.Queue()
threads = 20

def replace(file, pattern, subst):
    file_string=file_rd(file,'r')
    i=-1
    for j in range(i+1, len(file_string)):
    # for line in file_string:
        if pattern in file_string[j]:
            file_string[j]=file_string[j].replace(pattern,subst)

    file_handle = open(file, 'w')
    file_handle.write(file_string)
    file_handle.close()

def writer(f,rq):
    while True:
        line = rq.get()
        f.write(line+'\n')

    site= urlparse2(test_url).hostname
    l=0
    proxy_handler=[]
    pr_h=[]
    proxy_h=[]
    user_pass_h=[]
    try:

        listhandle = file_rd(input_file+site+".txt", 'r')

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

def make_txt_file(File_name,proxy,site,time_diff):
    with open(File_name, 'a+') as file:
    # read a list of lines into data
        data = file.readlines()
        file.close()
    data=file_rd(File_name,'a+')
    if data:
        i=-1
        No_proxy=0
        for j in range(i+1, len(data)):
        # for line in data:
            if proxy in data[j]:

                if  re.findall("For Site:",data[j]):
                    proxy1=data[j].split("For Site:")[0]
                    proxy2=data[j].split("For Site:")[1]

                    if  re.findall(site,proxy2):
                        s=proxy2.split(site)[0]
                        sss=proxy2.split(site)[1]
                        ss=s.split("*")
                        # pr_ar1=proxy2.split(site)[0].split("*")[1]
                        pr_ar2=proxy2.split(site)[1].split("*")[0].split("\n")[0]
                        if  re.findall(" Rs_Time ",pr_ar2):

                            replace(File_name, data[j].split(site)[0]+site+pr_ar2,data[j].split(site)[0]+site+" Rs_Time "+time_diff)
                        else:
                            replace(File_name,data[j].split(site)[0]+ site,data[j].split(site)[0]+site+" Rs_Time "+time_diff)
                        No_proxy=1

                    else:
                        No_proxy=1

                        replace(File_name, data[j].split('\n')[0] , data[j].split('\n')[0]+" * "+ site+" Rs_Time "+time_diff)

                else:
                    No_proxy=1
                    data[j]=data[j].split('\n')[0]
                    # data[j]=data[j].replace(data[j],data[j]+"  For Site:"+site+" Rs_Time "+time_diff+'\n')
                    replace(File_name, data[j],data[j]+"  For Site:"+site+" Rs_Time "+time_diff+'\n')


            else:
                pass

        if No_proxy==0:
            file=open(File_name, 'a+')


            file.write(proxy+"  For Site:"+site+" Rs_Time "+time_diff+"\n")
            file.close()

    else:
        file=open(File_name, 'a+')
        file.write(proxy+" For Site: "+site+'\n')
        file.close()

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
def checker(proxy_info,url=[],Tag=[],deftimeout=defaulttimeout,**kwargs):

    # proxy_info = q.get() #ip:port
    if kwargs:
        if kwargs['output_file']:output_file2=kwargs['output_file']
        else:output_file2=output_file

    done=0
    if  re.findall("For Site:",proxy_info) :

        proxy1=proxy_info.split("For Site:")[0]
        proxy2=proxy_info.split("For Site:")[1]
        if   ( re.findall("#",proxy1)):
            proxy_info=None
        # proxyList.append(proxy1)
        else:
            pr,proxy_info,user_pass=make_proxy_handler(proxy1)
            # if pr!=[]:

    if proxy_info == None:
        print "Finished"
        #quit()
        return
        #print "Checking %s"%proxy_info
    if url==[]:
        file_cheking=1
        listhandle = file_rd(sites_list,'r')
    else:
        # listhandle = open(sites_list).read().split('\n')
        listhandle=url.split()
        file_cheking=0
    for line in listhandle:
        if proxy_type == 'http':



            try:
                # saveAlive = open(output_file, 'w')

                details = line.split(':')
                email = details[0]
                password = details[1].replace('\n', '')

                time_diff=time.time()
                proxy_handler = urllib2.ProxyHandler({'http':proxy_info})
                opener = urllib2.build_opener(proxy_handler)
                opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; hu-HU; rv:1.7.8) Gecko/20050511 Firefox/1.0.4')]
                urllib2.install_opener(opener)
                if file_cheking==1:
                    if  re.findall("TAG:",line) :

                        url=line.split("TAG:")[0]
                        Tag=line.split("TAG:")[1]
                        print "<li><a>tag found</a></li>"
                        req = urllib2.Request(url)

                else:
                    req = urllib2.Request(url)



                # sock=urllib2.urlopen(req, timeout=3)
                sock=urllib2.urlopen(req, timeout=deftimeout)
                dlength = 0
                piece_size =1024*10 # 10KB
                rs = ''
                while True:
                    newdata = sock.read(piece_size)
                    dlength += len(newdata)
                    rs += newdata
                    if  re.findall(Tag,rs):
                        print Tag
                        break
                    if not newdata:
                        break
                        #data = openerdirector.read()
                # rs = sock.read(1000)
                print "<li><a>We can read it</a></li>"
                # print "We can read it"
                # print rs
                time_diff =str(round( time.time() - time_diff, 2))
                # if '<title>Google</title>' in rs:
                if  re.findall(Tag,rs):print Tag
                if Tag in rs:
                    # oq.put(proxy_info)
                    # print '[+] alive proxy' , proxy_info
                    # s="<h2>cheking proxy for </h2> <ul><li><a href="https://www.openshift.com/developers">Developer Center</a></li></ul>"

                    print '<pre>'
                    print ' [+] alive proxy' , proxy_info,"for",url+"With Tag:"+Tag+'\n'
                    print '</pre>'

                    make_txt_file(output_file2,proxy_info,line,time_diff)
                    # saveAlive.write(url)
                else:
                    print "<li><a>Tag Not found</a></li>"
                # saveAlive.close()
                # url=[]
            except urllib2.HTTPError,e:
                print 'url open error? slow?'
                pass
            except Exception,detail:
                # print "Exception details",detail+'\n'
                print '<pre>'
                print "Exception runned"
                print '[-] bad proxy' , proxy_info,"for",url+"With Tag:"+Tag+'\n'
                # print '[-] bad proxy' ,proxy_info
                print '</pre>'

        elif done==0:
        # gotta be socks
            try:
                time_diff =time.time()
                s = socks.socksocket()
                s.setdefaulttimeout(deftimeout)
                if proxy_type == "s4":
                    t = socks.PROXY_TYPE_SOCKS4
                else:
                    t = socks.PROXY_TYPE_SOCKS5
                ip,port = proxy_info.split(':')
                s.setproxy(t,ip,int(port))
                if file_cheking==1:
                    if  re.findall("TAG:",line) :

                        url=line.split("TAG:")[0]
                        Tag=line.split("TAG:")[1]
                        print "tag found"

                s.connect((url,80))
                time_diff =str(round( time.time() - time_diff, 2))
                make_txt_file(output_file2,proxy_info,line,time_diff)
                # oq.put(proxy_info)
                print proxy_info
            except Exception,error:
                print proxy_info
def form_get():
    # print "Content-type: text/html \n\n"
    form = cgi.FieldStorage()
    proxy = form["proxy"].value
    url=form["url"].value
    tag=form["tag"].value
    file_input=form["file_input"].value
    file_output=form["file_output"].value
    file_output_do=form["file_output_do"].value
    file_input_do=form['file_input_do'].value
    print "<h1>Hi there, %s!</h1>" % proxy
    print "<h1>Hi there, %s!</h1>" % url
    print "<h1>Hi there, %s!</h1>" % tag

    print 'Your guess is', url
    if url!=[]:
        checker(proxy,url,tag,output_file=file_output)
    if file_input_do=='1':
        proxylist = file_rd(file_input,'r')
        print file_rd(file_input,'r','1')
        # checker("222.66.115.233:80","http://stackoverflow.com/","<title>Stack Overflow</title>")

        for  proxy in proxylist:
            print "try checking"
            checker(proxy,url,tag,output_file=file_output)
        print "FINE :proxy Alive is "
    else:
        print "no file list of proxies tested"
    print file_rd(file_output,'r','1')




if __name__ == "__main__":
    try:
        print '</pre>'
        print '''<form method="post" action="hello_for_proxy.py">
        Enter proxy: <input type="text" name="proxy" value="222.66.115.233:80"><br>
        Enter url  : <input type="text" name="url" value="http://stackoverflow.com"><br>
        Enter tag  : <input type="text" name="tag" value="<title>Stack Overflow</title>"><br>
        Enter target file of ip&ports  : <input type="text" name="file_input" value="configs/proxylist.txt""><br>do it tick 1->do, 0 -> not to do <input type="text" name="file_input_do" value="0""><br>
        Enter target destination for putting alive proxy  : <input type="text" name="file_output" value="configs/proxy_alive.txt""><br>do it tick 1->do, 0 -> not to do <input type="text" name="file_output_do" value="0""><br>
        <input type="submit">
        </form>'''
        print '<pre>'

        form_get()
        # form = cgi.FieldStorage()
        # proxy = form["proxy"].value
        # url=form["url"].value
        # tag=form["tag"].value

        # data = sys.stdin.read()
        # url = int(data[data.find('=')+1:])
    except:
        url = []
        print "exp form"
    print 'Your guess is', url
    # if url!=[]:
    #     checker(proxy,url,tag)
    # try:
    #     proxylist = file_rd(input_file,'r')
    #     print file_rd(input_file,'r','1')
    #     # checker("222.66.115.233:80","http://stackoverflow.com/","<title>Stack Overflow</title>")
    # except:
    #     print "cheker problem"
    # for  proxy in proxylist:
    #     try:
    #
    #         # print "try checking"
    #         # checker(proxy)
    #         pass
    #     except:
    #         print "we cannt do try checking"
    print "FINE :proxy Alive is "
    # print file_rd(output_file,'r','1')

    print '</pre>'
