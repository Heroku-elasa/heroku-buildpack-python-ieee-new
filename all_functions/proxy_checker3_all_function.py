#!"E:/Program Files win 7 2nd/Python27/python.exe"
# -*- coding: UTF-8 -*-
__author__ = 's'
import urllib2, re, urlparse
from urlparse import urlsplit, urlparse
# import urllib
import cookielib, mechanize
import socket, time, md5, mimetypes
import os, re, sys
from urlparse import urlparse as urlparse2


def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body

# import time
class HTTPNoRedirector(urllib2.HTTPRedirectHandler):
    """This is a custom http redirect handler that FORBIDS redirection."""

    def http_error_302(self, req, fp, code, msg, headers):
        e = urllib2.HTTPError(req.get_full_url(), code, msg, headers, fp)
        if e.code in (301, 302):
            if 'location' in headers:
                newurl = headers.getheaders('location')[0]
            elif 'uri' in headers:
                newurl = headers.getheaders('uri')[0]
            e.newurl = newurl
        raise e


# Set some global variables
def proxy_checker(test_url="http://stackoverflow.com", input_file='configs//sites_proxy//proxylist.txt',
                  output_file='configs//proxy_alive.txt', site_file="configs//sites_proxy//", defaulttimeout=30):
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
    i = -1
    proxyList = []
    for j in range(i + 1, len(hosts)):
        if ( not re.findall("#", hosts[j]) and hosts[j] != '' ):
            proxyList.append(hosts[j])

    # proxyList=hosts
    # proxy=['151.236.14.48:80@ user:pass For Site:http://stackoverflow.com']
    # sites=['stackowerflow.com']
    proxy, index, sites, time_diff = getWorkingProxy(proxyList, test_url)
    if proxy != []:
        # _web = getOpener(proxy)
        # saveAlive = open("configs//proxy_alive.txt", 'wb')
        i = -1
        for j in range(i + 1, len(proxy)):
            if re.findall("For Site:", proxy[j]):
                proxy1 = proxy[j].split("For Site:")[0]
                proxy2 = proxy[j].split("For Site:")[1]
                if re.findall(sites[j], proxy2):
                    pass
                else:
                    # replace("configs//sites_proxy//"+sites[j]+".txt", proxyList[j],proxy1+"For Site:"+proxy2+";"+sites[j])
                    make_txt_file(site_file + sites[j] + ".txt", proxy1, sites[j], time_diff[j])
                    make_txt_file(output_file, proxy1, sites[j], time_diff[j])

            else:
                proxy1 = proxy[j]
                make_txt_file(site_file + sites[j] + ".txt", proxy1, sites[j], time_diff[j])
                make_txt_file(output_file, proxy1, sites[j], time_diff[j])
        sort_file(site_file + sites[j] + ".txt", " Rs_Time ")
        sort_file(output_file, " Rs_Time ")



        # return make_returning_proxy(site_file,test_url)


def proxy_finder(test_url="http://stackoverflow.com", input_file='configs//sites_proxy//all_proxies_list//proxylist.txt',
                  output_file='configs//all_proxies_list//proxy_alive.txt', site_file="configs//sites_proxy//all_proxies_list//site_list.txt", defaulttimeout=30):
# input_file = 'configs\\proxylist.txt'
#     proxy_list = open(input_file, 'r')
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
    i = -1
    proxyList = []
    for j in range(i + 1, len(hosts)):
        if ( not re.findall("#", hosts[j]) and hosts[j] != '' ):
            proxyList.append(hosts[j])

    # proxyList=hosts
    # proxy=['151.236.14.48:80@ user:pass For Site:http://stackoverflow.com']
    # sites=['stackowerflow.com']
    proxy, index, sites, time_diff = getWorkingProxy(proxyList, test_url)
    if proxy != []:
        # _web = getOpener(proxy)
        # saveAlive = open("configs//proxy_alive.txt", 'wb')
        i = -1
        for j in range(i + 1, len(proxy)):
            if re.findall("For Site:", proxy[j]):
                proxy1 = proxy[j].split("For Site:")[0]
                proxy2 = proxy[j].split("For Site:")[1]
                if re.findall(sites[j], proxy2):
                    pass
                else:
                    # replace("configs//sites_proxy//"+sites[j]+".txt", proxyList[j],proxy1+"For Site:"+proxy2+";"+sites[j])
                    make_txt_file(site_file + sites[j] + ".txt", proxy1, sites[j], time_diff[j])
                    make_txt_file(output_file, proxy1, sites[j], time_diff[j])

            else:
                proxy1 = proxy[j]
                make_txt_file(site_file + sites[j] + ".txt", proxy1, sites[j], time_diff[j])
                make_txt_file(output_file, proxy1, sites[j], time_diff[j])
        sort_file(site_file + sites[j] + ".txt", " Rs_Time ")
        sort_file(output_file, " Rs_Time ")



        # return make_returning_proxy(site_file,test_url)


