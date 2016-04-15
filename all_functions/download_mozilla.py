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
__author__ = 's'
# from __future__ import with_statement
# from google.appengine.api import files
import os, re, random
import urllib, mechanize
import urllib2, urlparse
import md5,hashlib
import mimetypes
from urlparse import urlparse as urlparse2
#from gzip import GzipFile
import cStringIO
from cPickle import loads, dumps
import cookielib

print "Content-type: text/html\n"
print "this is running"


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


class MozillaEmulator(object):
    def __init__(self, cacher={}, trycount=0, debug=False):
        """Create a new MozillaEmulator object.

        @param cacher: A dictionary like object, that can cache search results on a storage device.
            You can use a simple dictionary here, but it is not recommended.
            You can also put None here to disable caching completely.
        @param trycount: The download() method will retry the operation if it fails. You can specify -1 for infinite retrying.
                A value of 0 means no retrying. A value of 1 means one retry. etc."""
        # try:
        #     fo = os.getcwd()
        #     # os.chdir(fo)
        #     os.mkdir(fo + "\\Watermarked_PDF_Files\\")
        # except:
        #     pass
        # try:
        #     fo = os.getcwd()
        #     os.mkdir(fo + "\\PDF_Files\\")
        # except:
        #     pass

        self.cacher = cacher
        self.cookies = cookielib.CookieJar()
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

        if proxy != [] and (not re.findall("None", proxy)) and proxy!='':
            if User_Pass != [] and User_Pass!='':
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
                    req, u = self.build_opener(url, proxy, User_Pass, postdata, extraheaders, forbid_redirect)
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
                return data
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


def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


class MECAHNIZM(object):
    def __init__(self, proxy='', User_Pass=''):

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

    def BROWSER(self):
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
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        cookie3 = ''.join([random.choice(chars) for x in range(5)]) + ".txt"
        cj = cookielib.LWPCookieJar()
        # cj.revert(cookie3)
        opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cj))

        br.set_cookiejar(cj)
        fo = os.getcwd()
        # pathname = os.path.join("cookies", cookie3)
        cj.save(fo + "\\cookies\\" + cookie3)
        # os.chdir(..)


        # Browser options
        br.set_handle_equiv(True)
        br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)

        # Follows refresh 0 but not hangs on refresh > 0
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # Want debugging messages?
        #br.set_debug_http(True)
        #br.set_debug_redirects(True)
        #br.set_debug_responses(True)

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
        # dd=re.findall('None:None', proxy)
        if self.proxy != [] and self.proxy != '' and not (re.findall('None', self.proxy)):
            br.proxies = br.set_proxies({"http": self.proxy})
            # br.proxies=br.set_proxies( proxy)

        if self.User_Pass != [] and self.User_Pass != '' and not (re.findall('None:None', self.User_Pass)):
            br.add_proxy_password(self.User_Pass.split(":")[0], self.User_Pass.split(":")[1])

        # if  r!={}:
        # rr = br.open(url)
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
            if length!=0:
                status = r"%10d [%3.2f%%]" % (dlength, dlength * 100. / length)
                status = status + chr(8)*(len(status)+1)
                print status
            # pdf_path=PDF_File().file_save(data, "PDF_Files\\", localName.filename)
            # if onprogress:
            #     onprogress(length,dlength)
            if not newdata:
                break
        return data#,pdf_path


##GOOGLE FILE SAVE
# def file_save(filename='a.log',data=''):
#
#     # from google.appengine.api import files
#     # Create the file
#     file_name = files.blobstore.create(mime_type='application/pdf',_blobinfo_uploaded_filename=filename)
#
#     # Open the file and write to it
#     with files.open(file_name, 'wb') as f:
#         f.write(data)
#
#     # Finalize the file. Do this before attempting to read it.
#     files.finalize(file_name)
#
#     # Get the file's blob key
#     blob_key = files.blobstore.get_blob_key(file_name)
#
#     import os
#
#     # dir = 'text'
#     # filename = 'a.log'
#     # log_path = os.path.join(dir, filename)
#     #
#     # if not os.path.exists(dir):
#     #     os.makedirs(dir)
#
#     with open(filename, 'w') as f:
#         f.write("Nobody expects the Spanish inquisition!")


