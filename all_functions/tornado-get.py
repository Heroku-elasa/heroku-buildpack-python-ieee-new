#!"E:/Program Files win 7 2nd/python27/python.exe"
#!/usr/bin/python
__author__ = 's'
import tornado.httpserver, tornado.websocket
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
# from tornado.httpclient import
import os, re, sys
import socket, time,urllib
# import string
# from time import sleep
# from datetime import datetime
# import hashlib
import json
import logging
from urlparse import urlparse as urlparse2
from hurry.filesize import size
import logging
#from mongolog.handlers import MongoHandler
# import twill


from tornado.options import define, options
print "Content-type: text/html\n"
print ''
print '<pre>'

define("port", default=8001, help="run on the given port", type=int)

cl = []

def path2url(self, path):
    host = self.request.headers['Host']
    try:
        host=os.environ('OPENSHIFT_GEAR_DNS')
    except:
        # host=socket.gethostbyname(socket.gethostname())# get IP
        # host=socket.gethostname() # get host name
        host = self.request.headers['Host']

    myhost='http://'+host+''


    CurrentDir=os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
    path2 = path.replace(CurrentDir, '')

    # rp=os.getcwd().replace('\\','/').split('www')[0]+'www/'
    # path2 = path.replace(rp, '')
    # path2 = path.replace(os.getcwd().replace('\\','/'), '')
    # print urllib.pathname2url(path2)
    link = myhost + urllib.pathname2url(path2)
    # return link.replace('','%20')
    # return unicode(link)
    return link

    # return urlparse.urljoin('file:', urllib.pathname2url(path))

def url2Path(**kwargs):
    # myhost = "http://127.0.0.1/"
    url = kwargs['url']
    site = urlparse2(url).hostname
    port= urlparse2(url).port
    myhost = "http://" + site + ":"+str(port)+'/'
    try:
        kwargs['pdf_dir']
        pdf_dir = kwargs['pdf_dir']
    except:
        pdf_dir = url.split(myhost)[1]
    ph = pdf_dir.split('/')[0]
    f_ph = pdf_dir.split('/')[-1]
    rp = os.getcwd().replace('\\', '/').replace('%20', ' ').split(ph)[0]
    path = rp + '/'+pdf_dir.split(f_ph)[0].replace('%20', ' ') + f_ph
    return path


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


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
        self.render("index.html")

class AddHandler(tornado.web.RequestHandler):
    def get(self):
        CurrentDir = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
        htmls = CurrentDir.replace('\\', '/') + '/htmls/'
        self.render(htmls+"done - add.html")
    def post(self):
        CurrentDir = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
        htmls = CurrentDir.replace('\\', '/') + '/htmls/'
        try:
            url = self.get_argument('url_to_download')
        except:
            url=''
        # zz=pp=uu=0
        # if self.get_argument('ezproxy')!='':
        #     zz=1
        # if self.get_argument('proxy')!='':
        #     pp=1
        # if self.get_argument('upload')!='':
        #     uu=1
        # try:ezz=self.get_argument('ezproxy');    ezz2=1
        # except: ezz2=0
        # try:ezz=self.get_argument('proxy'); prz2=1
        # except: prz2=0
        if url!='' or self.get_argument('upload')!='':
            # poxy_checker_replcae = import_mod(from_module='proxy_checker3_all_function', from_module2='replace')

            url = str(self.get_argument('url_to_download'))
            if url[:3]=='www':url='http://'+url
            if self.get_argument('ezproxy')!='':
                ez=str(self.get_argument('ezproxy'))
                ez2=ez.split('USER:')[0]
                print 'url is '+url
                site = urlparse2(url).hostname
                fo=os.getcwd()
                CurrentDir=os.path.dirname(os.path.realpath(__file__))
                s=CurrentDir.replace('\\','/')+'/configs/Links_site/'
                print site

                # s2=os.getcwd()+'\\configs\\Links_site\\'
                self.file_exist=0

                if os.path.isfile(s+site.replace('.','_')+'.py'):
                    ez_file=CurrentDir.replace('\\','/')+'/configs/sites_proxy/'+site+'/site_list_form.txt'

                    f=open(ez_file,'r')
                    list=f.readlines()
                    f.close()

                    exist=0
                    for ll in list:
                        if re.findall(ez2,ll):
                            exist=1
                            break
                    if exist==0:
                        list.append(ez+'\n')
                        file_handle = open(ez_file, 'w')
                        file_handle.writelines(list)
                        file_handle.close()
                    self.render(htmls+'done - add.html',link=url,file=list,main_url=url)
                else:
                    self.render(htmls+"done - add.html")
                    print "@@@@@@@@@@@@@@ module "+CurrentDir.replace('\\','/')+'/configs/Links_site/'+site.replace('.','_')+'.py'+'\n Not found: @@@@@@@@@@@@@@\n\n'

            if self.get_argument('proxy')!='':
                pr=str(self.get_argument('proxy'))
                pr2=pr.split('For Site:')[0]
                print 'url is '+url
                site = urlparse2(url).hostname
                # scheme, netloc, path, params, query, fragment=urlparse2(url).hostname
                fo=os.getcwd()
                CurrentDir=os.path.dirname(os.path.realpath(__file__))
                s=CurrentDir.replace('\\','/')+'/configs/Links_site/'
                print site

                # s2=os.getcwd()+'\\configs\\Links_site\\'
                self.file_exist=0

                if os.path.isfile(s+site.replace('.','_')+'.py'):
                    ez_file=CurrentDir.replace('\\','/')+'/configs/sites_proxy/'+site+'/'+site+'.txt'

                    f=open(ez_file,'r')
                    list=f.readlines()
                    f.close()
                    # s=ez_file;s.replace('/','\\')
                    # f=open(s,'r')
                    # list2=f.readlines()
                    # f.close()

                    exist=0;num=-1
                    pr2_n=pr2.replace("#",'');
                    # pr2_n[:3]=pr2_n[:3].replace("-",'')
                    if '-' in pr2_n[:3]:
                        pr2_n=pr2_n.split('-')[1]
                        # print pr2_n
                    for ll in list:
                        num=num+1
                        if re.findall(pr2_n,ll):
                            if   re.findall("-",pr2[:7]):  # enable the old proxy
                                del list[num]
                                exist=-2;break
                            if  re.findall("#",ll) and (not re.findall("#",pr2)):  # enable the old proxy
                                ll2=ll;
                                # ll2.replace("#"+pr2,pr2_n)
                                # ll2.replace("#","")
                                ll3=ll2.split('#')[1]
                                # list.replace(ll,ll2)
                                list2=[ll3];list2[1:]=list;
                                del list2[num+1]
                                list=list2
                                # list[num]=ll3
                                exist=2;break
                            elif  (not re.findall("#",ll)) and ( re.findall("#",pr2)):# unable the old proxy
                                ll2=ll;ll2="#"+ll2
                                # list.replace(ll,ll2)
                                list2=[ll2];list2[1:]=list;
                                del list2[num+1]
                                list=list2
                                exist=2
                                break
                            else:
                                exist=1
                                break

                    if exist==0:
                        # list[len(list)+1]=pr

                        # list.append(pr+'\n');list2=list
                        f=open(ez_file,'r')
                        list=f.readlines()
                        f.close()
                        list2=[];
                        list2.append(pr+'\n')
                        list2[1:]=list
                        list=list2

                        file_handle = open(ez_file, 'w')
                        file_handle.writelines(list2)
                        file_handle.close()
                    if exist==2 or exist==-2 :
                        # list[len(list)+1]=pr
                        # list.append(pr+'\n')
                        file_handle = open(ez_file, 'w')
                        file_handle.writelines(list)
                        file_handle.close()
                    self.render(htmls+'done - add.html',link=url,file=list,main_url=url)



            if self.get_argument('upload')!='':
                pr=str(self.get_argument('upload'))
                pr2=pr.split('SUCCESS::')[0].replace(' ','')
                print 'url is '+url
                site = urlparse2(url).hostname
                fo=os.getcwd()
                CurrentDir=os.path.dirname(os.path.realpath(__file__))
                # s=CurrentDir.replace('\\','/')+'/configs/upload/'
                # print site
                #
                # # s2=os.getcwd()+'\\configs\\Links_site\\'
                # self.file_exist=0


                ez_file=CurrentDir.replace('\\','/')+'/configs/upload/upload_setting.txt'

                f=open(ez_file,'r')
                list=f.readlines()
                f.close()

                exist=0
                for ll in list:
                        if re.findall(pr2,ll):
                            exist=1
                            break
                if exist==0:
                        # list[len(list)+1]=pr
                        # list.insert('0',pr+'\n')
                        list.append(pr+'\n')
                        s_l=len(list)-1
                        s0=list[1];sn=list[s_l];
                        list[s_l]=s0;list[1]=sn;
                        file_handle = open(ez_file, 'w')
                        file_handle.writelines(list)
                        file_handle.close()
                self.render(htmls+'done - add.html',link=url,file=list,main_url=url)

            if self.get_argument('ezproxy')=='' and self.get_argument('proxy')=='' \
                and self.get_argument('upload')=='':


                # pr=str(self.get_argument('url_to_download'))
                #
                site = urlparse2(url).hostname
                # scheme, netloc, path, params, query, fragment=urlparse2(url).hostname
                fo=os.getcwd()
                CurrentDir=os.path.dirname(os.path.realpath(__file__))
                s=CurrentDir.replace('\\','/')+'/configs/Links_site/'
                # print site

                # s2=os.getcwd()+'\\configs\\Links_site\\'
                self.file_exist=0

                if os.path.isfile(s+site.replace('.','_')+'.py'):
                    ez_file=CurrentDir.replace('\\','/')+'/configs/sites_proxy/'+site+'/'+site+'.txt'

                    f=open(ez_file,'r')
                    list=f.readlines()
                    f.close()

                    self.render(htmls+'done - add.html',link=url,file=list,main_url=url)


                self.render(htmls+"done - add.html")
                print "@@@@@@@@@@@@@@ module "+CurrentDir.replace('\\','/')+'/configs/Links_site/'+site.replace('.','_')+'.py'+'\n Not found: @@@@@@@@@@@@@@\n\n'


        else:
            self.render(htmls+"done - add.html")
        # try:
        #     self.finish()
        # except:
        #     pass
        # password = self.get_argument('password')
        # if email_address == '':
        #     login_response = "{'error': true, 'msg': 'Please enter your email address.'}"
        # elif password == '':
        #     login_response = "{'error': true, 'msg': 'Please enter your password.'}"
        # else:
        #     login_response = "{'error': true, 'msg': 'Thank You.'}"
        #     self.response.headers['Content-Type'] = "application/json"
        #     self.response.out.write(json.dumps(login_response))