class MozillaEmulator(object):
    def __init__(self, cacher={}, trycount=0):
        """Create a new MozillaEmulator object.

        @param cacher: A dictionary like object, that can cache search results on a storage device.
            You can use a simple dictionary here, but it is not recommended.
            You can also put None here to disable caching completely.
        @param trycount: The download() method will retry the operation if it fails. You can specify -1 for infinite retrying.
                A value of 0 means no retrying. A value of 1 means one retry. etc."""
        self.cacher = cacher
        self.cookies = cookielib.CookieJar()
        self.debug = False
        self.trycount = trycount

    def _hash(self, data):
        h = md5.new()
        h.update(data)
        return h.hexdigest()

    def build_opener(self, url, proxy=[], User_Pass=[], postdata=None, extraheaders={}, forbid_redirect=False):

        txheaders = {
            'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
            'Accept-Language': 'en,hu;q=0.8,en-us;q=0.5,hu-hu;q=0.3',
            #            'Accept-Encoding': 'gzip, deflate',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
            #            'Keep-Alive': '300',
            #            'Connection': 'keep-alive',
            #            'Cache-Control': 'max-age=0',
        }
        for key, value in extraheaders.iteritems():
            txheaders[key] = value
        req = urllib2.Request(url, postdata, txheaders)
        self.cookies.add_cookie_header(req)
        if forbid_redirect:
            redirector = HTTPNoRedirector()
        else:
            redirector = urllib2.HTTPRedirectHandler()

        if proxy != [] and (not re.findall("None", proxy)):
            if User_Pass != []:
                proxies = {"http": "http://" + User_Pass + "@" + proxy}
            else:
                proxies = {"http": "http://%s" % proxy}
            proxy_support = urllib2.ProxyHandler(proxies)
            opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler(debuglevel=1))
        else:
            proxy_support = urllib2.ProxyHandler()
            opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler(debuglevel=1))
            # url=link.absolute_url
            # headers={'User-agent' : 'Mozilla/5.0'}

        http_handler = urllib2.HTTPHandler(debuglevel=self.debug)
        https_handler = urllib2.HTTPSHandler(debuglevel=self.debug)

        # default_classes = [ProxyHandler, UnknownHandler, HTTPHandler,
        #                    HTTPDefaultErrorHandler, HTTPRedirectHandler,
        #                    FTPHandler, FileHandler, HTTPErrorProcessor]

        u = urllib2.build_opener(proxy_support, http_handler, https_handler, urllib2.HTTPCookieProcessor(self.cookies),
                                 redirector)
        u.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; hu-HU; rv:1.7.8) Gecko/20050511 Firefox/1.0.4')]
        if not postdata is None:
            req.add_data(postdata)
        return (req, u)

    def download(self, url, proxy=[], User_Pass=[], postdata=None, extraheaders={}, forbid_redirect=False,
                 trycount=None, fd=None, onprogress=None, only_head=False, time_out=30):
        """Download an URL with GET or POST methods.

        @param proxy: set the proxy setting.
        @param User_Pass: user_pass for proxy.
        @param postdata: It can be a string that will be POST-ed to the URL.
            When None is given, the method will be GET instead.
        @param extraheaders: You can add/modify HTTP headers with a dict here.
        @param forbid_redirect: Set this flag if you do not want to handle
            HTTP 301 and 302 redirects.
        @param trycount: Specify the maximum number of retries here.
            0 means no retry on error. Using -1 means infinite retring.
            None means the default value (that is self.trycount).
        @param fd: You can pass a file descriptor here. In this case,
            the data will be written into the file. Please note that
            when you save the raw data into a file then it won't be cached.
        @param onprogress: A function that has two parameters:
            the size of the resource and the downloaded size. This will be
            called for each 1KB chunk. (If the HTTP header does not contain
            the content-length field, then the size parameter will be zero!)
        @param only_head: Create the openerdirector and return it. In other
            words, this will not retrieve any content except HTTP headers.

        @return: The raw HTML page data, unless fd was specified. When fd
            was given, the return value is undefined.
        """
        if trycount is None:
            trycount = self.trycount
        cnt = 0
        done = 0
        # self.cacher.has_key(key)=None

        while True:
            try:
                key = self._hash(url)
                prx_key = self._hash(proxy)
                if (self.cacher is None) or (
                        not self.cacher.has_key(key) or (not self.cacher.has_key(prx_key)) and (done == 0)):
                    done = done + 1
                    req, u = self.build_opener(url, proxy, User_Pass, postdata, extraheaders, forbid_redirect)
                    openerdirector = u.open(req, timeout=time_out)

                    if self.debug:
                        print req.get_method(), url
                        print openerdirector.code, openerdirector.msg
                        print openerdirector.headers
                    self.cookies.extract_cookies(openerdirector, req)
                    if only_head:
                        return openerdirector
                    if openerdirector.headers.has_key('content-length'):
                        length = long(openerdirector.headers['content-length'])
                    else:
                        length = 0
                    dlength = 0
                    # piece_size = 4096 # 4 KiB
                    piece_size = 1024 * 1024 # 1MB
                    if fd:
                        while True:
                            data = openerdirector.read(piece_size)
                            dlength += len(data)
                            fd.write(data)
                            if onprogress:
                                onprogress(length, dlength)
                            if not data:
                                break
                    else:
                        data = ''
                        while True:
                            newdata = openerdirector.read(piece_size)
                            dlength += len(newdata)
                            data += newdata
                            if onprogress:
                                onprogress(length, dlength)
                            if not newdata:
                                break
                                #data = openerdirector.read()
                        if not (self.cacher is None):
                            self.cacher[key] = data

                else:
                    data = self.cacher[key]
                    done = 1
                    break
                    # try:
                    #   d2= GzipFile(fileobj=cStringIO.StringIO(data)).read()
                    #   data = d2
                    # except IOError:
                    #   pass
                    # return data

            except urllib2.URLError:
                # cnt += 1
                done = 1
                if (trycount > -1) and (trycount < cnt):
                    raise
                    # Retry :-)
                if self.debug:
                    print "MozillaEmulator: urllib2.URLError, retryting ", cnt

                return data

    def post_multipart(self, url, fields, files, pr=[], Up=[], forbid_redirect=True, ):
        """Post fields and files to an http host as multipart/form-data.
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files
        Return the server's response page.
        """
        content_type, post_data = encode_multipart_formdata(fields, files)
        result = self.download(url, pr, Up, post_data, {
            'Content-Type': content_type,
            'Content-Length': str(len(post_data))
        }, forbid_redirect=forbid_redirect
        )
        return result


def is_bad_proxy_urlib(pip, url):
    site = urlparse(url).hostname
    time_diff = time.time()
    try:
        if (re.findall("For Site:", pip)):
            url2 = pip.split("For Site:")[1]
            pip2 = pip.split("For Site:")[0]
            if url == url2:
                dl = MozillaEmulator()
                data = dl.download('http://' + url, pip2)
            else:
                print ("please check proxy_list.txt file for " + "http://" + site + " to be adde")
                return True, site, time_diff

                # opnr = getOpener(pip2)
                # data,time_diff=getContentBrowser(pip2, site)
                # data = getContent(opnr, url)
        else:
            # opnr = getOpener(pip)
            # try:
            #     BROWSER(url)
            dl = MozillaEmulator()
            data = dl.download('http://' + site, pip)


            # data,time_diff=getContentBrowser(pip, site)
            # data = getContent(opnr, url)
            # site= urlparse(test_url).hostname
            # site2=urlparse.urlsplit(url).path.split('/')
    except urllib2.HTTPError, e:
        try:
            data, time_diff = getContentBrowser([], site)
            time_diff = str(round(time.time() - time_diff, 2))
            return e.code, site, time_diff
        except:
            print "No Connection Avalable To Test Proxis"
            return e.code, site, time_diff
    except Exception, detail:
        print detail
        print Exception
        print 'url open error? slow?'
        time_diff = str(round(time.time() - time_diff, 2))
        return True, site, time_diff
    time_diff = str(round(time.time() - time_diff, 2))
    return False, site, time_diff