class web(object):
    def __init__(self, url=''):
        self.url = url

    def download_mechanism(self, url='', proxy='', user_pass='', location='PDF_Files/'):
        """

        :param url:
        """
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
                        if  'user_pass_h[j]' is locals():
                            # frontpage=MECHANIZM( proxy='', User_Pass='').speed_download(pdf_url,piece_size=1024*1024)
                            frontpage = MECAHNIZM(pr_h[j],user_pass_h[j]).speed_download(url)
                            pr = pr_h[j]
                            upss = user_pass_h[j]
                        else:
                            # frontpage = dl.download(url, pr_h[j])
                            frontpage = MECAHNIZM(pr_h[j]).speed_download(url)
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
                    print "we could not download file with  proxy:"+pr_h[j]
            if don_flg != 1:
                print "we are unable to download your file Now!!" + '\n'
                frontpage = []
                pr = ''
                upss = ''
        else:
            print "we are unable to download your file Now!! Becaouse proxy is empty" + '\n'
        return frontpage, pr, upss

    def download(self, url='', proxy='', user_pass='', location='PDF_Files/'):
        """

        :param url:
        """
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
                    dl = MozillaEmulator(cash, 0)
                    try:
                        if  user_pass_h[j] !='':

                            frontpage = dl.download(url, pr_h[j], user_pass_h[j])
                            pr = pr_h[j]
                            upss = user_pass_h[j]
                        else:
                            frontpage = dl.download(url, pr_h[j])
                            pr = pr_h[j]
                            upss = ''



                    except:
                        print "we cant download because of invalid tag or invalid proxy line 620" + "\n"

                    if frontpage != []:
                        if len(user_pass_h[j])!=0:
                            print "file downloaded with "+str(pr_h[j])+'@'+str(user_pass_h[j])
                        else:print "file downloaded with "+str(pr_h[j])
                        don_flg = 1
                        # pr = pr_h[j]
                        # upss = user_pass_h[j]
                        break
                else:
                    print "we could not download file with  proxy:"+pr_h[j]
            if don_flg != 1:
                print "we are unable to download your file Now!!" + '\n'
                frontpage = []
                pr = ''
                upss = ''


        else:
            print "we are unable to download your file Now!! Beacouse proxy is empty" + '\n'

        return frontpage, pr, upss


def main():
    # HOW TO USE

    url = "http://127.0.0.1/1752-153X-2-5.pdf"

    pdf_url_link, pdf_dir_link = web().download(url)
    dl = MozillaEmulator()
    frontpage = dl.download(url, "202.202.0.163:3128")
    # frontpage = dl.download("https://somesite.net/login.php")

    # Make sure that we get cookies from the server before logging in
    if False:
        frontpage = dl.download("https://somesite.net/login.php")
        # Sign in POST
        post_data = "action=sign_in&username=user1&password=pwd1"
        page = dl.download("https://somesite.net/sign_in.php", post_data)
        if "Welcome" in page:
            # Send a file
            fdata = file("inventory.txt", "rb").read()
            dl.post_multipart('https://somesimte.net/upload-file.php',
                              [('uploadType', 'Inventory'), ('otherfield', 'othervalue')],
                              [('uploadFileName', 'inventory.txt', fdata)], "202.202.0.163:3128", []
            )

#=======================================================================================================================
# main
#=======================================================================================================================
if __name__ == '__main__':

    # url='http://127.0.0.1/Introduction to Tornado.pdf'
    # url='http://ieeexplore.ieee.org/xpl/articleDetails.jsp?tp=&arnumber=6180383&queryText%3Dpower' #91 KB

    # ad=os.system('python main_core.py --url'+url+'--pdfdir PDF_Files --wtdir Watermarked_PDF_Files')
    # ad=os.system('python main_core.py --url http://127.0.0.1/Introduction to Tornado.pdf')
    # ad=os.system('python main_core.py --url http://127.0.0.1/1752-153X-2-5.pdf')
    # python main_core.py --url "http://ieeexplore.ieee.org/xpl/articleDetails.jsp?tp=&arnumber=6180383&queryText%3Dpower"
    # $OPENSHIFT_HOMEDIR/app-root/runtime/srv/python/bin/python main_core.py --url "http://ieeexplore.ieee.org/xpl/articleDetails.jsp?tp=&arnumber=6180383&queryText%3Dpower"
    # python main_core.py --url "http://127.0.0.1"

    print "test main" + '\n' + "how to use:"
    print "html=web().download(url,'222.66.115.233:80')" + '\n'
    # import os,errno
    from optparse import OptionParser

    parser = OptionParser(description=__doc__)
    parser.add_option('-a', dest='url', help='adress url file name to be downloaded like:www.google.com',
                      default='www.google.com')
    parser.add_option('-p', dest='proxy', help=' proxy setting for url file name to be download like:121.121.21.21:90',
                      default='')
    parser.add_option('-u', dest='user_name', help='user & password of proxy setting', default='')
    # parser.add_option('-w', dest='watermark_fname', help='watermark file name (pdf)',default='tmp')
    # parser.add_option('-d', dest='pdfdir', help='make pdf files in this directory',default='tmp')
    # parser.add_option('-o', dest='watermark_outdir', help='make watermark_outdir pdf files in this directory', default='tmp')
    options, args = parser.parse_args()
    if options.url:
        if options.proxy and not options.user_name:
            html = web().download(options.url, options.proxy)
        elif options.proxy and options.user_name:
            html = web().download(options.url, options.proxy, options.user_name)
    else:
        parser.print_help()



        # main()
        # pdf_url_link, pdf_dir_link = web().download(url)
# pdf_url_link,pdf_dir_link=web().download(url,'222.66.115.233:80')
#pdf_url_link,pdf_dir_link=web().download(url,"202.202.0.163:3128")
#pdf_url_link,pdf_dir_link=web().download(url,"222.201.132.28:8888")
# pdf_url_link, pdf_dir_link = web().download(url, "143.107.192.112:21320")
