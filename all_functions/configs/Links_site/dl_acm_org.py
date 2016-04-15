#!/usr/bin/python
#----------------------------------------------------------------------
#
# Author:      Laszlo Nagy
#
# Copyright:   (c) 2005 by Szoftver Messias Bt.
# Licence:     BSD style
#
#
#----------------------------------------------------------------------
# from __future__ import with_statement
# from google.appengine.api import files
import os, re, errno, sys, time
import urllib
import urllib2, urlparse
from urlparse import urlparse as urlparse2
from BeautifulSoup import BeautifulSoup
import cookielib
import mimetypes

import random
import mechanize
import md5, hashlib


print "Content-type: text/html\n"
print "this is running"


def import_mod(**kwargs):
    # import_mod(from_module='sss',from_module2='s')
    from_module_name1 = kwargs['from_module']
    try:
        kwargs['from_module2']
        from_module_name2 = kwargs['from_module2']
    except:
        from_module_name2 = ''

    try:
        kwargs['dir_location']
        CurrentDir = os.path.dirname(os.path.realpath(__file__))
        s = CurrentDir.replace('\\', '/') + kwargs['dir_location']
        sys.path.insert(0, s)
    except:
        pass
    if from_module_name1 in sys.modules:
        print "@@@@@@@@@@@@@@ module already exist  for " + from_module_name1 + ' is \n: @@@@@@@@@@@@@@\n\n'
        if from_module_name2 == '':
            mod = sys.modules[from_module_name1]
        else:
            mod1 = sys.modules[from_module_name1]
            mod = getattr(mod1, from_module_name2)
            print "@@@@@@@@@@@@@@ module already exist  for " + from_module_name1 + '.' + from_module_name2 + ' is \n: @@@@@@@@@@@@@@\n\n'
    else:
        print "@@@@@@@@@@@@@@ module inserting for " + from_module_name1 + "  \n: @@@@@@@@@@@@@@\n\n"
        if from_module_name2 == '':
            mod = __import__(from_module_name1)
        else:
            mod1 = __import__(from_module_name1)
            mod = getattr(mod1, from_module_name2)
            # mod = getattr(mod1,from_module_name2)
            pass
            print's'
            # mod=mod1[from_module_name2]
    return mod

    # return urlparse.urljoin('file:', urllib.pathname2url(path))


class MozillaCacher(object):
    """A dictionary like object, that can cache results on a storage device."""

    def __init__(self, cachedir='.cache'):
        self.cachedir = cachedir
        if not os.path.isdir(cachedir):
            os.mkdir(cachedir)

    def name2fname(self, name):
        return os.path.join(self.cachedir, name)

    def __getitem__(self, name):
        if not isinstance(name, str):
            raise TypeError()
        fname = self.name2fname(name)
        if os.path.isfile(fname):
            return file(fname, 'rb').read()
        else:
            raise IndexError()

    def __setitem__(self, name, value):
        if not isinstance(name, str):
            raise TypeError()
        fname = self.name2fname(name)
        if os.path.isfile(fname):
            os.unlink(fname)
        f = file(fname, 'wb+')
        try:
            f.write(value)
        finally:
            f.close()

    def __delitem__(self, name):
        if not isinstance(name, str):
            raise TypeError()
        fname = self.name2fname(name)
        if os.path.isfile(fname):
            os.unlink(fname)

    def __iter__(self):
        raise NotImplementedError()

    def has_key(self, name):
        return os.path.isfile(self.name2fname(name))


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


class MozillaEmulator(object):
    def __init__(self, cacher={}, trycount=0, debug=False, **kwargs):
        """Create a new MozillaEmulator object.

        @param cacher: A dictionary like object, that can cache search results on a storage device.
            You can use a simple dictionary here, but it is not recommended.
            You can also put None here to disable caching completely.
        @param trycount: The download() method will retry the operation if it fails. You can specify -1 for infinite retrying.
                A value of 0 means no retrying. A value of 1 means one retry. etc."""

        if kwargs['cookies']:
            self.cookie3 = kwargs['cookies']
        else:
            self.cookie3 = ''
        self.cacher = cacher
        if self.cookie3 != '':
            self.cookies = cookielib.MozillaCookieJar(self.cookie3)
        else:
            self.cookies = cookielib.MozillaCookieJar()
        # self.cookies = cookielib.CookieJar()
        self.debug = debug
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

        if proxy != [] and (not re.findall("None", proxy)) and proxy != '':
            if User_Pass != [] and User_Pass != '':
                proxies = {"http": "http://" + User_Pass + "@" + proxy}
            else:
                proxies = {"http": "http://%s" % proxy}
            proxy_support = urllib2.ProxyHandler(proxies)
            # opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler(debuglevel=1))
        else:
            proxy_support = urllib2.ProxyHandler()
            # opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler(debuglevel=1))
            # url=link.absolute_url
            # headers={'User-agent' : 'Mozilla/5.0'}

        http_handler = urllib2.HTTPHandler(debuglevel=self.debug)
        https_handler = urllib2.HTTPSHandler(debuglevel=self.debug)

        # default_classes = [ProxyHandler, UnknownHandler, HTTPHandler,
        #                    HTTPDefaultErrorHandler, HTTPRedirectHandler,
        #                    FTPHandler, FileHandler, HTTPErrorProcessor]


        u = urllib2.build_opener(proxy_support, http_handler, https_handler, urllib2.HTTPCookieProcessor(self.cookies),
                                 redirector)
        urllib2.install_opener(u)

        u.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; hu-HU; rv:1.7.8) Gecko/20050511 Firefox/1.0.4')]
        if not postdata is None:
            req.add_data(postdata)

        if self.cookie3 == '':
            fo = os.getcwd().replace('\\', '/')
            # pathname = os.path.join("cookies", cookie3)
            site = urlparse2(url).hostname
            if not os.path.isdir(fo + "/cookies/" + site): os.mkdir(fo + "/cookies/" + site)
            chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            self.cookie3 = fo + "/cookies/" + site + '/' + ''.join([random.choice(chars) for x in range(5)]) + ".txt"
        self.cookies.save(self.cookie3)
        return (req, u, self.cookie3)

    def download(self, url, proxy=[], User_Pass=[], postdata=None, extraheaders={}, forbid_redirect=False,
                 trycount=None, fd=None, onprogress=None, only_head=False):
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
        while True:
            try:
                key = self._hash(url)
                if (self.cacher is None) or (not self.cacher.has_key(key)):
                    req, u, cookie3 = self.build_opener(url, proxy, User_Pass, postdata, extraheaders, forbid_redirect)
                    openerdirector = u.open(req)
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
                    #try:
                #    d2= GzipFile(fileobj=cStringIO.StringIO(data)).read()
                #    data = d2
                #except IOError:
                #    pass
                self.cookies.save(self.cookie3)
                return data, cookie3
            except urllib2.URLError:
                er = urllib2.URLError
                cnt += 1
                if (trycount > -1) and (trycount < cnt):
                    raise
                    # Retry :-)
                if self.debug:
                    print "MozillaEmulator: urllib2.URLError, retryting ", cnt


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
        if self.cookie3 == '':
            CurrentDir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
            fo = os.path.abspath(os.path.join(CurrentDir, '../..')).replace('\\', '/')
            # pathname = os.path.join("cookies", cookie3)
            site = urlparse2(self.url).hostname
            if not os.path.isdir(fo + "/cookies/" + site): os.mkdir(fo + "/cookies/" + site)
            chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            self.cookie3 = fo + "/cookies/" + site + '/' + ''.join([random.choice(chars) for x in range(5)]) + ".txt"
            self.cj = cookielib.LWPCookieJar()
        else:
            self.cj = cookielib.LWPCookieJar()
            self.cj.revert(self.cookie3)
        opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(self.cj))

        br.set_cookiejar(self.cj)
        # os.chdir(..)


        # Browser options
        br.set_handle_equiv(True)
        br.set_handle_gzip(True)
        br.set_handle_referer(True)    # no allow everything to be written to
        br.set_handle_robots(False)   # no robots
        br.set_handle_refresh(True)  # can sometimes hang without this
        br.set_handle_redirect(True)

        # Follows refresh 0 but not hangs on refresh > 0
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # Want debugging messages?
        #br.set_debug_http(True)
        #br.set_debug_redirects(True)
        #br.set_debug_responses(True)

        # User-Agent (this is cheating, ok?)
        br.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Linux; U; Android 2.3.4; en-us; T-Mobile myTouch 3G Slide Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'),
                         ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                         ('Accept-Language', 'en-gb,en;q=0.5'),
                         ('Accept-Encoding', 'gzip,deflate'),
                         ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'),
                         ('Keep-Alive', '115'),
                         ('Connection', 'keep-alive'),
                         ('Cache-Control', 'max-age=0'),
                         ('Referer', 'http://yahoo.com')]
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

        self.cj.save(self.cookie3)

        return br


    # Proxy password
    # br.add_proxy_password("joe", "password")
    # self.dl_acm = "http://dl.acm.org/citation.cfm?id=99977.100000&coll=DL&dl=ACM"


    def speed_download(self, pdf_url, piece_size=1024 * 1024):
        # br2=self.br
        openerdirector = self.br.open(pdf_url)
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
                localName = LINK(PDF_Dir=PDF_Dir, Watermarked_PDF_Files_Dir=Watermarked_PDF_Files_Dir).filename(
                    pdf_url.absolute_url)
                # pathname = os.path.join("PDF_Files", localName.filename)
                # s=get_full_url(pdf_url)
                f1 = self.br.retrieve(pdf_url.absolute_url, localName.pdf_Folder_filename)

        else:
            localName = LINK(PDF_Dir=PDF_Dir, Watermarked_PDF_Files_Dir=Watermarked_PDF_Files_Dir).filename(
                pdf_url.absolute_url)
            f1 = self.br.retrieve(pdf_url.absolute_url, localName.pdf_Folder_filename)
            # f1 = self.br.retrieve(pdf_url, localName.pdf_Folder_filename)

        if f1:
            self.cj.save(self.cookie3)

        return f1[0], self.cookie3 #,pdf_path



        # return os.getcwd()+PDF_File.pdf_Folder_filename,os.getcwd()+PDF_File.W_pdf_Folder_filename