# s = open("mount.txt").read()
# s = s.replace('mickey', 'minnie')
# f = open("mount.txt", 'w')
# f.write(s)
# f.close()
def sort_file(file_name, text_to_sort,next_text=' ',sort_type='Not_reversed'):
    f2 = open(file_name, "r");data=f2.readlines();data = list(set(data));f2.close()
    f2 = open(file_name, "w+");f2.writelines(data);f2.close()
    f = open(file_name, "r")
    # omit empty lines and lines containing only whitespace
    lines = [line for line in f if line.strip()]
    i = -1;
    t = 0
    sort_file = {};
    sort_file2 = {}

    for j in range(i + 1, len(lines)):
        if text_to_sort in lines[j]:
            # sort_file[j] = (lines[j].split(text_to_sort)[1]).replace('/n','')
            # f1=lines[j].split(text_to_sort+' ')[1].split(' ')[0]
            f1=lines[j].split(text_to_sort)[1].split(next_text)[0]
            sort_file[j] = float(f1.replace(' ',''))
            # sort_file[j] = float((lines[j].split(text_to_sort)[1].replace(' ','').split(next_text)[0]))
            sort_file2[j] = lines[j]
        else:
            t = t - 1;
            sort_file[j] = str(t)
            sort_file2[j] = lines[j]

    # for key in sorted(sort_file.values()):
    #     print "%s: %s" % (key, sort_file.values())
    # res = list(sorted(sort_file, key=sort_file.__contains__))
    # print res
    sorted([(value,key) for (key,value) in sort_file.items()])
    if sort_type=='Not_reversed':

        ds = sorted(sort_file.values())
        ds2 = sorted(sort_file.keys())
        sort_file3=sorted([(value,key) for (key,value) in sort_file.items()])
    else:
         sort_file3=sorted([(value,key) for (key,value) in sort_file.items()], reverse=True)
         ds = sorted(sort_file.values(),reverse=True)
         ds2 = sorted(sort_file.keys(),reverse=True)
    sd=([(value) for (key,value) in sort_file3])
    lin = []
    for j in range(0, len(sd)):
        # s = sort_file.keys()[sort_file.values().index(sd[j])]
        lin.append(sort_file2.values()[sd[j]])
    f = open(file_name, "wb")
    # omit empty lines and lines containing only whitespace
    f.writelines(lin)
    f.close()

    # ky=sort_file.keys()[ds]
    # k = 0
    # new = {}
    # i = -1
    # l = -1
    # for k in range(i + 1, len(ds)):
    #     for j in range(l + 1, len(lines)):
    #         if str(ds[k]) in lines[j]:
    #             new[k] = lines[j]
    #             break
    # i = -1
    # l = -1
    # t = len(ds) - 1
    # p = 0
    # for j in range(i + 1, len(lines)):
    #     for k in range(l + 1, len(ds)):
    #         if str(ds[k]) in lines[j]:
    #             p = 1
    #     if p != 1:
    #         new[t + 1] = lines[j]
    # f = open(file_name, "wb")
    # # omit empty lines and lines containing only whitespace
    # f.writelines(new.values())
    # f.close()


def make_returning_proxy(input_file, test_url, proxy_alive='configs//proxy_alive.txt', **kwargs):
    # import os
    if kwargs:
        if kwargs['proxy_alive']: proxy_alive = kwargs['proxy_alive']
        if kwargs['proxy_list_check']:
            proxy_list = kwargs['proxy_list_check']
        else:
            proxy_list = 'configs//proxylist.txt'
    else:
        proxy_list = 'configs//proxylist.txt'
    site = urlparse(test_url).hostname
    l = 0
    proxy_handler = []
    pr_h = []
    proxy_h = []
    user_pass_h = []
    CurrentDir = os.path.dirname(os.path.realpath(__file__))
    # Parent_Dir=os.path.abspath(os.path.join(CurrentDir, '..'))
    os.chdir(CurrentDir)
    print os.getcwd()
    done = 0
    if done == 0:
        try:
            listhandle = open(input_file + site + ".txt").readlines()
            if len(listhandle) != 0:
            # sort_file(name,text_to_sort)
                for line in listhandle:

                    if re.findall("For Site:", line) and (not re.findall("#", line)):
                        proxy1 = line.split("For Site:")[0]
                        proxy2 = line.split("For Site:")[1]
                        pr, proxy_han, user_pass = make_proxy_handler(proxy1)
                        # if pr!=[]:
                        pr_h.append(pr)
                        # if proxy_han!=[]:
                        proxy_h.append(proxy_han)
                        # if user_pass!=[]:
                        user_pass_h.append(user_pass)
                        done = 1
        except:
            print '****************Need to check proxy list ******************************'
            print 'we must ckeck' + proxy_list + 'For finding which proxy is proper for this site'

    if done == 0:
        listhandle = open(proxy_alive).readlines()
        for line in listhandle:
            if re.findall(site, line):
                if re.findall("For Site:", line) and not re.findall('#', line[:4]):
                    proxy1 = line.split("For Site:")[0]
                    proxy2 = line.split("For Site:")[1]
                    if re.findall(site, proxy2):
                    # proxyList.append(proxy1)
                        pr, proxy_han, user_pass = make_proxy_handler(proxy1)
                        # if pr!=[]:
                        pr_h.append(pr)
                        # if proxy_han!=[]:
                        proxy_h.append(proxy_han)
                        # if user_pass!=[]:
                        user_pass_h.append(user_pass)
        if pr_h == []:
            if not os.path.isdir('configs/sites_proxy/' + site):
                os.mkdir('configs/sites_proxy/' + site)
                sa = open('configs/sites_proxy/site_list_form.txt', 'r')
                ez = sa.read();
                sa.close()
                sa = open('configs/sites_proxy/' + site + '/site_list_form.txt', 'w')
                sa.write(ez);
                sa.close()

            proxy_checker(test_url, proxy_list, 'configs//sites_proxy//proxy_alive.txt', "configs//sites_proxy//", 30)
            # proxy_checker(test_url,input_file+"proxylist.txt",proxy_alive,input_file,30)
            try:
                listhandle = open(input_file + site + ".txt").readlines()

                for line in listhandle:
                    if re.findall("For Site:", line) and not re.findall('#', line[:3]):
                        proxy1 = line.split("For Site:")[0]
                        proxy2 = line.split("For Site:")[1]

                        # proxyList.append(proxy1)
                        pr, proxy_han, user_pass = make_proxy_handler(proxy1)
                        # if pr!=[]:
                        pr_h.append(pr)
                        # if proxy_han!=[]:
                        proxy_h.append(proxy_han)
                        # if user_pass!=[]:
                        user_pass_h.append(user_pass)
            except:
                pass
        try:
            listhandle = open(input_file + site + ".txt").readlines()
        except:
            # proxy_checker(test_url,input_file+"proxylist.txt",proxy_alive,input_file,30)
            proxy_checker(test_url, proxy_list, 'configs//sites_proxy//proxy_alive.txt', "configs//sites_proxy//", 30)
    return pr_h, proxy_h, user_pass_h