class LoginHandler0(tornado.web.RequestHandler):
    def get(self):
        email_address = self.get_argument('email')
        password = self.get_argument('password')
        if email_address == '':
            login_response = "{'error': true, 'msg': 'Please enter your email address.'}"
        elif password == '':
            login_response = "{'error': true, 'msg': 'Please enter your password.'}"
        else:
            login_response = "{'error': true, 'msg': 'Thank You.'}"
            self.response.headers['Content-Type'] = "application/json"
            self.response.out.write(json.dumps(login_response))


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

    def post(self):
        email_address = self.get_argument('email', '')
        password = self.get_argument('password', '')
        url_to_download = self.get_login_url()

        if not email_address:
            login_response = {
                'error': True,
                'msg': 'Please enter your email address.'
            }
        elif not password:
            login_response = {
                'error': True,
                'msg': 'Please enter your password.'
            }
        else:
            login_response = {
                'error': True,
                'msg': 'Thank You.'
            }
        if url_to_download:
            CurrentDir = os.path.dirname(os.path.realpath(__file__))
            os.chdir(CurrentDir)
            import ieeexplore_ieee_org_good

            os.chdir(CurrentDir)
            login_response = {
                "error": True,
                # 'msg':main().todo_url(url_to_download)
                'msg': url_to_download
            }


class SocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        s = logging.info('Client IP:' + self.request.remote_ip)
        if self not in cl:
            cl.append(self)

    def on_close(self):
        if self in cl:
            cl.remove(self)


class ApiHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, *args):
        self.finish()
        id = self.get_argument("id")
        value = self.get_argument("value")
        data = {"id": id, "value": value}
        data = json.dumps(data)
        for c in cl:
            c.write_message(data)

        @tornado.web.asynchronous
        def post(self):
            pass

# ----from 'introduction to tornado ebook'-----
class ReverseHandler(tornado.web.RequestHandler):
    def get(self, input):
        self.write(input[::-1])


class download(tornado.web.UIModule):
    def render(self, url_to_download):
        CurrentDir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(CurrentDir)
        client = tornado.httpclient.AsyncHTTPClient()
        from ieeexplore_ieee_org_good import ieee_main

        os.chdir(CurrentDir)
        if (re.findall('www', url_to_download) or re.findall('http://', url_to_download)) \
            or re.findall('https://', url_to_download):
            [pdf_path, war_path] = ((ieee_main().todo_url(str(url_to_download))))
        return pdf_path, war_path