class web(object):
    def __init__(self, url=''):
        self.url = url

    def download_mechanism(self, url='', proxy='', user_pass='', location='PDF_Files/', **kwargs):
        """

        :param url:
        """
        if kwargs['cookies']:
            cookies = kwargs['cookies']
        else:
            cookies = ''
        if proxy == '' or proxy == []:
            import proxy_checker3_all_function

            fo = os.getcwd().replace('\\', '/')
            pr_h, proxy_h, user_pass_h = proxy_checker3_all_function.make_returning_proxy("configs//sites_proxy//", url)
            os.chdir(fo)
        else:
            pr_h = []
            user_pass_h = []
            pr_h.append(proxy)
            user_pass_h.append(user_pass)
            try:
                i = user_pass_h.index("")
                del user_pass_h[i]
            except:
                print 'there is no empty lsit in user_password list'
            try:
                i = pr_h.index("")
                del pr_h[i]
            except:
                print 'there is no empty lsit in proxy list'

        # pr_h=['222.66.115.233:80 ', '202.202.0.163:3128 ', '151.236.14.48:80']

        pdf_dw_li = pdf_dw_Wr_li = []
        frontpage = []
        don_flg = -1
        if pr_h != []:
            i = -1
            for j in range(i + 1, len(pr_h)):
                if don_flg != 1:
                    # debug = True
                    # cash = None
                    # dl = MozillaEmulator(cash,0,debug)
                    # dl = MozillaEmulator(cash, 0)
                    try:
                        if 'user_pass_h[j]' is locals():
                            # frontpage,cookies=MECHANIZM( proxy='', User_Pass='').speed_download(pdf_url,piece_size=1024*1024)
                            # frontpage,cookies = MECAHNIZM(pr_h[j],user_pass_h[j],cookies=cookies,url=url).speed_download(url)
                            frontpage, cookies = MECAHNIZM(pr_h[j], user_pass_h[j], cookies=cookies,
                                                           url=url).download_pdf_br(url)
                            pr = pr_h[j]
                            upss = user_pass_h[j]
                        else:
                            frontpage, cookies = MECAHNIZM(pr_h[j], cookies=cookies, url=url).download_pdf_br(url)
                            # frontpage,cookies = MECAHNIZM(pr_h[j],cookies=cookies,url=url).speed_download(url)
                            pr = pr_h[j]
                            upss = ''
                    except:
                        print "we cant dowload beacuse of invalid tag or invalid proxy line 620" + "\n"
                    if frontpage != []:
                        print "file downloaded "
                        don_flg = 1
                        # pr = pr_h[j]
                        # upss = user_pass_h[j]
                        break
                else:
                    print "we could not download file with  proxy:" + pr_h[j]
            if don_flg != 1:
                print "we are unable to download your file Now!!" + '\n'
                frontpage = []
                pr = ''
                upss = ''
                cookies = ''
        else:
            print "we are unable to download your file Now!! Becaouse proxy is empty" + '\n'
        return frontpage, pr, upss, cookies


    def download_mechanism_link(self, url='', proxy='', user_pass='', location='PDF_Files/', **kwargs):
        """

        :param url:
        """
        if kwargs['cookies']:
            cookies = kwargs['cookies']
        else:
            cookies = ''
        if proxy == '' or proxy == []:
            import proxy_checker3_all_function

            fo = os.getcwd().replace('\\', '/')
            pr_h, proxy_h, user_pass_h = proxy_checker3_all_function.make_returning_proxy("configs//sites_proxy//", url)
            os.chdir(fo)
        else:
            pr_h = []
            user_pass_h = []
            pr_h.append(proxy)
            user_pass_h.append(user_pass)
            try:
                i = user_pass_h.index("")
                del user_pass_h[i]
            except:
                print 'there is no empty lsit in user_password list'
            try:
                i = pr_h.index("")
                del pr_h[i]
            except:
                print 'there is no empty lsit in proxy list'

        # pr_h=['222.66.115.233:80 ', '202.202.0.163:3128 ', '151.236.14.48:80']

        pdf_dw_li = pdf_dw_Wr_li = []
        frontpage = []
        don_flg = -1
        if pr_h != []:
            i = -1
            for j in range(i + 1, len(pr_h)):
                if don_flg != 1:
                    # debug = True
                    # cash = None
                    # dl = MozillaEmulator(cash,0,debug)
                    # dl = MozillaEmulator(cash, 0)
                    try:
                        if 'user_pass_h[j]' is locals():
                            # frontpage,cookies=MECHANIZM( proxy='', User_Pass='').speed_download(pdf_url,piece_size=1024*1024)
                            frontpage, cookies = MECAHNIZM(pr_h[j], user_pass_h[j], cookies=cookies,
                                                           url=url).speed_download(url)
                            # frontpage,cookies = MECAHNIZM(pr_h[j],user_pass_h[j],cookies=cookies,url=url).download_pdf_br(url)
                            pr = pr_h[j]
                            upss = user_pass_h[j]
                        else:
                            # frontpage,cookies = MECAHNIZM(pr_h[j],cookies=cookies,url=url).download_pdf_br(url)
                            frontpage, cookies = MECAHNIZM(pr_h[j], cookies=cookies, url=url).speed_download(url)
                            pr = pr_h[j]
                            upss = ''
                    except:
                        print "we cant dowload beacuse of invalid tag or invalid proxy line 620" + "\n"
                    if frontpage != []:
                        print "file downloaded "
                        don_flg = 1
                        # pr = pr_h[j]
                        # upss = user_pass_h[j]
                        break
                else:
                    print "we could not download file with  proxy:" + pr_h[j]
            if don_flg != 1:
                print "we are unable to download your file Now!!" + '\n'
                frontpage = []
                pr = ''
                upss = ''
                cookies = ''
        else:
            print "we are unable to download your file Now!! Becaouse proxy is empty" + '\n'
        return frontpage, pr, upss, cookies


    def download(self, url='', proxy='', user_pass='', location='PDF_Files/', **kwargs):
        """

        :param url:
        """
        if kwargs['cookies']:
            cookies = kwargs['cookies']
        else:
            cookies = ''
        if proxy == '' or proxy == []:
            import proxy_checker3_all_function

            fo = os.getcwd().replace('\\', '/')
            pr_h, proxy_h, user_pass_h = proxy_checker3_all_function.make_returning_proxy("configs//sites_proxy//", url)
            os.chdir(fo)
        else:
            pr_h = []
            user_pass_h = []
            pr_h.append(proxy)
            user_pass_h.append(user_pass)
            # try:
            #     i = user_pass_h.index("")
            #     del user_pass_h[i]
            # except:
            #     print 'there is no empty lsit in user_password list'
            try:
                i = pr_h.index("")
                del pr_h[i]
            except:
                pass
                # print 'there is no empty list in proxy list'

        # pr_h=['222.66.115.233:80 ', '202.202.0.163:3128 ', '151.236.14.48:80']

        pdf_dw_li = pdf_dw_Wr_li = []
        frontpage = []
        don_flg = -1
        if pr_h != []:
            i = -1
            for j in range(i + 1, len(pr_h)):
                if don_flg != 1:
                    debug = True
                    cash = None
                    # dl = MozillaEmulator(cash,0,debug)
                    dl = MozillaEmulator(cash, 0, cookies=cookies)
                    try:
                        if user_pass_h[j] != '':

                            frontpage, cookies = dl.download(url, pr_h[j], user_pass_h[j])
                            pr = pr_h[j]
                            upss = user_pass_h[j]
                        else:
                            frontpage, cookies = dl.download(url, pr_h[j])
                            pr = pr_h[j]
                            upss = ''



                    except:
                        print "we cant download because of invalid tag or invalid proxy line 620" + "\n"

                    if frontpage != []:
                        if len(user_pass_h[j]) != 0:
                            print "file downloaded with " + str(pr_h[j]) + '@' + str(user_pass_h[j])
                        else:
                            print "file downloaded with " + str(pr_h[j])
                        don_flg = 1
                        # pr = pr_h[j]
                        # upss = user_pass_h[j]
                        break
                else:
                    print "we could not download file with  proxy:" + pr_h[j]
            if don_flg != 1:
                print "we are unable to download your file Now!!" + '\n'
                frontpage = []
                pr = ''
                upss = ''
                # cookies=''


        else:
            print "we are unable to download your file Now!! Beacouse proxy is empty" + '\n'

        return frontpage, pr, upss, cookies


def twil_find_pdf_link(link):
    site = urlparse2(link).hostname
    # site2=site.replace('.','_')
    fo = os.getcwd().replace('\\', '/')
    CurrentDir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
    Parent_Dir = os.path.abspath(os.path.join(CurrentDir, '../')).replace('\\', '/')
    os.chdir(Parent_Dir)
    tw = twill(link, site_list_form='sites_proxy/' + site + '/site_list_form.txt')
    form = tw.find_form()
    for k in range(0, len(form)):
        # # br,cookies=tw.login_to_site(link,form[k],[],[])
        # [html, cookies, links, title, times,mydriver] = tw.login_to_site_selenium(link, form[k], [], [])
        # if links != []:
        #     html=tw.Download_selenium( links,cookies,mydriver)
        #     break
        [html, cookies, links, title, times, log_out] = tw.twill_find_link(link, form[k])
        if links != []:
            break
    os.chdir(fo)
    return html, cookies, links, title, form[k], times, log_out


def twil_download_pdf_link0(link):
    site = urlparse2(link).hostname
    # site2=site.replace('.','_')
    fo = os.getcwd().replace('\\', '/')
    CurrentDir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
    Parent_Dir = os.path.abspath(os.path.join(CurrentDir, '../')).replace('\\', '/')
    os.chdir(Parent_Dir)
    tw = twill(link, site_list_form='sites_proxy/' + site + '/site_list_form.txt')
    form = tw.find_form()
    for k in range(0, len(form)):
        # br,cookies=tw.login_to_site(link,form[k],[],[])
        [html, cookies, links, title, times] = tw.login_to_site_selenium(link, form[k], [], [])
        if links != []:
            break
        [html, cookies, links, title, times] = tw.twill_find_link(link, form[k])
        if links != []:
            break
    os.chdir(fo)
    return html, cookies, links, title, form[k], times


