#!"E:\Program Files win 7 2nd\Python27/python.exe"
# -*- coding: UTF-8 -*-

# enable debugging
import cookielib
import urllib
import urllib2
import urlparse
import sys
import os
import re
from urlparse import urlparse as urlparse2

import mechanize
import BeautifulSoup


# from BeautifulSoup import BeautifulSoup

from os.path import basename
from urlparse import urlsplit
# global br,r,cj
def url2name(pdf_url):
    global br

    """

    :param pdf_url:
    :return:
    """
    # req = urllib2.Request(url)
    # r = urllib2.urlopen(req)
    if 'pdf_url.absolute_url' is locals():
        url = pdf_url.absolute_url
    else:
        url = pdf_url
    localName = basename(urlsplit(url)[2])
    # localName=urlparse.urlsplit(pdf_url).path.split('/')[-1]

    if (r is globals()) and r.info().has_key('Content-Disposition'):
        global r
        # If the response has Content-Disposition, we take file name from it
        localName = r.info()['Content-Disposition'].split('filename=')[1]
        if localName[0] == '"' or localName[0] == "'":
            localName = localName[1:-1]
        elif r.url != url:
        # if we were redirected, the real file name we take from the final URL
            localName = url2name(r.url)
            # if 'localFileName' is locals():
            #     # we can force to save the file as specified name
            #     localName = localFileName
    return localName


# class CommentCleanProcessor(mechanize.BaseProcessor):
#     import copy
#     def http_response(self, request, response):
#         if not hasattr(response, "seek"):
#             response = mechanize.response_seek_wrapper(response)
#         response.seek(0)
#         new_response = copy.copy(response)
#         new_response.set_data(
#             re.sub("<!-([^-]*)->", "<!--\1-->", response.read()))
#         return new_response
#     https_response = http_response

# noinspection PyCallingNonCallable,PyCallingNonCallable
def login_to_site(url, username, password, user_tag, pass_tag):
    """

    :param url:
    :param username:
    :param password:
    :param user_tag:
    :param pass_tag:
    :return: :raise:
    """
    browser = mechanize.Browser(factory=mechanize.RobustFactory())
    browser.set_handle_robots(False)
    browser.set_handle_referer(True)
    browser.set_handle_refresh(True)

    browser.set_handle_robots(False)
    browser.open(url)
    # noinspection PyCallingNonCallable,PyCallingNonCallable,PyCallingNonCallable,PyCallingNonCallable
    browser.select_form(nr=0)
    browser["USER"] = username
    browser["password"] = password
    # noinspection PyCallingNonCallable
    browser.submit()

    # noinspection PyCallingNonCallable
    if "Case Search Login Error" in browser.response().get_data():
        raise ValueError("Could not login to PACER Case Search. Check your "
                         "username and password")
    print ("You are logged on to the Public Access to Court Electronic "
           "Records (PACER) Case Search website as " + username + ". All costs "
                                                                  "will be billed to this account.")
    return browser


def BROWSER(url):
    """
    :param url:
    """
    global br, cj, r, proxy, User_Pass
    # def __init__(self,url,proxy=None):
    #           self.proxy="202.202.0.163:3128"
    #           self.url=url
    #           # RUN_BR()
    # Browser
    # def RUN_BR(self):
    br = mechanize.Browser()
    print br

    # Cookie Jar
    import random
    import os
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
    try:
        fo = os.getcwd()
        os.chdir(fo)
        os.mkdir(fo + "\\cookies\\")
    except:
        pass
    os.chdir(fo)
    pathname = os.path.join("cookies", cookie3)
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
    if proxy != [] and not (re.findall('None:None', proxy)):
        br.proxies = br.set_proxies({"http": proxy})
        # br.proxies=br.set_proxies( proxy)

    if User_Pass != [] and not (re.findall('None:None', User_Pass)):
        br.add_proxy_password(User_Pass.split(":")[0], User_Pass.split(":")[1])

    # if  r!={}:
    # rr = br.open(url)
    r=1




    # Proxy password
    # br.add_proxy_password("joe", "password")
    # self.dl_acm = "http://dl.acm.org/citation.cfm?id=99977.100000&coll=DL&dl=ACM"


class URL(object):
    def __init__(self, self_m='www.google.com'):
        self.self = self_m
        self.dl_acm = "http://dl.acm.org/citation.cfm?id=99977.100000&coll=DL&dl=ACM"
        self.dl_acm = "http://dl.acm.org/citation.cfm?id=99999&CFID=395886596&CFTOKEN=87447830"
        # pdf_url = "http://dl.acm.org/citation.cfm?id=99977.100000&coll=DL&dl=ACM"
        self.acm_delivery = 'http://delivery.acm.org/10.1145/100000/100000/p170-neumann.pdf?ip=222.178.10.241&id=100000&acc=ACTIVE%20SERVICE&key=C2716FEBFA981EF168D0E2752692E814D4069E6317A6859A&CFID=291819527&CFTOKEN=51493694&__acm__=1392230444_23a2ac08156942c15b18c50addc8d3f4'
        # url="http://www.gams.com/presentations/"
        self.glype_test = "http://pr4ss.tk/ss_proxy/web-proxy-glype-1.1-1/glype-1.1/upload/browse.php?u=Oi8vd3d3LmdhbXMuY29tL3ByZXNlbnRhdGlvbnMv&b=13&f=norefer"
        self.local_s = "http://127.0.0.1/trash/test/tb_purity_starter%20reseted%20for%20speed%20problem    /"
        self.local_purity = "http://127.0.0.1/trash/test/tb_purity_starter%20reseted%20for%20speed%20problem/tb_purity_starter/en/content/%D9%85%D8%A7%DA%98%D9%88%D9%84-%D8%AF%D8%B1-%D9%BE%D8%A7%DB%8C%D8%AA%D9%88%D9%86-%DB%8C%D8%B9%D9%86%DB%8C-%DA%86%D9%87-%D8%9F"
        self.local = "http://127.0.0.1/"
        self.vid = "http://www.mpeghunter.com/tube-watch/966538/busty-laura-anal.html"
        self.ieee = 'http://ieeexplore.ieee.org/xpl/login.jsp?tp=&arnumber=1274437&url=http%3A%2F%2Fieeexplore.ieee.org%2Fxpls%2Fabs_all.jsp%3Farnumber%3D1274437'
        self.ieee='http://ieeexplore.ieee.org/xpl/articleDetails.jsp?tp=&arnumber=5211199&queryText%3Dpower'

    def url2name(self, url2=None):
        if url2 == None:
            returns = basename(urlsplit(self.self)[2])
        else:
            returns = basename(urlsplit(url2)[2])
        return returns


def file_rd(path, mode='r', main_data='0'):
    # proxylist = open(path).read().split('\n')
    f = open(path, mode)
    if main_data == '0':
        data = f.read().split('\n')
    else:
        data = f.read()
        # data=f.readlines()
    # print data
    f.close
    return data