class IndexHandler(tornado.web.RequestHandler):

    def write_error(self, status_code, **kwargs):
        self.write("Please Try in another time Error code is :" % status_code)

    # def head(self, frob_id):
    #     frob = retrieve_from_db(frob_id)
    #     if frob is not None:
    #         self.set_status(200)
    #     else:
    #         self.set_status(404)

    # @tornado.web.asynchronous
    # @tornado.gen.engine
    def post(self):
    # client = Client("vvc2y7nAjkx6fUaJqQ94FT7nAdZCWQrA", "CJYFj8Sy3WwDL2sFfQXJnDdyXh7BqDU2")
    # client.places.search(41.773847,-72.672477, callback=self.on_search_complete)
    # client = tornado.httpclient.AsyncHTTPClient()
    #
    # # client.fetch("http://search.twitter.com/search.json?" + \
    # #              urllib.urlencode({"q": query, "result_type": "recent", "rpp": 100}),
    # #              callback=self.on_response)
    # url_to_download = str(self.get_argument('url_to_download').replace(' ','%20'))
    # url="http://"+self.request.headers['Host']+'/index/?url='+url_to_download
    # self.download()
    # address = yield tornado.gen.Task(client.fetch(url))
    # url=address['url']
    # war_path=address['pdf_dw_Wr_li']
    # pdf_path=address['pdf_dw_li']
    # time1=str(round( time.time() - time_diff, 2))
    # self.render('done.html',pdf_path=pdf_path, url=url,war_path=war_path ,email=address['email'],ip=ip,time=str(round( time.time() - time_diff, 2)))
    # # client.fetch(url)
    # self.finish()

    # query =''

    # result =yield tornado.gen.Task(self.my_function())
        try:
            url_to_download = str(self.get_argument('url_to_download').replace(' ', '%20'))
        except:
            url_to_download = ''
        try:
            url_watermark = str(self.get_argument('url_watermark'))
        except:
            url_watermark='Please insert Your url to add as watermark'
        try:
            email = str(self.get_argument('email'))
        except:
            email = ''

        try:
            ftp_local_upload = str(self.get_argument('ftp_local_upload'))
        except:
            ftp_local_upload = ''
        try:
            ip_method = str(self.get_argument('ip_method'))
        except:
            ip_method = ''

        print '**********************we get this url to download:\n'
        print

        # result = self.download(url_to_download)
        details={
            'url_to_download':url_to_download,
            'url_watermark':url_watermark,
            'email':email,
            'ftp_local_upload':ftp_local_upload,
            'ip_method':ip_method
        }
        result = tornado.gen.Task(self.download(details))
        # result=self.async_path2url((url_to_download))
        print 'try'

        # os.environ['SHELL']
        print 'sleeping'
        # result =yield tornado.gen.Task(self.my_function())

        print 'result is';print result

        # self.write( 'result is', result)
        try:
            self.finish()
        except:pass

    def my_function(self, callback):
        print 'do some work'
        # Note: this line will block!
        time.sleep(1)
        callback(123)

    def on_search_complete(self, features):

        for feature in features:
            self.write(feature.properties["name"] + "")
        self.finish()

    def download(self, details=''):
        global server_ip, server_port,root,pdfdir,water_pdfdir
        url_watermark=details['url_watermark']
        url_to_download=details['url_to_download']
        try:
            ftp_upload=details['ftp_local_upload']
        except:
            ftp_upload=''
        try:
            ip_method=details['ip_method']
        except:
            ip_method='No'

        time_diff = time.time()
        ip = self.request.remote_ip
        # ip3=self.request
        CurrentDir = os.path.dirname(os.path.realpath(__file__))
        htmls = CurrentDir.replace('\\', '/') + '/htmls'
        sys.path.insert(0, htmls)
        address = {}
        try:
            address['email'] = str(self.get_argument('email'))
        except:
            address['email'] = ''
        try:
            address['email'] = details['email']
        except:
            address['email'] = ''
        address['ip'] = ip
        address['url'] = url_to_download
        address['main_url'] = url_to_download
        address['time'] = str(round(time.time() - time_diff, 2))
        address['pdf_dw_Wr_li'] = ''
        address['pdf_dw_li'] = ''
        address['done'] = 0
        address['link'] = ''
        done = 0
        donw_done=0
        if url_to_download != '' and (url_to_download.startswith("http") or url_to_download.startswith("www.")) :

            self.core = import_mod(from_module='main_core', from_module2='core')
            if (re.findall('www', url_to_download) or re.findall('http://', url_to_download)) \
                or re.findall('https://', url_to_download):
                valid_link = self.core().valid_link(url=url_to_download,root=root,pdfdir=root+pdfdir,
                                                    water_pdfdir=root+water_pdfdir,)
                link=valid_link['link']; proxy=valid_link['proxy']; user_pass=valid_link['user_pass']
                try:
                    html=valid_link['html']
                except:
                    html=''
                try:
                    log_out=valid_link['log_out']
                except:
                    log_out=''
                try:
                    cookies=valid_link['cookies']
                except:
                    cookies=''


                # self.render(htmls + '/done.html', pdf_path='link is found by:'+str(link), url=address['url'],
                #             war_path=address['pdf_dw_Wr_li'], email=address['email'], ip=address['ip'],
                #             time=address['time'])
                if link != []:
                    address['link'] = link
                    # self.write('<h2>link found is  :\n' + link+'by proxy\n'+ proxy+' and user pass : \n'+ str(user_pass) + '</h2>\n')
                    # self.write('<h2><a href=' + link + '>link found</a></h2>')
                    # self.write('<h2>by proxy\n' + proxy + ' and user pass : \n' + str(user_pass) + '</h2>\n')
                    print 'time to find link:' + str(round(time.time() - time_diff, 2))

                    if donw_done==0:
                        try:
                            host=os.environ['OPENSHIFT_GEAR_DNS']
                            # host=os.environ['OPENSHIFT_DIY_IP']
                        except:
                            host = server_ip
                        try:
                            hh=self.request.headers['Referer']
                            site = urlparse2(hh).hostname
                            port= str(urlparse2(hh).port)
                        except:
                            hh=self.request.host
                            site=hh.split(':')[0]
                            try:
                                port=hh.split(':')[1]
                            except:
                                port='8080'

                        if port=='None':port='8080'
                        # if site==host and server_port==port:pass
                        # else:print 'tornado server and host is not the same maybe need to better config!!'
                        # host=site+':'+port
                        try:
                            host=os.environ['OPENSHIFT_GEAR_DNS']
                            # host=os.environ['OPENSHIFT_DIY_IP']
                            myhost='http://'+host
                        except:
                            if host!=server_ip:
                                myhost='http://127.0.0.1:86'
                            else:
                                if port=='86'  :#and port!=str(urlparse2(url_to_download).port):
                                    myhost='http://'+server_ip+':'+port
                                else:
                                    # myhost='http://'+server_ip+':'+server_port
                                    myhost='http://'+server_ip+':86'
                        address['pdf_dw_li']='We find link but we could not download file becuse of some problem !!'

                        # self.render(htmls + '/invalid_url.html',link=address['link'],pdf_path=address['pdf_dw_li'], url=address['url'],
                        #             war_path=address['pdf_dw_Wr_li'], email=address['email'], ip=address['ip'],
                        #             time=address['time'], main_url=address['main_url'])

                        if url_watermark !='':
                            need_watermarker=True
                        else:
                            need_watermarker=False
                        address = self.core().download_link(main_url=url_to_download,link=link, need_watermarker=need_watermarker,
                                                            server=myhost,root=root,pdfdir=root+pdfdir,
                                                            water_pdfdir=root+water_pdfdir,url_watermark=url_watermark,
                                                            proxy=proxy,user_pass=user_pass,cookies=cookies,log_out=log_out,ftp_upload=ftp_upload,html=html)
                        donw_done=1
                        try:os.remove(cookies)
                        except:pass
                        print 'adress in tornado downloaded line 368 tornado-get.py'
                        # try:path = url2Path(url=address['pdf_dw_li'])
                        path=address['wt_pdf_dir']
                        try:
                            address['email'] = str(self.get_argument('email'))
                        except:
                            address['email'] = ''
                        try:
                            address['email'] = details['email']
                        except:
                            address['email'] = ''
                        address['ip'] = ip
                        address['url'] = url_to_download
                        address['main_url'] = url_to_download
                        if address['email'] != '':
                            try:
                                email = str(self.get_argument('email'))
                                self.mail = import_mod(from_module='send_email', from_module2='main_server',
                                                       dir_location='/email/')
                                mail_server='smtp.gmail.com:587'
                                # mail_server='smtp.mail.yahoo.com:587',user ='soheil_paper' ,
                                # password='32913291'
                                self.mail(mail_server=mail_server,user ='soheilpaper' ,
                                     password='ss329132913291',name ='Free',to_name ='our Guest',to_email =email,
                                     subject ='Download succesfully' , message ='This is your file requested is in Atachment',attachments =[path])
                                # self.mail(mail_server='smtp.mail.yahoo.com:587',user ='soheil_paper' ,
                                #      password='32913291',name ='Free',to_name ='our Guest',to_email =email,
                                #      subject ='Download succesfully' , message ='This is your file requested is in Atachment',attachments =[path])
                                self.mail(mail_server='127.0.0.1:1025', user='soheil_paper',
                                          password='32913291', name='Free', to_name='our Guest', to_email=email,
                                          subject='Download succesfully',
                                          message='This is your file requested is in Atachment',
                                          attachments=[path])
                                address['email'] = email
                            except:
                                address['email'] = 'we have some problem for sending via Emails'

                        address['link']=str(link).replace('%20',' ')
                        if need_watermarker!=True:
                            address['pdf_dw_Wr_li']=address['pdf_dw_li'].replace('%20',' ')
                            address['wt_pdf_size']=address['pdf_size']

                        address['pdf_dw_li']=address['pdf_dw_li'].replace('%20',' ')
                        address['user_pass_worked']=str(address['user_pass_worked'])
                        address['main_url'] = url_to_download.replace('%20',' ')
                        address['ip'] = ip
                        address['time'] = str(round(time.time() - time_diff, 2))
                        address['done'] = 1
                        done = 1
                        print '\n' + address['time']
                        # items = []
                        # for filename in os.listdir(address['W_pdf_local']):
                        #     items.append(filename)

                        # self.render('htmls/files.html', items=items,url=address["pdf_dw_Wr_li"].split(address['W_pdf_name'])[0])
                        # x = open(address['wt_pdf_dir'])
                        # self.set_header('Content-Type', 'text/csv')
                        # self.set_header('Content-Disposition', 'attachment; filename=' + address['W_pdf_name'])
                        # self.finish(x.read())
                        # if os.path.isfile(root+water_pdfdir):
                        if os.path.isfile(address['wt_pdf_dir']):
                            static='1'
                        else:
                            static='0'
                        self.render(htmls + '/get_done.html',link=address['link'],pdf_path=address['pdf_dw_li'].replace('%20',' '),pdf_size=address['pdf_size'], url=address['url'],
                                    war_path=address['pdf_dw_Wr_li'].replace('%20',' '),wt_pdf_size=address['wt_pdf_size'], email=address['email'], ip=address['ip'],
                                    time=address['time'], main_url=address['main_url'],static=static, address= address)
                        print 'download end and done.html page is made'
                        return address
                    if donw_done==0:
                        address['pdf_dw_li']='We find link but we could not download file becuse of some problem !!'
                        self.render(htmls + '/invalid_url.html',link=address['link'],pdf_path=address['pdf_dw_li'], url=address['url'],
                                    war_path=address['pdf_dw_Wr_li'], email=address['email'], ip=address['ip'],
                                    time=address['time'], main_url=address['main_url'])
                        return address
        if done == 0 or url_to_download=='':
            address['main_url'] = url_to_download.replace('%20',' ')
            address['ip'] = ip
            address['time'] = str(round(time.time() - time_diff, 2))
            print 'you have inserted invalid url'
            self.render(htmls + '/invalid_url.html',link=address['link'],pdf_path=address['pdf_dw_li'], url=address['url'],
                        war_path=address['pdf_dw_Wr_li'], email=address['email'], ip=address['ip'],
                        time=address['time'], main_url=address['main_url'])
            # yield address
        print 'post done'
        return address
    def download_get(self, url_to_download=''):
        global server_ip, server_port,root,pdfdir,water_pdfdir
        time_diff = time.time()
        ip = self.request.remote_ip
        # ip3=self.request
        CurrentDir = os.path.dirname(os.path.realpath(__file__))
        htmls = CurrentDir.replace('\\', '/') + '/htmls'
        sys.path.insert(0, htmls)
        address = {}
        try:
            address['email'] = str(self.get_argument('email'))
        except:
            address['email'] = ''
        address['ip'] = ip
        address['url'] = url_to_download
        address['main_url'] = url_to_download
        address['pdf_dw_Wr_li'] = ''
        address['pdf_dw_li'] = ''
        address['time'] = str(round(time.time() - time_diff, 2))
        address['done'] = 0
        address['link'] = ''
        done = 0
        donw_done=0
        url_to_download=str(url_to_download)
        if url_to_download != '':

            self.core = import_mod(from_module='main_core', from_module2='core')
            if (re.findall('www', url_to_download) or re.findall('http://', url_to_download)) \
                or re.findall('https://', url_to_download):
                valid_link = self.core().valid_link(url=url_to_download)
                link=valid_link['link']; proxy=valid_link['proxy']; user_pass=valid_link['user_pass']
                try:
                    cookies=valid_link['cookies']
                except:
                    cookies=''
                    # self.render(htmls + '/done.html', pdf_path='link is found by:'+str(link), url=address['url'],
                #             war_path=address['pdf_dw_Wr_li'], email=address['email'], ip=address['ip'],
                #             time=address['time'])
                if link != []:
                    address['link'] = link
                    # self.write('<h2>link found is  :\n' + link+'by proxy\n'+ proxy+' and user pass : \n'+ str(user_pass) + '</h2>\n')
                    # self.write('<h2><a href=' + link + '>link found</a></h2>')
                    # self.write('<h2>by proxy\n' + proxy + ' and user pass : \n' + str(user_pass) + '</h2>\n')
                    print 'time to find link:' + str(round(time.time() - time_diff, 2))

                    if donw_done==0:
                        try:
                            host=os.environ('OPENSHIFT_GEAR_DNS')
                        except:
                            host = server_ip
                        try:
                            hh=self.request.headers['Referer']
                            site = urlparse2(hh).hostname
                            port= str(urlparse2(hh).port)
                        except:
                            hh=self.request.host
                            site=hh.split(':')[0]
                            try:
                                port=hh.split(':')[1]
                            except:
                                port='8080'

                        if port=='None':port='8080'
                        if site==host and server_port==port:pass
                        else:print 'tornado server and host is not the same mybe need to better config!!'
                        host=site+':'+port
                        myhost='http://'+host
                        address = self.core().download_link(link=link, need_watermarker=True,
                                                            server=myhost,root=root,pdfdir=root+pdfdir,
                                                            water_pdfdir=root+water_pdfdir,
                                                            # server=myhost,root=root,pdfdir=root+'/PDF_Files',
                                                            # water_pdfdir=root+'/Watermarked_PDF_Files',
                                                            proxy=proxy,user_pass=user_pass,cookies=cookies)
                        donw_done=1
                        print 'adress in tornado downloaded line 340 tornado-get.py'
                        try:path = url2Path(url=address['pdf_dw_li'])
                        except:path=address['wt_pdf_dir']
                        try:
                            address['email'] = str(self.get_argument('email'))
                        except:
                            address['email'] = ''
                        if address['email'] != '':
                            try:
                                email = str(self.get_argument('email'))
                                self.mail = import_mod(from_module='send_email', from_module2='main_server',
                                                       dir_location='/email/')
                                # mail_server='smtp.gmail.com:587'
                                # mail_server='smtp.mail.yahoo.com:587',user ='soheil_paper' ,
                                # password='32913291'
                                # self.mail(mail_server='smtp.mail.yahoo.com:587',user ='soheil_paper' ,
                                #      password='32913291',name ='Free',to_name ='our Guest',to_email =email,
                                #      subject ='Download succesfully' , message ='This is your file requested is in Atachment',attachments =[path])
                                self.mail(mail_server='127.0.0.1:1025', user='soheil_paper',
                                          password='32913291', name='Free', to_name='our Guest', to_email=email,
                                          subject='Download succesfully',
                                          message='This is your file requested is in Atachment',
                                          attachments=[path])
                                address['email'] = email
                            except:
                                address['email'] = 'we have some problem for sending via Emails'

                        address['link']=str(link).replace('%20',' ')
                        address['pdf_dw_li']=address['pdf_dw_li'].replace('%20',' ')
                        address['user_pass_worked']=str(address['user_pass_worked'])
                        address['main_url'] = url_to_download.replace('%20',' ')
                        address['ip'] = ip
                        address['time'] = str(round(time.time() - time_diff, 2))
                        address['done'] = 1
                        done = 1
                        print '\n' + address['time']
                        # items = []
                        # for filename in os.listdir(address['W_pdf_local']):
                        #     items.append(filename)

                        # self.render('htmls/files.html', items=items,url=address["pdf_dw_Wr_li"].split(address['W_pdf_name'])[0])
                        # x = open(address['wt_pdf_dir'])
                        # self.set_header('Content-Type', 'text/csv')
                        # self.set_header('Content-Disposition', 'attachment; filename=' + address['W_pdf_name'])
                        # self.finish(x.read())
                        self.render(htmls + '/get_done.html',link=address['link'],pdf_path=address['pdf_dw_li'].replace('%20',' '),pdf_size=address['pdf_size'], url=address['url'],
                                    war_path=address['pdf_dw_Wr_li'].replace('%20',' '),wt_pdf_size=address['wt_pdf_size'], email=address['email'], ip=address['ip'],
                                    time=address['time'], main_url=address['main_url'])
                        print 'download end and done.html page is made'
                        return address
                    if donw_done==0:
                        address['pdf_dw_li']='We find link but we could not download file becuse of some problem !!'
                        self.render(htmls + '/invalid_url.html',link=address['link'],pdf_path=address['pdf_dw_li'], url=address['url'],
                                    war_path=address['pdf_dw_Wr_li'], email=address['email'], ip=address['ip'],
                                    time=address['time'], main_url=address['main_url'])
                        return address
        if done == 0 or url_to_download=='':
            print 'you have inserted invalid url'
            self.render(htmls + '/invalid_url.html',link=address['link'],pdf_path=address['pdf_dw_li'], url=address['url'],
                        war_path=address['pdf_dw_Wr_li'], email=address['email'], ip=address['ip'],
                        time=address['time'], main_url=address['main_url'])
            # yield address
        print 'post done'
        return address

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        # try:
            CurrentDir = os.path.dirname(os.path.realpath(__file__))
            htmls = CurrentDir.replace('\\', '/') + '/htmls'
            sys.path.insert(0, htmls)

            print '@@@@@getting client ip'
            time_diff = time.time()
            ip = self.request.remote_ip
            ip2 = socket.gethostbyname(socket.gethostname())
            print 'Client IP:' + ip
            # self.write('<h2>&mdash;Client Virtual IP:' + ip + '</h2>\n')
            # self.write('<h2>&mdash;Client IP2:' + ip2 + '</h2>\n')
            # ip3=repr(self.request)
            ip3 = self.request
            host_cdn = self.request.headers['Host']
            print 'ip3=' + repr(ip3)
            # self.write('<h5>Request :' + repr(self.request) + '</h5>\n')
            # self.write(repr(self.request))
            self.set_header('url', 'wwwwwwww')
            headr_to_download = self._headers
            # print "your header is"+self._headers
            # url = self.get_argument('url', 'Hello')
            try:
                url = self.request.arguments.get('url')
                # url2=self.get_query_argument(input)
                link = self.request.query
                req=self.request.uri;
                link=req
                url_watermark='';email='';
                url = link.split('url=')[1]
                if re.findall('wt_url=',url)or re.findall('email_adress=',url):
                    url= link.split('url=')[1].split('wt_url=')[0]

                if re.findall('wt_url=',url):
                    if re.findall('email_adress=',url):
                        url_watermark = link.split('wt_url=')[1].split('email_adress=')[0]
                    else:
                        url_watermark = link.split('wt_url=')[1]
                if re.findall('email_adress=',url):
                    email = link.split('email_adress=')[1]
                url_watermark = url_watermark.replace(' ', '%20')

                # self.write(url + ', \nfriendly user!\n')
                url = url.replace(' ', '%20').replace("%22","").replace('"',"")
                if len(re.findall(str("http://"),url))==0:
                    if len(re.findall(str("http:/"),url))!=0:
                       print "Url is :"+url
                       # url.replace("http:/","http://")
                       url=str("http://")+url.split('http:/')[1]
                       print "Url NEW is :"+url
                if len(re.findall(str("https://"),url))==0:
                    if len(re.findall(str("https:/"),url))!=0:
                       url.replace("https:/","https://")
            except:
                url = []
                host = (socket.gethostname())
                socket.gethostbyaddr(socket.gethostname())[0]
                self.render(htmls + '/index.html')
                # self.write('\r\nfPlease ins insert url for this app like:www.'+host+'!!!.com/index/?url=www.google.com\n')
                self.finish()
            url_to_download=url

            details={
                'url_to_download':url_to_download,
                'url_watermark':url_watermark,
                'email':email
            }
            # result = tornado.gen.Task(self.download_get(url))
            result = tornado.gen.Task(self.download(details))
            print 'try'
            print 'sleeping'
            # result =yield tornado.gen.Task(self.my_function())
            print 'result is'
            print result

            # self.write( 'result is', result)
            self.finish()
        # except:
        #     pass

            # @tornado.web.asynchronous
            # @tornado.gen.engine
            # def get(self):
            #     print '@@@@@getting client ip'
            #     time_diff=time.time()
            #     ip=self.request.remote_ip
            #     ip2=socket.gethostbyname(socket.gethostname())
            #     print 'Client IP:' +ip
            #     self.write('Client IP:'+ip+'\n')
            #     self.write('Client IP2:'+ip2+'\n')
            #     # ip3=repr(self.request)
            #     ip3=self.request
            #     print 'ip3='+repr(ip3)
            #     self.write(repr(self.request))
            #     self.set_header('url','wwwwwwww')
            #     headr_to_download=self._headers
            #     # print "your header is"+self._headers
            #     # url = self.get_argument('url', 'Hello')
            #     url = self.request.arguments.get('url')
            #     # url2=self.get_query_argument(input)
            #     link=self.request.query
            #     try:
            #         url=link.split('url=')[1]
            #         url=url.replace(' ','%20')
            #         self.write(url + ', \nfriendly user!\n')
            #     except:
            #         url=[]
            #         host=(socket.gethostname())
            #
            #         socket.gethostbyaddr(socket.gethostname())[0]
            #         self.render('index.html')
            #         # self.write('\r\nfPlease ins insert url for this app like:www.'+host+'!!!.com/index/?url=www.google.com\n')
            #         # self.finish()
            #
            #     if   url!=[]:
            #
            #         url_to_download=url
            #
            #         client = tornado.httpclient.AsyncHTTPClient()
            #         # from main_core import core
            #         self.core=import_mod(from_module='main_core',from_module2='core')
            #
            #         # from ieeexplore_ieee_org_good import ieee_main
            #         if  (re.findall('www', url_to_download) or re.findall('http://', url_to_download)) \
            #             or re.findall('https://', url_to_download):
            #             # [pdf_path , war_path]=download().render(url)
            #             done=0
            #             # from main_core import core
            #             # from ieeexplore_ieee_org_good import ieee_main
            #
            #             link,proxy,user_pass=self.core().valid_link(url=url_to_download)
            #             if link!=[]:
            #                     address=self.core().download_link(link=link,need_watermarker=True)
            #                     path=url2Path(url=address['pdf_dw_li'])
            #                     try:
            #                         email=self.request.query.split('email_to=')[1]
            #                         main(mail_server='smtp.gmail.com:587',user ='soheilpaper' ,
            #                              password='ss32913291',name ='Free-papers.tk',to_name ='our Guest',to_email =email,
            #                              subject ='Download succesfully' , message ='This is your file requested is in Atachment',attachments =path)
            #                     except:
            #                         pass
            #                     # address=core().main(url=url_to_download,need_watermarker=True)
            #                     url=address['url']
            #                     war_path=address['pdf_dw_Wr_li']
            #                     pdf_path=address['pdf_dw_li']
            #                     # time1=str(round( time.time() - time_diff, 2))
            #                     done=1
            #                     # print time1
            #             if done==0:
            #                 url=url_to_download
            #                 war_path=''
            #                 pdf_path=''
            #                 # time1=str(round( time.time() - time_diff, 2))
            #             self.render('done.html',pdf_path=pdf_path, url=url,war_path=war_path ,ip=ip,time=str(round( time.time() - time_diff, 2)))
            #         else:
            #             self.render('\htmls\invalid_url.html',url=url,time=str(round( time.time() - time_diff, 2)))
            #         # self.render('done.html', url=url,time=str(round( time.time() - time_diff, 2)))
            #         # self.finish()

