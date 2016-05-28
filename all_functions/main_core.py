#!"E:/Program Files win 7 2nd/python27/python.exe"
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
__author__ = 'soheil sab by www.elec-lab.tk'
# from __future__ import with_statement
# from google.appengine.api import files
import os,sys,re
import urllib,socket
from hurry.filesize import size
from urlparse import urlparse as urlparse2
print "Content-type: text/html\n"
print ''
print '<pre>'
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


def import_once(modulenames, silent=1):
##    import_once
##    Fedmich   Last modified: 3:38 PM 5/15/2006
##    version 1.1
##    Usage:
##    import_once('os')
##    import_once( ["os", 'sys'] )
    
    if type(modulenames) is list:
        pass
    elif type(modulenames) is tuple:
        pass
    else:
        modulenames = [modulenames]

    imported = 0
    for modulename in modulenames:
        print modulename
        if globals().has_key(modulename):
            if not silent:  print """Already imported module "%s"...""" % modulename
            imported +=1
        else:
            try:
                if not silent:
                    print """%s is not yet imported so import it now...""" % modulename
                globals()[modulename] = __import__(modulename, globals(), locals(), [])
                imported += 1
            except:
                if not silent:  print """Error while importing "%s"...""" % modulename

    return (imported == len(modulenames) )  #return true if every modules are successfuly imported