class LINK(object):
    global br, r, cj

    def __init__(self, url=''):
        self.url = url
        # def __int__(br):

    #  br.dd='none'
    def soap_my(self, data, tag, attr='a', href='href'):
        from BeautifulSoup import BeautifulSoup
        import re

        site = urlparse2(self.name).hostname
        soup = BeautifulSoup(data)
        ###################


        # pdfTags = soup.findAll('a', target='ft_gateway')
        # pdfUrlList = []
        # for result in pdfTags:
        #   pdfUrlList.append(result['href'])
        # thetds = soup.findAll('div', attrs={'id','divmain'})
        #
        # for thetd in thetds:
        #     print thetd.string
        links = soup.findAll(attr, href == True)
        print links
        try:
            if links == []: links = soup.findAll(attr, href == True)
        except:
            pass
        done=0
        for everytext in links:
            # e = re.compile('<'+attr+'*[^>]*>.*</'+attr+' *>')
            # soup2 = BeautifulSoup(str( everytext))
            # title = soup2.find(tag).text
            # print title
            # abstract_match = re.search(tag,str( everytext))
            # print abstract_match
            #
            # abstract_match = re.match('1752-153X-2-5',str( everytext))
            # print abstract_match
            #
            # abstract_match = re.search('1752-153X-2-5',str( everytext))
            # print abstract_match
            # match = re.findall(r'<a href="(.*?)".*>(.*)</a>', content)
            if re.findall(tag, str(everytext)):
                print everytext
                print everytext[href]
                if not (re.findall('www', everytext[href]) or re.findall('http://', everytext[href])):
                    f_nmae = urlparse.urljoin("http://" + site, everytext[href])
                    print f_nmae
                else:
                    f_nmae = everytext[href]
                    print f_nmae
                text = ''.join(everytext.findAll(text=True))
                data = text.strip()
                done=1
                return f_nmae
                break
                # print data
                #     if re.findall(tag, data):
                #         print everytext
                #         print everytext['href']
                #         if not (re.findall('www', everytext['href']) or re.findall('http://', everytext['href'])):
                #             f_nmae = urlparse.urljoin("http://" + site, everytext['href'])
                #             print f_nmae
                #         return f_nmae
                #         break
                # return f_nmae
                ###############
        if done==0:
            link=[]
            return link

    def beati_soap(self, data, tag, attr, classes, herf):
        bs = BeautifulSoup.BeautifulSoup(data)
        ingreds = [bs.getText().strip() for s in bs.findAll(tag)]

        fname = 'PorkChopsRecipe.txt'
        with open(fname, 'w') as outf:
            outf.write('\n'.join(ingreds))

        universities = BeautifulSoup.findAll(tag, attr)
        for eachuniversity in universities:
            print eachuniversity[herf] + "," + eachuniversity.string

    # noinspection PyCallingNonCallable
    def Text_to_link(self, text):
        text_link = {}
        # noinspection PyCallingNonCallable
        for text_link in br.links(text_regex=text):
            print (text_link)
        return text_link

    def find_link_better(self, tag='no'):
    # r = br.open(url)
        links_direct = {}
        links = {}
        i = 0
        if tag == 'no':
            # noinspection PyCallingNonCallable
            for link in br.links(text_regex='Full Text as PDF'):
                i = i + 1
                print (link)
                links = link
            for link in br.links(text_regex='Fulltext'):
                i = i + 1
                print (link)
                links = link
            for link in br.links(text_regex='pdf-link webtrekk-track'):
                i = i + 1
                print (link)
                links = link
            for link_direct in br.links(url_regex='/stamp/stamp.jsp?tp=&arnumber='):
                i = i + 1
                print (link_direct)
                links_direct = link_direct
        else:
            ll = []
            for link in br.links():
                i = i + 1
                print (link)
                ll.append(link)
            for link_direct in br.links(url_regex='/stamp/stamp.jsp?tp=&arnumber='):
                i = i + 1
                print (link_direct)
                links_direct = link_direct
            for link_direct in br.links(url='/stamp/stamp.jsp?tp=&arnumber='):
                i = i + 1
                print (link_direct)
                links_direct = link_direct

            for link in br.links(text_regex='Full Text'):
                i = i + 1
                print (link)
                links = link
                break
            for link in br.links(text_regex='Full Text as PDF'):
                i = i + 1
                print (link)
                links = link
                break
            for link in br.links(text='Full Text as PDF'):
                i = i + 1
                print (link)
                links = link
                break

            for link in br.links(text_regex='pdf'):
                i = i + 1
                print (link)
                links = link
                break

            for link in br.links(name='button btn-style-a'):
                i = i + 1
                print (link)
                links = link
                break
                # for link in br.links(name_regex= 'title'):
            #     i=i+1
            #     print (link)
            #     links=link
            # for link in br.links(tag='a'):
            #     i=i+1
            #     print (link)
            #     links=link


            for link_direct in br.links(url_regex='/stamp/stamp.jsp?tp=&arnumber='):
                i = i + 1
                print (link_direct)
                links_direct = link_direct
        return links, links_direct


    def find_link(self, tag='no'):
        # FInd Link of PDF
        global br, r, cj
        # r = br.open(url)
        data = br.links()
        i = 0
        link = {}
        links = {}
        if tag == 'no':
            for ii in data("\n"):
                if "href=" in ii:
                    s = 1
                if ".pdf" in ii:
                    i = i + 1
                    link[i] = ii
                    links.append = link[i]
                    print (link)
                if "PDF" in ii:
                    i = i + 1
                    link[i] = ii
                    links.append = link[i]
                    print (link)
                if "Fulltext" in ii:
                    i = i + 1
                    link[i] = ii
                    links.append = link[i]
                    print (link)
        else:
            for ii in data("\n"):
                if "href=" in ii:
                    s = 1
                if tag in ii:
                    i = i + 1
                    link[i] = ii
                    links.append = link[i]
                    print (link)
        return link

    # find pdf link by clicking on it
    def find_pdf_link(self, url):
        global br, cj, r, proxy, User_Pass
        # BROWSER(url.absolute_url)  #make r=br.open(url)
        # html = r.read()
        links_direct = {}
        links = {}

        br.set_cookiejar(cj)
        req = br.follow_link(url)
        pdf_url = req.wrapped._url
        url.absolute_url = pdf_url
        pdf_url_STR = str(pdf_url)
        if re.findall('&isnumber=', pdf_url_STR):
            done = 1
            return pdf_url_STR
        else:
        # Clicking the link to My CIMIS
            req = br.click_link(url)
            html = br.open(req).read()
            req = LINK(url.absolute_url).soap_my(html, '<frame src="http://ieeexplore.ieee.org', 'frame', 'src')
            print req

            pdf_url_STR = str(req)
            if re.findall('&isnumber=', pdf_url_STR):
                done = 1
                return pdf_url_STR
                # links=self(url.absolute_url).soap_my(html,'Full Text as PDF','a','href')
                # req = br.click_link(text='Full Text')
                # br.open(req)
                # print br.response().read()
                # print br.geturl()
                # # req = br.follow_link(url)
                # pdf_url = req.wrapped._url
                # url.absolute_url = pdf_url
                # pdf = self().pdf_link_urlib2(url)


        # pdf_url_STR=' '.join(pdf_url.keys())
        # req = br.click_link(text_regex='PDF')
        # page2 = br.follow_link(text_regex="PDF")
        # print page2
        # print req.geturl()

        def pdf_link_urlib2(url, headers={'User-agent': 'Mozilla/5.0'}):
            if proxy != None:
                proxies = {"http": "http://%s" % proxy}
                proxy_support = urllib2.ProxyHandler(proxies)
                opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler(debuglevel=1))
            else:
                opener = urllib2.build_opener('', urllib2.HTTPHandler(debuglevel=1))
                # url=link.absolute_url
            headers = {'User-agent': 'Mozilla/5.0'}
            opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler(debuglevel=1))
            urllib2.install_opener(opener)
            # requrllib2 = urllib2.Request(url, None, headers)

            requrllib2s = urllib2.Request(url.absolute_url, None, headers)
            # pdf_url=requrllib2s.redirect_dict
            htmls = urllib2.urlopen(requrllib2s).read()
            pdf_url = requrllib2s.redirect_dict
            pdf_url_STR = str(pdf_url)
            # pdf_url_STR=' '.join(pdf_url.keys())
            localFileName = None
            localName = basename(urlsplit(pdf_url_STR)[2])
            return pdf_url_STR

        return pdf_url_STR


