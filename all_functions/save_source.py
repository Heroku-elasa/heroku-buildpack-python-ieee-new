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
import os, re, errno
import urllib
import urllib2, urlparse
# from urlparse import urlparse as urlparse2
# from hurry.filesize import size


print "Content-type: text/html\n"
print "this is running"


class PDF_File:
    def __init__(self,url='',PDF_Dir='',Watermarked_PDF_Files_Dir=''):

        CurrentDir = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
        if PDF_Dir=='':PDF_Dir=CurrentDir+'/PDF_Files'
        if Watermarked_PDF_Files_Dir=='':Watermarked_PDF_Files_Dir=CurrentDir+'/static'
        self.Watermarked_PDF_Dir=Watermarked_PDF_Files_Dir
        self.PDF_Files_Dir=PDF_Dir
        self.url = url
        # self.make_sure_path_exists( self.PDF_Files_Dir, self.Watermarked_PDF_Dir)

    def make_sure_path_exists(self, pdf_dir='', water_dir=''):
        if pdf_dir=='':
            pdf_dir=self.PDF_Files_Dir+"/"
        if water_dir=='':
            water_dir=self.Watermarked_PDF_Dir+"/"
        # fo = os.getcwd().replace('\\','/')
        # CurrentDir = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
        # os.chdir(CurrentDir)
        try:
            if not os.path.isdir(water_dir):
                os.mkdir(water_dir)
        except OSError as exception:
            if exception.errno != errno.EEXIST: pass
        try:
            if not os.path.isdir(pdf_dir):os.mkdir( pdf_dir)
        except:
            pass
        # os.chdir(fo)


    def filename(self, pdf_url0):
        pdf_url = str(pdf_url0)
        CurrentDir=os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
        if re.findall('/', pdf_url):
            self.suffix = os.path.splitext(pdf_url)[1]
            self.file_name_decode = urllib2.unquote(pdf_url).decode('utf8').split('/')[-1]
            self.filename = urlparse.urlsplit(pdf_url).path.split('/')[-1]
            # self.pdf_Folder_filename = CurrentDir + "/"+self.PDF_Files_Dir+"/" + self.filename
            # self.W_pdf_Folder_filename = CurrentDir + "/"+self.Watermarked_PDF_Dir+"/" + self.filename
            self.pdf_Folder_filename = self.PDF_Files_Dir+"/" + self.filename
            self.W_pdf_Folder_filename =self.Watermarked_PDF_Dir+"/" + self.filename
            self.chdir=CurrentDir
            self.url_watermark="http://free-papers.elasa.ir"
        else:
            self.filename = urlparse.urlsplit(pdf_url).path.split('\\')[-1]
            self.chdir=CurrentDir
            # self.pdf_Folder_filename = CurrentDir+ "/"+self.PDF_Files_Dir+"/" + self.filename
            # self.W_pdf_Folder_filename = CurrentDir + "/"+self.Watermarked_PDF_Dir+"/" + self.filename
            self.pdf_Folder_filename =self.PDF_Files_Dir+"/" + self.filename
            self.W_pdf_Folder_filename =self.Watermarked_PDF_Dir+"/" + self.filename
            self.url_watermark="http://free-papers.elasa.ir"

        return self

    def pdf_cheker(self, pathname): # CHEcking if pdf is Correct
        from pyPdf import PdfFileReader

        pathname = pathname.replace("\\", '/')

        doc = PdfFileReader(file(pathname, "rb"))
        return doc


    def file_save(self, data, folder_name='', pathname2='test.pdf'):
        if folder_name=='':
            folder_name=self.PDF_Files_Dir+'/'
        # CurrentDir=os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
        try:
            f = open(os.path.join(folder_name, pathname2), 'wb')
            f.write(data)
            f.close()
        except:
            self.make_sure_path_exists()
            f = open(os.path.join(folder_name, pathname2), 'wb')
            f.write(data)
            f.close()
        return  folder_name+'/'+ pathname2

    def path2url(self, path, myhost="http://127.0.0.1/cgi-bin2/wrapper%20work" ):
        CurrentDir=os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
        path2 = path.replace(CurrentDir, '')
        link = myhost + urllib.pathname2url(path2)
        return link
        # return urlparse.urljoin('file:', urllib.pathname2url(path))

    def watermark_file(self, packet, text='hello',**kwargs):
        try:
            from reportlab.pdfgen import canvas
        except:
            if not os.path.isdir(os.getcwd().replace('\\','/')+'/PYTHON_EGG_CACHE'):
                os.mkdir(os.getcwd().replace('\\','/')+'/PYTHON_EGG_CACHE')
            os.environ['PYTHON_EGG_CACHE']=os.getcwd().replace('\\','/')+'/PYTHON_EGG_CACHE'
            from reportlab.pdfgen import canvas
        import reportlab.lib.pagesizes as ps
        from reportlab.lib.pagesizes import letter
        try:
            if kwargs['center_text']:
                center_text=kwargs['center_text']
            else:
                center_text=False
        except:
            center_text=False



        data = []
        pack = open(packet, 'a+')

        p = canvas.Canvas(packet, pagesize=letter)
        p.drawString(10, 10, text)
        # data.append(pack)
        # data.append(p)
        if not center_text==False:
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

    def pdf_watermark_fast_sell_cpdf(self, pathname, Wm_f, wt1='',**kwargs):
        try :
            url_watermark=kwargs['url_wtm']
        except:pass


        url_watermark2=url_watermark.replace(".","_")
        url_watermark2=url_watermark2.replace("://","__")
        # CurrentDir=os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
        if wt1 == '':
            import os
            if not os.path.isfile(self.Watermarked_PDF_Dir+"/" + "watermarker_slow"+url_watermark2+".pdf"):
                wt1 = self.watermark_file(self.Watermarked_PDF_Dir+"/" + "watermarker_slow"+url_watermark2+".pdf", url_watermark,center_text=False)
            else:
                wt1=self.Watermarked_PDF_Dir+"/" + "watermarker_slow"+url_watermark2+".pdf"
            # if True:
            #     wt1 = self.watermark_file(self.Watermarked_PDF_Dir+"/" + "watermarker_slow"+url_watermark2+".pdf", url_watermark,center_text=False)

            # cpdf -stamp-on watermark.pdf in.pdf -o out.pdf
            import subprocess

            try:
                home_dir=os.environ['OPENSHIFT_HOMEDIR']
                if os.path.isfile(home_dir+'/app-root/runtime/srv/cpdf/cpdf'):
                    st=home_dir+'/app-root/runtime/srv/cpdf/cpdf -stamp-on '+wt1+ " "+pathname+' -o '+Wm_f
                else:
                    st='/app/all_functions/srv/cpdf/cpdf -stamp-on '+wt1+ " "+pathname+' -o '+Wm_f
            except:
                home_dir='C:/Users/Hamed/IGC/Desktop/CNC DIY/cpdfdemo/cpdf.exe'
                st=home_dir+' -stamp-on '+wt1+ " "+pathname+' -o '+Wm_f

            awk_sort = subprocess.Popen( [st ], stdin= subprocess.PIPE, stdout= subprocess.PIPE,shell=True)
            awk_sort.wait()
            output = awk_sort.communicate()[0]
            print output.rstrip()
        return Wm_f

    def pdf_watermark_fast_first_page(self, pathname, Wm_f, wt1='',**kwargs):
        try :
            url_watermark=kwargs['url_wtm']
        except:pass
        from pyPdf import PdfFileWriter, PdfFileReader
        import StringIO
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter

        packet = StringIO.StringIO()
        # create a new PDF with Reportlab
        can = canvas.Canvas(packet, pagesize=letter)
        can.drawString(10, 100, url_watermark)
        can.save()

        #move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        # read your existing PDF
        existing_pdf = PdfFileReader(file(pathname, "rb"))
        output = PdfFileWriter()
        # add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        # finally, write "output" to a real file
        outputStream = file(Wm_f, "wb")
        # import sys;sys.setrecursionlimit(11500)
        output.write(outputStream)
        outputStream.close()
        return Wm_f

    def pdf_watermark_fast(self, pathname, Wm_f, wt1='',**kwargs):
        try :
            url_watermark=kwargs['url_wtm']
        except:pass

        from pyPdf import PdfFileWriter, PdfFileReader
        # fo=os.getcwd()
        # CurrentDir=os.path.dirname(os.path.realpath(__file__))
        import watter_marker
        url_watermark2=url_watermark.replace(".","_")
        url_watermark2=url_watermark2.replace("://","__")
        # CurrentDir=os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
        if wt1 == '':
            if not os.path.isfile(self.Watermarked_PDF_Dir+"/" + "watermarker_slow"+url_watermark2+".pdf"):
                wt1 = self.watermark_file(self.Watermarked_PDF_Dir+"/" + "watermarker_slow"+url_watermark2+".pdf", url_watermark,center_text=False)
            else:
                wt1=self.Watermarked_PDF_Dir+"/" + "watermarker_fast.pdf"
            if True:
                watermark1 = PdfFileReader(file(wt1, 'rb'))
            else:
                wt1 = self.watermark_file(self.Watermarked_PDF_Dir+"/" + "watermarker_slow"+url_watermark2+".pdf", url_watermark,center_text=False)
                watermark1 = PdfFileReader(file(wt1, 'rb'))
            wtt = watermark1.getPage(0)

        watter_marker.op_w_input(pathname, wt1, Wm_f)
        # Wm_f is full address
        return Wm_f
    #https://www.daniweb.com/software-development/python/threads/427722/convert-pdf-to-image-with-pythonmagick-
    # def pdf_to_image(self,**kwargs):
    #     from pyPdf import PdfFileReader
    #     from PythonMagick import Image
    #     if kwargs:
    #         if 'pdf' in kwargs:pdf_file=kwargs['pdf']
    #         if 'photo' in kwargs:photo_file=kwargs['photo']
    #         else:photo_file=pdf_file.split('/')[-1].split('.')[0]
    #         if 'pages' in kwargs:target_pages=kwargs['pages']
    #         else:pages=0
    #
    #     myfile = PdfFileReader(pdf_file)
    #     pages = myfile.getNumPages()
    #     photos=[]
    #     for i in range(0,target_pages):
    #         im= PythonMagick.Image()
    #         im.density('300')
    #         im .read(myfile.getPage(i+1))
    #         # im.write('file_image{}.png'.format(i+1))
    #         im.write(photo_file+'{}.png'.format(i+1))
    #         photos.append(photo_file+'{'+i+'}.png')
    #     return photos






    def pdf_watermark_slow(self, pathname, Wm_f,  wt1='',**kwargs):
        from pyPdf import PdfFileWriter, PdfFileReader
        try :
            url_watermark=kwargs['url_wtm']
        except:
            pass
        url_watermark2=url_watermark.replace(".","_")
        url_watermark2=url_watermark2.replace("://","__")
        # CurrentDir=os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
        if wt1 == '':
            try:wt1 = self.watermark_file(self.Watermarked_PDF_Dir+"/" + "watermarker_slow_"+url_watermark2+".pdf", url_watermark,center_text=True)
            except:print "erro in writing new watermarker files"
            try:
                if not os.path.isfile(self.Watermarked_PDF_Dir+"/" + "watermarker_slow_"+url_watermark2+".pdf"):
                    wt1 = self.watermark_file(self.Watermarked_PDF_Dir+"/" + "watermarker_slow_"+url_watermark2+".pdf", url_watermark,center_text=True)
                else:
                    wt1=self.Watermarked_PDF_Dir+"/" + "watermarker_slow_"+url_watermark2+".pdf"
                    sa=file(wt1, 'rb')
                    watermark1 = PdfFileReader(sa)
                    wtt = watermark1.getPage(0)
            except:
                print 'if not os.path.isfile(self.Watermarked_PDF_Dir+"/" + "watermarker_slow_"+url_watermark2+".pdf"): is not working'

        else:
            watermark1 = PdfFileReader(wt1)
            wtt = watermark1.getPage(0)
            # wt2=self.watermark_file(pathname,'www.free-papers.tk')

        output = PdfFileWriter()

        # input1 = PdfFileReader(file(pathname, "r"))
        # inf = PdfFileReader(file(pathname, "r")).getDocumentInfo

        # print the title of document1.pdf
        fh=file(pathname, 'rb')
        pdf = PdfFileReader(fh)

        print "title = %s" % (pdf.getDocumentInfo().title)
        f = pdf.getNumPages()
        # j = self.pdf_cheker(pathname)
        wt = watermark1.getPage(0)
        try:
            for i in range(0, pdf.getNumPages()):
                watermark = []
                wt = []
                p = pdf.getPage(i)
                # p.mergePage(wt)
                # output.addPage(p)
                watermark = PdfFileReader(sa)
                # # watermark = watermark1
                wt = watermark.getPage(0)
                wt.mergePage(p)
                output.addPage(wt)

            outputStream = open(Wm_f, 'wb')
            # outputStream=StringIO.StringIO()
            # output.write(open(Wm_f, 'wb'))
            # import sys;sys.setrecursionlimit(11500)
            output.write(outputStream)
            print ('output.write(outputStream) is done'+'wtl is :'+wt1)
            outputStream.close()
        except:
            print ('Please make correct Wattermarket')
            # return address of files
        # Wm_f is full address
        fh.close()
        try:
            sa.close()
        except:pass
        return Wm_f


    def WM_Chk_Pdf(self, pdf_url):
        pdf_dw_Wr_li = pdf_dw_li = []
        localName = self.filename(pdf_url)

        try:

            # doc = self.pdf_cheker(localName.pdf_Folder_filename)
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
            return pdf_dw_li, pdf_dw_Wr_li, localName.pdf_Folder_filename

    def finall_file_saving(self, frontpage, file_name, location0='',no_watermarker=0):
        localName = file_name

        if location0=='':
            location=self.PDF_Files_Dir+'/'
            ## saving file
        else:
            location=location0
        url_watermark=localName.url_watermark
        try:
            if not os.path.isfile(frontpage):
                test=pp
            if no_watermarker==0 and frontpage.endswith('.pdf') :
                pdf_size=(os.path.getsize(frontpage))
                if pdf_size>=190000: # >=190 KB
                    # self.pdf_watermark_fast(localName.pdf_Folder_filename, localName.W_pdf_Folder_filename,url_wtm=url_watermark)
                    try:
                        self.pdf_watermark_fast_sell_cpdf(localName.pdf_Folder_filename, localName.W_pdf_Folder_filename,url_wtm=url_watermark)
                    except:
                        self.pdf_watermark_slow(localName.pdf_Folder_filename, localName.W_pdf_Folder_filename,url_wtm=url_watermark)
                    # self.pdf_watermark_fast_first_page(localName.pdf_Folder_filename, localName.W_pdf_Folder_filename,url_wtm=url_watermark)
                else:
                    self.pdf_watermark_slow(localName.pdf_Folder_filename, localName.W_pdf_Folder_filename,url_wtm=url_watermark)
                # self.pdf_watermark_slow(localName.pdf_Folder_filename, localName.W_pdf_Folder_filename,url_wtm=url_watermark)
                pdf_dw_li = localName.pdf_Folder_filename
                pdf_dw_Wr_li = localName.W_pdf_Folder_filename
            else:

                pdf_dw_li = localName.pdf_Folder_filename
                pdf_dw_Wr_li = ''
        except:
            try:
                if not os.path.isfile(frontpage):
                    pdf = self.file_save(frontpage, location, localName.filename)
                    print "we have saved html to pdf file"
            except:
                pdf = self.file_save(frontpage, location, localName.filename)
                print "we have saved html to pdf file"
            # if len(frontpage)<= 4194304 :# 4*1024*1024=4194304 4MB
            #     doc = self.pdf_cheker(localName.pdf_Folder_filename)
            if no_watermarker==0:
                print "no_watermarker==0"
                if url_watermark!='':
                    # os.remove(location+'/'+localName.filename)
                    pdf_size=(os.path.getsize(localName.pdf_Folder_filename))
                    try:
                        if pdf_size>=190000: # >=190 KB
                            # self.pdf_watermark_fast(localName.pdf_Folder_filename, localName.W_pdf_Folder_filename,url_wtm=url_watermark)
                            try:
                                self.pdf_watermark_fast_sell_cpdf(localName.pdf_Folder_filename, localName.W_pdf_Folder_filename,url_wtm=url_watermark)
                            except:
                                self.pdf_watermark_slow(localName.pdf_Folder_filename, localName.W_pdf_Folder_filename,url_wtm=url_watermark)
                            # self.pdf_watermark_fast_first_page(localName.pdf_Folder_filename, localName.W_pdf_Folder_filename,url_wtm=url_watermark)
                        else:
                            self.pdf_watermark_slow(localName.pdf_Folder_filename, localName.W_pdf_Folder_filename,url_wtm=url_watermark)
                    except:
                        # self.pdf_watermark_slow(localName.pdf_Folder_filename, localName.W_pdf_Folder_filename,url_wtm=url_watermark)
                        self.pdf_watermark_fast_sell_cpdf(localName.pdf_Folder_filename, localName.W_pdf_Folder_filename,url_wtm=url_watermark)



                    # self.pdf_watermark_fast_sell_cpdf(localName.pdf_Folder_filename, localName.W_pdf_Folder_filename,url_wtm=url_watermark)

                    # self.pdf_watermark_slow(localName.pdf_Folder_filename, localName.W_pdf_Folder_filename,url_wtm=url_watermark)
                    pdf_dw_li = localName.pdf_Folder_filename
                    pdf_dw_Wr_li = localName.W_pdf_Folder_filename
                else:
                    pdf_dw_li = localName.pdf_Folder_filename
                    pdf_dw_Wr_li = localName.W_pdf_Folder_filename
                    import shutil
                    shutil.copy2(pdf_dw_li, pdf_dw_Wr_li)
            else:

                pdf_dw_li = localName.pdf_Folder_filename
                pdf_dw_Wr_li = ''
        # sp = self.path2url(pdf_dw_li)

        # pdf_dw_li =self.path2url(localName.pdf_Folder_filename)
        # pdf_dw_Wr_li = self.path2url(localName.W_pdf_Folder_filename)

        # print "fetching main paper link url ...\n\t%s" % pdf_dw_li[:]
        # print "fetching waterarker paper link url ...\n\t%s" % pdf_dw_Wr_li
        return pdf_dw_li, pdf_dw_Wr_li