class core(object):

    def __init__(self,sites_list = 'configs/sites_list_pdf_tags.txt',
                 sites_list_files = "configs/sites_list_files.txt",
                 site_proxy="configs//sites_proxy//",**kwargs):

        CurrentDir=os.path.dirname(os.path.realpath(__file__))
        fo=CurrentDir.replace('\\','/')+"/cookies/"
        if not os.path.isdir(fo):
            os.mkdir(fo)
        proxy_checker3_all_function=import_mod(from_module='proxy_checker3_all_function')
        # import proxy_checker3_all_function
        self.proxy_checker3=proxy_checker3_all_function
        self.sites_list = sites_list
        self.sites_list_files = sites_list_files
        self.site_proxy = site_proxy
        # from find_link import Find_Link as self.Find_Link2
        if 'find_link' in sys.modules:
            print "@@@@@@@@@@@@@@ module already exist  for  find_link "+' is \n: @@@@@@@@@@@@@@\n\n'
            self.Find_Link=sys.modules['find_link'].Find_Link
        else:
            print "@@@@@@@@@@@@@@ module inserted for   \n: @@@@@@@@@@@@@@\n\n"
            from find_link import Find_Link
            self.Find_Link=Find_Link



        # if kwargs:
        #     if 'url' in kwargs:
        #         self.url=kwargs['url']
        #     if url[:4]=='www.':
        #         self.url='http://'+self.url[4:]
        #     else:self.url=''
        #     if 'proxy' in kwargs:pr=kwargs['proxy']
        #     else:self.pr=''
        #     if 'user_pass' in kwargs:self.us_pss=kwargs['user_pass']
        #     else:self.us_pss=''
        #     if 'pdfdir' in kwargs:self.pdf_download_location=kwargs['pdfdir']
        #     else:self.pdf_download_location='PDF_Files'
        #     if 'water_pdfdir' in kwargs:self.wat_locatton=kwargs['water_pdfdir']
        #     else:self.wat_locatton='Watermarked_PDF_Files'
        #     if 'need_watermarker' in kwargs:self.need_watermarker=kwargs['need_watermarker']
        #     else:self.need_watermarker=False
    # self.core().update_urls_to_proxy_find_link(proxylist_file='configs//sites_proxy//proxylist.txt',url_file='configs//sites_proxy//urllist.txt')
    def update_urls_to_proxy_find_link(self,**kwargs):
        if kwargs['url_file']:url_file=kwargs['url_file']
        else:url_file='configs//sites_proxy//urllist.txt'
        if kwargs['proxylist_file']:proxylist_file=kwargs['proxylist_file']
        else:proxylist_file='configs//sites_proxy//proxylist.txt';
        self.proxy_checker3.update_urls_to_proxy(proxylist_file=proxylist_file,url_file=url_file)

    def valid_link(self,**kwargs):
        if kwargs:
            CurrentDir=os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
            if 'url' in kwargs:
                self.url=kwargs['url']
                if self.url[:4]=='www.':
                    self.url='http://'+self.url[4:]
            else:self.url=''
            if 'proxy' in kwargs:self.pr=kwargs['proxy']
            else:self.pr=''
            if 'user_pass' in kwargs:self.us_pss=kwargs['user_pass']
            else:self.us_pss=''
            if 'pdfdir' in kwargs:pdf_download_location=kwargs['pdfdir']
            else:pdf_download_location=CurrentDir+'/PDF_Files'
            if 'water_pdfdir' in kwargs:wat_locatton=kwargs['water_pdfdir']
            else:wat_locatton=CurrentDir+'/Watermarked_PDF_Files'
            if 'root' in kwargs:root=kwargs['root']
            else:root=CurrentDir
            if 'cookies' in kwargs:cookies=kwargs['cookies']
            else:cookies=''




        responce= self.Find_Link(self.url,pdfdir=pdf_download_location,water_pdfdir=wat_locatton,cookies=cookies).find_link(self.pr,self.us_pss)
        print '***************link which we found is********\n'
        print responce['link']
        print "proxy setting is :"+str(responce['proxy'])+'user pass is :'+str(responce['user_pass'])
        print '*************** end of finding links ********\n'
        # lin={
        #     'link':link,
        #     'proxy':proxy,
        #     'user_pass':user_pass,
        #     'cookies':cookies
        # }
        return responce

    def usr_tag(self,pip):
        z='--'
        try :
            # s=pip.split('SERVER_IP:'+z)[1].split(":")[0]
            proxy_info = {
                'upload_host' : pip.split('SUCCESS:'+z)[0].replace(' ',''),
                'METODE':pip.split('METODE:'+z)[1].split(z)[0],
                'user' : pip.split('USER:'+z)[1].split(":")[0],
                'pass' : pip.split('USER:'+z)[1].split(z)[0].split(":")[1],
                'APP_KEY' : pip.split('APP_KEY:'+z)[1].split(z)[0],
                'APP_SECRET' : pip.split('APP_SECRET:'+z)[1].split(z)[0],
                'APP_TOKEN' : pip.split('APP_TOKEN:'+z)[1].split(z)[0],
                'REMOTE_PATH' : pip.split('REMOTE_PATH:'+z)[1].split(z)[0],
                'SUCCESS' : pip.split('SUCCESS:'+z)[1].split(z)[0],
                'QUOTA' : pip.split('SUCCESS:'+z)[1].split(z)[0],
                'Success_try' : pip.split('Success_try:'+z)[1].split(z)[0],
                'Failed_try' : pip.split('Failed_try:'+z)[1].split(z)[0].replace('\n', '')
            }
            return  proxy_info
        except:
            return  ''


    def find_form(self,form_file):
        sa=open(form_file,'rb')
        listform=sa.readlines()
        # time.sleep(10)
        sa.close()
        k=-1
        form_data={}
        list_s={}
        # for line in listform:
        #     print '&&&&&&&&'
        #     print line+'\n'
        #     print '&&&&&&&&'
        for line in listform:
            if not re.findall('#',line[:3]) and line!='\n'and line!='\r\n':
                k=k+1
                form_data[k]=self.usr_tag(line.replace('\n',''))
                list_s[k]=line

        return form_data,list_s

        # self.url=url

    def upload_file(self, **kwargs):
        # global form,main_url
        if kwargs:
            CurrentDir=os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
            # if 'link' in kwargs:
            #     url=kwargs['link']
            if 'pdfdir' in kwargs:pdf_download_location= kwargs['pdfdir']
            else:pdf_download_location=''
            if 'water_pdfdir' in kwargs:wat_locatton= kwargs['water_pdfdir']
            else:wat_locatton=''
            if 'METODE' in kwargs:METODE= kwargs['METODE']
            else:METODE='FTP'
        upload_text_fle=CurrentDir+'/configs/upload/upload_setting.txt'
        form,list=self.find_form(upload_text_fle)
        for i in range(0,len(form)):
            form2=form[i]
            if METODE=='FTP' and form2['METODE']=='FTP':
                file=wat_locatton.split('/')[-1]
                remotepath=form2['REMOTE_PATH']+file
                m_ftp=import_mod(from_module='my_ftp',dir_location='/uploading/ftp')
                # from m_ftp import class_my_ftp
                public_url=m_ftp.class_my_ftp().my_ftplib(form2['upload_host'], form2['user'], form2['pass'], wat_locatton, remotepath)
                pattern=[];new_pattenr=[]
                if public_url!='None':
                    pattern=[list[i].split('SUCCESS:--')[0]+'SUCCESS:--'+form2['SUCCESS'],
                             list[i].split('Success_try:--')[0]+'Success_try:--'+form2['Success_try']
                    ];
                    new_pattenr=[list[i].split('SUCCESS:--')[0]+'SUCCESS:--'+'1',
                                 list[i].split('Success_try:--')[0]+'Success_try:--'+str(int(form2['Success_try'])+1)
                    ]

                    self.proxy_checker3.replace(upload_text_fle,pattern ,new_pattenr )
                    break

                if public_url=='None':
                    pattern=[list[i].split('SUCCESS:--')[0]+'SUCCESS:--'+form2['SUCCESS'],
                             list[i].split('Failed_try:--')[0]+'Failed_try:--'+form2['Failed_try']
                    ];
                    new_pattenr=[list[i].split('SUCCESS:--')[0]+'SUCCESS:--'+'0',
                                 list[i].split('Failed_try:--')[0]+'Failed_try:--'+str(int(form2['Failed_try'])+1)
                    ]
                    # pattern=list[i].split('SUCCESS:--')[0]+'SUCCESS:--'+form2['SUCCESS']
                    # new_pattenr=list[i].split('SUCCESS:--')[0]+'SUCCESS:--'+'0'
                    self.proxy_checker3.replace(upload_text_fle,pattern ,new_pattenr )
        return public_url

    # def main(self,url,pr='',us_pss='',pdf_download_location='PDF_Files',wat_locatton=''):
    def download_link(self,**kwargs):
        # global form,main_url
        if kwargs:
            CurrentDir=os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
            if 'link' in kwargs:
                url0=kwargs['link']
                if type(url0) is list:
                    url=url0[0]
                else:
                    if url0[:4]=='www.':
                        url='http://'+url0[4:]
                    else:
                        url=url0
            else:
                url=''
            if 'html' in kwargs:html=kwargs['html']
            else:html=''
            if 'proxy' in kwargs:pr=kwargs['proxy']
            else:pr=''
            if 'user_pass' in kwargs:us_pss=kwargs['user_pass']
            else:us_pss=''
            if 'pdfdir' in kwargs:pdf_download_location=kwargs['pdfdir']
            else:pdf_download_location=CurrentDir+'/PDF_Files'
            if 'water_pdfdir' in kwargs:wat_locatton=kwargs['water_pdfdir']
            else:wat_locatton=CurrentDir+'/Watermarked_PDF_Files'
            if 'root' in kwargs:root=kwargs['root']
            else:root=CurrentDir
            if 'need_watermarker' in kwargs:need_watermarker=kwargs['need_watermarker']
            else:need_watermarker=True
            if 'server' in kwargs:server_cdn=kwargs['server']
            else:server_cdn=''
            if 'cookies' in kwargs:cookies=kwargs['cookies']
            else:cookies=''
            if 'ftp_upload' in kwargs:ftp_upload=kwargs['ftp_upload']
            else:ftp_upload=''
            if 'log_out' in kwargs:
                log_out=kwargs['log_out']
                if log_out!='':
                    link={
                        'link':url,
                        'log_out':log_out
                    }
                else:
                    link=url
                    log_out=''
            else:
                link=url
                log_out=''
        try:

            url_watermark=kwargs['url_watermark']
        except:
            # url_watermark='Please insert Your url to add as watermark'
            url_watermark='www.free-peprs.elasa.ir'

        done=0
        try:
            main_url=kwargs['main_url']

        except:
            main_url=url

        # link,proxy,user_pass = Find_Link(url).find_link(pr,us_pss)
        # link,proxy,user_pass=self.valid_link()
        # link=url


        if link!=[] and link!=None:
            if main_url!=url:
                data_base_host = str(urlparse2(main_url).hostname)
                try:
                    ez_host = str(urlparse2(url).hostname)
                except:
                    ez_host = str(urlparse2(url[0]).hostname)
                try:
                    base_url='http://'+data_base_host
                    file_name_link=base_url+url.split(ez_host)[1]
                except:
                    base_url='http://'+data_base_host
                    try:
                        file_name_link=base_url+url[0].split(ez_host)[1]
                    except:
                        file_name_link=url
            else:
                file_name_link=url

            os.chdir(CurrentDir)
            # file_name = self.Find_Link(file_name_link).find_name(pdf_download_location,wat_locatton)
            # file_name.url_watermark=url_watermark

            # [html,proxy,user_pass,cookies]=self.Find_Link(link,pdfdir=pdf_download_location,water_pdfdir=wat_locatton,cookies=cookies).dowload_basePr_userpass(pr,us_pss,cookies)
            if (not (html.endswith('.pdf'))) and (html[:4]!='%PDF' or html[-7:]!='%%EOF' )  :
                [html,proxy,user_pass,cookies]=self.Find_Link(main_url,pdfdir=pdf_download_location,water_pdfdir=wat_locatton,cookies=cookies).dowload_basePr_userpass(pr,us_pss,cookies,url=link)
            else:
                proxy=pr;user_pass=us_pss;
            try:
                os.path.isfile(html)
                file_is=1
            except:
                file_is=0

            if (html!=[] and html[:4]=='%PDF')or file_is==1 :
                PDF_File=import_mod(from_module='save_source',from_module2='PDF_File')
                if  not (html.endswith('.pdf')):

                    # from save_source import PDF_File
                    file_name = self.Find_Link(file_name_link).find_name(pdf_download_location,wat_locatton)
                    # file_name['url_watermark']=url_watermark
                    file_name.url_watermark=url_watermark
                else:
                    os.remove(cookies)
                    file_name = self.Find_Link(file_name_link).find_name(pdf_download_location,wat_locatton)
                    file_name.filename=html.split('/')[-1]
                    # file_name.pdf_Folder_filename=file_name.pdf_Folder_filename.split('/')[-1]
                    file_name.url_watermark=url_watermark
                # file_name = PDF_File(link,pdf_download_location,wat_locatton).filename(link)
                # file_name = self.Find_Link(link).find_name(pdf_download_location,wat_locatton)

                if not need_watermarker==False:#need wtaremarker is ok
                    os.chdir(CurrentDir)
                    if not os.path.isdir(pdf_download_location):
                        os.mkdir(pdf_download_location)
                    if not os.path.isdir(wat_locatton):
                        os.mkdir(wat_locatton)
                    pdf_dw_dir, pdf_dw_Wr_dir = PDF_File(url,pdf_download_location,wat_locatton).finall_file_saving(html, file_name,pdf_download_location,no_watermarker=0)
                    # photo=PDF_File(url,pdf_download_location,wat_locatton).pdf_to_image(pdf=pdf_dw_dir,pages=0)
                    pdf_size=size(os.path.getsize(pdf_dw_dir))

                    pdf_dw_li =self.path2url(file_name.pdf_Folder_filename,server_cdn,pdf_download_location,root)
                    if file_is==1 and html.endswith('.pdf'):
                        wt_pdf_size=size(os.path.getsize(pdf_dw_Wr_dir))
                        pdf_dw_Wr_li = self.path2url(file_name.W_pdf_Folder_filename,server_cdn,wat_locatton,root)
                    elif file_is==1 and not html.endswith('.pdf'):
                        wt_pdf_size=pdf_size
                        pdf_dw_Wr_li=pdf_dw_li

                    else:
                        wt_pdf_size=size(os.path.getsize(pdf_dw_Wr_dir))
                        pdf_dw_Wr_li = self.path2url(file_name.W_pdf_Folder_filename,server_cdn,wat_locatton,root)

                    os.remove(cookies)
                    print "fetching main paper link url ...\n\t%s" % pdf_dw_li[:]
                    print "fetching waterarker paper link url ...\n\t%s" % pdf_dw_Wr_li
                else:
                    if not os.path.isdir(pdf_download_location):
                        os.mkdir(pdf_download_location)

                    pdf_dw_dir, pdf_dw_Wr_dir = PDF_File(url,pdf_download_location,wat_locatton).finall_file_saving(html, file_name,pdf_download_location,no_watermarker=1)
                    pdf_size=size(os.path.getsize(pdf_dw_dir))
                    # pdf_size=len(html)/1024 #in kbit
                    wt_pdf_size=''
                    pdf_dw_li =self.path2url(file_name.pdf_Folder_filename,server_cdn,pdf_download_location,root)
                    print "fetching main paper link url ...\n\t%s" % pdf_dw_li[:]
                    pdf_dw_Wr_li="No watter marker requested my be becuase of big size or lack of time"
                    print "fetching waterarker paper link url ...\n\t%s" % pdf_dw_Wr_li
                done=1
                if ftp_upload=='1':
                    public_url='None'

                    if  need_watermarker==True:#need wtaremarker is ok
                        public_url=self.upload_file(water_pdfdir=pdf_dw_Wr_dir,METODE='FTP')
                    else:
                        public_url=self.upload_file(water_pdfdir=pdf_dw_li,METODE='FTP')
                else:
                    public_url='None'
                if public_url!='None':
                    # try:
                    #     file=open(pdf_dw_dir);
                    #     file.close()
                    #     file=open(pdf_dw_Wr_dir);
                    #     file.close()
                    # except:
                    #     print 'pdfs are closed and reasy to removed from loal host!'
                    # os.close(pdf_dw_dir);os.close(pdf_dw_Wr_dir);
                    os.remove(pdf_dw_dir);os.remove(pdf_dw_Wr_dir);
                    pdf_dw_Wr_li=public_url;pdf_dw_li=public_url;
                else:
                    public_url=pdf_dw_Wr_li;
                address={
                    'url':str(url),
                    'pdf_name':file_name.filename,
                    'W_pdf_name':file_name.filename,
                    'W_pdf_local':wat_locatton,
                    'pdf_size':pdf_size,
                    'wt_pdf_size':wt_pdf_size,
                    'pdf_dir':pdf_dw_dir,
                    'wt_pdf_dir':pdf_dw_Wr_dir,
                    'pdf_dw_li':pdf_dw_li,
                    "pdf_dw_Wr_li":pdf_dw_Wr_li,
                    'public_url':public_url,
                    'proxy_worked':proxy,
                    'user_pass_worked':user_pass}
                return address

            # elif os.path.isfile(html):

            elif html[:4]!="%PDF" and html!=[]:

                print 'file is not in PDF Format do you want to make a save it as html file'
                print 'format is '+html[:4]
                print '*************html is :***********\n\n'
                print html
                print '************* end of html :***********\n\n'
                print '\n file link which found is :\n'+link+'\nbut file can not be downloaded '
            else:
                print 'file link which found is :\n';#print str(link['link']);
                print 'but file can not be downloaded '

        if done==0:
            print 'we are unable to download from this address because can not find proper link '
            address={
                'url':str(url),
                'pdf_dir':'',
                'pdf_size':'',
                'wt_pdf_size':'',
                'wt_pdf_dir':'',
                'pdf_dw_li':'',
                "pdf_dw_Wr_li":'',
                'public_url':'',
                'proxy_worked':'',
                'user_pass_worked':''}
            return address


    def main(self,**kwargs):

        # address =core().main(url=options.url,proxy=options.proxy,user_pass=options.user_name,pdfdir=options.pdfdir,water_pdfdir=options.water_pdfdir)
        if kwargs:
            CurrentDir=os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
            if 'url' in kwargs:
                url=kwargs['url']
                if url[:4]=='www.':
                    url='http://'+url[4:]

            else:url=''
            if 'root' in kwargs:root=kwargs['root']
            else:root=CurrentDir
            if 'proxy' in kwargs:pr=kwargs['proxy']
            else:pr=''
            if 'user_pass' in kwargs:us_pss=kwargs['user_pass']
            else:us_pss=''
            if 'pdfdir' in kwargs:pdf_download_location=kwargs['pdfdir']
            else:pdf_download_location=root+'/PDF_Files'
            if 'water_pdfdir' in kwargs:wat_locatton=kwargs['water_pdfdir']
            else:wat_locatton=root+'/Watermarked_PDF_Files'
            if 'need_watermarker' in kwargs:need_watermarker=kwargs['need_watermarker']
            else:need_watermarker=False


            valid_link = self.valid_link(url=url,proxy=pr,user_pass=us_pss)
            link=valid_link['link']; proxy=valid_link['proxy']; user_pass=valid_link['user_pass'];log_out=valid_link['log_out']
            try:
                cookies=valid_link['cookies']
            except:
                cookies=''
            try:
                self.form=valid_link['form']
            except:
                self.form=''

            main_url=url

            # global form,main_url
            address=self.download_link(main_url=main_url,link=link,pdfdir=pdf_download_location,
                                       proxy=proxy,user_pass=user_pass,water_pdfdir=wat_locatton,
                                       need_watermarker=need_watermarker,cookies=cookies,root=root,log_out=log_out)
            # link,proxy,user_pass,cookies=self.valid_link(url=url,proxy=pr,user_pass=us_pss)
            print 'link we found is \n'+str(link)

            if 'root' in kwargs:root=kwargs['root']
            else:root=CurrentDir
            if 'server' in kwargs:server_cdn=kwargs['server']
            else:server_cdn=''
            # address=self.download_link(link=link,pdfdir=pdf_download_location,
            #                            proxy=pr,user_pass=us_pss,water_pdfdir=wat_locatton,
            #                            need_watermarker=need_watermarker,cookies=cookies)
            print 'address file is \n'
            print address
            return address




    def path2url(self, path,server_cdn,pdf_download_location,root):
        if server_cdn=='':
            try:
                host=os.environ('OPENSHIFT_GEAR_DNS')
            except:pass
            host=socket.gethostbyname(socket.gethostname())+'/'# get IP
        else:
            host=server_cdn # get host name
            # host=os.environ['OPENSHIFT_GEAR_DNS']
        myhost='http://'+host.replace('http://','').replace('/','')


        # CurrentDir=os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
        path2 = path.replace(root, '').replace('%20',' ')

        # rp=os.getcwd().replace('\\','/').split('www')[0]+'www/'
        # path2 = path.replace(rp, '')
        # path2 = path.replace(os.getcwd().replace('\\','/'), '')
        # print urllib.pathname2url(path2)
        link = myhost + urllib.pathname2url(path2)
        # return link.replace('','%20')
        # return unicode(link)
        return link

        # return urlparse.urljoin('file:', urllib.pathname2url(path))



