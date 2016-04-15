#!/usr/bin/python
#----------------------------------------------------------------------
#
# Author:      Soheil Sab
#
# Copyright:   (c) 214 by www.elec-lab.tk.
# Licence:     BSD style
#
#
#----------------------------------------------------------------------
# from __future__ import with_statement
# from google.appengine.api import files
import os, re, errno, sys
import urllib
import urllib2, urlparse
from urlparse import urlparse as urlparse2


print "Content-type: text/html\n"
print "this is running"


def import_mod(**kwargs):
    # import_mod(from_module='sss',from_module2='s',dir_location='c:/path-to-module')
    # or import_mod(from_module='sss',import_from='s',dir_location='c:/path-to-module')
    # or import_mod(import_single='os')
    try:
        from_module_name1 = kwargs['from_module']
    except:
        from_module_name1 = kwargs['import_single']
    try:
        kwargs['from_module2']
        from_module_name2 = kwargs['from_module2']
    except:
        try:
            kwargs['import_from']
            from_module_name2 = kwargs['import_from']
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


class Find_Link(object):
    def __init__(self, url='', sites_list='configs/sites_list_pdf_tags.txt',
                 sites_list_files="configs/sites_list_files.txt",
                 site_proxy="configs//sites_proxy//", **kwargs):
        self.sites_list = sites_list
        self.sites_list_files = sites_list_files
        self.site_proxy = site_proxy
        self.url = url

        CurrentDir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
        try:
            if kwargs['cookies']:
                self.cookies = kwargs['cookies']
            else:
                self.cookies = ''
        except:
            self.cookies = ''
        try:
            if 'pdfdir' in kwargs: self.pdf_download_location = kwargs['pdfdir']
        except:
            self.pdf_download_location = CurrentDir + '/PDF_Files'
        try:
            if 'water_pdfdir' in kwargs: self.wat_locatton = kwargs['water_pdfdir']

        except:
            self.wat_locatton = CurrentDir + '/Watermarked_PDF_Files'
        try:
            if 'root' in kwargs: self.root = kwargs['root']
        except:
            self.root = CurrentDir


        # from  download_mozilla import web
        proxy_checker3_all_function = import_mod(from_module='proxy_checker3_all_function')
        # import proxy_checker3_all_function
        self.proxy_checker3 = proxy_checker3_all_function
        # self.Mozilla_Web=web
        print 'url is ' + url
        site = urlparse2(url).hostname
        fo = os.getcwd()
        CurrentDir = os.path.dirname(os.path.realpath(__file__))
        s = CurrentDir.replace('\\', '/') + '/configs/Links_site/'
        print site

        # s2=os.getcwd()+'\\configs\\Links_site\\'
        self.file_exist = 0
        if os.path.isfile(s + site.replace('.', '_') + '.py'):
            # sys.path.insert(0, s)
            # ss=sys.path
            # print ss
            sys.path.insert(0, s)
            # os.chdir(s)
            # import importlib
            # module2 = importlib.import_module(site.replace('.','_'), package=None)
            # del module2
            si = sys.modules
            if site.replace('.', '_') in si:
                print "@@@@@@@@@@@@@@ module already exist  for  " + site + ' is \n: @@@@@@@@@@@@@@\n\n'
                self.new_module = si[site.replace('.', '_')]
            else:
                print "@@@@@@@@@@@@@@ module inserted for  " + site + ' is \n: @@@@@@@@@@@@@@\n\n'
                self.new_module = __import__(site.replace('.', '_'), {}, {}, [], 2)

            # import imp
            # try:
            #     imp.find_module(site.replace('.','_'))
            #     found = True
            #     self.new_module=site.replace('.','_')
            #     print "@@@@@@@@@@@@@@ module already exist  for  "+site+' is \n: @@@@@@@@@@@@@@\n\n'
            # except ImportError:
            #     found = False
            #     self.new_module = __import__(site.replace('.','_'),{},{},[],2)
            #     print "@@@@@@@@@@@@@@ module inserted for  "+site+' is \n: @@@@@@@@@@@@@@\n\n'

            # self.new_module = __import__(site.replace('.','_'),{},{},[],2)
            print self.new_module
            self.file_exist = 1
        else:
            print "@@@@@@@@@@@@@@ module " + CurrentDir.replace('\\', '/') + '/configs/Links_site/' + site.replace('.',
                                                                                                                   '_') + '.py' + '\n Not found: @@@@@@@@@@@@@@\n\n'
        os.chdir(fo)


    def filename(self, pdf_url0):
        pdf_url = str(pdf_url0)
        if re.findall('/', pdf_url):
            self.suffix = os.path.splitext(pdf_url)[1]
            self.file_name_decode = urllib2.unquote(pdf_url).decode('utf8').split('/')[-1]
            self.filename = urlparse.urlsplit(pdf_url).path.split('/')[-1]
        else:
            self.filename = urlparse.urlsplit(pdf_url).path.split('\\')[-1]

        return self


    def dowload_basePr_userpass_main(self, pr_h, user_pass_h):
        try:
            url = self.url
            url = url.replace(' ', '%20')
            web = import_mod(from_module='download_mozilla', from_module2='web')
            # web=self.Mozilla_Web
            if re.findall('None:None', pr_h) and url != []:

                html, proxy_get, user_pass_get = web().download(url, pr_h)
                # proxy_get=pr_h

            elif (not re.findall('None:None', pr_h)) and 'user_pass_h' is locals():


                html, proxy_get, user_pass_get = web().download(url, pr_h, user_pass_h)
                # proxy_get=pr_h

            elif (not re.findall('None:None', pr_h)) and not ('user_pass_h' is locals()):

                html, proxy_get, user_pass_get = web().download(url, pr_h)
                pass
                # proxy_get=pr_h
        except:
            html = []
            proxy_get = []
            user_pass_get = []
            print "we cant dowload beacuse of invalid tag or invalid proxy line 620 in find_link.py" + "\n"

        return html, proxy_get, user_pass_get

    def dowload_basePr_userpass(self, pr_h, user_pass_h, cookies='', **kwargs):
        try:
            cookies = kwargs['cookies']
        except:
            cookies = self.cookies
        try:
            url = kwargs['url']
        except:
            url = self.url
        try:
            # url=self.url
            main_url = self.url
            res = self.new_module.LINK(url, PDF_Dir=self.pdf_download_location,
                                       Watermarked_PDF_Files_Dir=self.wat_locatton) \
                .dowload_basePr_userpass(url, pr_h, user_pass_h, cookies=cookies)
            html = res['html'];
            proxy_get = res['proxy'];
            user_pass_get = res['user_pass'];
            cookies = res['cookies'];#mech=re['mechanizm']
            # html,proxy_get,user_pass_get,cookies=self.new_module.LINK(url).dowload_basePr_userpass(url,pr_h,user_pass_h,cookies=cookies)
        except:

            main_url = self.url
            res = Find_Link(main_url).new_module.LINK(url, PDF_Dir=self.pdf_download_location,
                                                      Watermarked_PDF_Files_Dir=self.wat_locatton) \
                .dowload_basePr_userpass(url, pr_h, user_pass_h, cookies=self.cookies)
            html = res['html'];
            proxy_get = res['proxy'];
            user_pass_get = res['user_pass'];
            cookies = res['cookies'];#mech=re['mechanizm']
            # html,proxy_get,user_pass_get,cookies=self.new_module.LINK(url).dowload_basePr_userpass(url,pr_h,user_pass_h,cookies=self.cookies)
        return html, proxy_get, user_pass_get, cookies


    def find_name(self, pdf_download_location, wat_locatton):
        url = self.url
        filename = self.new_module.LINK(url, Watermarked_PDF_Files_Dir=wat_locatton,
                                        PDF_Dir=pdf_download_location).filename(url)
        return filename


    def find_link(self, proxy='', user_pass=''):
        url = self.url
        site = urlparse2(url).hostname
        link_done = 0
        url_pdf = {}
        if not url.endswith('.pdf'):
            # from  download_mozilla import web
            # from importlib import import_module
            # html=web().download(url)
            # html = br.open(url).read()

            # s=os.getcwd().replace('\\','/')+'/configs/Links_site/'
            # s2=os.getcwd()+'\\configs\\Links_site\\'
            # if os.path.isfile(os.getcwd().replace('\\','/')+'/configs/Links_site/'+site.replace('.','_')+'.py'):
            #         fo = os.getcwd().replace('\\','/')
            #         sys.path.insert(0, s)
            #         # CurrentDir = os.path.dirname(os.path.realpath(__file__))
            #         # os.chdir(s)
            #         # import importlib
            #         # module2 = importlib.import_module(site.replace('.','_'), package=None)
            #         new_module = __import__(site.replace('.','_'))
            #
            if self.file_exist == 1:

                res = self.new_module.LINK(url).get_pdf_link(proxy, user_pass)
                link = res['links'];
                proxy = res['proxy'];
                user_pass = res['user_pass'];
                cookies = res['cookies']
                title = res['title'];
                html = res['html'];
                try:
                    log_out = res['log_out']
                except:
                    log_out = ''
                try:
                    form = res['form']
                except:
                    form = ''
                responce = {
                    'html': html,
                    'url': url,
                    'link': link,
                    'title': title,
                    'proxy': proxy,
                    'user_pass': user_pass,
                    'cookies': cookies,
                    'form': form,
                    'log_out': log_out
                }

            else:
                print "No " + site + '.py in config in ' + os.getcwd() + "\configs\Links_site"
                link = []
                responce = {
                    'html': html,
                    'url': url,
                    'link': link,
                    'title': title,
                    'proxy': proxy,
                    'user_pass': user_pass,
                    'cookies': cookies,
                }




                # for line in listhandle:
                #     if re.findall(site, line) and link_done == 0 and (not re.findall("#", line.split("TAG:")[0])) :
                #         new_module = __import__(line)
                #     import importlib
                #     module = importlib.import_module(line, package=None)


                # # lookup in a set is in constant time
                # safe_names = {"file1.py", "file2.py", "file3.py", ...}
                #
                # user_input = ...
                #
                # if user_input in safe_names:
                #     file = import_module(user_input)
                # else:
                #     print("Nope, not doing this.")

                #
                # if re.findall(site, line) and link_done == 0 and (not re.findall("#", line.split("TAG:")[0])) :
        else:#if not  url.endwith( '.pdf'):
            print 'address you have entered is end with .pdf and link is the same'
            link = url

            responce = {
                'html': [],
                'url': url,
                'link': link,
                'title': '',
                'proxy': [],
                'user_pass': [],
                'cookies': '',
            }
        return responce
        # return link,proxy,user_pass,cookies


    def path2url(self, path, myhost="http://free-papers.tk/python test/" ):
        link = myhost + urllib.pathname2url(path)
        return link