if __name__ == '__main__':
    #HOW TO USE:
    url = "http://127.0.0.1/1752-153X-2-5%20-%20Copy.pdf"
    url = "http://127.0.0.1/1-s2.0-S0142061516305774-main.pdf"
    # url='http://ieeexplore.ieee.org/xpl/articleDetails.jsp?tp=&arnumber=6180383&queryText%3Dpower' #91 KB
    url_watermark="http://test"
    file_name = PDF_File().filename(url)

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

    try:
        html=os.environ['OPENSHIFT_HOMEDIR']+"app-root/runtime/srv/tornado3/PDF_Files/1-s2.0-S0142061516305774-main.pdf"
    except:
        CurrentDir = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
        html=CurrentDir+"/PDF_Files/1-s2.0-S0142061516305774-main.pdf"
        # dir=CurrentDir+"/htmls/paper.txt"
        # f = open(dir, 'r')
        # html=f.read()
        # f.close()

    # pdf='E:/Program Files win 7 2nd/Ampps/www/cgi-bin2/wrapper work/all_functions/PDF_Files/1752-153X-2-5%20-%20Copy.pdf'
    # from  download_mozilla import web
    # html=web().download(url)

    pdf_dw_li, pdf_dw_Wr_li = PDF_File(url).finall_file_saving(html, file_name)
                            


    




    
