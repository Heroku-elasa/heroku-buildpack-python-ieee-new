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
import os, re, errno,sys
import urllib
import urllib2, urlparse
from urlparse import urlparse as urlparse2
from BeautifulSoup import BeautifulSoup


print "Content-type: text/html\n"
print "this is running"

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

    # return urlparse.urljoin('file:', urllib.pathname2url(path))

class LINK:
    def __init__(self,url='',sites_list = 'configs/sites_list_pdf_tags.txt',
                 sites_list_files = "configs/sites_list_files.txt",
                 site_proxy="configs//sites_proxy//"):

        fo = os.getcwd().replace('\\','/')
        CurrentDir = os.path.dirname(os.path.realpath(__file__))
        Parent_Dir=os.path.abspath(os.path.join(CurrentDir, '../..'))
        os.chdir(Parent_Dir)
        if Parent_Dir not in sys.path:
            sys.path.insert(0, Parent_Dir)
        from  download_mozilla import web
        import proxy_checker3_all_function
        self.proxy_checker3=proxy_checker3_all_function
        self.Mozilla_Web=web
        self.url = url
        self.sites_list=Parent_Dir.replace('\\','/')+'/'+sites_list
        self.sites_list_files=Parent_Dir.replace('\\','/')+'/'+sites_list_files
        self.site_proxy=site_proxy
        os.chdir(fo)


    def filename(self, pdf_url0):
        pdf_url = str(pdf_url0)
        if re.findall('/', pdf_url):
            self.suffix = os.path.splitext(pdf_url)[1]
            self.file_name_decode = urllib2.unquote(pdf_url).decode('utf8').split('/')[-1]
            self.filename = urlparse.urlsplit(pdf_url).path.split('/')[-1]
            self.pdf_Folder_filename = os.getcwd().replace('\\','/') + "/"+PDF_Files_Dir+"/" + self.filename
            self.W_pdf_Folder_filename = os.getcwd().replace('\\','/') + "/"+Watermarked_PDF_Dir+"/" + self.filename
            self.chdir=os.getcwd().replace('\\','/')
        else:
            self.filename = urlparse.urlsplit(pdf_url).path.split('\\')[-1]
            self.chdir=os.getcwd().replace('\\','/')
            self.pdf_Folder_filename = os.getcwd().replace('\\','/') + "/"+PDF_Files_Dir+"/" + self.filename
            self.W_pdf_Folder_filename = os.getcwd().replace('\\','/') + "/"+Watermarked_PDF_Dir+"/" + self.filename


        return self
    def file_rd(self,path, mode='r', main_data='0'):
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
        data=kwargs['data']
        tag=kwargs['tag']
        try:attr=kwargs['attr']
        except:attr='a'
        try:href=kwargs['href']
        except:href='href'
        try:url=kwargs['url']
        except:
            url = "http://"+urlparse2(self.url).hostname


        # from BeautifulSoup import BeautifulSoup
        # import re

        # site = urlparse2(self.url).hostname
        soup = BeautifulSoup(data)
        ###################
        links = soup.findAll(attr, href == True)
        print links
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
                if not (re.findall('www', everytext[href]) or re.findall('http://', everytext[href])):
                    f_nmae = urlparse.urljoin( url, everytext[href])

                else:
                    f_nmae = everytext[href]

                print unicode(f_nmae)
                text = ''.join(everytext.findAll(text=True))
                data = text.strip()
                done = 1
                return f_nmae

                ###############
        if done == 0:
            link = []
            return link
    def dowload_basePr_userpass(self,url,pr_h,user_pass_h):
        try:
            web=self.Mozilla_Web

            if  'user_pass_h' is locals():

                html,pr,upss=web().download(url,pr_h,user_pass_h)
                # or by mechanizm method
                # html,pr,upss=web().download_mechanism(url,pr_h,user_pass_h)

            else:
                html,pr,upss=web().download(url,pr_h)
                # or by mechanizm method
                # html,pr,upss=web().download_mechanism(url,pr_h)

        except:
            html=[]
            pr=[]
            upss=[]
            print "we cant dowload beacuse of invalid tag or invalid proxy line 620" + "\n"

        return  html,pr,upss

    def get_pdf_link(self,proxy='', user_pass=''):

        url=self.url


        if proxy == '':

            fo = os.getcwd()
            pr_h, proxy_h, user_pass_h = self.proxy_checker3.make_returning_proxy("configs//sites_proxy//", url)
            os.chdir(fo)
        else:
            pr_h = []
            user_pass_h = []
            pr_h.append(proxy)
            user_pass_h.append(user_pass)
            i = user_pass_h.index("")
            del user_pass_h[i]
            try:
                i = pr_h.index("")
                del pr_h[i]
            except:
                pass

        don_flg = -1
        if pr_h != []:
            i = -1
            site = urlparse2(url).hostname
            listhandle = self.file_rd(self.sites_list, 'r')
            file_listhandle = self.file_rd(self.sites_list_files, 'r')
            link_done = 0
            url_pdf = {}
            for j in range(i + 1, len(pr_h)):
                if don_flg != 1 and not url.endswith('.pdf') and link_done == 0:

                    [html,proxy0,user_pass]=self.dowload_basePr_userpass(url,pr_h[j],user_pass_h[j])


                    if link_done == 0 and html!=[]:
                        links =self.soap_my(data=html, tag='Full Text as PDF', attr='a', href='href',url=url)
                        # links = self.soap_my(html, 'Full Text as PDF', 'a', 'href')
                        if links!=[]:
                            [html,proxy0,user_pass]=self.dowload_basePr_userpass(links,pr_h[j],user_pass_h[j])
                            links =self.soap_my(data=html, tag='<frame src="http://ieeexplore.ieee.org', attr='frame', href='src',url=str(links))
                            # links2=self.soap_my(html,'<frame src="http://ieeexplore.ieee.org','frame','src')
                            # links=links2
                        if links == [] or links==None:
                            pass
                        else:
                            link_done = 1
                            break

                        for line in listhandle:
                            if re.findall(site, line) and link_done == 0 and (not re.findall("#", line.split("TAG:")[0])) :
                                if re.findall("TAG1:", line):
                                    try:
                                        Tag = line.split("TAG1:")[1].split("---")[0]
                                        Tag=Tag.replace("+++",'')
                                        atrr = line.split("Attr1:")[1].split("---")[0]
                                        atrr=atrr.replace("+++",'')
                                        href=line.split('Href1:')[1].split("---")[0]
                                        href=href.replace("+++",'')
                                        links =self.soap_my(data=html, tag=Tag, attr=atrr, href=href,url=url)
                                        # links = self.soap_my(html, Tag, atrr,href)
                                        if links != [] and link_done!=None:
                                            try:
                                                Tag = line.split("TAG2:")[1].split("---")[0]
                                                Tag=Tag.replace("---",'').replace("+++",'')

                                                atrr = line.split("Attr2:")[1].split("---")[0]
                                                atrr=atrr.replace('---','').replace("+++",'')
                                                href=line.split('Href2:')[1].split("---")[0]
                                                href=href.replace("+++",'')
                                                [html,proxy0,user_pass]=self.dowload_basePr_userpass(links,pr_h[j],user_pass_h[j])
                                                links =self.soap_my(data=html, tag=Tag, attr=atrr, href=href,url=str(links))
                                                # links = self.soap_my(html, Tag, atrr,href)
                                            except:pass
                                                # [html,proxy0,user_pass]=self.dowload_basePr_userpass(links,pr_h[j],user_pass_h[j])
                                                # links =self.soap_my(data=html, tag=Tag, attr=atrr, href=href,url=url)
                                                # links = self.soap_my(html, Tag, atrr,href)
                                            if links != [] or links!=None:
                                                link_done = 1
                                                print '---------------we found Proper link which is :------------\n'+str(links)+\
                                                      '\n ----with proxy-------\n'+str(pr_h[j])+':'+str(user_pass_h[j])
                                                print '----------------- Link Found -------------------------'
                                                return links,pr_h[j],user_pass_h[j]

                                    except:
                                        pass
                                        #     Tag = line.split("TAG1:")[1]
                                        #     Tag=Tag.replace("---",'')
                                        #     try:
                                        #         abstract_match = re.search("Full Text as PDF([^\']+)", html, re.IGNORECASE)
                                        #         abstract_url = "http://ieeexplore.ieee.org%s" % abstract_match.group(0)
                                        #         import lxml.html, codecs
                                        #         abs = []
                                        #         root = lxml.html.fromstring(html)
                                        #         for div in root:
                                        #             t = div.text_content()
                                        #             if t:
                                        #                 abs.append(t)
                                        #
                                        #         links = LINK(url).soap_my(html, Tag)
                                        #         if links != []  and link_done!=None:
                                        #             link_done = 1
                                        #     except:
                                        #         pass
                                        # break


                    elif link_done == 1:
                        print "<li><a>tag found</a></li>"
                        print links
                        break

                elif url!=[] and url.endswith('.pdf'):

                    return url,'',''


            if link_done==0:
                links=[]
                pr_h[j]=[]
                user_pass_h[j]=[]
                print "we couldnt find link beacuase of no proxy is able to download .find good proxy over internet"


            return links,pr_h[j],user_pass_h[j]

        else: # pr_h[j]=[] there is no trusted proxy for it
            html=self.dowload_basePr_userpass(url,'None')
            links = LINK(url).soap_my(html, 'Full Text as PDF', 'a', 'href')
            if links==[]:
                html=self.dowload_basePr_userpass(links,'None')
                links2=LINK(links).soap_my(html,'<frame src="http://ieeexplore.ieee.org','frame','src')
                link=links2
                if links == [] or links==None:
                    print'there is no trusted proxy for downloading it'
                else:
                    link_done = 1
            return links,[],[]





if __name__ == '__main__':
    #HOW TO USE:
    url = "http://127.0.0.1/1752-153X-2-5%20-%20Copy.pdf"
    url = "http://127.0.0.1/1752-153X-2-5.pdf"
    url='http://ieeexplore.ieee.org/xpl/articleDetails.jsp?tp=&arnumber=6180383&queryText%3Dpower' #91 KB
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