class twill:
    def __init__(self, link, **kwargs):

        # import socket
        # if kwargs['url']:self.url=kwargs['url']
        if kwargs['site_list_form']: self.site_list_form = kwargs['site_list_form']
        # if kwargs['url_to_ez_file']:self.url_to_ez_file=kwargs['url_to_ez_file']
        self.socket = import_mod(from_module='socket')
        self.socket.setdefaulttimeout(100)
        self.main_url = link
        self.site = urlparse2(link).hostname
        self.cookies_dir = os.getcwd().replace('\\', '/') + '/sites_proxy/' + self.site + '/cookies'
        if not os.path.isdir(self.cookies_dir):
            os.mkdir(self.cookies_dir)
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.cookies = self.cookies_dir + '/' + ''.join([random.choice(chars) for x in range(5)]) + ".txt"


    def find_form(self):
        sa = open(self.site_list_form, 'r')
        listform = sa.readlines()
        sa.close()
        k = -1
        form_data = {}
        for line in listform:
            if not re.findall('#', line) and line != '\n':
                k = k + 1
                form_data[k] = self.usr_tag(line.replace('\n', ''))
        return form_data

        # self.url=url

    def find_ez_base_url(self, link):
        form = self.find_form()
        for k in range(0, len(form)):
            self.twill_download(self, link, form[k])
            #     sa=open(self.site_list_form,'r')

    #     listform=sa.readlines()
    #     sa.close()
    #     host= urlparse2(self.url).hostname
    #     k=-1
    #     for line in listform:
    #         if line.find(host)!=-1:
    #             k=k+1
    #             form_data[k]=self.usr_tag(line)
    #             # break
    #     return form_data

    def usr_tag(self, pip):
        z = '--'
        try:
            s = pip.split('USER:' + z)[1].split(":")[0]
            proxy_info = {
                'ezproxy_host': pip.split('USER:' + z)[0].replace(' ', ''),
                'user': pip.split('USER:' + z)[1].split(":")[0],
                'pass': pip.split('USER:' + z)[1].split(z)[0].split(":")[1],
                'user_tag': pip.split('Form_Tag:' + z)[1].split(":")[0],
                'pass_tag': pip.split('Form_Tag:' + z)[1].split(z)[0].split(":")[1],
                'submit_tag_name': pip.split('Submit_tag:' + z)[1].split(":")[0],
                'submit_tag_value': pip.split('Submit_tag:' + z)[1].split(z)[0].split(":")[1],
                'Form_id': pip.split('Form_id:' + z)[1].split(z)[0],
                'Form_Type': pip.split('Form_Type:' + z)[1].split(z)[0],
                'database_link': pip.split('database_link:' + z)[1].split(z)[0].replace('\n', ''),
                'Log_test': pip.split('Log_test:' + z)[1].split(z)[0].replace('\n', ''), # or 8080 or whatever
                'Log_out': pip.split('Log_out:' + z)[1].split(z)[0].replace('\n', '') # or 8080 or whatever


            }
            try:

                proxy_info['submit_tag_name2'] = pip.split('Submit_tag2:' + z)[1].split(":")[0]

                proxy_info['user_tag2'] = pip.split('Form_Tag2:' + z)[1].split(":")[0]
                proxy_info['pass_tag2'] = pip.split('Form_Tag2:' + z)[1].split(z)[0].split(":")[1],
                proxy_info['submit_tag_value2'] = pip.split('Submit_tag2:' + z)[1].split(z)[0].split(":")[1]
                proxy_info['Form_id2'] = pip.split('Form_id2:' + z)[1].split(z)[0]
                proxy_info['Form_Type2'] = pip.split('Form_Type2:' + z)[1].split(z)[0].replace('\n',
                                                                                               '') # or 8080 or whatever
            except:
                proxy_info['submit_tag_name2'] = ''

                # proxy_="http://%(user)s:%(pass)s@%(host)s:%(port)s" % proxy_info
                # proxy_handler = urllib2.ProxyHandler({"http" : "http://%(user)s:%(pass)s@%(host)s:%(port)s" % proxy_info})
        except:
            proxy_info = {
                'Form_Tag': pip.split('Form_Tag:')[1].replace('\n', '') # or 8080 or whatever
            }
        return proxy_info

    def twill_download(self, link, cookies):
        # self.url="%(ezproxy_host)s"%form_data
        # self.database_link="%(database_link)s"%form_data
        # self.username="%(user)s"%form_data
        # self.password="%(pass)s"%form_data
        # self.user_tag="%(user_tag)s"%form_data
        # self.pass_tag="%(pass_tag)s"%form_data
        # self.Form_id="%(Form_id)s"%form_data
        # self.submit_tag_name="%(submit_tag_name)s"%form_data
        # self.submit_tag_value="%(submit_tag_value)s"%form_data
        # self.Form_Type="%(Form_Type)s"%form_data
        # self.log_done="%(Log_test)s"%form_data
        site = urlparse2(link).hostname


        # self.a.config("readonly_controls_writeable", 1)
        # self.b = self.a.get_browser()
        # self.b.set_agent_string("Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14")
        # self.b.clear_cookies()
        twill = import_mod(from_module='twill')

        # t_com = twill.commands
        # t_com.reset_browser
        # t_com.reset_output
        t_com = twill.commands

        ## get the default browser
        t_brw = t_com.get_browser()
        t_brw.set_agent_string(
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14")
        t_brw.load_cookies(cookies)
        socket = import_mod(from_module='socket')
        socket.setdefaulttimeout(3000)
        ## open the url
        # url = 'http://google.com'
        # t_brw.find_link(link)
        t_brw.go(link)
        html0 = t_brw.result.page
        print '@@@@@@@@@@@@@ html0 download by twill is @@@@@@@@@@@@'
        print html0[:20]
        print '@@@@@@@@@@@@@ html0 download by twill is @@@@@@@@@@@@'
        # time.sleep(10)
        link2 = t_brw.result.url
        if not (html0[:4] == '%PDF') or html0 == []:
            html, cookies = MECAHNIZM('', '', cookies=cookies, url=link2).speed_download(link2)
            # html3,pr,upss,cookies=web().download_mechanism_link(link,'',cookies=cookies)
            if not (html[:4] == '%PDF') or html == []:
                t_brw.save_cookies(cookies)
                t_brw = t_com.get_browser()
                t_brw.set_agent_string(
                    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14")
                t_brw.load_cookies(cookies)
                socket = import_mod(from_module='socket')
                socket.setdefaulttimeout(3000)
                html3, pr, upss, cookies = web().download_mechanism_link(link, '', cookies=cookies)
                t_brw.go(link2)
                html = t_brw.result.page

                print '@@@@@@@@@@@@@ html download by twill is @@@@@@@@@@@@'
                print html
                print '@@@@@@@@@@@@@ html download by twill is @@@@@@@@@@@@'
                # time.sleep(10)
        else:
            html = html0
        try:
            sa = open(self.site_list_form, 'r')
            listform = sa.readlines()
            # time.sleep(10)
            sa.close()
            k = -1
            form_data = {}
            # for line in listform:
            #     print '&&&&&&&&'
            #     print line+'\n'
            #     print '&&&&&&&&'
            for line in listform:
                if not re.findall('#', line) and line != '\n':
                    site2 = urlparse2(self.url).hostname
                    if re.findall('#', line): pass
        except:
            pass
        return html

    def twill_find_link(self, link, form_data):
        # from goto import goto, label
        self.url = "%(ezproxy_host)s" % form_data
        self.database_link = "%(database_link)s" % form_data
        self.username = "%(user)s" % form_data
        self.password = "%(pass)s" % form_data
        self.user_tag = "%(user_tag)s" % form_data
        self.pass_tag = "%(pass_tag)s" % form_data
        self.Form_id = "%(Form_id)s" % form_data
        self.submit_tag_name = "%(submit_tag_name)s" % form_data
        self.submit_tag_value = "%(submit_tag_value)s" % form_data
        self.Form_Type = "%(Form_Type)s" % form_data
        self.log_done = "%(Log_test)s" % form_data
        self.log_out = "%(Log_out)s" % form_data

        self.submit_tag_name2 = '%(submit_tag_name2)s' % form_data

        site = urlparse2(link).hostname

        self.cookies_dir = os.getcwd().replace('\\', '/') + '/sites_proxy/' + site + '/cookies'
        if not os.path.isdir(self.cookies_dir):
            os.mkdir(self.cookies_dir)
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.cookies = self.cookies_dir + '/' + ''.join([random.choice(chars) for x in range(5)]) + ".txt"
        # self.a.config("readonly_controls_writeable", 1)
        # self.b = self.a.get_browser()
        # self.b.set_agent_string("Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14")
        # self.b.clear_cookies()
        twill = import_mod(from_module='twill')
        t_com = twill.commands
        t_com.reset_browser
        t_com.reset_output
        t_com = twill.commands
        ## get the default browser
        t_brw = t_com.get_browser()
        t_brw.set_agent_string(
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14")
        ## open the url
        # url = 'http://google.com'
        t_brw.go(self.url)
        html = t_brw.result.page
        print html
        # print fill_login_form(url, html, "john", "secret")
        if re.findall(self.log_done, html):
            # goto .find
            print ("You are logged on to the Public Access to Court Electronic "
                   "Records (PACER) Case Search website as " + self.url + ". All costs "
                                                                          "will be billed to this account.")

            # t_brw.go(self.database_link)
            # site = urlparse2(link).hostname
            site2 = urlparse2(self.url).hostname
            base_url = 'http://' + site + '.' + site2
            ez_link = 'http://' + site + '.' + site2 + link.split(site)[1]
            time0 = time.time()
            t_brw.go(ez_link)
            time_diff = str(round(time.time() - time0, 2))
            html = t_brw.result.page
            # f=1
            # links=LINK().find_my_tilte(data=html,start_dash='<a id="pdfLink" href="',end_dash='"',make_url=True)
            #
            # if links==''or links==[]:
            #     links =LINK().soap_my(data=html, tag='title="Download PDF" ', attr='a', href='href',url=base_url)
            #
            # if links==[] or links=='':
            #     links =LINK().soap_my(data=html, tag="Download PDF", attr='a', href='href',url=base_url)
            # if links==[] or links=='':
            #     links=LINK().soap_my(data=html,tag='pdfLink',attr='a',href='href',url=base_url)
            # re.findall('if(SDM.pageType'.html)
            if self.submit_tag_name2 != '' and not re.findall("SDM.pageType", html):
                self.submit_tag_value2 = '%(submit_tag_value2)s' % form_data
                self.Form_id2 = '%(Form_id2)s' % form_data
                self.Form_Type2 = '%(Form_Type2)s' % form_data
                all_forms = t_brw.get_all_forms()         ## this returns list of form objects
                print "Forms:"
                t_brw.showforms()

                ## now, you have to choose only that form, which is having POST method

                self.formnumber = 0
                formnumber = 1
                for each_frm in all_forms:
                    self.formnumber = 1 + self.formnumber
                    attr = each_frm.attrs             ## all attributes of form
                    try:
                        form_id = each_frm.attrs['id']
                    except:
                        form_id = ''

                    if each_frm.method == 'POST' and (form_id == self.Form_id2 ):
                        ctrl = each_frm.controls
                        for ct in ctrl:
                            if ct.type == 'radio':     ## i did it as per my use, you can put your condition here
                                # ct._value = "twill"

                                # t_com.clicked(each_frm,'%(user_tag2)s'%form_data)            ## clicked takes two parameter, form object and button name to be clicked.

                                t_com.showforms()
                                t_com.fv(self.formnumber, '%(user_tag2)s' % form_data, each_frm.controls[3]._value)
                                t_com.showforms()
                                t_com.submit()
                                content = t_com.show()
                                break
                                # print 'debug twill post content:', content


                        # t_com.formclear(formnumber)
                        # va=each_frm.controls[3]._value
                        # t_com.fv(self.formnumber, '%(user_tag2)s'%form_data, each_frm.controls[3]._value)
                        # # t_com.fv(self.formnumber, self.pass_tag, self.password)
                        # print "Forms:"
                        # t_brw.showforms()
                        # # t_com.submit(self.formnumber)
                        # # t_brw.submit(self.submit_tag_name)
                        # t_com.submit(self.submit_tag_name2)
                        # #
                        # content = t_com.show()
                        # print 'debug twill post content:', content
                        # t_com.save_cookies(self.cookies)
                        t_brw.save_cookies(self.cookies)
                        t_brw.load_cookies(self.cookies)




            # print t_brw.find_link('http://64.62.211.131:2082/frontend/x3/mail/fwds.html')
            t_brw.save_cookies(self.cookies)
            print t_com.show_extra_headers()
            print t_com.show_cookies()
            print t_com.showlinks()
            links2 = t_com.showlinks()
            print t_brw.result.page
            html = t_brw.result.page

            links, title = self.link_tag_find(html, self.base_url)
            if links == []:
                try:
                    # title=LINK().find_my_tilte(data=html,start_dash='<h1 class="article-title"',end_dash='1>',make_url=False)
                    title = LINK().find_my_tilte(data=html, start_dash='type="image/x-icon"><title>',
                                                 end_dash='</title>', make_url=False)
                except:
                    title = ''

                links = LINK().find_my_tilte(data=html, start_dash='<a id="pdfLink" href="', end_dash='"',
                                             make_url=True)

                if links == '' or links == []:
                    links = LINK().soap_my(data=html, tag='title="Download PDF" ', attr='a', href='href', url=base_url)

                if links == [] or links == '':
                    links = LINK().soap_my(data=html, tag="Download PDF", attr='a', href='href', url=base_url)
                if links == [] or links == '':
                    links = LINK().soap_my(data=html, tag='pdfLink', attr='a', href='href', url=base_url)
                if title == '' or title == []:
                    title = LINK().soap_my(data=html, tag='class="article-title"', attr='h1', href='', url=base_url)
                if title == '' or title == []:
                    title = LINK().soap_my(data=html, tag='<title>', attr='', href='', url=base_url)
            if links != []:
            # t_brw.go(links)
            # html0=t_brw.result.page
            # print '@@@@@@@@@@@@@ html0 download by twill is @@@@@@@@@@@@'
            # print html0
            # print '@@@@@@@@@@@@@ html0 download by twill is @@@@@@@@@@@@'
            # time.sleep(10)
            # link2=t_brw.result.url
            # print '@@@@@@@@@@@@@ time.sleep(10) download by twill is @@@@@@@@@@@@'
            # print link2
            # print '@@@@@@@@@@@@@ time.sleep(10) download by twill is @@@@@@@@@@@@'
            # time.sleep(10)
            # if  not (html0[:4]=='%PDF') or html0==[] :
            #     html2,cookies = MECAHNIZM('','',cookies=self.cookies,url=link2).speed_download(link2)
            #     print '@@@@@@@@@@@@@ MECAHNIZM download by twill is @@@@@@@@@@@@'
            #     print html2
            #     print '@@@@@@@@@@@@@ MECAHNIZM download by twill is @@@@@@@@@@@@'
            #     time.sleep(10)
                return html, self.cookies, links, title, time_diff, self.log_out
                ## get all forms from that URL
        all_forms = t_brw.get_all_forms()         ## this returns list of form objects
        print "Forms:"
        t_brw.showforms()

        ## now, you have to choose only that form, which is having POST method

        self.formnumber = 0
        formnumber = 1
        for each_frm in all_forms:
            self.formnumber = 1 + self.formnumber
            attr = each_frm.attrs             ## all attributes of form
            try:
                form_id = each_frm.attrs['id']
            except:
                form_id = ''

            if each_frm.method == 'POST' and (form_id == self.Form_id ):


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
                t_com.save_cookies(self.cookies)
                t_brw.load_cookies(self.cookies)
                if re.findall(self.log_done, content):
                    # label .find
                    print ("You are logged on to the Public Access to Court Electronic "
                           "Records (PACER) Case Search website as " + self.url + ". All costs "
                                                                                  "will be billed to this account.")

                    # t_brw.go(self.database_link)
                    # site = urlparse2(link).hostname
                    site2 = urlparse2(self.url).hostname
                    base_url = 'http://' + site + '.' + site2
                    ez_link = 'http://' + site + '.' + site2 + link.split(site)[1]
                    time0 = time.time()
                    t_brw.go(ez_link)
                    time_diff = str(round(time.time() - time0, 2))
                    html = t_brw.result.page
                    if self.submit_tag_name2 != '' and not re.findall("SDM.pageType", html):
                        self.submit_tag_value2 = '%(submit_tag_value2)s' % form_data
                        self.Form_id2 = '%(Form_id2)s' % form_data
                        self.Form_Type2 = '%(Form_Type2)s' % form_data
                        all_forms = t_brw.get_all_forms()         ## this returns list of form objects
                        print "Forms:"
                        t_brw.showforms()

                        ## now, you have to choose only that form, which is having POST method

                        self.formnumber = 0
                        formnumber = 1
                        for each_frm in all_forms:
                            self.formnumber = 1 + self.formnumber
                            attr = each_frm.attrs             ## all attributes of form
                            try:
                                form_id = each_frm.attrs['id']
                            except:
                                form_id = ''

                            if each_frm.method == 'POST' and (form_id == self.Form_id2 ):
                                ctrl = each_frm.controls
                                for ct in ctrl:
                                    if ct.type == 'radio':     ## i did it as per my use, you can put your condition here
                                        # ct._value = "twill"

                                        # t_com.clicked(each_frm,'%(user_tag2)s'%form_data)            ## clicked takes two parameter, form object and button name to be clicked.

                                        t_com.showforms()
                                        t_com.fv(self.formnumber, '%(user_tag2)s' % form_data,
                                                 each_frm.controls[3]._value)
                                        t_com.showforms()
                                        t_com.submit()
                                        content = t_com.show()
                                        break
                                        # print 'debug twill post content:', content


                                # t_com.formclear(formnumber)
                                # va=each_frm.controls[3]._value
                                # t_com.fv(self.formnumber, '%(user_tag2)s'%form_data, each_frm.controls[3]._value)
                                # # t_com.fv(self.formnumber, self.pass_tag, self.password)
                                # print "Forms:"
                                # t_brw.showforms()
                                # # t_com.submit(self.formnumber)
                                # # t_brw.submit(self.submit_tag_name)
                                # t_com.submit(self.submit_tag_name2)
                                # #
                                # content = t_com.show()
                                # print 'debug twill post content:', content
                                # t_com.save_cookies(self.cookies)
                                t_brw.save_cookies(self.cookies)
                                t_brw.load_cookies(self.cookies)




                    # print t_brw.find_link('http://64.62.211.131:2082/frontend/x3/mail/fwds.html')

                    print t_com.show_extra_headers()
                    print t_com.show_cookies()
                    print t_com.showlinks()
                    print t_brw.result.page
                    html = t_brw.result.page

                    links, title = self.link_tag_find(html, self.base_url)
                    if links == []:
                        try:
                            # title=LINK().find_my_tilte(data=html,start_dash='<h1 class="article-title"',end_dash='1>',make_url=False)
                            title = LINK().find_my_tilte(data=html, start_dash='type="image/x-icon"><title>',
                                                         end_dash='</title>', make_url=False)
                        except:
                            title = ''
                        links = LINK().find_my_tilte(data=html, start_dash='<a id="pdfLink" href="', end_dash='"',
                                                     make_url=True)

                        if links == '' or links == []:
                            links = LINK().soap_my(data=html, tag='title="Download PDF" ', attr='a', href='href',
                                                   url=base_url)

                        if links == [] or links == '':
                            links = LINK().soap_my(data=html, tag="Download PDF", attr='a', href='href', url=base_url)
                        if links == [] or links == '':
                            links = LINK().soap_my(data=html, tag='pdfLink', attr='a', href='href', url=base_url)
                        if title == '' or title == []:
                            title = LINK().soap_my(data=html, tag='class="article-title"', attr='h1', href='',
                                                   url=base_url)
                        if title == '' or title == []:
                            title = LINK().soap_my(data=html, tag='<title>', attr='', href='', url=base_url)
                    if links != []:
                    # t_brw.go(links)
                    # html0=t_brw.result.page
                    # print '@@@@@@@@@@@@@ html0 download by twill is @@@@@@@@@@@@'
                    # print html0
                    # print '@@@@@@@@@@@@@ html0 download by twill is @@@@@@@@@@@@'
                    # time.sleep(10)
                    # link2=t_brw.result.url
                    # print '@@@@@@@@@@@@@ time.sleep(10) download by twill is @@@@@@@@@@@@'
                    # print link2
                    # print '@@@@@@@@@@@@@ time.sleep(10) download by twill is @@@@@@@@@@@@'
                    # time.sleep(10)
                    # if  not (html0[:4]=='%PDF') or html0==[] :
                    #     html2,cookies = MECAHNIZM('','',cookies=self.cookies,url=link2).speed_download(link2)
                    #     print '@@@@@@@@@@@@@ MECAHNIZM download by twill is @@@@@@@@@@@@'
                    #     print html2
                    #     print '@@@@@@@@@@@@@ MECAHNIZM download by twill is @@@@@@@@@@@@'
                    #     time.sleep(10)
                        return html, self.cookies, links, title, time_diff, self.log_out
                else:
                    # return html,self.cookies,links,title,0,self.log_out
                    return html, '', [], [], 0, self.log_out

        return html, self.cookies, links, title, 0, self.log_out

    def twill_find_link0(self, link, form_data):
        self.url = "%(ezproxy_host)s" % form_data
        self.database_link = "%(database_link)s" % form_data
        self.username = "%(user)s" % form_data
        self.password = "%(pass)s" % form_data
        self.user_tag = "%(user_tag)s" % form_data
        self.pass_tag = "%(pass_tag)s" % form_data
        self.Form_id = "%(Form_id)s" % form_data
        self.submit_tag_name = "%(submit_tag_name)s" % form_data
        self.submit_tag_value = "%(submit_tag_value)s" % form_data
        self.Form_Type = "%(Form_Type)s" % form_data
        self.log_done = "%(Log_test)s" % form_data
        # site = urlparse2(link).hostname


        # self.a.config("readonly_controls_writeable", 1)
        # self.b = self.a.get_browser()
        # self.b.set_agent_string("Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14")
        # self.b.clear_cookies()
        twill = import_mod(from_module='twill')
        t_com = twill.commands
        t_com.reset_browser
        t_com.reset_output
        t_com = twill.commands
        ## get the default browser
        t_brw = t_com.get_browser()
        t_brw.set_agent_string(
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14")
        ## open the url
        # url = 'http://google.com'
        t_brw.go(self.url)
        html = t_brw.result.page
        print html
        # print fill_login_form(url, html, "john", "secret")

        ## get all forms from that URL
        all_forms = t_brw.get_all_forms()         ## this returns list of form objects
        print "Forms:"
        t_brw.showforms()

        ## now, you have to choose only that form, which is having POST method

        self.formnumber = 0
        formnumber = 1
        for each_frm in all_forms:
            self.formnumber = 1 + self.formnumber
            attr = each_frm.attrs             ## all attributes of form
            try:
                form_id = each_frm.attrs['id']
            except:
                form_id = ''

            if each_frm.method == 'POST' and (form_id == self.Form_id ):


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
                t_com.save_cookies(self.cookies)
                t_brw.load_cookies(self.cookies)
                if re.findall(self.log_done, content):
                    print ("You are logged on to the Public Access to Court Electronic "
                           "Records (PACER) Case Search website as " + self.url + ". All costs "
                                                                                  "will be billed to this account.")

                    # t_brw.go(self.database_link)
                    # site = urlparse2(link).hostname
                    site2 = urlparse2(self.url).hostname
                    self.base_url = 'http://' + self.site + '.' + site2
                    ez_link = 'http://' + self.site + '.' + site2 + link.split(site)[1]
                    time0 = time.time()
                    t_brw.go(ez_link)
                    time_diff = str(round(time.time() - time0, 2))
                    html = t_brw.result.page
                    # print t_brw.find_link('http://64.62.211.131:2082/frontend/x3/mail/fwds.html')

                    print t_com.show_extra_headers()
                    print t_com.show_cookies()
                    print t_com.showlinks()
                    print t_brw.result.page
                    links, title = self.link_tag_find(html, self.base_url)
                    if link != []:
                        return html, self.cookies, links, title, time_diff
                else:
                    return [], [], [], [], 0
                    # return html,self.cookies,links,title,0
        return [], [], [], [], 0

    def twill_download0(self, link, cookies):
        # self.url="%(ezproxy_host)s"%form_data
        # self.database_link="%(database_link)s"%form_data
        # self.username="%(user)s"%form_data
        # self.password="%(pass)s"%form_data
        # self.user_tag="%(user_tag)s"%form_data
        # self.pass_tag="%(pass_tag)s"%form_data
        # self.Form_id="%(Form_id)s"%form_data
        # self.submit_tag_name="%(submit_tag_name)s"%form_data
        # self.submit_tag_value="%(submit_tag_value)s"%form_data
        # self.Form_Type="%(Form_Type)s"%form_data
        # self.log_done="%(Log_test)s"%form_data
        # site = urlparse2(link).hostname


        # self.a.config("readonly_controls_writeable", 1)
        # self.b = self.a.get_browser()
        # self.b.set_agent_string("Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14")
        # self.b.clear_cookies()
        twill = import_mod(from_module='twill')

        # t_com = twill.commands
        # t_com.reset_browser
        # t_com.reset_output
        t_com = twill.commands

        ## get the default browser
        t_brw = t_com.get_browser()
        t_brw.set_agent_string(
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14")
        t_brw.load_cookies(cookies)
        socket = import_mod(from_module='socket')
        socket.setdefaulttimeout(3000)
        ## open the url
        # url = 'http://google.com'
        # t_brw.find_link(link)
        t_brw.go(link)
        html = t_brw.result.page

        # print html
        return html

    def login_to_site_selenium(self, link, form_data, proxy=[], User_Pass=[]):

        from selenium import webdriver

        self.url = "%(ezproxy_host)s" % form_data
        self.database_link = "%(database_link)s" % form_data
        username = "%(user)s" % form_data
        password = "%(pass)s" % form_data
        user_tag = "%(user_tag)s" % form_data
        pass_tag = "%(pass_tag)s" % form_data
        Form_id = "%(Form_id)s" % form_data
        submit_tag_name = "%(submit_tag_name)s" % form_data
        submit_tag_value = "%(submit_tag_value)s" % form_data
        Form_Type = "%(Form_Type)s" % form_data
        log_done = "%(Log_test)s" % form_data
        log_done = "%(Log_test)s" % form_data
        # try:
        #     form_id=form.attrs['id']
        # except:
        #     form_id=''

        file_location = os.getcwd()
        profile = webdriver.FirefoxProfile()
        from selenium import webdriver
        #phantomjs --webdriver=8080 --webdriver-selenium-grid-hub=http://127.0.0.1:4444


        try:
            home = os.environ['OPENSHIFT_HOMEDIR'];
            path = home + 'app-root/runtime/srv/phantomjs/bin/phantomjs'
            ip = os.environ['OPENSHIFT_DIY_IP']
            dr = '--webdriver=8080 --webdriver-selenium-grid-hub=http://' + ip + ':15022'
            driver = webdriver.PhantomJS(executable_path=path, port=15022, service_args=dr)
        except:
            try:
                path = 'E:\Program Files win 7 2nd\phantomjs-1.9.2-windows'
                ip='127.0.0.1'
                dr = '--webdriver=8080 --webdriver-selenium-grid-hub=http://' + ip + ':15022'
                driver = webdriver.PhantomJS(executable_path=path, port=15022, service_args=dr,service_log_path=os.path.devnull)
                # driver = webdriver.PhantomJS(
                #     port=29842,service_log_path=os.path.devnull,
                #     desired_capabilities={
                #         'javascriptEnabled': True,
                #         'platform': 'windows',
                #         'browserName': 'Mozilla',
                #         'version': '5.0',
                #         'phantomjs.page.settings.userAgent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
                #     }
                # )
            except:
                path = home + 'app-root/runtime/srv/phantomjs/bin/phantomjs';home = os.environ['OPENSHIFT_HOMEDIR'];
                driver = webdriver.PhantomJS(executable_path=path, port=15022)



        # from selenium import webdriver
        # driver = webdriver.PhantomJS(executable_path='E:/Program Files win 7 2nd/phantomjs-1.9.2-windows/phantomjs')

        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference('browser.download.useDownloadDir', True)
        profile.set_preference('browser.download.dir', file_location)
        profile.set_preference("browser.download.default_directory", file_location)
        profile.set_preference("browser.download.lastDir", file_location)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        # profile.set_preference("browser.cache.disk.enable", False)

        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", 'application/pdf')
        profile.set_preference("pdfjs.disabled", True)
        profile.set_preference("plugin.scan.Acrobat", "99.0")
        # mydirver.setPreference("plugin.scan.plid.all", False)
        profile.set_preference("plugin.disable_full_page_plugin_for_types", "application/pdf")
        mydriver = webdriver.Firefox(profile)

        time0 = time.time()
        self.socket.setdefaulttimeout(360)
        mydriver.set_page_load_timeout(1700)
        mydriver.get(self.url)



        # mydriver.maximize_window()
        username1 = mydriver.find_element_by_name(user_tag)
        password1 = mydriver.find_element_by_name(pass_tag)

        username1.send_keys(username)
        password1.send_keys(password)

        submit_button = mydriver.find_element_by_xpath("//input[@value='" + submit_tag_value + "']")
        s = submit_button.click()
        s2 = mydriver.page_source
        if log_done in s2:
            site2 = urlparse2(self.url).hostname
            self.base_url = 'http://' + self.site + '.' + site2
            ez_link = 'https://' + self.site + '.' + site2 + link.split(self.site)[1]
            ez_sign_in = 'https://' + self.site + '.' + site2 + '/lib/scitechjo/login.action'
            # mydriver.set_page_load_timeout(1700)

            mydriver.get(ez_sign_in)
            # time.sleep(5)

            # sign_in = mydriver.find_element_by_partial_link_text('Sign')
            # sg = sign_in.click()
            username1 = mydriver.find_element_by_name('username')
            password1 = mydriver.find_element_by_name('password')
            username1.send_keys('ss3@elec-lab.tk')
            password1.send_keys('ss123456')
            submit_button = mydriver.find_element_by_xpath("//input[@name='" + 'login_btn_1' + "']")
            s = submit_button.click()
            try:
                mydriver.get(ez_link)
                # time.sleep(5)
                mydriver.set_page_load_timeout(1700)
                html = mydriver.page_source

                # continue_link1= mydriver.find_element_by_link_text('Download')
                # elent=mydriver.find_elements()


                title = mydriver.find_element_by_xpath("//title").get_attribute('text')
                print title
                continue_link = mydriver.find_element_by_class_name('download_button')
                print continue_link.get_attribute("href")
                links = continue_link.get_attribute("href")
                # mydriver.get(links)

                self.cookies = mydriver.get_cookies()
                time_diff = str(round(time.time() - time0, 2))
                if link != []:
                    return html, self.cookies, links, title, time_diff, mydriver


            except:
                return [], [], [], [], 0, []
        else:
            return [], [], [], [], 0, []

    def Download_selenium(self, link, cookies, mydriver, form_data='', proxy=[], User_Pass=[]):

        # from selenium import webdriver

        # self.url = "%(ezproxy_host)s" % form_data
        # self.database_link = "%(database_link)s" % form_data
        # username = "%(user)s" % form_data
        # password = "%(pass)s" % form_data
        # user_tag = "%(user_tag)s" % form_data
        # pass_tag = "%(pass_tag)s" % form_data
        # Form_id = "%(Form_id)s" % form_data
        # submit_tag_name = "%(submit_tag_name)s" % form_data
        # submit_tag_value = "%(submit_tag_value)s" % form_data
        # Form_Type = "%(Form_Type)s" % form_data
        # log_done = "%(Log_test)s" % form_data
        # log_done = "%(Log_test)s" % form_data
        # # try:
        # #     form_id=form.attrs['id']
        # # except:
        #     form_id=''
        # mydriver = webdriver.Firefox()
        time0 = time.time()
        mydriver.add_cookie(cookies)
        # mydriver.get(self.url)
        # # mydriver.maximize_window()
        # username1 = mydriver.find_element_by_name(user_tag)
        # password1 = mydriver.find_element_by_name(pass_tag)
        #
        # username1.send_keys(username)
        # password1.send_keys(password)
        #
        # submit_button = mydriver.find_element_by_xpath("//input[@value='" + submit_tag_value + "']")
        # s = submit_button.click()
        # s2 = mydriver.page_source
        # site2 = urlparse2(self.url).hostname
        # self.base_url = 'http://' + self.site + '.' + site2
        # ez_link = 'https://' + self.site + '.' + site2 + link.split(self.site)[1]
        # ez_sign_in = 'https://' + self.site + '.' + site2 + '/lib/scitechjo/login.action'
        # # mydriver.set_page_load_timeout(1700)
        # self.socket.setdefaulttimeout(360)
        # mydriver.get(ez_sign_in)
        # # time.sleep(5)
        # mydriver.set_page_load_timeout(1700)
        # sign_in = mydriver.find_element_by_partial_link_text('Sign')
        # sg = sign_in.click()
        # username1 = mydriver.find_element_by_name('username')
        # password1 = mydriver.find_element_by_name('password')
        # username1.send_keys('ss3@elec-lab.tk')
        # password1.send_keys('ss123456')
        # submit_button = mydriver.find_element_by_xpath("//input[@name='" + 'login_btn_1' + "']")
        # s = submit_button.click()
        try:
            mydriver.get(link)
            # time.sleep(5)
            mydriver.set_page_load_timeout(1700)
            html = mydriver.page_source

            va = []
            # file_location = os.getcwd()
            # mydriver.set_preference("download.default_directory", file_location)
            # mydriver.set_preference("browser.download.folderList",2)
            # mydriver.set_preference("browser.download.manager.showWhenStarting",False)
            # mydriver.set_preference("browser.cache.disk.enable", False)
            #
            # mydriver.set_preference("browser.helperApps.neverAsk.saveToDisk", 'application/pdf')
            # mydriver.set_preference("pdfjs.disabled",True)
            # mydriver.set_preference("plugin.scan.Acrobat", "99.0")
            # # mydirver.setPreference("plugin.scan.plid.all", False)
            # mydriver.set_preference("plugin.disable_full_page_plugin_for_types", "application/pdf")


            for i in mydriver.find_elements_by_xpath("//select /*"):
                # i.click()
                print i.get_attribute("value")
                va.append(i.get_attribute("value"))
                i.click()
                # ok_l = mydriver.find_elements_by_xpath("//input[@name='submit']")
                ok_l = mydriver.find_element_by_name('submit')

                ok_l.click()

                break

            # for i in mydriver.find_elements_by_xpath(
            #         "//select[@name='chapterDownloadPageNumber']/option[text()='option_text']"):
            #     # i.click()
            #     # print i.get_attribute("href")
            #     print 'ssssssssssssssss'
            #     # for i in mydriver.find_elements_by_xpath("//option[@value=*]"):
            # #     # i.click()
            # #     print i.get_attribute("href")
            #
            # # for a in continue_link:
            # #     print(a.get_attribute('href'))
            # # s=1;
            # html = continue_link.click()
            # s = 1
            time_diff = str(round(time.time() - time0, 2))
            return 1
        except:
            pass

    def login_to_site(self, link, form_data, proxy=[], User_Pass=[]):
        self.url = "%(ezproxy_host)s" % form_data
        self.database_link = "%(database_link)s" % form_data
        username = "%(user)s" % form_data
        password = "%(pass)s" % form_data
        user_tag = "%(user_tag)s" % form_data
        pass_tag = "%(pass_tag)s" % form_data
        Form_id = "%(Form_id)s" % form_data
        log_done = "%(Log_test)s" % form_data
        br = mechanize.Browser(factory=mechanize.RobustFactory())
        # Browser options
        br.set_handle_robots(False)
        br.set_handle_referer(True)
        br.set_handle_refresh(True)

        br.set_handle_equiv(True)
        br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        cj = cookielib.LWPCookieJar()
        # cj.revert(cookie3)
        opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cj))

        br.set_cookiejar(cj)

        cj.save(self.cookies)
        # Follows refresh 0 but not hangs on refresh > 0
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # Want debugging messages?
        # User-Agent (this is cheating, ok?)
        br.addheaders = [('User-agent',
                          'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        # br.addheaders =[('Content-type', 'application/x-www-form-urlencoded'), ('Content-length', '39'), ('Referer', 'http://lib.just.edu.jo/login?url='), ('Host', 'lib.just.edu.jo'), ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

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
        if proxy != [] and not (re.findall('None:None', proxy)):
            br.proxies = br.set_proxies({"http": proxy})
            # br.proxies=br.set_proxies( proxy)

        if User_Pass != [] and not (re.findall('None:None', User_Pass)):
            br.add_proxy_password(User_Pass.split(":")[0], User_Pass.split(":")[1])

        try:
            br.open(self.url)
        except urllib2.HTTPError, e:
            print "Got error code", e.code
            try:
                br.open(self.url)
            except urllib2.HTTPError, e:
                print "Got error code", e.code
        except urllib2.URLError, e:
            print "Got error code", e.code

        # os.environ['http_proxy']=''

        if br.forms():
            print [form for form in br.forms()]
            # br.select_form(name="USER")
            # [f.id for f in br.forms()]
            formcount = done = 0
            for form in br.forms():
                try:
                    form_id = form.attrs['id']
                except:
                    form_id = ''
                if form_id == Form_id:
                    br.form = form
                    done = 1
                if done == 0: formcount = formcount + 1

            formcount = 0
            for frm in br.forms():
                try:
                    form_id = form.attrs['id']
                except:
                    form_id = ''
                if str(form_id) == Form_id:
                    done = 1
                if done == 0: formcount = formcount + 1

            br.select_form(nr=formcount)
            # br.select_form(nr = 0)
            br[user_tag] = username
            br[pass_tag] = password
            br.submit()

        print br.response().get_data()
        # print current url
        print "We are now at:", br.geturl()
        # print error
        if br.geturl() == self.url:
            print "Login Failed"
        else:
            print "Successfully logged in"

        if log_done in br.response().get_data():
            print ("You are logged on to the Public Access to Court Electronic "
                   "Records (PACER) Case Search website as " + username + ". All costs "
                                                                          "will be billed to this account.")
            # print "<li><a>"
            # print (link)
            # print "</a></li>"
            # print "<li><a>"
            # print link.base_url
            # print "</a></li>"
            site2 = urlparse2(self.url).hostname
            self.base_url = 'http://' + self.site + '.' + site2
            ez_link = 'http://' + self.site + '.' + site2 + link.split(self.site)[1]
            cj.save(self.cookies)
            for link1 in br.links():

                # http://www.rfc-editor.org/rfc/rfc2606.txt
                if re.findall(self.site, link1.url):
                    print(link1)
                    # Link(base_url='http://www.example.com/', url='http://www.rfc-editor.org/rfc/rfc2606.txt', text='RFC 2606', tag='a', attrs=[('href', 'http://www.rfc-editor.org/rfc/rfc2606.txt')])
                    print(link1.url)
                    print('match found')
                    # match found
                    break

            # br.follow_link(link1)   # link still holds the last value it had in the loop
            # print(br.geturl())
            req = br.click_link(link1)
            html = br.open(req).read()
            html2 = br.open(ez_link).read()
            print html2

            # frontpage,cookies = MECAHNIZM([],[],cookies=self.cookies,url=ez_link).speed_download(ez_link)

            request = br.request
            header = request.header_items()
            # header=request.get_header()

            # Browser options
            br.set_handle_robots(False)
            # br.set_handle_referer(True)
            # br.set_handle_refresh(True)
            #
            br.set_handle_equiv(True)
            br.set_handle_gzip(True)
            # br.set_handle_redirect(True)
            cj = cookielib.LWPCookieJar()
            # cj.revert(cookie3)
            opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cj))

            br.set_cookiejar(cj)

            cj.save(self.cookies)
            # Follows refresh 0 but not hangs on refresh > 0
            br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

            time0 = time.time()

            # request = urllib2.Request(ez_link, None, header)
            # openerdirector = br.open(request)
            # br.addheaders(header)
            openerdirector = br.open(ez_link)
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
            piece_size = 1024 * 1024 # 1MB
            data = ''
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
                    cj.save(self.cookies)
                    break
            self.br = br;
            self.cj = cj;
            time_diff = str(round(time.time() - time0, 2))
            links, title = self.link_tag_find(data, self.base_url)
            if link != []:
                return data, self.cookies, links, title, time_diff
            return data, self.cookies #,pdf_path


        else:
            raise ValueError("Could not login to PACER Case Search. Check your "
                             "username and password")
        return br

    def link_tag_find(self, html, base_url):
        try:
            # title=LINK().find_my_tilte(data=html,start_dash='<h1 class="article-title"',end_dash='1>',make_url=False)
            title = LINK().find_my_tilte(data=html, start_dash='type="image/x-icon"><title>', end_dash='</title>',
                                         make_url=False)
        except:
            title = ''

        links = LINK().find_my_tilte(data=html, start_dash='<a id="pdfLink" href="', end_dash='"', make_url=True)

        if links == '' or links == []:
            links = LINK().soap_my(data=html, tag='title="Download PDF" ', attr='a', href='href', url=base_url)
        if links == [] or links == '':
            links = LINK().soap_my(data=html, tag='pdfLink', attr='a', href='href', url=base_url)
        if title == '' or title == []:
            title = LINK().soap_my(data=html, tag='class="article-title"', attr='h1', href='', url=base_url)
        if title == '' or title == []:
            title = LINK().soap_my(data=html, tag='<title>', attr='', href='', url=base_url)
        if links != []: pass
        return links, title

    def download_mechanize(self, link, form_data):
        self.url = "%(ezproxy_host)s" % form_data
        self.database_link = "%(database_link)s" % form_data
        self.username = "%(user)s" % form_data
        self.password = "%(pass)s" % form_data
        self.user_tag = "%(user_tag)s" % form_data
        self.pass_tag = "%(pass_tag)s" % form_data
        self.Form_id = "%(Form_id)s" % form_data
        self.submit_tag_name = "%(submit_tag_name)s" % form_data
        self.submit_tag_value = "%(submit_tag_value)s" % form_data
        self.Form_Type = "%(Form_Type)s" % form_data
        self.log_done = "%(Log_test)s" % form_data
        browser = mechanize.Browser(factory=mechanize.RobustFactory())
        browser.set_handle_robots(False)

        browser.open(link)
        self.formnumber = 0
        formnumber = 1
        all_forms = browser.forms()
        for each_frm in all_forms:
            self.formnumber = 1 + self.formnumber
            attr = each_frm.attrs             ## all attributes of form
            try:
                form_id = each_frm.attrs['id']
            except:
                form_id = ''

            if each_frm.method == 'POST' and (form_id == self.Form_id ):
            # browser.follow_link(text="Package Index", nr=0)
            # for form in browser.forms():
            #     if form.attrs['id'] == 'password':
            #         browser.form = form

                d = browser.select_form(nr=self.formnumber)
                browser[self.user_tag] = self.username
                browser[self.pass_tag] = self.password
                browser.submit()

                # browser.select_form(name="password")
                # browser.select_form(name="user")
                # browser.select_form(name="searchform")
                # browser.form["term"] = "mechanize"
                # browser.submit()
                # browser.follow_link(text_regex="mechanize-?(.*)")
                # link = browser.find_link(text_regex=r"\.tar\.gz")
                filename = os.path.basename(urlparse.urlsplit(link.url)[2])
                if os.path.exists(filename):
                    sys.exit("%s already exists, not grabbing" % filename)
                browser.retrieve(link.url, filename)


class LINK:
    def __init__(self, url='', sites_list='configs/sites_list_pdf_tags.txt',
                 sites_list_files="configs/sites_list_files.txt",
                 site_proxy="configs//sites_proxy//", **kwargs):
        global PDF_Dir, Watermarked_PDF_Files_Dir

        fo = os.getcwd().replace('\\', '/')
        CurrentDir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
        Parent_Dir = os.path.abspath(os.path.join(CurrentDir, '../..')).replace('\\', '/')
        os.chdir(Parent_Dir)
        if Parent_Dir not in sys.path:
            sys.path.insert(0, Parent_Dir)
            # from  download_mozilla import web
        import proxy_checker3_all_function

        self.proxy_checker3 = proxy_checker3_all_function
        self.Mozilla_Web = web
        self.url = url
        self.sites_list = Parent_Dir.replace('\\', '/') + '/' + sites_list
        self.sites_list_files = Parent_Dir.replace('\\', '/') + '/' + sites_list_files
        self.site_proxy = site_proxy
        os.chdir(fo)

        if kwargs:
            if kwargs['PDF_Dir']:
                PDF_Dir = kwargs['PDF_Dir']
            else:
                PDF_Dir = Parent_Dir + '/PDF_Files'
            if kwargs['Watermarked_PDF_Files_Dir']:
                Watermarked_PDF_Files_Dir = kwargs['Watermarked_PDF_Files_Dir']
            else:
                Watermarked_PDF_Files_Dir = Parent_Dir + '/Watermarked_PDF_Files'
        else:
            PDF_Dir = Parent_Dir + '/PDF_Files'
            Watermarked_PDF_Files_Dir = Parent_Dir + '/Watermarked_PDF_Files'
        self.Watermarked_PDF_Dir = Watermarked_PDF_Files_Dir
        self.PDF_Files_Dir = PDF_Dir
        self.url = url

    def filename(self, pdf_url0):
        pdf_url = str(pdf_url0)

        CurrentDir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
        if re.findall('/', pdf_url):
            self.suffix = os.path.splitext(pdf_url)[1]
            self.file_name_decode = urllib2.unquote(pdf_url).decode('utf8').split('/')[-1]
            self.filename = (pdf_url).split('id=')[1].split('&')[0] + '.pdf'
            # self.filename = urlparse.urlsplit(pdf_url).path.split('/')[-1]
            # if self.filename.endswith('.jsp'):
            #     self.filename=(self.suffix).split('arnumber=')[1]+'.pdf'

            # self.filename=(pdf_url).split('id=')[1].split('&')[0]+'.pdf'
            # self.pdf_Folder_filename = CurrentDir + "/"+self.PDF_Files_Dir+"/" + self.filename
            # self.W_pdf_Folder_filename = CurrentDir + "/"+self.Watermarked_PDF_Dir+"/" + self.filename
            self.pdf_Folder_filename = self.PDF_Files_Dir + "/" + self.filename
            self.W_pdf_Folder_filename = self.Watermarked_PDF_Dir + "/" + self.filename
            self.chdir = CurrentDir
        else:
            self.filename = urlparse.urlsplit(pdf_url).path.split('\\')[-1]
            self.chdir = CurrentDir
            # self.pdf_Folder_filename = CurrentDir+ "/"+self.PDF_Files_Dir+"/" + self.filename
            # self.W_pdf_Folder_filename = CurrentDir + "/"+self.Watermarked_PDF_Dir+"/" + self.filename
            self.pdf_Folder_filename = self.PDF_Files_Dir + "/" + self.filename
            self.W_pdf_Folder_filename = self.Watermarked_PDF_Dir + "/" + self.filename

        return self


    def file_rd(self, path, mode='r', main_data='0'):
        # proxylist = open(path).read().split('\n')
        # print os.getcwd()
        f = open(path, mode)
        if main_data == '0':
            data = f.read().split('\n')
        else:
            data = f.read()
            # data=f.readlines()
        # print data
        f.close
        return data


    # def soap_my(self, data, tag, attr='a', href='href'):
    def soap_my(self, **kwargs):
        data = kwargs['data']
        tag = kwargs['tag']
        try:
            attr = kwargs['attr']
        except:
            attr = 'a'
        try:
            href = kwargs['href']
        except:
            href = 'href'
        try:
            url = kwargs['url']
        except:
            url = "http://" + urlparse2(self.url).hostname


        # from BeautifulSoup import BeautifulSoup
        # import re

        # site = urlparse2(self.url).hostname
        soup = BeautifulSoup(data)
        ###################
        links = soup.findAll(attr, href == True)
        # print links
        try:
            if links == []:
                links = soup.findAll(attr, href == True)
        except:
            pass
        done = 0
        for everytext in links:

            if re.findall(tag, str(everytext)):
                print " link url finded for downloading...\n\t%s" % everytext
                # print everytext
                if len(href) != 0:
                    if not (re.findall('www', everytext[href]) or re.findall('http://', everytext[href])):
                        f_nmae = urlparse.urljoin(url, everytext[href])

                    else:
                        f_nmae = everytext[href]
                    print unicode(f_nmae)
                    return f_nmae
                else:
                    text = ''.join(everytext.findAll(text=True))
                    data = text.strip()
                    done = 1
                    return text

                    ###############
        if done == 0:
            link = []
            return link

    def find_my_tilte(self, **kwargs):
        data = kwargs['data']
        start_dash = kwargs['start_dash']
        end_dash = kwargs['end_dash']
        try:
            make_url = kwargs['make_url']
            url = "http://" + urlparse2(self.url).hostname

        except:
            make_url = False
        try:
            revers = kwargs['reverce']
        except:
            revers = False


        # data_lowered = data.lower();
        if revers == False:
            begin = data.find(start_dash)
            end = data[begin + len(start_dash):].find(end_dash) + begin + len(start_dash)
        else:
            end = data.find(end_dash)
            begin = data[:end].rfind(start_dash)
        if begin == -1 or end == -1:
            return []
        else:
            # Find in the original html
            f_nmae = data[begin + len(start_dash):end].strip()
            if not (re.findall('www', f_nmae) or re.findall('http://', f_nmae)) and make_url == True:
                f_nmae = urlparse.urljoin(url, f_nmae)
                print " link url finded for downloading...\n\t%s" % unicode(f_nmae)
            else:
                print " link target  finded is ...\n\t%s" % f_nmae

            return f_nmae


    def dowload_basePr_userpass_link(self, url, pr_h, user_pass_h, **kwargs):
        try:
            if kwargs['cookies']:
                cookies = kwargs['cookies']
            else:
                cookies = ''
            web = self.Mozilla_Web

            if len(user_pass_h) != 0: #user_pass_h !='' or

                # html,pr,upss,cookies=web().download(url,pr_h,user_pass_h,cookies=cookies)
                # or by mechanizm method
                html, pr, upss, cookies = web().download_mechanism_link(url, pr_h, user_pass_h, cookies=cookies)
                mech = 1


            else:
                # html,pr,upss,cookies=web().download(url,pr_h,cookies=cookies)
                # or by mechanizm method
                html, pr, upss, cookies = web().download_mechanism_link(url, pr_h, cookies=cookies)
                mech = 1

        except:
            html = []
            pr = []
            upss = []
            cookies = ''
            mech = 0
            print "we cant dowload beacuse of invalid tag or invalid proxy line 620" + "\n"
        responce = {
            'html': html,
            'proxy': pr,
            'user_pass': upss,
            'cookies': cookies,
            'mechanizm': mech,
        }

        return responce

    def dowload_basePr_userpass(self, url, pr_h, user_pass_h, **kwargs):
        try:
            if kwargs['cookies']:
                cookies = kwargs['cookies']
            else:
                cookies = ''
            web = self.Mozilla_Web

            if len(user_pass_h) != 0: #user_pass_h !='' or

                html, pr, upss, cookies = web().download(url, pr_h, user_pass_h, cookies=cookies);
                mech = 0

                # or by mechanizm method
                # html,pr,upss,cookies=web().download_mechanism(url,pr_h,user_pass_h,cookies=cookies)
                mech = 1

            else:
                html, pr, upss, cookies = web().download(url, pr_h, cookies=cookies);
                mech = 0
                # or by mechanizm method
                # html,pr,upss,cookies=web().download_mechanism(url,pr_h,cookies=cookies)
                mech = 1

        except:
            html = []
            pr = []
            upss = []
            cookies = ''
            mech = 0
            print "we cant dowload beacuse of invalid tag or invalid proxy line 620" + "\n"
        responce = {
            'html': html,
            'proxy': pr,
            'user_pass': upss,
            'cookies': cookies,
            'mechanizm': mech,
        }
        return responce


    def get_pdf_link(self, proxy='', user_pass=''):

        url = self.url
        site = urlparse2(url).hostname

        if proxy == '':

            fo = os.getcwd()
            pr_h, proxy_h, user_pass_h = self.proxy_checker3.make_returning_proxy(
                "configs//sites_proxy//" + site + '//', url)
            os.chdir(fo)
        else:
            pr_h = []
            user_pass_h = []
            pr_h.append(proxy)
            user_pass_h.append(user_pass)
            # i = user_pass_h.index("")
            # del user_pass_h[i]
            try:
                i = pr_h.index("")
                del pr_h[i]
            except:
                pass

        don_flg = -1
        if pr_h != []:
            i = -1
            # site = urlparse2(url).hostname
            listhandle = self.file_rd(self.sites_list, 'r')
            file_listhandle = self.file_rd(self.sites_list_files, 'r')
            link_done = 0
            url_pdf = {}
            for j in range(i + 1, len(pr_h)):
                if don_flg != 1 and not url.endswith('.pdf') \
                    and not url.endswith('.zip') and link_done == 0:
                    time0 = time.time()

                    if re.findall('None', pr_h[j]):
                        [html, cookies, links, title, form, time_diff, log_out] = twil_find_pdf_link(url)
                        # time_diff = str(round(time.time() - time0, 2))
                        if links != []:
                            try:
                                site_file = "configs//sites_proxy//"
                                if user_pass_h[j] != []:
                                    pp = pr_h[j] + '@' + user_pass_h[j]
                                else:
                                    pp = pr_h[j]

                                self.proxy_checker3.make_txt_file(site_file + site + ".txt", pp, site, time_diff)
                                self.proxy_checker3.sort_file(site_file + site + ".txt", " Rs_Time ")
                            except:
                                print 'we could not update proxy list for site:' + site + " that is worked with proxy "+pr_h[j] + '\n'
                            responce = {
                                'html': html,
                                'url': url,
                                'links': links,
                                'title': title,
                                'proxy': pr_h[j],
                                'user_pass': user_pass_h[j],
                                'cookies': cookies,
                                'mechanizm': 0,
                                'form': form,
                                'log_out': log_out
                            }
                            return responce
                        else:
                            CurrentDir = os.path.dirname(os.path.realpath(__file__))
                            Parent_Dir = os.path.abspath(os.path.join(CurrentDir, '../..')).replace('\\', '/')
                            if not os.path.isdir(Parent_Dir + '/configs/sites_proxy/' + site):
                                os.mkdir(Parent_Dir + '/configs/sites_proxy/' + site)
                            time_diff = str(round(time.time() - time0, 2))
                            if len(user_pass) != 0:
                                self.proxy_checker3.make_txt_file(
                                    Parent_Dir + '/configs/sites_proxy/' + site + "/badproxylist.txt",
                                    str(pr_h[j]) + '@' + str(user_pass_h[j]), site, time_diff)
                            else:
                                self.proxy_checker3.make_txt_file(
                                    Parent_Dir + '/configs/sites_proxy/' + site + "/badproxylist.txt", str(pr_h[j]),
                                    site, time_diff)
                            j = j + 1

                    res = self.dowload_basePr_userpass_link(url, pr_h[j], user_pass_h[j], cookies='')
                    html = res['html'];
                    proxy0 = res['proxy'];
                    user_pass = res['user_pass'];
                    cookies = res['cookies'];
                    mech = res['mechanizm']

                    if link_done == 0 and html != []:
                        # try:
                        #     if os.path.isfile(html):
                        #         h=open(html)
                        #         ht=h.read()
                        #         h.close()
                        #         os.remove(html)
                        #         html=ht
                        # except:
                        #     pass
                        # links =self.soap_my(data=html, tag='FullTextPdf', attr='a', href='href',url=url)
                        title = self.find_my_tilte(data=html,
                                                   start_dash='<h1 class="mediumb-text" style="margin-top:0px; margin-bottom:0px;"><strong>',
                                                   end_dash='</strong>', make_url=False)

                        links = self.find_my_tilte(data=html,
                                                   start_dash='<a name="FullTextPDF" title="FullText PDF" href="',
                                                   end_dash='" target="_blank">', make_url=True)
                        #
                        # links =self.soap_my(data=html, tag='title="FullText PDF"', attr='a', href='href',url=url)
                        # title=self.soap_my(data=html, tag='class="mediumb-text" style="margin-top:0px; margin-bottom:0px;"', attr='h1', href='href',url=url)


                        # if links == [] or links==None:
                        #     links =self.soap_my(data=html, tag='Full Text', attr='a', href='href',url=url)
                        # clear = lambda: os.system(['clear','cls'][os.name == 'nt']);clear()
                        # print html


                        # if links!=[] and mech!=1 :
                        #     res=self.dowload_basePr_userpass_link(url,pr_h[j],user_pass_h[j],cookies='')
                        #     html=res['html'];proxy0=res['proxy'];user_pass=res['user_pass'];cookies=res['cookies'];mech=res['mechanizm']
                        #     # try:
                        #     #     if os.path.isfile(html):
                        #     #         h=open(html)
                        #     #         ht=h.read()
                        #     #         h.close()
                        #     #         os.remove(html)
                        #     #         html=ht
                        #     # except:
                        #     #     pass
                        #
                        #     links =self.soap_my(data=html, tag='<frame src="http://ieeexplore.ieee.org', attr='frame', href='src',url=str(links))
                        #     # links2=self.soap_my(html,'<frame src="http://ieeexplore.ieee.org','frame','src')
                        # links=links2
                        if links == [] or links == None or links == '':
                            pass
                        else:
                            link_done = 1
                            print '---------------we found Proper link which is :------------\n' + str(links) + \
                                  '\n ----with proxy-------\n' + str(pr_h[j]) + ':' + str(user_pass_h[j])
                            print '----------------- Link Found -------------------------'
                            break

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
                            #                 # links = self.soap_my(html, Tag, atrr,href)
                            #                 if links != [] and link_done!=None and mech!=1:
                            #                     try:
                            #                         Tag = line.split("TAG2:")[1].split("---")[0]
                            #                         Tag=Tag.replace("---",'').replace("+++",'')
                            #
                            #                         atrr = line.split("Attr2:")[1].split("---")[0]
                            #                         atrr=atrr.replace('---','').replace("+++",'')
                            #                         href=line.split('Href2:')[1].split("---")[0]
                            #                         href=href.replace("+++",'')
                            #                         res=self.dowload_basePr_userpass_link(url,pr_h[j],user_pass_h[j],cookies='')
                            #                         html=res['html'];proxy0=res['proxy'];user_pass=res['user_pass'];cookies=res['cookies'];mech=res['mechanizm']
                            #                         # links = self.soap_my(html, Tag, atrr,href)
                            #                     except:pass
                            #                     # [html,proxy0,user_pass]=self.dowload_basePr_userpass(links,pr_h[j],user_pass_h[j])
                            #                     # links =self.soap_my(data=html, tag=Tag, attr=atrr, href=href,url=url)
                            #                     # links = self.soap_my(html, Tag, atrr,href)
                            #                     if links != [] or links!=None:
                            #                         link_done = 1
                            #                         print '---------------we found Proper link which is :------------\n'+str(links)+ \
                            #                               '\n ----with proxy-------\n'+str(pr_h[j])+':'+str(user_pass_h[j])
                            #                         print '----------------- Link Found -------------------------'
                            #                         return links,pr_h[j],user_pass_h[j]
                            #
                            #             except:
                            #                 pass



                    elif link_done == 1:
                        print "<li><a>tag found</a></li>"
                        print links
                        break
                    elif link_done == 0:
                        CurrentDir = os.path.dirname(os.path.realpath(__file__))
                        Parent_Dir = os.path.abspath(os.path.join(CurrentDir, '../..')).replace('\\', '/')
                        if not os.path.isdir(Parent_Dir + '/configs/sites_proxy/' + site):
                            os.mkdir(Parent_Dir + '/configs/sites_proxy/' + site)
                        time_diff = str(round(time.time() - time0, 2))
                        if len(user_pass) != 0:
                            self.proxy_checker3.make_txt_file(
                                Parent_Dir + '/configs/sites_proxy/' + site + "/badproxylist.txt",
                                str(pr_h[j]) + '@' + str(user_pass_h[j]), site, time_diff)
                        else:
                            self.proxy_checker3.make_txt_file(
                                Parent_Dir + '/configs/sites_proxy/' + site + "/badproxylist.txt", str(pr_h[j]), site,
                                time_diff)


                elif url != [] or (url.endswith('.pdf') or url.endswith('.zip')):

                    cookies = ''
                    mech = 0
                    responce = {
                        'html': '',
                        'url': url,
                        'links': url,
                        'title': '',
                        'proxy': '',
                        'user_pass': '',
                        'cookies': cookies,
                        'mechanizm': mech,
                        # 'log_out':''
                    }
                    return responce

                    # return url,'','',cookies

            if link_done == 0:
                links = []
                pr_h[j] = []
                user_pass_h[j] = []
                title = ''
                cookies = ''
                mech = 0
                print "we couldnt find link beacuase of no proxy is able to download .find good proxy over internet"
            responce = {
                'html': html,
                'url': url,
                'links': links,
                'title': title,
                'proxy': pr_h[j],
                'user_pass': user_pass_h[j],
                'cookies': cookies,
                'mechanizm': mech,
                # 'log_out':''
            }
            return responce


            # return links,pr_h[j],user_pass_h[j],cookies,

        else: # pr_h[j]=[] there is no trusted proxy for it
            res = self.dowload_basePr_userpass_link(url, "None:None", [], cookies='')
            html = res['html'];
            proxy0 = res['proxy'];
            user_pass = res['user_pass'];
            cookies = res['cookies'];
            mech = res['mechanizm']
            # [html,proxy0,user_pass,cookies]=self.dowload_basePr_userpass_link(url,"None:None",[],cookies='')
            links = self.soap_my(data=html, tag='title="FullText PDF"', attr='a', href='href', url=url)
            title = self.soap_my(data=html, tag='class="mediumb-text" style="margin-top:0px; margin-bottom:0px;"',
                                 attr='h1', href='href', url=url)
            # if links==[]:
            #     res=self.dowload_basePr_userpass_link(links,"None:None",[],cookies=cookies)
            #     html=res['html'];proxy0=res['proxy'];user_pass=res['user_pass'];cookies=res['cookies'];mech=res['mechanizm']
            #     # [html,proxy0,user_pass,cookies]=self.dowload_basePr_userpass_link(links,"None:None",[],cookies=cookies)
            #     links2=LINK(links).soap_my(html,'<frame src="http://ieeexplore.ieee.org','frame','src')
            #     link=links2
            if links == [] or links == None or links == '':
                print'there is no trusted proxy for downloading it'
            else:
                link_done = 1
            responce = {
                'html': html,
                'url': url,
                'links': links,
                'title': title,
                'proxy': [],
                'user_pass': [],
                'cookies': cookies,
                'mechanizm': mech,
                # 'log_out':''
            }
            return responce
            # return links,[],[],cookies


if __name__ == '__main__':
    #HOW TO USE:
    url = "http://127.0.0.1/1752-153X-2-5%20-%20Copy.pdf"
    url = "http://127.0.0.1/1752-153X-2-5.pdf"
    url = 'http://ieeexplore.ieee.org/xpl/articleDetails.jsp?tp=&arnumber=6180383&queryText%3Dpower' #91 KB
    # url = "http://127.0.0.1/"
    # url = "http://dl.acm.org/citation.cfm?id=99977.100000&coll=DL&dl=ACM"


    # link,proxy,user_pass=LINK(url).get_pdf_link()

    from optparse import OptionParser

    parser = OptionParser(description=__doc__)
    parser.add_option('-a', dest='url', help='adress url file name to be downloaded like:www.google.com')
    parser.add_option('-p', dest='url', help=' proxy setting for url file name to be download like:121.121.21.21:90')
    parser.add_option('-u', dest='user_name', help='user & password of proxy setting')
    parser.add_option('-i', dest='input_fname', help='file name to be watermarked (pdf)')
    parser.add_option('-w', dest='watermark_fname', help='watermark file name (pdf)')
    parser.add_option('-d', dest='pdfdir', help='make pdf files in this directory')
    parser.add_option('-o', dest='outdir', help='outputdir used with option -d', default='tmp')
    options, args = parser.parse_args()