if __name__ == '__main__':

    #HOW TO USE:
    url = "http://127.0.0.1/1752-153X-2-5%20-%20Copy.pdf"
    url = "http://127.0.0.1/1752-153X-2-5.pdf"
    url = 'http://ieeexplore.ieee.org/xpl/articleDetails.jsp?tp=&arnumber=6180383&queryText%3Dpower' #91 KB

    # print 'url in fink_link.py is'+url
    #
    # [link,proxy,user_pass ] = Find_Link(url).find_link()
    # $OPENSHIFT_HOMEDIR/app-root/runtime/srv/python/bin/python find_link.py --url "http://ieeexplore.ieee.org/xpl/articleDetails.jsp?tp=&arnumber=6180383&queryText%3Dpower" -p  "222.66.115.233:80"
    # python find_link.py --url "http://ieeexplore.ieee.org/xpl/articleDetails.jsp?tp=&arnumber=6180383&queryText%3Dpower" -p  "222.66.115.233:80"



    from optparse import OptionParser

    parser = OptionParser(description=__doc__)
    parser.add_option('-a', '--url', dest='url', help='adress url file name to be downloaded like:www.google.com')
    parser.add_option('-p', dest='proxy', help=' proxy setting for url file name to be download like:121.121.21.21:90')
    parser.add_option('-u', dest='user_name', help='user & password of proxy setting')
    # parser.add_option('-i', dest='input_fname', help='file name to be watermarked (pdf)')
    # parser.add_option('-w', dest='watermark_fname', help='watermark file name (pdf)')
    # parser.add_option('-d', dest='pdfdir', help='make pdf files in this directory')
    # parser.add_option('-o', dest='outdir', help='outputdir used with option -d', default='tmp')
    options, args = parser.parse_args()
    # options.url=url
    # options.proxy="222.66.115.233:80"

    if options.url:
        if options.proxy and not options.user_name:
            link, proxy, user_pass = Find_Link(options.url).find_link(options.proxy)
        elif options.proxy and options.user_name:
            link, proxy, user_pass = Find_Link(options.url).find_link(options.proxy, options.user_name)
        else:
            link, proxy, user_pass = Find_Link(options.url).find_link()
    else:
        parser.print_help()