if __name__ == '__main__':
    # import twill
    # t_com = twill.commands


    # print("Content-type: text/html")
    core().update_urls_to_proxy_find_link(proxylist_file='configs//proxy_scraper//scraped_list.txt',url_file='configs//sites_proxy//urllist.txt')

    CurrentDir=os.path.dirname(os.path.realpath(__file__)).replace('\\','/')

    if not os.path.isdir(CurrentDir+'/PDF_Files'):os.mkdir(CurrentDir+'/PDF_Files')
    if not os.path.isdir(CurrentDir+'/Watermarked_PDF_Files'):os.mkdir(CurrentDir+'/Watermarked_PDF_Files')

    page = """
    <html>
    <head>
    <title>Hello World Page!</title>
    </head>
    <body>
    """
    # print (page)
    #HOW TO USE:
    url = "http://127.0.0.1/1752-153X-2-5%20-%20Copy.pdf"
    url = "http://127.0.0.1/1752-153X-2-5.pdf"

    # url='http://127.0.0.1/Introduction to Tornado.pdf'
    url='http://ieeexplore.ieee.org/xpl/articleDetails.jsp?tp=&arnumber=6180383&queryText%3Dpower' #91 KB
    url= "http://onlinelibrary.wiley.com/doi/10.1111/ncmr.12022/abstract" #127 KB
    url = "http://127.0.0.1/"
    # url='http://dl.acm.org/citation.cfm?id=1165573.1165663&coll=DL&dl=GUIDE&CFID=548314837&CFTOKEN=29773674'
    # url='http://www.sciencedirect.com/science/article/pii/S0142061514004'
    # $OPENSHIFT_HOMEDIR/app-root/runtime/srv/python/bin/python main_core.py --url "http://ieeexplore.ieee.org/xpl/articleDetails.jsp?tp=&arnumber=6180383&queryText%3Dpower"
    # $OPENSHIFT_HOMEDIR/app-root/runtime/srv/python/bin/python main_core.py --url "http://onlinelibrary.wiley.com/doi/10.1111/ncmr.12022/abstract"
    # $OPENSHIFT_HOMEDIR/app-root/runtime/srv/python/bin/python main_core.py --root  "${OPENSHIFT_HOMEDIR}app-root/runtime/repo/www" --wtdir '/static' -n 'True' --url  'http://www.sciencedirect.com/science/article/pii/S0957417414005284'


    # $OPENSHIFT_HOMEDIR/app-root/runtime/srv/python/bin/python main_core.py --root  "${OPENSHIFT_HOMEDIR}app-root/runtime/repo/www" --wtdir '/static' --url "http://pr4ss.tk/ss_proxy/host-manager-phps.zip"