# ----end of 'introduction to tornado ebook'----

class ListIndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        items = []
        for filename in os.listdir("upload/"):
            items.append(filename)
        self.render('html/files.html', items=items)
    def post(self):
        file_content = self.request.files['datafile'][0]['body']
        file_name = self.request.files['datafile'][0]['filename']
        x = open("upload/" + file_name, 'w')
        x.write(file_content)
        x.close()
        self.redirect("/")
class UploadHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, filename):
        import codecs
        items = []
        path=os.path.join(os.path.dirname(__file__), "Watermarked_PDF_Files").replace('\\','/')
        for filename in os.listdir(path):
            items.append(filename)

        self.render('htmls/files.html', items=items,url='http://127.0.0.1:15001/Watermarked_PDF_Files/')
        # path=str('C:/nginx/html/Watermarked_PDF_Files/' + filename)
        # # x = open('C:/nginx/html/Watermarked_PDF_Files/' + filename)
        # self.set_header('Content-Type','application/pdf; charset="utf-8"')
        # # self.set_header('Content-Type', 'application/octet-stream')
        # self.set_header('Content-Disposition', 'attachment; filename=' + str(filename));
        # self.set_header('Content-Length: ' , size(os.path.getsize(path)));
        # self.set_header("Cache-control"," private");
        # buf_size =1024*1024
        # # f=open(path, 'r','utf-8')
        # # self.write(f.read())
        # # f.close()
        # with open(path, 'r') as f:
        #     while True:
        #         data = f.read(buf_size)
        #         if not data:
        #             break
        #         self.write(data)
        self.finish()
        # self.finish(x.read())
    def recaptcha(self):
        recaptcha_challenge=self.get_argument('recaptcha_challenge','')
        recaptcha_response=self.get_argument('recaptcha_response','')
        recaptcha_http=tornado.httpclient.AsyncHTTPClient()
        recaptcha_priv_key='xxxxxxyyyyyyyyzzzzz'
        remote_addr=self.request.headers['X-Real-Ip']
        recaptcha_req_data={
                            'privatekey':recaptcha_priv_key,
                            'remoteip':remote_addr,
                            'challenge':recaptcha_challenge,
                            'response':recaptcha_response
        }
        recaptcha_req_body=urllib.urlencode(recaptcha_req_data)

        try:
            recaptcha_http.fetch('http://www.google.com/recaptcha/api/verify', self.callback, method='POST',body=recaptcha_req_body) #https://developers.google.com/recaptcha/docs/verify
        except tornado.httpclient.HTTPError,e:
            print 'Error:',e