class TWILL_Browser(object):
    def __init__(self, url="http://www.slashdot.org", form_data=None, proxy=[]):

        import twill
        from proxy_checker3 import make_returning_proxy

        self.a = twill.commands
        self.cookies = 'configs/cookies'
        self.proxy = proxy
        # if self.proxy == []:
        #     [self.proxy, self.proxy_h, self.prx_pass] = make_returning_proxy('configs//sites_proxy//', url,
        #                                                                      'configs//proxy_alive.txt')
        # elif self.proxy != [] and not (re.findall('None:None', self.proxy)) and (
        #     User_Pass != []) :
        #     proxy = 'http://' + ''.join(self.proxy)
        #
        # # br.proxies=br.set_proxies( proxy)
        #
        # else: # Proxy is on and no password is set
        #     self.proxy = 'http://' + ''.join(User_Pass) + '@' + ''.join(self.proxy)
        #
        # host = urlparse2(url).hostname
        # os.environ['http_proxy'] = self.proxy

        self.url = url
        self.username = "%(user)s" % form_data
        self.password = "%(pass)s" % form_data
        self.user_tag = "%(user_tag)s" % form_data
        self.pass_tag = "%(pass_tag)s" % form_data
        self.Form_id = "%(Form_id)s" % form_data
        self.submit_tag_name = "%(submit_tag_name)s" % form_data
        self.submit_tag_value = "%(submit_tag_value)s" % form_data
        self.Form_Type = "%(Form_Type)s" % form_data
        self.log_done = "%(Log_test)s" % form_data
        self.a.config("readonly_controls_writeable", 1)
        self.b = self.a.get_browser()
        self.b.set_agent_string(
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14")
        self.b.clear_cookies()

    def twill_work(self, url2='www.google.com'):
        # global r
        import sys, os

        os.environ['http_proxy'] = 'http://222.66.115.233:80'
        import twill,socket
        from twill import get_browser
        from twill.commands import *
        from twill.commands import reset_output,reset_browser
        from twill import get_browser
        import time
        # Navigate to Google
        # b = get_browser()
        # url = 'http://ieeexplore.ieee.org/xpl/articleDetails'
        # b.go(url2)
        # html = b.get_html()
        # print html
        #
        # try:
        #     html = b.get_html()
        # except:
        #     html = b.result.page
        # reset_browser()
        # reset_output()
        # os.environ['http_proxy'] = 'http://' + ''.join(self.proxy)
        # os.environ['http_proxy'] = 'http://222.66.115.233:80'
        t_com = twill.commands
        t_com.reset_browser
        t_com.reset_output
        t_com = twill.commands
        ## get the default browser
        t_brw = t_com.get_browser()
        # t_brw = b
        # open the url
        # url = 'http://google.com'
        final=t_brw.go(url2)
        # try:
        #     final=t_brw.go(url2)
        # except:
        #     final=b.go(url2)
        #     t_brw = b

        try:

            html = t_brw.result.page
        except:
            html = t_brw.get_html()
            # print html
        try:
            links2 = LINK(url2).soap_my(html, 'Full Text as PDF', 'a', 'href')
        except:
            links = t_brw.find_link('Full Text as PDF')
            links2 = links.absolute_url
        print links2
        # t_com = twill.commands
        t_com.reset_browser
        t_com.reset_output
        t_com = twill.commands
        t_brw = t_com.get_browser()
        try:
            try:
                t_brw.go(links2)
            except:
                # b.go(links2)
                # t_brw = b
                pass


            try:
                html = t_brw.result.page
                if re.findall('An error has occurred while trying to load your document.', html):
                    t_brw.go(links2)
                    html = t_brw.result.page



            except:
                html = t_brw.get_html()

            # print file

            try:
                links3 = LINK(links2).soap_my(html, '<frame src="http://ieeexplore.ieee.org', 'frame', 'src')
                if links3 == None:
                    links3 = LINK(links2).soap_my(html, 'Full Text as PDF', 'a', 'href')
                    # [l2, links] = t_com.showlinks()
                    # links3 = links.absolute_url
            except:
                links3 = LINK(links2).soap_my(html, '<frame src="http://ieeexplore.ieee.org', 'frame', 'src')
                [l2, links] = t_com.showlinks()
                links3 = links.absolute_url
                # link3=LINK(links).soap_my(html,' src="http://ieeexplore.ieee.org/')

            # links=t_brw.find_link('frameborder="0" src="http://ieeexplore.ieee.org/')
            # [l2, links3] = t_com.showlinks()

            # links=soap_my(file)
            # print links
            # t_com = twill.commands
            # t_com.reset_browser
            # t_com.reset_output
            # t_com = twill.commands
            try:
                socket.setdefaulttimeout(1000)
                t_brw.go(links3)
            except:
                # b.go(links3)
                # t_brw = b
                pass



            try:
                file = t_brw.result.page
            except:
                file = t_brw.get_html()
                # file = t_brw.result.page
            # print file
            # files=t_brw.follow_link(links)
            # print files
            # url2name=basename(urlsplit(l3)[2])
            r = t_com.show_extra_headers()
            # print file
            print url2name(links3)
            # pathname = os.path.join("PDF_Files", url2name(l3.absolute_url))
            pathname = url2name(links3)

        except:
            print 'we can not dowdnload this file by TWILL there is no link found Check proxy setting!!'

        try:
            if file!=[]:
                pdf_path = PDF_File().file_save(file, "PDF_Files", pathname)
                return pdf_path
            else:print 'we can not wodnload this file by TWILL Please Check another Menthod'
        except:
            print 'we can not wodnload this file by TWILL Please Check another Menthod'

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

            self.formnumber = 0
            formnumber = 1
            for each_frm in all_forms:
                self.formnumber = 1 + self.formnumber
                attr = each_frm.attrs             ## all attributes of form
                if each_frm.method == 'POST' and each_frm.attrs['id'] == self.Form_id:


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

                    t_brw.go('http://johnny.heliohost.org:2082/frontend/x3/index.phpcp')
                    print t_brw.find_link('http://64.62.211.131:2082/frontend/x3/mail/fwds.html')
                    print t_com.show_extra_headers()
                    print t_com.show_cookies()
                    print t_com.showlinks()
                    print t_brw.result.page

                    each_frm = t_brw.get_form(self.Form_id)
                    ctrl = each_frm.controls    ## return all control objects within that form (all html tags as control inside form)
                    for ct in ctrl:

                        if ct.attrs[
                            'name'] == self.user_tag and ct.type == 'text':     ## i did it as per my use, you can put your condition here
                            ct._value = self.username
                            # t_brw.clicked(each_frm,ct.attrs['name'])            ## clicked takes two parameter, form object and button name to be clicked.
                            # each_frm2=t_brw.get_form(1)
                            # t_com.fv(ct, self.user_tag, self.username)

                        if ct.attrs[
                            'name'] == self.pass_tag and ct.type == 'password':     ## i did it as per my use, you can put your condition here
                            ct._value = self.password
                            # t_com.fv(formnumber, self.pass_tag, self.password)
                            # t_brw.clicked(each_frm,ct.attrs['name'])            ## clicked takes two parameter, form object and button name to be clicked.

                        if ct.type == self.Form_Type and ct.attrs['name'] == self.submit_tag_name:
                            t_brw.clicked(each_frm, self.submit_tag_name)
                            t_brw.submit(formnumber)
                        formnumber = formnumber + 1
                        all_forms = t_brw.get_all_forms()         ## this returns list of form objects
                        print "Forms:"
                        t_brw.showforms()

                        # t_com.fv(self.formnumber, self.user_tag, self.username)
                        # t_com.fv(self.formnumber, self.pass_tag, self.password)
                        # t_brw.clicked(each_frm,ct.attrs['name'])            ## clicked takes two parameter, form object and button name to be clicked.
                        # t_brw.get_form_field(each_frm,'login')
                        # t_com.formvalue()
                        # t_brw.submit(3)
                    html = t_brw.get_html()
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
            # print t_brw.find_link(text="Full Text as PDF", url_regex=re.compile("/stamp/stamp.jsp?tp=&arnumber"))

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


    def slashdot(self):
        self.b.go(self.url)
        t_brw = self.b
        print t_brw.result.page
        ## get all forms from that URL
        all_forms = t_brw.get_all_forms()         ## this returns list of form objects
        print "Forms:"
        t_brw.showforms()
        formnumberr = 1
        for each_frm in all_forms:
            attr = each_frm.attrs             ## all attributes of form
            if each_frm.method == 'POST' and each_frm.attrs['id'] == self.Form_id:
                f = self.b.get_form(formnumberr)
            regexp = re.compile(self.submit_tag_value)
            link = self.b.find_link(regexp)
            if link:
                self.b.follow_link(link)
                f = self.b.get_form(self.Form_id)
                f[self.user_tag] = self.username
                f[self.pass_tag] = self.password
                self.a.fv("2", self.submit_tag_name, self.submit_tag_value)
            formnumberr = formnumberr + 1

        return self

    def splinter(self):
        from splinter import Browser

        with Browser('firefox') as browser:
            browser.visit(self.url)
            browser.find_by_name('element_name').click()


class PDF_File:
    def __init__(self):
        global br
        try:
            fo = os.getcwd()
            # os.chdir(fo)
            os.mkdir(fo + "/Watermarked_PDF_Files//")
        except:
            pass
        try:
            fo = os.getcwd()
            os.mkdir(fo + "/PDF_Files//")
        except:
            pass

    def pdf_cheker(self, pathname): # CHEcking if pdf is Correct
        from pyPdf import PdfFileReader
        pathname=pathname.replace("\\",'/')

        doc = PdfFileReader(file(pathname, "rb"))
        return doc

    def filename(self, pdf_url0):
        # import _rfc3986
        # localName = basename((pdf_url))
        # pathname = os.path.join("pdf_files", localName)
        # f_nmae=urlparse.urlsplit(pdf_url)
        # # d=urlparse.urlsplit(pdf_url).path.split('/')[-1]
        pdf_url=str(pdf_url0)
        if re.findall('/', pdf_url):
            self.suffix = os.path.splitext(pdf_url)[1]
            self.filename = urlparse.urlsplit(pdf_url).path.split('/')[-1]
            self.pdf_Folder_filename = os.getcwd() + "\\PDF_Files\\" + self.filename
            self.W_pdf_Folder_filename = os.getcwd() + "\\Watermarked_PDF_Files\\" + self.filename
        else:
            self.filename = urlparse.urlsplit(pdf_url).path.split('\\')[-1]
            self.pdf_Folder_filename = os.getcwd() + "\\PDF_Files\\" + self.filename
            self.W_pdf_Folder_filename = os.getcwd() + "\\Watermarked_PDF_Files\\" + self.filename

        # try:
        #     # localFile, mimeType = geturl(pdf_url, ".pdf")
        #     s=_rfc3986.urlsplit(pdf_url)
        #     for link in s:
        #         for match in re.finditer('href="([^"]+\.pdf)"', link):
        #             chapterLink = match.group(1)
        #         # self.filename=i.search(r'.pdf')
        #             # self.filename=f.find(".pdf")
        #
        #     self.path = _rfc3986.urlsplit(pdf_url)[2]
        #     self.suffix = os.path.splitext(self.path)[1]
        #     # self.fd, self.filename = tempfile.mkstemp(self.suffix)
        #     self.filename=urlparse.urlsplit(pdf_url).path.split('/')[-1]
        #     self.pdf_filename="\\PDF_Files\\"+self.filename
        #     self.W_pdf_filename="\\Watermarked_PDF_Files\\"+self.filename
        # except:
        #     self.path = _rfc3986.urlsplit(pdf_url)[2]
        #     self.suffix = os.path.splitext(self.path)[1]
        #     self.fd, self.filename = tempfile.mkstemp(self.suffix)
        #     self.filename=urlparse.urlsplit(pdf_url).path.split('/')[-1]
        #     self.pdf_filename="\\PDF_Files\\"+self.filename
        #     self.W_pdf_filename="\\Watermarked_PDF_Files\\"+self.filename
        #     print "Tere is problen in dilename funtion"
        return self

    def file_save(self, data, folder_name='PDF_Files\\', pathname2='test.pdf'):
        f = open(os.path.join(folder_name, pathname2), 'wb')
        f.write(data)
        f.close()
        return os.getcwd() + "\\" + os.path.join(folder_name, pathname2)

    def speed_download(self,pdf_url,br2,piece_size=1024*1024):
        localName = PDF_File().filename(pdf_url)
        openerdirector=br2.open(pdf_url)
        try:
            if (openerdirector._headers.dict['content-type'])=='application/pdf':
                length = long(openerdirector._headers.dict['content-length'])
                ok=True
        except:
            length=0
        dlength = 0
        # piece_size = 4096 # 4 KiB
        # piece_size =1024*1024 # 1MB
        data = ''
        while True:
            newdata = openerdirector.read(piece_size)
            dlength += len(newdata)
            data += newdata
            # pdf_path=PDF_File().file_save(data, "PDF_Files\\", localName.filename)
            # if onprogress:
            #     onprogress(length,dlength)
            if not newdata:
                break
        return data#,pdf_path
    def path2url(self, path, myhost="http://127.0.0.1/cgi-bin2/wrapper%20work" ):
        path2 = path.replace(os.getcwd(), '')
        link = myhost + urllib.pathname2url(path2)
        return link
        # return urlparse.urljoin('file:', urllib.pathname2url(path))

    def watermark_file(self, packet, text='hello'):
        from reportlab.pdfgen import canvas
        import reportlab.lib.pagesizes as ps
        from reportlab.lib.pagesizes import letter
        data=[]
        pack = open(packet, 'a+')

        p = canvas.Canvas(packet,pagesize=letter)
        p.drawString(10, 10, text)
        # data.append(pack)
        # data.append(p)
        p.setFont("Times-Roman", 60)
        p.setStrokeColorRGB(0.97, 0.97, 0.97)
        p.setFillColorRGB(0.974, 0.974, 0.974)
        p.translate(ps.A4[0] / 2, ps.A4[1] / 2)
        p.rotate(45)
        p.drawCentredString(10, 10, text)
        # p.showPage()
        # pack.write(data)
        pack.close()
        # c = canvas.Canvas(packet, pagesize=letter)
        # width, height = letter
        # p.drawImage(filename, inch, height - 2 * inch) # Who needs consistency?
        # p.showPage()

        # p.drawString(10, 10, text)
        # p.drawCentredString(80, 60, "Hannah Hu")
        # p.drawCentredString(80, 120, "2010/12/21")
        # p.drawCentredString(80, 0, "Confidential")
        p.save()
        return packet

    def pdf_watermark(self, pathname, Wm_f,speed='slow',wt1=''):
        from pyPdf import PdfFileWriter, PdfFileReader
        import watter_marker
        # from reportlab.pdfgen import canvas
        # from reportlab.lib.pagesizes import letter
        # pdf = PdfFileReader(file('arecibo.pdf', 'rb'))

        if wt1=='':
            wt1 = self.watermark_file(os.getcwd() + "\\Watermarked_PDF_Files\\" + "watermarker.pdf", 'www.free-papers.tk')
            watermark1 = PdfFileReader(file(wt1, 'rb'))
            wtt=watermark1.getPage(0)


        else:
            watermark1 = PdfFileReader(wt1)
            wtt=watermark1.getPage(0)
        # wt2=self.watermark_file(pathname,'www.free-papers.tk')
        if speed=='fast':
            watter_marker.op_w_input(pathname, wt1, Wm_f)
            return Wm_f

        # import pdftk

        output = PdfFileWriter()
        output2 = PdfFileWriter()
        input1 = PdfFileReader(file(pathname, "rb"))
        inf = PdfFileReader(file(pathname, "rb")).getDocumentInfo

        # watermark=PdfFileReader(file(os.getcwd()+"\\Watermarked_PDF_Files\\"+"watermarker.pdf","rb"))
        # print the title of document1.pdf
        print "title = %s" % (input1.getDocumentInfo().title)

        pdf = PdfFileReader(file(pathname, 'rb'))
        f = pdf.getNumPages()
        j = self.pdf_cheker(pathname)
        wt = watermark1.getPage(0)
        # for i in range(0,pdf.getNumPages()):
        #     output2.addPage(wt)
        # outputStream=open(os.getcwd()+"\\Watermarked_PDF_Files\\"+"watermarker.pdf", 'wb')
        # # output2.write(open(Wm_f, 'wb'))
        # output2.write(outputStream)
        # outputStream.close()
        # w=PdfFileReader(open(os.getcwd()+"\\Watermarked_PDF_Files\\"+"watermarker.pdf",'rb'))
        # ss=w.getpage(0)

        # for i in range(0,w.getNumPages()):
        #     p = pdf.getPage(i)
        #     print w
        #     st=w.getpage(i)
        #     st.mergePage(p)
        #     output.addPage(st)


        try:
            for i in range(0, pdf.getNumPages()):

                watermark =[]
                wt = []
                p = pdf.getPage(i)
                # p.mergePage(wt)
                # output.addPage(p)
                watermark = PdfFileReader(file(wt1, 'rb'))
                # # watermark = watermark1
                wt = watermark.getPage(0)


                # # wt=wtt
                # wt=watermark
                wt.mergePage(p)
                output.addPage(wt)
                # watermark.mergePage(p)
                # output.addPage(watermark)



            outputStream = open(Wm_f, 'wb')
            # outputStream=StringIO.StringIO()
            # output.write(open(Wm_f, 'wb'))
            output.write(outputStream)
            outputStream.close()
        except:
            print ('Please make correct Wattermarket')


            # print f1
            # f = open(pathname, 'wb')
            # data = f1.read()
            # with open(pathname, "wb") as code:
            #         code.write(data)
            #         # f2 = open(os.path.join("pdf_filesclick", localName), 'wb')
            #         # f2.write(req.read())
            # f.close()
            # f2.close()
            # return address of files

    def download_pdf_br(self, pdf_url1):
        # def filename(self):
        #    self.__original=unwrap(self)
        #    self.__fragment = splittag(self.__original)
        #    if self.__fragment:
        #     return '%s#%s' % (self.__original, self.__fragment)
        #    else:
        #     return self.__original
        # pdf_url = list
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
        if pdf_url.absolute_url.endswith(".pdf"):
            if pdf_url.absolute_url:
                # localName1 = basename(urlsplit(pdf_url.absolute_url)[2])
                localName = PDF_File().filename(pdf_url.absolute_url)
                # pathname = os.path.join("PDF_Files", localName.filename)
                # s=get_full_url(pdf_url)
                try:

                    data=PDF_File().speed_download(pdf_url.absolute_url,br,1024*1024)
                    if data!='':pdf=PDF_File().file_save(data, "PDF_Files\\", localName.filename)
                    done=1
                except:
                    try :
                        data
                        if  data=='':
                                f1 = br.retrieve(pdf_url.absolute_url, localName.pdf_Folder_filename)
                    except:
                        f1 = br.retrieve(pdf_url.absolute_url, localName.pdf_Folder_filename)
                # f1 = br.retrieve(pdf_url.absolute_url)
            else:
                # localName=urlparse.urlsplit(pdf_url).path.split('/')[-1]
                localName = PDF_File().filename(pdf_url)
                # pathname = os.path.join("PDF_Files", localName.filename)
                data=PDF_File().speed_download(pdf_url,br,1024*1024)
                if data!='':pdf=PDF_File().file_save(data, "PDF_Files\\", localName.filename)
                if data=='':f1 = br.retrieve(pdf_url.absolute_url, localName.pdf_Folder_filename)

        else:
            pdf_url = LINK().find_pdf_link(pdf_url)
            localName = self.filename(pdf_url)
            Pdf_folder_filename = localName.pdf_Folder_filename
            pathname = localName.filename
            # Pdf_W_pdf_filename="\\Watermarked_PDF_Files\\"+self.filename

            # localName = basename(pdf_url)
            # pathname = os.path.join("PDF_Files", localName)
            data=PDF_File().speed_download(pdf_url,br,1024*200)
            if data!='':pdf=PDF_File().file_save(data, "PDF_Files\\", localName.filename)
            if data=='':f1 = br.retrieve(pdf_url, localName.pdf_Folder_filename)
        doc = self.pdf_cheker(localName.pdf_Folder_filename)
        self.pdf_watermark(localName.pdf_Folder_filename, localName.W_pdf_Folder_filename,'fast')

        pdf_dw_li = localName.pdf_Folder_filename
        pdf_dw_Wr_li = localName.W_pdf_Folder_filename
        sp = self.path2url(pdf_dw_li)

        pdf_dw_li = self.path2url(localName.pdf_Folder_filename)
        pdf_dw_Wr_li = self.path2url(localName.W_pdf_Folder_filename)

        print "fetching main paper link url ...\n\t%s" % pdf_dw_li[:]
        print "fetching waterarker paper link url ...\n\t%s" % pdf_dw_Wr_li
        return pdf_dw_li, pdf_dw_Wr_li


        # return os.getcwd()+PDF_File.pdf_Folder_filename,os.getcwd()+PDF_File.W_pdf_Folder_filename

    def WM_Chk_Pdf(self, pdf_url):
        pdf_dw_Wr_li = pdf_dw_li = []
        localName = self.filename(pdf_url)

        try:

            doc = self.pdf_cheker(localName.pdf_Folder_filename)
            self.pdf_watermark(localName.pdf_Folder_filename, localName.W_pdf_Folder_filename)

            pdf_dw_li = localName.pdf_Folder_filename
            pdf_dw_Wr_li = localName.W_pdf_Folder_filename
            sp = self.path2url(pdf_dw_li)

            pdf_dw_li = self.path2url(localName.pdf_Folder_filename)
            pdf_dw_Wr_li = self.path2url(localName.W_pdf_Folder_filename)

            print "fetching main paper link url ...\n\t%s" % pdf_dw_li[:]
            print "fetching waterarker paper link url ...\n\t%s" % pdf_dw_Wr_li
            return pdf_dw_li, pdf_dw_Wr_li


        except:
            print ("Please Check url downloaded that is not in pdf format")
            return pdf_dw_li, pdf_dw_Wr_li,localName.pdf_Folder_filename


class PDF(object):
    def __init__(self, url=[]):
        self.url = url
        pass

        # global br,r,cj

    def url2name(url2):
        return basename(urlsplit(url2)[2])

    def get_pdf(self, pr=[], Us=[],
                sites_list = 'configs/sites_list_pdf_tags.txt',
                sites_list_files = "configs/sites_list_files.txt",
                site_proxy="configs//sites_proxy//"):
        global br, cj, r, proxy, User_Pass
        proxy = pr
        User_Pass = Us
        url = self.url
        pdf_path = []
        war_path = []
        # url=URL()
        # # url=url.local
        # url=url.dl_acm
        # url=url.glype_test
        # BR=BROWSER(url,'')
        # BR=BROWSER(url,None)
        # CommentCleanProcessor()
        if not url.endswith('.pdf') and url!=[]:
            BROWSER(url)
            # tet=url.glype_test
            # localName1=basename(urlsplit(tet)[2])
            # link=LINK(url.glype_test)
            localName1 = url2name(url)
            site = urlparse2(url).hostname
            listhandle = file_rd(sites_list, 'r')
            file_listhandle = file_rd(sites_list_files, 'r')

            link_done = 0
            url_pdf = {}

            if not url.endswith('.pdf'):
                html = br.open(url).read()
                # link_done = 0
                # url_pdf = {}

                while link_done == 0 and not ('Tag' in locals()):
                    for line in listhandle:
                        if re.findall(site, line) and link_done == 0 and (not re.findall("#", line.split("TAG:")[0])) :
                            if re.findall("TAG:", line):
                                try:
                                    # Tag = line.split("TAG:")["Attr:"]
                                    # atrr = line.split("Attr:")["CLASS"]
                                    Tag = line.split("TAG:")[1].split("Attr:")[0]
                                    Tag=Tag.replace("---",'')
                                    atrr = line.split("Attr:")[1].split("CLASS")[0]
                                    atrr=atrr.replace('---','')
                                    # [links,url_pdf]=LINK(url).beati_soap(html.read(),Tag,atrr,classes,herf)
                                    # links = LINK(url).soap_my(html, 'Full Text as PDF', 'a', 'href')
                                    links = LINK(url).soap_my(html, Tag, atrr)
                                    if links != [] and link_done!=None:
                                        link_done = 1

                                except:
                                    Tag = line.split("TAG:")[1]
                                    Tag=Tag.replace("---",'')
                                    try:
                                        # links=LINK(url).soap_my(html,Tag,attrs={'class': 'fulltext_lnk'},classes,herf)
                                        abstract_match = re.search("Full Text as PDF([^\']+)", html, re.IGNORECASE)
                                        abstract_url = "http://ieeexplore.ieee.org%s" % abstract_match.group(0)
                                        import lxml.html, codecs

                                        abs = []
                                        root = lxml.html.fromstring(html)
                                        for div in root:
                                            t = div.text_content()
                                            if t:
                                                abs.append(t)

                                        links = LINK(url).soap_my(html, Tag)
                                        if links != []  and link_done!=None:
                                            link_done = 1
                                    except:
                                        pass
                                    if link_done == 0 :
                                        links = LINK(url).soap_my(html, 'Full Text as PDF', 'a', 'href')
                                        # if links==[]:links3=LINK(links).soap_my(html,'<frame src="http://ieeexplore.ieee.org','frame','src')
                                        if links == [] or links==None:
                                            [links, url_pdf] = LINK(url).find_link_better(Tag)
                                        else:
                                            link_done = 1

                                if link_done == 1:
                                    print "<li><a>tag found</a></li>"
                                    break

                print html
            else:
                links=url

            # Tag="citation_pdf_url"

            # url_pdf=LINK(url).find_link(Tag)
            # [links,url_pdf]=LINK(url).find_link_better(Tag)
            if links != {} or url_pdf != {}:

                if url_pdf != {}:
                    pdf_path, war_path = PDF_File().download_pdf_br(url_pdf)
                    PDF_File().download_pdf_urllib2(url_pdf)
                    # pdf_path,war_path=PDF_File().download_pdf_br(url_pdf)
                    # PDF_File().download_pdf_urllib2(url_pdf)
                else:
                    # PDF_File().download_pdf_urllib2(links)
                    pdf_path, war_path = PDF_File().download_pdf_br((links))

        elif url!=[] and url.endswith('.pdf'):
            BROWSER(url)
            pdf_path, war_path = PDF_File().download_pdf_br(url)

        else:
            url_pdf = {}
            links = LINK(url).Text_to_link('Tags')
            links = LINK(url).Text_to_link('.flv')

            links2 = LINK(url).Text_to_link("کتاب")
            # PDF_File().download_pdf_br(url_pdf)
            try:
                if links != {}:
                    pdf_path, war_path = PDF_File().download_pdf_br(links)
                    PDF_File().download_pdf_urllib2(links)
                elif url_pdf != {}:
                    pdf_path, war_path = PDF_File().download_pdf_br(url_pdf)
                    PDF_File().download_pdf_urllib2(url_pdf)


            except IOError:
                if br.forms():
                    br.select_form(nr=0)
                    print [form for form in br.forms()]
                    # print [form for form in forms._forms._id_to_labels(text_regex='name')][0]
                    br.select_form(nr=1)
                    for form in br.forms():
                        print  form
                    br.select_form(nr=2)
                    print [form for form in br.forms()]

                    # print [form for form in br.forms(id='edit-name',name='name')]

                    br.form['name'] = "ss"
                    br.form['pass'] = "ss"
                    br.submit()
                    links2 = LINK(url).Text_to_link("کتاب")
                    PDF_File().download_pdf_urllib2(links2.absolute_url)

            except:
                if links2 != {}:
                    PDF_File().download_pdf_urllib2(links2.absolute_url)
                if links != {}:
                    PDF_File().download_pdf_urllib2(links.absolute_url)
        return pdf_path, war_path
    def get_pdf_sumery(self, pr=[], Us=[],
                sites_list = 'configs/sites_list_pdf_tags.txt',
                sites_list_files = "configs/sites_list_files.txt",
                site_proxy="configs//sites_proxy//"):
        global br, cj, r, proxy, User_Pass
        proxy = pr
        User_Pass = Us
        url = self.url
        pdf_path = []
        war_path = []
        if not url.endswith('.pdf') and url!=[]:
            BROWSER(url)
            localName1 = url2name(url)
            site = urlparse2(url).hostname
            listhandle = file_rd(sites_list, 'r')
            file_listhandle = file_rd(sites_list_files, 'r')
            link_done = 0
            url_pdf = {}
            if not url.endswith('.pdf'):
                html = br.open(url).read()
                while link_done == 0 and not ('Tag' in locals()):
                    for line in listhandle:
                        if re.findall(site, line) and link_done == 0 and (not re.findall("#", line.split("TAG:")[0])) :
                            if re.findall("TAG:", line):
                                try:
                                    # Tag = line.split("TAG:")["Attr:"]
                                    # atrr = line.split("Attr:")["CLASS"]
                                    Tag = line.split("TAG:")[1].split("Attr:")[0]
                                    Tag=Tag.replace("---",'')
                                    atrr = line.split("Attr:")[1].split("CLASS")[0]
                                    atrr=atrr.replace('---','')
                                    # [links,url_pdf]=LINK(url).beati_soap(html.read(),Tag,atrr,classes,herf)
                                    # links = LINK(url).soap_my(html, 'Full Text as PDF', 'a', 'href')
                                    links = LINK(url).soap_my(html, Tag, atrr)
                                    if links != [] and link_done!=None:
                                        link_done = 1

                                except:
                                    Tag = line.split("TAG:")[1]
                                    Tag=Tag.replace("---",'')
                                    try:
                                        # links=LINK(url).soap_my(html,Tag,attrs={'class': 'fulltext_lnk'},classes,herf)
                                        abstract_match = re.search("Full Text as PDF([^\']+)", html, re.IGNORECASE)
                                        abstract_url = "http://ieeexplore.ieee.org%s" % abstract_match.group(0)
                                        import lxml.html, codecs

                                        abs = []
                                        root = lxml.html.fromstring(html)
                                        for div in root:
                                            t = div.text_content()
                                            if t:
                                                abs.append(t)

                                        links = LINK(url).soap_my(html, Tag)
                                        if links != []  and link_done!=None:
                                            link_done = 1
                                    except:
                                        pass
                                    if link_done == 0 :
                                        links = LINK(url).soap_my(html, 'Full Text as PDF', 'a', 'href')
                                        # if links==[]:links3=LINK(links).soap_my(html,'<frame src="http://ieeexplore.ieee.org','frame','src')
                                        if links == [] or links==None:
                                            [links, url_pdf] = LINK(url).find_link_better(Tag)
                                        else:
                                            link_done = 1

                                if link_done == 1:
                                    print "<li><a>tag found</a></li>"
                                    break

                print html
            else:
                links=url

            # Tag="citation_pdf_url"

            # url_pdf=LINK(url).find_link(Tag)
            # [links,url_pdf]=LINK(url).find_link_better(Tag)
            if links != {} or url_pdf != {}:

                if url_pdf != {}:
                    pdf_path, war_path = PDF_File().download_pdf_br(url_pdf)

                    data=PDF_File().speed_download(url_pdf,br,1024*200)

                    PDF_File().download_pdf_urllib2(url_pdf)
                    # pdf_path,war_path=PDF_File().download_pdf_br(url_pdf)
                    # PDF_File().download_pdf_urllib2(url_pdf)
                else:
                    # PDF_File().download_pdf_urllib2(links)
                    pdf_path, war_path = PDF_File().download_pdf_br((links))

        elif url!=[] and url.endswith('.pdf'):
            BROWSER(url)
            pdf_path, war_path = PDF_File().download_pdf_br(url)

        else:
            url_pdf = {}
            links = LINK(url).Text_to_link('Tags')
            links = LINK(url).Text_to_link('.flv')

            links2 = LINK(url).Text_to_link("کتاب")
            # PDF_File().download_pdf_br(url_pdf)
            try:
                if links != {}:
                    pdf_path, war_path = PDF_File().download_pdf_br(links)
                    PDF_File().download_pdf_urllib2(links)
                elif url_pdf != {}:
                    pdf_path, war_path = PDF_File().download_pdf_br(url_pdf)
                    PDF_File().download_pdf_urllib2(url_pdf)


            except IOError:
                if br.forms():
                    br.select_form(nr=0)
                    print [form for form in br.forms()]
                    # print [form for form in forms._forms._id_to_labels(text_regex='name')][0]
                    br.select_form(nr=1)
                    for form in br.forms():
                        print  form
                    br.select_form(nr=2)
                    print [form for form in br.forms()]

                    # print [form for form in br.forms(id='edit-name',name='name')]

                    br.form['name'] = "ss"
                    br.form['pass'] = "ss"
                    br.submit()
                    links2 = LINK(url).Text_to_link("کتاب")
                    PDF_File().download_pdf_urllib2(links2.absolute_url)

            except:
                if links2 != {}:
                    PDF_File().download_pdf_urllib2(links2.absolute_url)
                if links != {}:
                    PDF_File().download_pdf_urllib2(links.absolute_url)
        return pdf_path, war_path

    def form(self, usr_psw, pr=[], Us=[]):
        global br, cj, r, proxy, User_Pass
        proxy = pr
        User_Pass = Us
        url = self.url
        pdf_path = []
        war_path = []
        links = {}
        BROWSER(url)
        localName1 = url2name(url)
        if br.forms():
            br2 = br
            print [form for form in br.forms()]
            br.select_form(nr=0)
            # br.select_form(name="USER")
            # [f.id for f in br.forms()]
            for form in br.forms():
                if form.attrs['id'] == 'password':
                    br.form = form
            formcount = 0
            for frm in br.forms():
                if str(frm.attrs["id"]) == "password":
                    # break
                    pass
                formcount = formcount + 1
            br.select_form(nr=formcount)

            br.select_form(nr=0)
            print [form for form in br.forms()]
            # print [form for form in forms._forms._id_to_labels(text_regex='name')][0]
            br.select_form(nr=1)
            for form in br.forms():
                print  form
            br.select_form(nr=2)
            print [form for form in br.forms()]

            # print [form for form in br.forms(id='edit-name',name='name')]

            br.form['password'] = "ss"
            br.form['USER'] = "ss"
            br.submit()
            links2 = LINK(url).Text_to_link("کتاب")
            PDF_File().download_pdf_urllib2(links2.absolute_url)
            if links2 != {}:
                PDF_File().download_pdf_urllib2(links2.absolute_url)
            if links != {}:
                PDF_File().download_pdf_urllib2(links.absolute_url)


def TWIll_MAIN(url='http://ieeexplore.ieee.org/ielx5/8981/28518/01274437.pdf?tp=&arnumber=1274437&isnumber=28518',
               proxy=[], User_Pass=[]):
    """

    :param url:
    :return:
    """
    import socket
    from form_test_goodworking import usr_tag, make_returning_proxy

    site_list_form = 'configs/sites_form_user.txt'
    cookies = 'configs/cookies'

    # url = 'http://ieeexplore.ieee.org/ielx5/8981/28518/01274437.pdf?tp=&arnumber=1274437&isnumber=28518'
    # url = 'http://ieeexplore.ieee.org/xpl/login.jsp?tp=&arnumber=1274437&url=http%3A%2F%2Fieeexplore.ieee.org%2Fxpls%2Fabs_all.jsp%3Farnumber%3D1274437'

    if proxy == []:
        [proxy, proxy_h, prx_pass] = make_returning_proxy('configs//sites_proxy//', url,
                                                          'configs//proxy_alive.txt')
    elif proxy != [] and not (re.findall('None:None', proxy)) and (
            User_Pass != []):
        proxy = 'http://' + ''.join(proxy)

    # br.proxies=br.set_proxies( proxy)

    else: # Proxy is on and no password is set
        proxy = 'http://' + ''.join(User_Pass) + '@' + ''.join(proxy)

    host = urlparse2(url).hostname
    os.environ['http_proxy'] = proxy

    #timeout in seconds see http://docs.python.org/library/socket.html#socket.setdefaulttimeout
    socket.setdefaulttimeout(100)

    # Navigate to Google
    listform = file_rd(site_list_form, 'r')
    ## main download prosses with twill for try
    try:
        for line in listform:
            if line.find(host) != -1:
                form_data = usr_tag(line)
                # html=login_to_site(url,form_data)
                import twill.commands
                # t1=TWILL_Browser(url,form_data).splinter()
                # twill_work(url)
                # t=TWILL_Browser(url,form_data).slashdot()
                pdf_link = TWILL_Browser(url, form_data, proxy).twill_work(url)
                break
        return pdf_link
        # try:

        txheaders = {
            'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
            'Accept-Language': 'en,hu;q=0.8,en-us;q=0.5,hu-hu;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
            'Keep-Alive': '300',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Host': 'johnny.heliohost.org:2082',
            'Referer': 'http://johnny.heliohost.org:2082/frontend/x3/index.phpcp',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': '	cprelogin=no; cpsession=soheilsa%3aZTw6vgajGklrpoKSKboU0Rj0SRJvL65dK4Qgx22qJNe1mrrLeAOB5uil3gRLDK6V; _jsuid=2121790376; langedit=; lang='
        }

        y = {'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
             'Connection': 'keep-alive',
             'Host': 'johnny.heliohost.org:2082',
             'Accept-Language': 'en,hu;q=0.8,en-us;q=0.5,hu-hu;q=0.3',
             'Accept-Encoding': 'gzip, deflate',
             'Cache-Control': 'max-age=0',
             'Referer': 'http://johnny.heliohost.org:2082/frontend/x3/index.phpcp',
             'X-Requested-With': 'XMLHttpRequest',
             'Keep-Alive': '300',
             'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5'}


    except urllib2.HTTPError, e:
        print e.headers
        print e.headers.has_key('WWW-Authenticate')
        try:
            # p = urllib2.HTTPPasswordMgrWithDefultRealm()
            req = urllib2.Request(url)
            handler = urllib2.HTTPBasicAuthHandler()
            opener = urllib2.build_opener(handler)
            urllib2.install_opener(opener)
            page = urllib2.urlopen(req).read()
            print page
        except:
            pass

        for line in listform:
            if line.find(host) != -1:
                form_data = usr_tag(line)
                html = login_to_site(url, form_data)

        print '</pre>'
        return pdf_link
    except IOError:
        print IOError

# FInd PDf Lins Functions


# Download Pdf files by urlins TOO Long

# dDOwnload BY Browser Function
# def download_pdf_twill(self,pdf_url1):
#     def __init__(self, url="http://www.slashdot.org",form_data=None):
#         self.a=twill.commands
#         self.url=url
#         self.username="%(user)s"%form_data
#         self.password="%(pass)s"%form_data
#         self.user_tag="%(user_tag)s"%form_data
#         self.pass_tag="%(pass_tag)s"%form_data
#         self.Form_id="%(Form_id)s"%form_data
#         self.submit_tag_name="%(submit_tag_name)s"%form_data
#         self.submit_tag_value="%(submit_tag_value)s"%form_data
#         self.Form_Type="%(Form_Type)s"%form_data
#         self.log_done="%(Log_test)s"%form_data
#         self.a.config("readonly_controls_writeable", 1)
#         self.b = self.a.get_browser()
#         self.b.set_agent_string("Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14")
#         self.b.clear_cookies()









# url = URL()
# url_l = url.local
# localName1 = url.url2name(url_l)




class ieee_main(object):
    def __init__(self, sites_list = 'configs/sites_list_pdf_tags.txt',
                 sites_list_files = "configs/sites_list_files.txt",
                 site_proxy="configs//sites_proxy//"):
        self.sites_list = sites_list
        self.sites_list_files = sites_list_files
        self.site_proxy = site_proxy
        # def __int__(br):

    def todo_url(self,url = URL().ieee):
        import proxy_checker3

        # sites_list = "configs/sites_list.txt"
        # sites_list_files = "configs/sites_list_files.txt"
        # sites_list = 'configs/sites_list_pdf_tags.txt'
        sites_list = self.sites_list
        sites_list_files = self.sites_list_files
        site_proxy = self.site_proxy

        # url = URL().ieee
        url=url.replace(' ','%20')

        pr_h, proxy_h, user_pass_h = proxy_checker3.make_returning_proxy("configs//sites_proxy//", url)

        # usr_psw='jnu:jnulib'
        # # PDF('http://164.100.247.17/').form(usr_psw,pr_h[j],user_pass_h[j])
        # url="http://164.100.247.17/"
        # login_to_site(url,usr_psw, usr_psw,user_tag,pass_tag)
        #
        # login_to_site(url,'jnu', 'jnulib')
        # PDF('http://164.100.247.17/').form(usr_psw,[],[])
        i = -1
        pdf_path = war_path = []
        if pr_h != []:
            for j in range(i + 1, len(pr_h)):

                [pdf_path, war_path] = PDF(url).get_pdf(pr_h[j], user_pass_h[j])
                if pdf_path != [] or war_path != [] and (os.path.getsize((pdf_path))):
                    break
                pdf_h = TWIll_MAIN(url, pr_h[j], user_pass_h[j])
                # pdf = PDF_File().filename(pdf_h)
                pdf_path, war_path = PDF_File().WM_Chk_Pdf(pdf_h)
                print "your download link is:"
                try:
                    print pdf_path + '\n' + war_path
                except:
                    print 'problem is here in twill'
                if pdf_path != [] or war_path != [] and (os.path.getsize((pdf_path))):
                    break

                [pdf_path, war_path] = PDF(url).get_pdf(pr_h[j], user_pass_h[j])
                if pdf_path != [] or war_path != []:
                    break

                usr_psw = 'jnu:jnulib'
                # # PDF('http://164.100.247.17/').form(usr_psw,pr_h[j],user_pass_h[j])
                # PDF('http://164.100.247.17/').form(usr_psw,[],[])
                pdf_path, war_path = PDF(url).get_pdf(pr_h[j], user_pass_h[j])
                pdf_path, war_path = PDF(url).get_pdf(pr_h, [])




                # pdf=PDF(URL().vid).get_pdf("127.0.0.1:8580")
                #            pdf=PDF(URL().local).get_pdf([])



        elif pr_h == "None:None":
            pdf_path, war_path = PDF(url).get_pdf(pr_h, [])

        if pdf_path == [] or war_path == []:
            print "we are unable to download your file with " + url + " address !!"
        return pdf_path , war_path


if __name__ == "__main__":
    # main().todo_url(URL().ieee)
    url='http://127.0.0.1/1752-153X-2-5 - Copy.pdf'
    try:

        url = int(sys.argv[0])
        print 'url is:'+url

    except:
        url='http://ieeexplore.ieee.org/xpl/articleDetails.jsp?tp=&arnumber=6698740&queryText%3Dpower+market'
        url='http://ieeexplore.ieee.org/xpl/login.jsp?tp=&arnumber=6698740&url=http%3A%2F%2Fieeexplore.ieee.org%2Fstamp%2Fstamp.jsp%3Ftp%3D%26arnumber%3D6698740'

        url='http://ieeexplore.ieee.org/xpl/articleDetails.jsp?tp=&arnumber=6180383&queryText%3Dpower' #91 KB

        # url='http://127.0.0.1/1752-153X-2-5 - Copy.pdf'
        # url='http://127.0.0.1/'
    for x in sys.argv:
        print "Argument: ", x

    # url='http://127.0.0.1/'
    ieee_main().todo_url(url)
        # html = urllib2.urlopen(requrllib2).read()
        # html.info()['Content-Disposition']
        # # for link in br.links ('a', href=True, text='PDF'):
        # #     print link
        # br.set_proxies({"http": proxy})
        #
        # req = br.
        # c
        # lick_link(text_regex='Stochastic Programming')
        # requrllib2s = urllib2.Request(url, None, headers)
        # pdf_url=requrllib2s.redirect_dict
        # htmls = urllib2.urlopen(requrllib2s).read()
        #
        # f1 = br.retrieve(pdf_url)
        # print f1
        # fh = open(f1)
        #
        #
        #
        # s=br.open(req);
        #
        # # Download
        # br.set_proxies({"http": proxy})
        #
        # f = br.retrieve(link)
        # print f
        # fh = open(f)
        #
        # # Show the source
        # pr    int html
        # # or
        # print br.response().read()
        #
        # # Show the html title
        # print br.title()
        #
        # # Show the response headers
        # print r.info()
        # # or
        # print br.response().info()
        #
        #
        # # from bs4 import BeautifulSoup
        # # for link in soup.findAll('a', href=True, text='TEXT'):
        # #      print link['href']
        #
        # # Show the available forms
        # for f in br.forms():
        #print f
        #
        # # Select the first (index zero) form
        # br.select_form(nr=0)
        #
        # # Let's search
        # # br.form['a']='PDF'
        # br.submit()
        # # print br.response().read()
        #
        # # Looking at some results in link format
        # for link in br.links(text_regex='PDF'):
        #     print link
        #
        # for link in br.links ('a', href=True, text='PDF'):
        #     print link
        #
        # # Testing presence of link (if the link is not found you would have to
        # # handle a LinkNotFoundError exception)
        # br.find_link(text='FullText PDF')
        #
        # # Actually clicking the link
        # req = br.click_link(text='PDF')
        # br.open(req)
        # print br.response().read()
        # print br.geturl()
        #
        # #Back
        # br.back()
        # print br.response().read()
        # print br.geturl()
        # endregion