def BROWSER(proxy, url, User_Pass=[]):
    br = mechanize.Browser()

    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    # cj.revert(cookie3)
    opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cj))

    br.set_cookiejar(cj)
    cj.save("configs//PR_TEST-COOKIE.txt")
    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)


    # User-Agent (this is cheating, ok?)
    br.addheaders = [('User-agent',
                      'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

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
    if proxy != []:
        br.proxies = br.set_proxies({"http": proxy})
    if User_Pass != []:
        # g=User_Pass.split(":")[0]
        br.add_proxy_password(User_Pass.split(":")[0], User_Pass.split(":")[1])
        # r = br.open(url)
    return br


def replace(file, pattern, subst):
    # Read contents from file as a single string
    file_handle = open(file, 'r')
    # file_string1 = file_handle.read()
    file_string = file_handle.readlines()
    file_handle.close()
    i = -1
    for j in range(i + 1, len(file_string)):
        if not re.findall('#', file_string[j][:3]) and not file_string[j] == '\n':
            if type(pattern) is list:
                for i in range(0, len(pattern)):
                    if pattern[i] in file_string[j]:
                        file_string[j] = file_string[j].replace(pattern[i], subst[i])
            else:
                file_string[j] = file_string[j].replace(pattern, subst)
                # if  re.findall("For Site:",file_string[j]):
                #     proxy1=file_string[j].split("For Site:")[0]
                #     proxy2=file_string[j].split("For Site:")[1]
                #     if  re.findall(subst,proxy2):
                #         pass
                #     else:
                #         file_string[j]=proxy1+"For Site:"+proxy2+";"+subst
                # else:
                #     proxy1=file_string[j]
                #     file_string[j]=proxy1+"For Site:"+subst
                #       p1=file_string[j].split(pattern)[0]
                #       p2=file_string[j].split(pattern)[1]




                # line.replace(pattern, 'bar')
                # Use RE package to allow for replacement (also allowing for (multiline) REGEX)
                # file_string[j].replace(pattern, subst)
                # file_string[j] = (re.sub(pattern, subst, file_string[j]))

                # Write contents to file.
                # Using mode 'w' truncates the file.

    file_handle = open(file, 'w')
    file_handle.writelines(file_string)
    file_handle.close()


def make_txt_file(File_name, proxy, site, time_diff, **kwargs):
    if True:
        try:
            For_Site = kwargs['For_Site']
        except:
            For_Site = "  For Site:"
        try:
            Rs_Time = kwargs['Rs_Time']
        except:
            Rs_Time = " Rs_Time "
    with open(File_name, 'a+') as file:
    # read a list of lines into data
        data = file.readlines()
        file.close()
    if data:
        i = -1
        No_proxy = 0
        for j in range(i + 1, len(data)):
        # for line in data:
            if proxy in data[j]:

                if re.findall(For_Site, data[j]):
                    proxy1 = data[j].split(For_Site)[0]
                    proxy2 = data[j].split(For_Site)[1]

                    if re.findall(site, proxy2):
                        s = proxy2.split(site)[0]
                        sss = proxy2.split(site)[1]
                        ss = s.split("*")
                        # pr_ar1=proxy2.split(site)[0].split("*")[1]
                        pr_ar2 = proxy2.split(site)[1].split("*")[0].split("\n")[0]
                        if re.findall(" Rs_Time ", pr_ar2):
                            # print data[j]
                            # print (site+pr_ar2,site+" Rs_Time "+time_diff)
                            # re.sub(site+pr_ar2,site+" Rs_Time "+time_diff, data[j])
                            # data[j]=data[j].replace(site+pr_ar2,site+" Rs_Time "+time_diff)
                            replace(File_name, data[j].split(site)[0] + site + pr_ar2,
                                    data[j].split(site)[0] + site + Rs_Time + str(time_diff))
                        else:
                            # data[j]=data[j].replace(site,site+" Rs_Time "+time_diff)
                            replace(File_name, data[j].split(site)[0] + site,
                                    data[j].split(site)[0] + site + Rs_Time + str(time_diff))
                        No_proxy = 1

                    else:
                        No_proxy = 1

                        # data[j]=data[j].replace(data[j], data[j]+" * "+ site+" Rs_Time "+time_diff+"\n")
                        replace(File_name, data[j].split('\n')[0],
                                data[j].split('\n')[0] + " * " + site + Rs_Time + str(time_diff))
                        #         data[j]=proxy1+"For Site:"+proxy2+";"+site
                else:
                    No_proxy = 1
                    data[j] = data[j].split('\n')[0]
                    # data[j]=data[j].replace(data[j],data[j]+"  For Site:"+site+" Rs_Time "+time_diff+'\n')
                    replace(File_name, data[j], data[j] + For_Site + site + Rs_Time + time_diff + '\n')
                break

                #  proxy1=file_string[j]
                #     data[j]=proxy1+"For Site:"+site+"\n"
                # file=open(File_name, 'w')
                # file.write(data)

                # replace(File_name, proxy, site)
                # # file.write(line.replace(';', ' '))
                # data[j]=proxy+"For Site:"+site+'\n'
            else:
                pass
                # file=open(File_name, 'a+')
                # # file.write(proxy+"For Site:"+site+'\n')
                # file.writelines( proxy+"For Site:"+site+'\n')
                # file_handle = open(File_name, 'w')
                # file_handle.writelines(data)
            # file_handle.close()
        if No_proxy == 0:
            file = open(File_name, 'a+')

            # s=file.readlines()
            # if s[len(s)]:
            #     if s[len(s)].split("\n"):
            #
            #       print s
            file.write(proxy + For_Site + site + Rs_Time + str(time_diff) + "\n")
            file.close()
            # file=open(File_name, 'w')
            # file.writelines( proxy+"For Site:"+site+'\n')
            #     data = file.readlines(proxy)
    # if data:
    #    data=proxy+"For Site:"+site+'\n'
    #    with open(File_name, 'w') as file:
    #        file.writelines( data )
    else:
        file = open(File_name, 'a+')
        file.write(proxy + For_Site + site + Rs_Time + str(time_diff) + "\n")
        # file.write(proxy + " For Site: " + site + '\n')
        file.close()


def writer(f, rq):
    while True:
        line = rq.get()
        f.write(line + '\n')


def getOpener(pip=None):
    proxy_handler = []
    if pip:
        # try :
        #    pip.split('@')[1]
        #
        #    proxy_info = {
        #         'user' : pip.split('@')[1].split(":")[0],
        #         'pass' : pip.split('@')[1].split(":")[1].replace('\n', ''),
        #         'host' : pip.split('@')[0].split(":")[0],
        #         'port' : pip.split('@')[0].split(":")[1] # or 8080 or whatever
        #    }
        #    proxy_="http://%(user)s:%(pass)s@%(host)s:%(port)s" % proxy_info
        #    proxy_handler = urllib2.ProxyHandler({"http" : "http://%(user)s:%(pass)s@%(host)s:%(port)s" % proxy_info})
        # except:
        #     proxy_info = {
        #     'host' : pip.split(":")[0],
        #     'port' : pip.split(":")[1].replace('\n', '') # or 8080 or whatever
        #     }
        #     s=pip.split("#")
        #     ss=re.findall("#",pip)
        #     if  re.findall("#",pip):
        #         return False
        #     else:
        #     # b="http://%(host)s:%(port)d" % proxy_info
        #         proxy_="http://%(host)s:%(port)s" % proxy_info
        pr, proxy_han, user_pass = make_proxy_handler(pip)
        proxy_handler = urllib2.ProxyHandler(proxy_han)
        # proxy_handler = urllib2.ProxyHandler({'http': pip})
        # b="http://%(host)s:%(port)s" % proxy_info
        opener = urllib2.build_opener(proxy_handler)
    else:
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1')]
    urllib2.install_opener(opener)
    return opener


def make_proxy_handler(pip=None):
    proxy_handler = []
    user_pass = []
    proxy_ = []
    if pip:
        try:
            pip.split('@')[1]

            proxy_info = {
                'user': pip.split('@')[1].split(":")[0],
                'pass': pip.split('@')[1].split(":")[1].replace('\n', ''),
                'host': pip.split('@')[0].split(":")[0],
                'port': pip.split('@')[0].split(":")[1] # or 8080 or whatever
            }
            user_pass = "%(user)s:%(pass)s" % proxy_info
            proxy_ = "%(host)s:%(port)s" % proxy_info
            proxy_handler = {"http": "http://%(user)s:%(pass)s@%(host)s:%(port)s" % proxy_info}
        except:
            proxy_info = {
                'host': pip.split(":")[0],
                'port': pip.split(":")[1].replace('\n', '') # or 8080 or whatever
            }
            s = pip.split("#")
            ss = re.findall("#", pip)
            if re.findall("#", pip):
                return False
            else:
            # b="http://%(host)s:%(port)d" % proxy_info
                proxy_ = "%(host)s:%(port)s" % proxy_info
                proxy_handler = {"http": "http://%(host)s:%(port)s" % proxy_info}

    return proxy_, proxy_handler, user_pass


def getContent(opnr, url):
    # socket.setdefaulttimeout(60)
    req = urllib2.Request(url)
    sock = opnr.open(req)
    return sock.read()


def getContentBrowser(proxy, url):
    proxy_, proxy_han, user_pass = make_proxy_handler(proxy)
    url = 'http://' + url
    time_start = time.time()

    br = BROWSER(proxy_, url, user_pass)
    html = br.open(url)
    req = br.response()
    rt = br.response().read()
    time_end = time.time()
    # Calculate request time
    time_diff = str(round(time_end - time_start, 2))
    return rt, time_diff


def is_bad_proxy(pip, url):
    site = urlparse(url).hostname
    time_diff = time.time()
    try:
        if re.findall("For Site:", pip):
            url = pip.split("For Site:")[1]
            pip2 = pip.split("For Site:")[0]
            opnr = getOpener(pip2)
            data, time_diff = getContentBrowser(pip2, site)
            # data = getContent(opnr, url)
        else:
            opnr = getOpener(pip)
            # try:
            #     BROWSER(url)
            data, time_diff = getContentBrowser(pip, site)
            # data = getContent(opnr, url)
            # site= urlparse(test_url).hostname
            # site2=urlparse.urlsplit(url).path.split('/')
    except urllib2.HTTPError, e:
        try:
            data, time_diff = getContentBrowser([], site)
            time_diff = str(round(time.time() - time_diff, 2))
            return e.code, site, time_diff
        except:
            print "No Connection Avalable To Test Proxis"
            return e.code, site, time_diff
    except Exception, detail:
        print detail
        print Exception
        print 'url open error? slow?'
        time_diff = str(round(time.time() - time_diff, 2))
        return True, site, time_diff
    return False, site, time_diff


def check_module(url, target_folder='/configs/Links_site/'):
    print 'url is ' + url
    site = urlparse2(url).hostname
    fo = os.getcwd()
    CurrentDir = os.path.dirname(os.path.realpath(__file__))
    s = CurrentDir.replace('\\', '/') + target_folder
    print site
    file_exist = 0
    if os.path.isfile(s + site.replace('.', '_') + '.py'):
        sys.path.insert(0, s)
        si = sys.modules
        if site.replace('.', '_') in si:
            print "@@@@@@@@@@@@@@ module already exist  for  " + site + ' is \n: @@@@@@@@@@@@@@\n\n'
            new_module = si[site.replace('.', '_')]
        else:
            print "@@@@@@@@@@@@@@ module inserted for  " + site + ' is \n: @@@@@@@@@@@@@@\n\n'
            new_module = __import__(site.replace('.', '_'), {}, {}, [], 2)

        print new_module
        file_exist = 1
    else:
        print "@@@@@@@@@@@@@@ module " + CurrentDir.replace('\\', '/') + target_folder + site.replace('.',
                                                                                                      '_') + '.py' + '\n Not found: @@@@@@@@@@@@@@\n\n'
    os.chdir(fo)
    return new_module


def getProxiesList(
        ProxiesList_site='http://pr4ss.tk/ss_proxy/web-proxy-glype-1.1-1/glype-1.1/upload/browse.php?u=Oi8vd3d3LnNlbnNhbGdvLmNvbS90cmlzdGF0Mi9wcm8yLw%3D%3D&b=13&f=norefer'):
    proxies = []
    opnr = getOpener()
    content = getContent(opnr, ProxiesList_site)
    urls1 = re.findall("<a href='([^']+)'[^>]*>.*?HTTP Proxies.*?</a>", content)
    urls = re.findall("<p class=left>*</p>", content)

    for eachURL in urls:
        content = getContent(opnr, eachURL)
        proxies.extend(re.findall('\d{,3}\.\d{,3}\.\d{,3}\.\d{,3}:\d+', content))
    return proxies

# update_urls_to_proxy(proxylist_file='configs//sites_proxy//proxylist.txt',url_file='configs//sites_proxy//urllist.txt')
def update_urls_to_proxy(**kwargs):
    try:
        if kwargs['link_checker']: link_checker = kwargs['link_checker']

    except:
        link_checker = 'http://ss-link-checker.com'

    try:
        if kwargs['url_list']:
            url_list = kwargs['url_list']
        else:
            url_list = ''
    except:
        url_list = ''
    try:
        if kwargs['url_file']:
            url_file = kwargs['url_file']
        else:
            url_file = 'configs//sites_proxy//urllist.txt'
    except:
        url_file = 'configs//sites_proxy//urllist.txt'
    try:
        if kwargs['proxylist_file']:
            proxylist_file = kwargs['proxylist_file']
        else:
            proxylist_file = 'configs//sites_proxy//proxylist.txt';
    except:
        proxylist_file = 'configs//sites_proxy//proxylist.txt';
    try:
        if kwargs['output_file']:
            output_file = kwargs['output_file']
        else:
            output_file = 'configs//proxy_alive.txt'
    except:
        output_file = 'configs//proxy_alive.txt'
    try:
        if kwargs['site_file']:
            site_file = kwargs['site_file']
        else:
            site_file = "configs//sites_proxy//"
    except:
        site_file = "configs//sites_proxy//"
    if url_list == '':
        sa = open(url_file, 'r')
        url_list = sa.readlines()
        sa.close()
        # k = -1
    s2 = open(proxylist_file, 'r')
    proxyList = s2.readlines()
    s2.close()
    # for line in listhandle:
    #     if re.findall(site, line) and link_done == 0 and (not re.findall("#", line.split("TAG:")[0])) :
    #         if re.findall("TAG1:", line):
    #             try:
    #                 Tag = line.split("TAG1:")[1].split("---")[0]
    #                 Tag=Tag.replace("+++",'')
    #                 atrr = line.split("Attr1:")[1].split("---")[0]
    #                 atrr=atrr.replace("+++",'')
    #                 href=line.split('Href1:')[1].split("---")[0]
    #                 href=href.replace("+++",'')
    #                 links =self.soap_my(data=html, tag=Tag, attr=atrr, href=href,url=url)


    for kk in range(0, len(url_list)):
        if not re.findall("#", url_list[kk]) and url_list[kk] != '\n':
            url = url_list[kk].split("TAG1:")[0].replace('\n', '').replace(' ', '')
            Tag = url_list[kk].split("TAG1:")[1].split("---")[0]
            Tag = Tag.replace("+++", '')
            atrr = url_list[kk].split("Attr1:")[1].split("---")[0]
            atrr = atrr.replace("+++", '')
            href = url_list[kk].split('Href1:')[1].split("---")[0]
            href = href.replace("+++", '')
            i = -1
            index = []
            workproxy = []
            time_diff2 = []
            sites = []

            site = urlparse(url).hostname
            # T_F=True


            for j in range(i + 1, len(proxyList)):
                if not re.findall("#", proxyList[j]) and proxyList[j] != '\n':
                    time_diff = time.time()
                    link = []
                    T_F = True
                    currentProxy = proxyList[j].replace('\n', '')
                    # [T_F,site,time_diff]=is_bad_proxy(currentProxy,url)

                    # [T_F, site, time_diff] = is_bad_proxy_urlib(currentProxy, url)
                    # if not is_bad_proxy(currentProxy,url):
                    proxy_, proxy_han, user_pass = make_proxy_handler(currentProxy)
                    link_checker=url

                    new_module = check_module(link_checker, '/configs/Links_site/')

                    responce = new_module.LINK(url).get_pdf_link_two_state(proxy_, user_pass, tag=Tag, attr=atrr, href=href)
                    link = responce['links'];
                    proxy = responce['proxy'];
                    user_pass = responce['user_pass'];
                    responce['user_pass']

                    # proxy_=proxy_.split("http://")[1]
                    link_done = 0

                    if link != []:
                        # k = k + 1
                        # new_module=check_module(url,'/configs/Links_site/')
                        # responce=new_module.LINK(url).get_pdf_link(proxy_,user_pass)
                        # link=responce['links'];proxy=responce['proxy'];user_pass=responce['user_pass'];responce['user_pass']
                        # log("%s is working" % (currentProxy))
                        if link != []:
                            link_done = 1
                            time_diff = str(round(time.time() - time_diff, 2))
                            print(
                                     "%s is working for site " % proxy_ + site + " With Time  " + str(time_diff)) + 'Second'
                            workproxy.append(currentProxy)
                            sites.append(site)
                            time_diff2.append(time_diff)
                            index.append(j)
                            # return currentProxy, j
                    elif link_done == 0:
                        # log("Bad Proxy %s" % (currentProxy))
                        time_diff = str(round(time.time() - time_diff, 2))
                        make_txt_file("configs//badproxylist.txt", proxy_, site, time_diff)
                        print("%s is Bad Proxy for site " % proxy_ + site + " With Time " + str(time_diff))
                        # print ("Bad Proxy %s" % (currentProxy))
                        # return workproxy, index, sites, time_diff2
            proxy = workproxy;

            if proxy != []:
                # _web = getOpener(proxy)
                # saveAlive = open("configs//proxy_alive.txt", 'wb')
                i = -1
                for j in range(i + 1, len(proxy)):
                    if re.findall("For Site:", proxy[j]):
                        proxy1 = proxy[j].split("For Site:")[0]
                        proxy2 = proxy[j].split("For Site:")[1]
                        if re.findall(sites[j], proxy2):
                            pass
                        else:
                            # replace("configs//sites_proxy//"+sites[j]+".txt", proxyList[j],proxy1+"For Site:"+proxy2+";"+sites[j])
                            make_txt_file(site_file + sites[j] + ".txt", proxy1, sites[j], time_diff[j])
                            make_txt_file(output_file, proxy1, sites[j], time_diff[j])

                    else:
                        proxy1 = proxy[j]
                        make_txt_file(site_file + sites[j] + ".txt", proxy1, sites[j], time_diff[j])
                        make_txt_file(output_file, proxy1, sites[j], time_diff[j])
                sort_file(site_file + sites[j] + ".txt", " Rs_Time ")
                sort_file(output_file, " Rs_Time ")


def getWorkingProxy(proxyList, url='http://www.google.com'):
    k = -1
    i = -1
    index = []

    workproxy = []
    time_diff2 = []
    sites = []
    site = urlparse(url).hostname
    # T_F=True

    for j in range(i + 1, len(proxyList)):
        time_diff = time.time()
        link = []
        T_F = True
        currentProxy = proxyList[j]
        # [T_F,site,time_diff]=is_bad_proxy(currentProxy,url)

        # [T_F, site, time_diff] = is_bad_proxy_urlib(currentProxy, url)
        # if not is_bad_proxy(currentProxy,url):
        proxy_, proxy_han, user_pass = make_proxy_handler(currentProxy)

        new_module = check_module(url, '/configs/Links_site/')
        responce = new_module.LINK(url).get_pdf_link(proxy_, user_pass)
        link = responce['links'];
        proxy = responce['proxy'];
        user_pass = responce['user_pass'];
        try:
            log_out = responce['log_out']
        except:
            log_out = ''

        # proxy_=proxy_.split("http://")[1]
        link_done = 0

        if link != []:
            # k = k + 1
            # new_module=check_module(url,'/configs/Links_site/')
            # responce=new_module.LINK(url).get_pdf_link(proxy_,user_pass)
            # link=responce['links'];proxy=responce['proxy'];user_pass=responce['user_pass'];responce['user_pass']
            # log("%s is working" % (currentProxy))
            if link != []:
                link_done = 1
                time_diff = str(round(time.time() - time_diff, 2))
                print("%s is working for site " % proxy_ + site + " With Time  " + str(time_diff)) + 'Second'
                workproxy.append(currentProxy)
                sites.append(site)
                time_diff2.append(time_diff)
                index.append(j)
                # return currentProxy, j
        elif link_done == 0:
            # log("Bad Proxy %s" % (currentProxy))
            time_diff = str(round(time.time() - time_diff, 2))
            make_txt_file("configs//badproxylist.txt", proxy_, site, time_diff)
            print("%s is Bad Proxy for site " % proxy_ + site + " With Time " + str(time_diff))
            # print ("Bad Proxy %s" % (currentProxy))
    return workproxy, index, sites, time_diff2


def bad_proxy_tag(pip):
    z = ''
    pip=pip.replace('\r', '')
    try:
        # s=pip.split('SERVER_IP:'+z)[1].split(":")[0]
        proxy_info = {
            'ip': pip.split('For Site:' + z)[0].replace(' ', ''),
            'For Site:': pip.split('For Site:' + z)[1].split('Rs_Time' + z)[0],
            'time': pip.split('Rs_Time' + z)[1].split("Success_try:" + z)[0].replace(' ', ''),
            'Success_try': pip.split('Success_try:' + z)[1].split('Failed_try:' + z)[0],
            'Failed_try': pip.split('Failed_try:' + z)[1].split("av_Rs_Time:" + z)[0].replace(' ', ''),
            'av_time': pip.split('av_Rs_Time' + z)[1].split("av_Failed_try:" + z)[0].replace(' ', ''),
            'av_Failed_try': pip.split('av_Failed_try' + z)[1].split("av_Success_try:" + z)[0].replace(' ', ''),
            'av_Success_try': pip.split('av_Success_try:' + z)[1].replace('\n', '').replace('\r', '')
        }
        return proxy_info
    except:

        try:
            proxy_info = {
                'ip': pip.split('For Site:' + z)[0].replace(' ', ''),
                'For Site:': pip.split('For Site:' + z)[1].split('Rs_Time' + z)[0],
                'time': pip.split('Rs_Time' + z)[1].split("Success_try:" + z)[0].replace(' ', ''),
                'Success_try': pip.split('Success_try:' + z)[1].split('Failed_try:' + z)[0],
                'Failed_try': pip.split('Failed_try:' + z)[1].split("av_Rs_Time:" + z)[0].replace(' ', ''),
                'av_time': '0',
                'av_Failed_try': '0',
                'av_Success_try': '0'
            }
        except:
            proxy_info = {
                'ip': pip.replace('\n', '').replace('\r', ''),
                'For Site:': '',
                'time': '1',
                'Success_try': '0',
                'Failed_try': '0',
                'av_time': '0',
                'av_Failed_try': '0',
                'av_Success_try': '0'
            }
        return proxy_info


def find_form(form_file):
    sa = open(form_file, 'rb')
    listform = sa.readlines()
    # time.sleep(10)
    sa.close()
    k = -1
    form_data = {}
    list_s = {}
    # for line in listform:
    #     print '&&&&&&&&'
    #     print line+'\n'
    #     print '&&&&&&&&'
    f1=f2=f3=0
    for line in listform:
        if not re.findall('#', line.replace(' ','')[:3]) and line != '\n' and line != '\r\n':
            k = k + 1
            form_data[k] = bad_proxy_tag(line.replace('\n', ''))
            # f=form_data[k]
            # f1[k]=f['time'];f2[k]=f['Success_try'];f3[k]=f['Failed_try']
            list_s[k] = line
    # kk=len(f1)
    # f1_av=sum(f1 )/kk;f2_av=sum(f2 )/kk;f3_av=sum(f3 )/kk;
    # av_={
    #     'time_av':f1_av,
    #     'Success_try_av':f2_av,
    #     'Failed_try_av':f3_av,
    # }
    return form_data, list_s

def find_form_av(form_file):
    sa = open(form_file, 'rb')
    listform = sa.readlines()
    # time.sleep(10)
    sa.close()
    k = -1
    form_data = {}
    list_s = {}
    # for line in listform:
    #     print '&&&&&&&&'
    #     print line+'\n'
    #     print '&&&&&&&&'
    f1=[0];f2=[0];f3=[0]
    for line in listform:
        if not re.findall('#', line.replace(' ','')[:3]) and line != '\n' and line != '\r\n':
            k = k + 1
            form_data[k] = bad_proxy_tag(line.replace('\n', ''))
            f=form_data[k]
            if k>=1:
                f1.append(float(f['time']))
                f2.append(float(f['Success_try']))
                f3.append(float(f['Failed_try']))
            else:
                f1[k]=float(f['time'])
                f2[k]=float(f['Success_try'])
                f3[k]=float(f['Failed_try'])

            list_s[k] = line
    kk=len(f1)
    f1_av=sum(f1 )/kk;f2_av=sum(f2 )/kk;f3_av=sum(f3 )/kk;
    f1_av="%.3f" %f1_av;f2_av="%.3f" %f2_av;f3_av="%.3f" %f3_av
    av_form={
        'time_av':f1_av,
        'Success_try_av':f2_av,
        'Failed_try_av':f3_av,
        }
    for k2 in  range(0,kk):
            f=form_data[k2]
            f['av_time']=f1_av;f['av_Failed_try']=f2_av;f['av_Success_try']=f3_av;
            form_data[k2]=f
    return form_data, list_s,av_form


    # self.url=url


if __name__ == "__main__":
    # test_url = 'http://pr4ss.tk/'
    # test_url = "http://ieeexplore.ieee.org/xpl/articleDetails.jsp?tp=&arnumber=6180383&queryText%3Dpower"
    # test_url ='http://jstor.org/action/showJournals'


    # proxy_checker(test_url,input_file = 'configs//proxylist.txt',output_file = 'configs//proxy_alive.txt',site_file="configs//sites_proxy//",defaulttimeout=30)
    # import commands
    # commands.getstatusoutput('python  proxy_checker3_all_function.py  --list "configs//proxylist2.txt" --url "www.jstor.org/action/showJournals"')
    # test_url='http://127.0.0.1'
    # replace("configs//badproxylist.txt", proxy_, +"For Site: "+site+" With Time "+time_diff)

    # ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python  proxy_checker3_all_function.py  --list 'configs//proxylist2.txt' --url "http://ieeexplore.ieee.org/xpl/articleDetails.jsp?tp=&arnumber=6180383&queryText%3Dpower"

    # proxy_checker(test_url,input_file = 'configs//proxylist2.txt',output_file = 'configs//proxy_alive.txt',site_file="configs//sites_proxy//",defaulttimeout=30)
    # proxy_checker(test_url,input_file ,output_file ,defaulttimeout)
    import django

    # data,time_diff=getContentBrowser([],'pr2ss.tk/ss/')


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
    help1 = 'Address url file name to be downloaded like:"www.google.com"\n' + \
            "Please make attention 'www.google.com' is risky use  only with" + '"blabla"'
    parser.add_option('-u', '--url', type='string', dest='url', help=help1)
    # parser.add_option('-p','--proxy', dest='proxy', help=' proxy setting for url file name to be download like:121.121.21.21:90')
    # parser.add_option('-s','--user', dest='user_name', help='user & password of proxy setting')
    # parser.add_option('-i', dest='input_fname', help='file name to be watermarked (pdf)')
    # parser.add_option('-w', dest='watermark_fname', help='watermark file name (pdf)')

    parser.add_option('-l', '--list', dest='list',
                      help='list file  proxy for checkig via url like =configs//proxylis2.txt',
                      default='configs//proxylis2.txt')
    parser.add_option('-v', '--alive', dest='alive',
                      help='list file  proxy for writing alive proxy via url like =configs//proxy_alive.txt',
                      default='configs//proxy_alive.txt')
    parser.add_option('-V', '--alive_host', dest='alive_host',
                      help='list file  proxy for writing alive proxy based of hosts via url like =configs//sites_proxy//',
                      default='configs//sites_proxy//')
    parser.add_option('-t', '--time', dest='timeout', help='default timeout to end connection=30', default=30)
    # parser.add_option('-o', dest='outdir', help='outputdir used with option -d', default='tmp')
    options, args = parser.parse_args()
    if options.url:
        proxy_checker(options.url, options.list, options.alive, options.alive_host, options.timeout)
    else:
        parser.print_help()
        pass

        # socket.setdefaulttimeout(30)
        # # proxyList = getProxiesList()
        # # for host in open(input_file).readlines():
        # #  g= host.strip()
        # hosts = [host.strip() for host in open(input_file).readlines()]
        # # pr=['198.27.97.214:3127', '202.202.0.163:3128']
        # # listhandle = open(input_file).read().split('\n')
        # # for line in listhandle:
        # #     proxyList.append( line.split('@')[0])
        # #     details= line.split('@')
        # #     email = details[1].split(':')[0]
        # #     password = details[1].split(':')[1].replace('\n', '')
        #
        # proxyList=hosts
        # proxy=['151.236.14.48:80@ user:pass For Site:http://stackoverflow.com']
        # sites=['stackowerflow.com']
        # # proxy, index,sites = getWorkingProxy(proxyList,test_url)
        # if proxy!=[]:
        #     # _web = getOpener(proxy)
        #     # saveAlive = open("configs//proxy_alive.txt", 'wb')
        #     i=-1
        #     for j in range(i+1, len(proxyList)):
        #         if  re.findall("For Site:",proxyList[j]):
        #             proxy1=proxyList[j].split("For Site:")[0]
        #             proxy2=proxyList[j].split("For Site:")[1]
        #             if  re.findall(sites[j],proxy2):
        #                 pass
        #             else:
        #                 # replace("configs//sites_proxy//"+sites[j]+".txt", proxyList[j],proxy1+"For Site:"+proxy2+";"+sites[j])
        #                 make_txt_file(site_file+sites[j]+".txt",proxy1,sites[j])
        #                 make_txt_file(output_file,proxy1,sites[j])
        #
        #         else:
        #             proxy1=proxyList[j]
        #             make_txt_file(site_file+sites[j]+".txt",proxy1,sites[j])
        #             make_txt_file(output_file,proxy1,sites[j])

        #     replace("configs//sites_proxy//"+sites[j]+".txt", proxyList[j],proxyList[j]+"For Site:"+sites[j])
        # # make_txt_file("configs//sites_proxy//"+sites[j]+".txt",proxyList[j],sites[j])
        # make_txt_file("configs//proxy_alive.txt",proxyList[j],sites[j])
        #
        # with open("configs//sites_proxy//"+sites[j]+".txt", 'r') as file:
        # # read a list of lines into data
        #     data = file.readlines()
        # data=proxy[j]+sites[j]+'\n'
        # with open("configs//sites_proxy//"+sites[j]+".txt", 'w') as file:
        #     file.writelines( data )
        # # saveAlive_sites = open("configs//sites_proxy//"+sites[j]+".txt", 'w')
        # # saveAlive_sites.write(proxy[j]+sites[j]+'\n')
        # saveAlive.write(proxy[j]+"For Site:"+sites[j]+'\n')
        # saveAlive.close()
        # saveAlive_sites.close()

        # for current_proxy in proxyList:
        #     saveAlive = open("proxy_alive.txt", 'wb')
        #     proxy, index = getWorkingProxy(current_proxy,test_url)
        #     if proxy:
        #       _web = getOpener(current_proxy)
        #       saveAlive.write(proxy)
        # saveAlive.close()