class MyFileHandler(tornado.web.StaticFileHandler):
    def initialize(self, path):
        self.dirname, self.filename = os.path.split(path)
        super(MyFileHandler, self).initialize(self.dirname)

    def get(self, path=None, include_body=True):
        # Ignore 'path'.
        super(MyFileHandler, self).get(self.filename, include_body)

class DownloadHandler(tornado.web.RequestHandler):
    def get(self):
        # self.render("index.html")
        # self._headers
        # print "your header is"+self._header
        # print 'your status'+self.get_status
        # print "Content-type: text/html\n"
        # print ''
        # print '<pre>'
        # print 'tanks'
        # from 'introduction to tornado ebook'

        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')

        # or

        self.write('thanks')
        # self.write("your header is"+self._header+'\n')
        # self.write("your status"+self.get_status+'\n')

    def post(self):
        import re
        import socket

        ip = socket.gethostbyname(socket.gethostname())
        print 'Client IP:' + ip
        self.set_header('url', 'wwwwwwww')
        headr_to_download = self._headers
        print "your header is" + self._header
        url_to_download = str(self.get_argument('url_to_download', ''))

        if url_to_download :
            CurrentDir = os.path.dirname(os.path.realpath(__file__))
            os.chdir(CurrentDir)
            from ieeexplore_ieee_org_good import ieee_main

            os.chdir(CurrentDir)
            if (re.findall('www', url_to_download) or re.findall('http://', url_to_download)) \
                or re.findall('https://', url_to_download):
                [pdf_path, war_path] = ieee_main().todo_url(url_to_download)
                download_response = {
                    "error": True,
                    # 'msg':main().todo_url(url_to_download)
                    'msg': url_to_download,
                    'header': headr_to_download,
                    'your_link': pdf_path,
                    'watermarker link': war_path}
            else:
                download_response = {
                    "error": True,
                    # 'msg':main().todo_url(url_to_download)
                    'msg': url_to_download,
                    'header': headr_to_download,
                    'your_link': ' Your link is not corrcet .Please enter your corrcet link.',
                    'watermarker link': 'Please enter your corrcet link.'}

        self.write(download_response)


