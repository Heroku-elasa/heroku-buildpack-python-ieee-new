import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.httpclient
import time,os,sys,re,socket
from urlparse import urlparse as urlparse2

def url2Path(**kwargs):
    myhost="http://127.0.0.1/"
    url=kwargs['url']
    site = urlparse2(url).hostname
    myhost="http://"+site+"/"
    try:
        kwargs['pdf_dir']
        pdf_dir=kwargs['pdf_dir']
    except:pdf_dir=url.split(myhost)[1]
    ph=pdf_dir.split('/')[0]
    f_ph=pdf_dir.split('/')[-1]
    rp=os.getcwd().replace('\\','/').replace('%20',' ').split(ph)[0]
    path=rp+pdf_dir.split(f_ph)[0].replace('%20',' ')+f_ph
    return path

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


class DownloadHandler(tornado.web.RequestHandler):
    # @tornado.web.asynchronous
    # @tornado.gen.engine
    def get(self):
        url = self.request.arguments.get('url')
        # url2=self.get_query_argument(input)
        link=self.request.query
        try:
            url=link.split('url=')[1]
            url=url.replace(' ','%20')
            self.write(url + ', \nfriendly user!\n')
            address=self.download(url)
        except:
            url=[]
            host=(socket.gethostname())

            socket.gethostbyaddr(socket.gethostname())[0]
            self.render('index.html')



            # http_client = tornado.httpclient.AsyncHTTPClient()
            # print 'start'
            # # response = yield tornado.gen.Task(http_client.fetch, "http://google.com")
            # print 'done'
            # self.finish('Fin.')






class GenAsyncHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):

        print 'start'
        # response = yield tornado.gen.Task(http_client.fetch, "http://google.com")
        # address = yield tornado.gen.Task(http_client.fetch, "http://127.0.0.1:8888/download/?url=http://127.0.0.1/")
        address =  tornado.gen.Task(self.download('http://127.0.0.1/'))
        # address = self.download('http://127.0.0.1/')

        print address
        print 'done'
        # self.render('done.html',pdf_path=address['pdf_dw_li'], url=address['url'],war_path=address['pdf_dw_Wr_li'] ,email=address['email'],ip=address['ip'],time=address['time'])
        self.finish('Fin.')

    def download(self,url=''):
        time_diff=time.time()
        # ip3=self.request
        ip=self.request.remote_ip
        try :
            # url_to_download = str(self.get_argument('url_to_download').replace(' ','%20'))
            url_to_download=url
            if   url_to_download!='':
                done=0
                # from main_core import core
                self.core=import_mod(from_module='main_core',from_module2='core')
                # from ieeexplore_ieee_org_good import ieee_main
                if  (re.findall('www', url_to_download) or re.findall('http://', url_to_download)) \
                    or re.findall('https://', url_to_download):
                    link,proxy,user_pass=self.core().valid_link(url=url_to_download)
                    print 'time to find link:'+str(round( time.time() - time_diff, 2))
                    if link!=[]:
                        address=self.core().download_link(link=link,need_watermarker=False)
                        path=url2Path(url=address['pdf_dw_li'])
                        try:
                            email=str(self.get_argument('email'))
                            self.mail=import_mod(from_module='send_email',from_module2='main_server',dir_location='/email/')
                            # mail_server='smtp.gmail.com:587'
                            # mail_server='smtp.mail.yahoo.com:587',user ='soheil_paper' ,
                            # password='32913291'
                            # self.mail(mail_server='smtp.mail.yahoo.com:587',user ='soheil_paper' ,
                            #      password='32913291',name ='Free',to_name ='our Guest',to_email =email,
                            #      subject ='Download succesfully' , message ='This is your file requested is in Atachment',attachments =[path])
                            self.mail(mail_server='127.0.0.1:1025',user ='soheil_paper' ,
                                      password='32913291',name ='Free',to_name ='our Guest',to_email =email,
                                      subject ='Download succesfully' , message ='This is your file requested is in Atachment',attachments =[path])
                            address['email']=email
                        except:
                            address['email']=''

                            # address=core().main(url=url_to_download,need_watermarker=True)
                        url=address['url']
                        address['ip']=ip
                        war_path=address['pdf_dw_Wr_li']
                        pdf_path=address['pdf_dw_li']
                        address['time']=str(round( time.time() - time_diff, 2))
                        address['done']=1
                        done=1
                        print '\n'+address['time']
                if done==0:
                    address['ip']=ip
                    address['url']=''
                    address['pdf_dw_Wr_li']=''
                    address['pdf_dw_li']=''
                    address['time']=str(round( time.time() - time_diff, 2))
                    address['done']=0

                self.render('done.html',pdf_path=address['pdf_dw_li'], url=address['url'],war_path=address['pdf_dw_Wr_li'] ,email=address['email'],ip=address['ip'],time=address['time'])
            else:
                pass
                self.render('invalid_url.html')

        except:
            pass
            self.render('index.html')
        # yield address
        # self.render('done.html',pdf_path=address['pdf_dw_li'], url=address['url'],war_path=address['pdf_dw_Wr_li'] ,email=address['email'],ip=address['ip'],time=address['time'])

        print 'post done'
        # self.finish()
        return address


application = tornado.web.Application([
    (r"/", GenAsyncHandler),
    (r"/download/", DownloadHandler),
    ])

if __name__ == "__main__":
    application.listen(8888,'127.0.0.1')
    tornado.ioloop.IOLoop.instance().start()