# $OPENSHIFT_HOMEDIR/app-root/runtime/srv/python/bin/python main_core.py --root  "${OPENSHIFT_HOMEDIR}app-root/runtime/repo/www" --wtdir '/static' -n 'True' --url "http://onlinelibrary.wiley.com/doi/10.1111/ncmr.12022/abstract"

# $OPENSHIFT_HOMEDIR/app-root/runtime/srv/python/bin/python $OPENSHIFT_HOMEDIR/app-root/runtime/repo/tornado/main_core.py --root  "${OPENSHIFT_HOMEDIR}app-root/runtime/repo/www" --wtdir '/static' -n 'True' --url "http://ieeexplore.ieee.org/xpl/articleDetails.jsp?tp=&arnumber=6180383&queryText%3Dpower"
# $OPENSHIFT_HOMEDIR/app-root/runtime/srv/python/bin/python $OPENSHIFT_HOMEDIR/app-root/runtime/repo/tornado/main_core.py --root  "${OPENSHIFT_HOMEDIR}app-root/runtime/repo/www" --wtdir '/static' -n 'True' --url  'http://www.sciencedirect.com/science/article/pii/S0957417414005284'
# $OPENSHIFT_HOMEDIR/app-root/runtime/srv/python/bin/python $OPENSHIFT_HOMEDIR/app-root/runtime/repo/tornado/main_core.py --root  "${OPENSHIFT_HOMEDIR}app-root/runtime/repo/www" --wtdir '/static' -n 'True' --url  'http://www.sciencedirect.com/science/article/pii/S0957417414005284' --proxy '150.188.84.18:8080'
# $OPENSHIFT_HOMEDIR/app-root/runtime/srv/python/bin/python $OPENSHIFT_HOMEDIR/app-root/runtime/repo/tornado/main_core.py --url
    # $OPENSHIFT_HOMEDIR/app-root/runtime/srv/python/bin/python $OPENSHIFT_HOMEDIR/app-root/runtime/repo/tornado/main_core.py --url "http://ieeexplore.ieee.org/xpl/articleDetails.jsp?tp=&arnumber=6180383&queryText%3Dpower" --proxy '150.188.84.18:8080'


    # $OPENSHIFT_HOMEDIR/app-root/runtime/srv/python/bin/python $OPENSHIFT_HOMEDIR/app-root/runtime/repo/tornado/main_core.py --url  "http://diy4ng4django4php-freepaper.rhcloud.com/PDF_Files2/" --proxy 'None:None'
    # $OPENSHIFT_HOMEDIR/app-root/runtime/srv/python/bin/python $OPENSHIFT_HOMEDIR/app-root/runtime/repo/tornado/main_core.py --url --proxy "143.107.192.112:21320"
    #python main_core.py --url "http://127.0.0.1/"
    # ad=os.system('python main_core.py --url'+url+'--pdfdir PDF_Files --wtdir Watermarked_PDF_Files')
    # address=core().main(url=url,need_watermarker=True)
    # print address
    pag2="""
    <p>Hello World</p>
    <p>{{address}}</P>
    </body>
    </html>
    """
    # print pag2
    # address =core().main(url=url,proxy=options.proxy,user_pass=options.user_name,pdfdir=options.pdfdir,water_pdfdir=options.water_pdfdir)

    from optparse import OptionParser
    parser = OptionParser(description=__doc__)
    CurrentDir = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
    help1='Address url file name to be downloaded like:"www.google.com"\n'+\
          "Please make attention 'www.google.com' is risky use  only with"+'"blabla"'
    parser.add_option('-u','--url',type='string', dest='url', help=help1)
    parser.add_option('-p','--proxy', dest='proxy', help=' proxy setting for url file name to be download like:121.121.21.21:90')
    parser.add_option('-s','--user', dest='user_name', help='user & password of proxy setting')
    # parser.add_option('-i', dest='input_fname', help='file name to be watermarked (pdf)')
    parser.add_option('-n', dest='no_watermarker', help='if you dont need watermarker please insert False defualt is True',default=True)
    parser.add_option('-r', '--root', dest='root', help='Root folder  for putting pdf files ', default=CurrentDir )
    parser.add_option('-f','--pdfdir', dest='pdfdir', help='make pdf files in this directory default is PDF_Files',default='/PDF_Files')
    parser.add_option('-w','--wtdir', dest='water_pdfdir', help='make  watermarker pdf files in this directory is Watermarked_PDF_Files',default='/static')
    # parser.add_option('-o', dest='outdir', help='outputdir used with option -d', default='tmp')
    options, args = parser.parse_args()
    # options.root='${OPENSHIFT_HOMEDIR}/app-root/runtime/repo/www'
    # options.root='C:/nginx/html'
    # # # # # options.ip = '127.0.0.1'
    # # # # # # options.port = '15001'
    # options.proxy='161.6.45.63:21320'
    # options.url='http://pr4ss.tk/ss_proxy/host-manager-phps.zip'
    # options.url='http://dl.acm.org/citation.cfm?id=1165573.1165663&coll=DL&dl=ACM&CFID=417871757&CFTOKEN=21919719'#75KB
    # options.url='http://www.springer.com/engineering/energy+technology/journal/11708'
    # options.url='http://link.springer.com/article/10.1186/s13058-014-0417-7'
    # options.url='http://ieeexplore.ieee.org/xpl/articleDetails.jsp?tp=&arnumber=6180383&queryText%3Dpower' #91 KB
    # options.url='http://www.scopus.com/record/display.url?eid=2-s2.0-84906221694&origin=resultslist&sort=plf-f&src=s&st1=power&sid=029E1E633018D5F5E9347C0252726E06.53bsOu7mi7A1NSY7fPJf1g%3a30&sot=b&sdt=b&sl=20&s=TITLE-ABS-KEY%28power%29&relpos=1&relpos=1&citeCnt=0&searchTerm=TITLE-ABS-KEY%28power%29#'
    # options.url='http://site.ebrary.com/lib/scitechjo/docDetail.action?docID=10256206&p00=eball'
    # options.url='http://onlinelibrary.wiley.com/doi/10.1111/ncmr.12022/abstract'
    # options.url='http://www.sciencedirect.com/science/article/pii/S0142061514004463'
    options.url='http://www.sciencedirect.com/science/article/pii/S105905601400029X'# 274 KB
    # options.url="http://127.0.0.1/new"
    # options.url='http://link.springer.com/chapter/10.1007/978-3-211-89836-9_1089'
    # options.url='http://www.sciencedirect.com/science/article/pii/S0957417414005284'
    # # os.environ['OPENSHIFT_HOMEDIR']='C:/nginx/html/'
    if options.url:
        f=options.root
        print 'options.root is'+options.root
        if re.findall('{',f):
            o=options.root.split('{')[1].split('}')[0]
            # options.root=os.environ[o]+options.root.split('}')[1]
            s=options.root.split('}')[1]
            print s
            ss2=os.environ[o][:-1]+s
            print 'ss2 is '+ss2
            # ss2=ss.split('//')[0]+'/'+ss.split('//')[1]
            options.root=ss2
        else:
            if re.findall('//',f):
                f=f.replace('//','/')
            ss2=f
        print '*********** *********************************************************'
        print '*********** *********************************************************'
        print '*********** *********************************************************'
        print '*********** *********************************************************'
        print '*********** option.root is :\n'
        print options.root+'\n'
        print '*********** *********************************************************'
        print '*********** *********************************************************'
        options.pdfdir=options.root+options.pdfdir;options.water_pdfdir=options.root+options.water_pdfdir

        if options.proxy and not options.user_name:
            address =core().main(url=options.url,proxy=options.proxy,user_pass='',root=options.root,
                                 need_watermarker=options.no_watermarker,pdfdir=options.pdfdir,water_pdfdir=options.water_pdfdir)

            # address =core().main(options.url,options.proxy,'',options.pdfdir,options.water_pdfdir)
        elif options.proxy and  options.user_name:
            address =core().main(url=options.url,proxy=options.proxy,user_pass=options.user_name,root=options.root,
                                 need_watermarker=options.no_watermarker,pdfdir=options.pdfdir,water_pdfdir=options.water_pdfdir)
            # address = core().main(options.url,options.proxy,options.user_name,options.pdfdir,options.water_pdfdir)
        else:
            print type(options.url)
            print options.url


            address =core().main(url=options.url,proxy='',user_pass='',root=options.root,
                                 need_watermarker=options.no_watermarker,pdfdir=options.pdfdir,water_pdfdir=options.water_pdfdir)#good work
            # address = core().main(options.url,proxy='',user_pass='',options.pdfdir,options.water_pdfdir)
            # address = core().main(options.url,'','',options.pdfdir,options.water_pdfdir)

    else:
        parser.print_help()
        pass
    print '</pre>'