# def log_request( handler):
#     log = logging.getLogger('demo')
#     log.setLevel(logging.DEBUG)
#     log.addHandler(MongoHandler.to(db='mongolog', collection='log', host='db.example.com'))
#
#     if handler.get_status():# & lt; 400:
#         log_method = log.info
#     elif handler.get_status():# &lt; 500:
#         log_method = log.warn
#     else:
#         log_method = log.error
#
#     request_time = 1000.0 * handler.request.request_time()
#     log_message = '%d %s %.2fms' % (handler.get_status(), handler._request_summary(), request_time)
#     log_method(log_message)
class StaticFileHandler(tornado.web.RequestHandler):
    """A simple handler that can serve static content from a directory.

    To map a path to this handler for a static data directory /var/www,
    you would add a line to your application like:

    application = web.Application([
    (r"/static/(.*)", web.StaticFileHandler, {"path": "/var/www"}),
    ])

    The local root directory of the content should be passed as the "path"
    argument to the handler.

    To support aggressive browser caching, if the argument "v" is given
    with the path, we set an infinite HTTP expiration header. So, if you
    want browsers to cache a file indefinitely, send them to, e.g.,
    /static/images/myimage.png?v=xxx.
    """
    def initialize(self, path, default_filename=None):
        self.root = os.path.abspath(path) + os.path.sep
        self.default_filename = default_filename

    def head(self, path):
        self.get(path, include_body=False)

    def get(self, path, include_body=True):
        if os.path.sep != "/":
            path = path.replace("/", os.path.sep)
        abspath = os.path.abspath(os.path.join(self.root, path))
        # os.path.abspath strips a trailing /
        # it needs to be temporarily added back for requests to root/
        if not (abspath + os.path.sep).startswith(self.root):
            raise tornado.web.HTTPError(403, "%s is not in root static directory", path)
        if os.path.isdir(abspath) and self.default_filename is not None:
        # need to look at the request.path here for when path is empty
        # but there is some prefix to the path that was already
        # trimmed by the routing
            if not self.request.path.endswith("/"):
                self.redirect(self.request.path + "/")
                return
            abspath = os.path.join(abspath, self.default_filename)
        if not os.path.exists(abspath):
            raise tornado.web.HTTPError(404)
        if not os.path.isfile(abspath):
            raise tornado.web.HTTPError(403, "%s is not a file", path)

        stat_result = os.stat(abspath)
        modified = tornado.web.datetime.datetime.fromtimestamp(stat_result[tornado.web.stat.ST_MTIME])

        self.set_header("Last-Modified", modified)
        if "v" in self.request.arguments:
            self.set_header("Expires", tornado.web.datetime.datetime.utcnow() + \
                                   tornado.web.datetime.timedelta(days=365*10))
            self.set_header("Cache-Control", "max-age=" + str(86400*365*10))
        else:
            self.set_header("Cache-Control", "public")
        mime_type, encoding = tornado.web.mimetypes.guess_type(abspath)
        if mime_type:
            self.set_header("Content-Type", mime_type)

        self.set_extra_headers(path)

        # Check the If-Modified-Since, and don't send the result if the
        # content has not been modified
        ims_value = self.request.headers.get("If-Modified-Since")
        if ims_value is not None:
            pass
            date_tuple = tornado.web.email.utils.parsedate(ims_value)
            if_since = tornado.web.datetime.datetime.fromtimestamp(time.mktime(date_tuple))
            if if_since >= modified:
                self.set_status(304)
                return

        if not include_body:
            return
        file = open(abspath, "rb")
        try:
            self.write(file.read())
        finally:
            file.close()

    def set_extra_headers(self, path):
        """For subclass to add extra headers to the response"""
        pass

from urllib import urlopen
from urllib import urlencode
# Get key: https://www.google.com/recaptcha/whyrecaptcha
publickey = '01kRun3VzCzCoGYUvJ44lHUQ=='
privatekey = '9b6294915e5d969e709b2f469ae065d7'
class CaptchaHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('htmls/recaptcha.html', publickey=publickey)

    def post(self):
        url = 'http://www.google.com/recaptcha/api/verify'

        # verification code
        challenge = self.get_argument('recaptcha_challenge_field')
        # user input
        response = self.get_argument('recaptcha_response_field')

        data = {
            'privatekey': privatekey,
            'remoteip': self.request.remote_ip,
            'challenge': challenge,
            'response': response
        }

        res = urlopen(url, data=urlencode(data).encode())
        # obtain verification results , where the results will be returned directly to the page output
        self.write(res.read().decode())



def main(**kwargs):
    global server_ip, server_port,root,pdfdir,water_pdfdir
    server_ip = kwargs['ip']
    root=kwargs['root']
    server_port = kwargs['port']
    index = kwargs['index']
    user_pass = kwargs['user_pass']

    print '@@@@@@@@@@ main ip is :' + server_ip
    CurrentDir = os.path.dirname(os.path.realpath(__file__))
    if not os.path.isdir(CurrentDir+"/logs"):
        os.mkdir(CurrentDir+"/logs")
    log_name = CurrentDir.replace('\\', '/') + "/logs/my_app" + server_port + ".log"
    args = sys.argv
    print '@@@@@@@@@@@@arg is:######'
    print args
    log = [args[0], "--log_file_prefix=" + log_name]
    print '@@@@@@@@@@@@arg is:######'
    print log
    tornado.options.parse_command_line(log)
    application = tornado.web.Application([
                                              # (r'', IndexHandler),
                                              (r"/", IndexHandler),
                                              # (r"/(\d+$)", IndexHandler),
                                              # (r"/(\d{4})/(\d{2})/(\d{2})/([a-zA-Z\-0-9\.:,_]+)/?", IndexHandler),
                                              # (r"/(\d+)$", IndexHandler),
                                              (r"/main", MainHandler),
                                              (r"/login", LoginHandler),
                                              (r"/download", DownloadHandler),
                                              (r"/reverse/(\d+)", ReverseHandler),
                                              (r"/index/.*", IndexHandler),
                                              (r"/add/", AddHandler),
                                              (r"/" + index, IndexHandler),
                                              (r'/api', ApiHandler),
                                              (r'/ws', SocketHandler),
                                              (r"/Watermarked_PDF_Files/([A-Za-z0-9\_\.\-]+)", UploadHandler),
                                              (r'/recaptcha', CaptchaHandler),
                                              # (r"/Watermarked_PDF_Files/([A-Za-z0-9\_\.\-]+)", MyFileHandler, {'path': 'C:/nginx/html/Watermarked_PDF_Files/'}),
                                              # (r'/Watermarked_PDF_Files/\.pdf', MyFileHandler, {'path': 'C:/nginx/html/Watermarked_PDF_Files/'}),
                                              # ('.*', SocketHandler)],
                                              (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': root+water_pdfdir}),
                                              (r'/PDF_Files/(.*)', tornado.web.StaticFileHandler, {'path': root+pdfdir})
                                          ],
                                          # template_path=os.path.join(os.path.dirname(__file__), "htmls").replace('\\','/'),
                                          template_path=os.path.join(os.path.dirname(__file__), '').replace('\\','/'),
                                          # static_path=os.path.join(os.path.dirname(__file__).replace('\\','/'), "Watermarked_PDF_Files"),
                                          # static_path=os.path.dirname('C:/nginx/html/Watermarked_PDF_Files/'),
                                          static_path=root+water_pdfdir,
                                          # static_path=root+pdfdir,
                                          debug=True

                                          # ui_modules={'download_modle', download}
    )
    CurrentDir = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.abspath(os.path.join(CurrentDir, '..'))

    # http_server = tornado.httpserver.HTTPServer(application, ssl_options={
    #  "certfile": os.path.join(data_dir, "configs//LocalProxyServer.cert"),
    #  "keyfile": os.path.join(data_dir, "configs/LocalProxyServer.key"),
    #  })
    # #
    # http_server.listen(443)
    # tornado.ioloop.IOLoop.instance().start()
    # tornado.log.define_logging_options(log_file_prefix='/log.txt')
    http_server = tornado.httpserver.HTTPServer(application)
    print " &&&&&&&&&&&&&&&Before Starting Torando on ip and port:" + server_ip + ':' + server_port
    try:
        http_server.listen(server_port)
        print "Starting Torando on only  port:" ':' + server_port
    except:
        http_server.listen(server_port, server_ip)
        print "Starting Torando on ip and port:" + server_ip + ':' + server_port

    tornado.ioloop.IOLoop.instance().start()
    # print "Tornado finished"


def stopTornado():
    global ip, port
    try:
        from tornado.log import gen_log

        sss = tornado.log
        s = tornado.ioloop.IOLoop.instance()
        # for fd, sock in s._sockets.items():
        #     pass
        CurrentDir = os.path.dirname(os.path.realpath(__file__))
        log_name = CurrentDir.replace('\\', '/') + "/logs/my_app" + port + ".log"
        args = sys.argv
        args2 = [args[0], "--log_file_prefix=" + log_name]
        tornado.options.parse_command_line(args2)
        ioloop = tornado.ioloop.IOLoop.instance()
        ioloop.add_callback(lambda x: x.stop(), ioloop)

        s2 = tornado.ioloop.IOLoop.instance().stop()
        args.append("--log_file_prefix=" + log_name)
        tornado.options.parse_command_line(args)

        print "Asked Tornado to exit on ip:port \n" + ip + ':' + port
    except:
        print 'There is no Tornado Runing That you have asked to Terminate in ip:port'#+ip+':'+port


if __name__ == "__main__":
    global pdfdir,water_pdfdir
    CurrentDir=os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
    # core = import_mod(from_module='main_core', from_module2='core')
    # core().update_urls_to_proxy_find_link(proxylist_file='configs//proxylist.txt',url_file='configs//sites_proxy//urllist.txt')


    # nohup sh -c "${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/tornado3/tornado-get.py  --port '8080'" > ${OPENSHIFT_LOG_DIR}/tornado1.log /dev/null 2>&1 &

    # nohup sh -c " ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/tornado8/tornado-get.py  --port '15001' --root '${OPENSHIFT_HOMEDIR}/app-root/runtime/repo/www' --wtdir '/static'" > ${OPENSHIFT_LOG_DIR}/tornado1.log /dev/null 2>&1 &

    # ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/tornado9/tornado-get.py  --port '15001' --root '${OPENSHIFT_HOMEDIR}/app-root/runtime/repo/www' --wtdir '/static'


    # ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/tornado5/tornado-get.py  --port '8080' --root '${OPENSHIFT_HOMEDIR}/app-root/runtime/repo/www' --wtdir '/static'
    # ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python tornado-get.py  --port '15001' --root '${OPENSHIFT_HOMEDIR}/app-root/runtime/repo/www' --wtdir '/static'

    # ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/tornado/tornado-get.py  --port '8080'


    from optparse import OptionParser
    # import pymongo
    # conn = pymongo.Connection("localhost", 27017)
    CurrentDir = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')

    parser = OptionParser(description=__doc__)
    help1 = 'Address url file name to be downloaded like:"www.google.com"\n' + \
            "Please make attention 'www.google.com' is risky use  only with" + '"blabla"'
    parser.add_option('-i', '--ip', type='string', dest='ip', help='please insert your ip to make a server'
                                                                   ' based on it like:121.121.21.21 \nIf you'
                                                                   ' dont know print os enviroment for it like :'
                                                                   ' OPENSHIFT_DIY_IP',default='OPENSHIFT_DIY_IP')
    parser.add_option('-p', '--port', dest='port', help=' port setting for server like:15001', default='15001')
    parser.add_option('-s', '--user', dest='user_pass', help='user & password of proxy setting like admin:admin ',
                      default='admin:admin')
    parser.add_option('-n', '--index', dest='index', help='link added to your ip for running server download for it',
                      default='index')
    parser.add_option('-x', '--stop', dest='stop', help='stop tornado if  -x 1', default=False)
    parser.add_option('-r', '--root', dest='root', help='Root folder  for putting pdf files ', default=CurrentDir )
    parser.add_option('-f','--pdfdir', dest='pdfdir', help='make pdf files in this directory default is PDF_Files',default='/PDF_Files')
    parser.add_option('-w','--wtdir', dest='water_pdfdir', help='make  watermarker pdf files in this directory is Watermarked_PDF_Files',default='/static')
    # parser.add_option('-u', '--root_url', dest='root_url', help='Root url for downloading  pdf files ', default=CurrentDir )
    parser.add_option('-H', '--HELP', dest='HELP', help='For Getting Help')
    options, args = parser.parse_args()
    #python tornado-get.py -p 15001 --root 'C:/nginx/html' --ip 127.0.0.1
    # options.ip = '127.0.0.1'
    # options.port = '15001'
    # options.root='C:/nginx/html'
    # options.stop=True
    # os.environ['OPENSHIFT_DIY_IP']='127.0.0.1'
    # options.root='${OPENSHIFT_HOMEDIR}/app-root/runtime/repo/www'
    if options.ip and not options.stop:
        pdfdir=options.pdfdir;water_pdfdir=options.water_pdfdir
        if options.ip == 'OPENSHIFT_DIY_IP':

            try:
                try:
                    options.ip = os.environ['OPENSHIFT_DIY_IP']
                except:
                    options.ip = '127.0.0.1'
                print "the environ_diy_ip is:\n" + options.ip
                if re.findall('{',options.root):
                    o=options.root.split('{')[1].split('}')[0]
                    options.root=os.environ[o]+options.root.split('}')[1]

                if not os.path.isdir(options.root+options.pdfdir):os.mkdir(options.root+options.pdfdir)
                if not os.path.isdir(options.root+options.water_pdfdir):os.mkdir(options.root+options.water_pdfdir)
                print "you entered thi ip \n" + options.ip
                print "you entered thi port \n" + options.port


            except:
                try:

                    try:
                        options.ip = os.environ['OPENSHIFT_NGINX_IP']
                    except:
                        options.ip = '127.0.0.1'
                    print "the environ_diy_ip is:\n" + options.ip
                    if re.findall('{', options.root):
                        o = options.root.split('{')[1].split('}')[0]
                        options.root = os.environ[o] + options.root.split('}')[1]

                    if not os.path.isdir(options.root + options.pdfdir): os.mkdir(options.root + options.pdfdir)
                    if not os.path.isdir(options.root + options.water_pdfdir): os.mkdir(
                        options.root + options.water_pdfdir)
                    print "you entered thi ip \n" + options.ip
                    print "you entered thi port \n" + options.port
                except:
                    options.ip = '127.0.0.1'
                    options.port = '15001'
                    options.root=CurrentDir;
                    #options.root='C:/nginx/html'
                    if not os.path.isdir(options.root+options.pdfdir):os.mkdir(options.root+options.pdfdir)
                    if not os.path.isdir(options.root+options.water_pdfdir):os.mkdir(options.root+options.water_pdfdir)
                    print "you entered thi ip \n" + options.ip
                    print "you entered thi port \n" + options.port
            main(ip=options.ip, port=options.port, user_pass=options.user_pass, index=options.index,root=options.root)
        else:

            print "you entered thi ip \n" + options.ip
            print "you entered thi port \n" + options.port
            if not os.path.isdir(options.root+options.pdfdir):os.mkdir(options.root+options.pdfdir)
            if not os.path.isdir(options.root+options.water_pdfdir):os.mkdir(options.root+options.water_pdfdir)
            main(ip=options.ip, port=options.port, user_pass=options.user_pass, index=options.index,root=options.root)

    elif options.HELP:
        parser.print_help()
    elif options.stop:
        stopTornado()
    else:
        try:
            import os

            try:
                options.ip = os.environ['OPENSHIFT_DIY_IP']
            except:
                options.ip = '127.0.0.1'
            # port = '15001'
            print 'this server will be runned on ip:' + options.ip + 'and port:' + options.port
            if not os.path.isdir(options.root+options.pdfdir):os.mkdir(options.root+options.pdfdir)
            if not os.path.isdir(options.root+options.water_pdfdir):os.mkdir(options.root+options.water_pdfdir)
            main(ip=options.ip, port=options.port, user_pass='', index='index',root=options.root)

        except:
            print 'we could not run server bacuase you dont entered proper ip and port'
            # options.url='http://ieeexplore.ieee.org/xpl/articleDetails.jsp?tp=&arnumber=6180383&queryText%3Dpower' #91 KB
            parser.print_help()

    print '</pre>'
