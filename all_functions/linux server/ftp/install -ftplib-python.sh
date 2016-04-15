#!/bin/sh
cat <<'EOF'  >> ftp_lib.py
def timeStamp():
    """returns a formatted current time/date"""
    import time
    return str(time.strftime("%a %d %b %Y %I:%M:%S %p"))



from fabric.api import run
def host_type():
    run('uname -s')




if __name__ == '__main__':
    import os

    # ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python my_ftp.py  --url 'http://restss2.frogcp.com/tmp/rapiech/files/tb_blog_starter_beffor_ieee.zip' -f 'http://azmon.fulba.com' --user 'u981025896:ss123456' --File_name 'elec-lab.zip'
    # ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python my_ftp.py   -f 'http://azmon.fulba.com' --user 'u981025896:ss123456' --File_name 'elec-lab.zip'
# ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python my_ftp.py  --url 'http://restss2.frogcp.com/tmp/rapiech/files/tb_blog_starter_beffor_ieee.zip' -f 'http://power-market-lab.tk' --user 'u683103535:ss123456'
# ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python my_ftp.py  --url 'http://restss2.frogcp.com/tmp/rapiech/files/tb_blog_starter_beffor_ieee.zip' -f 'http://mygly.allalla.com' --user 'u811535169:ss123456'

# ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python my_ftp.py  --url 'https://www.dropbox.com/s/yk8eaijvtv6wr7l/tb_blog_starter_beffor_ieee.zip?dl=1' -f 'http://mygly.allalla.com' --user 'u811535169:ss123456' -i '/s/'


    from optparse import OptionParser
    parser = OptionParser(description=__doc__)
    CurrentDir = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
    help1='Address url file name to be downloaded like:"www.google.com"\n'+ \
          "Please make attention 'www.google.com' is risky use  only with"+'"blabla"'
    parser.add_option('-u','--url',type='string', dest='url', help=help1)#,default='http://pr8ss.tk/web/tmp/present_sp_98.pdf')
    #
    parser.add_option('-n','--File_name', dest='File_name', help=' File_name')#,default='http://irancall.tk')
    # parser.add_option('-s','--user', dest='user_name', help='user & password of ftp like (user:password)',default='u967933577:ss123456')


    parser.add_option('-f','--ftp', dest='ftp_url', help=' ftp url  name to be download like:121.121.21.21',default='http://azmon.fulba.com')
    parser.add_option('-s','--user', dest='user_name', help='user & password of ftp like (user:password)',default='u981025896:ss123456')

    parser.add_option('-i', dest='input_fname', help='folder name to file been uploaded',default='/test21/')
    options, args = parser.parse_args()
    # options.url='http://pr8ss.tk/web/tmp/present_sp_98.pdf'
    if not options.url:
        USERNAME =options.user_name.split(':')[0]
        PASSWORD = options.user_name.split(':')[1]
        file_name=options.File_name
    if options.url:
        server_address_com = options.ftp_url
        # server_address_com = '31.170.166.100'
        USERNAME =options.user_name.split(':')[0]
        PASSWORD = options.user_name.split(':')[1]

        # USERNAME = 'u391528959';
        # server_address_com = 'http://irancall.tk'
        # USERNAME = 'u967933577'
        # PASSWORD = 'ss123456';

        # import wget
        # url = options.url
        # file_name = wget.download(url)

        if True:
            import requests

            url = options.url
            r = requests.get(url)
            print len(r.content)
            # response = urlopen(r)

            #http://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python
            import urllib2

            url = options.url
            file_name = url.split('/')[-1]
            u = urllib2.urlopen(url)
            f = open(file_name, 'wb')
            meta = u.info()
            file_size = int(meta.getheaders("Content-Length")[0])
            print "Downloading: %s Bytes: %s" % (file_name, file_size)

            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break

                file_size_dl += len(buffer)
                f.write(buffer)
                status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                status = status + chr(8)*(len(status)+1)
                print status,

            f.close()


        # #http://www.blog.pythonlibrary.org/2012/06/07/python-101-how-to-download-a-file/
        # import urllib
        # import urllib2
        # import requests
        #
        # url = 'http://www.blog.pythonlibrary.org/wp-content/uploads/2012/06/wxDbViewer.zip'
        # url = options.url
        #
        # print "downloading with urllib"
        #
        # urllib.urlretrieve(url, "code.zip")
        #
        # print "downloading with urllib2"
        # f = urllib2.urlopen(url)
        # data = f.read()
        # with open("code2.zip", "wb") as code:
        #     code.write(data)
        #
        # print "downloading with requests"
        # r = requests.get(url)
        # with open("code3.zip", "wb") as code:
        #     code.write(r.content)


        # localpath = os.getcwd().replace("\\", "/") +'/'+ 'mediafire';
        # for root, dirs, files in os.walk(localpath):
        #     print dirs

        localpath = os.getcwd().replace("\\", "/") +'/'+ file_name;
        main_root=localpath.split(localpath.split('/')[-1])[0]

        remotepath = options.input_fname + localpath.split('/')[-1]

        # end_loop=True
        # import ftplib
        # session = ftplib.FTP(server_address_com, USERNAME, PASSWORD)
        # while end_loop==True:
        #     for root, dirs, files in os.walk(main_root):
        #
        #
        #         s=0
        #         for dir2 in dirs:
        #             s=1
        #             if root!=main_root:
        #                 remotepath = options.input_fname + main_root.split(root)[1]+localpath.split('/')[-1]
        #             else:
        #                 remotepath = options.input_fname + localpath.split('/')[-1]
        #                 class_my_ftp().my_ftplib_folder(server_address_com, USERNAME, PASSWORD, localpath, remotepath,session)
        #         for file2 in files:
        #             if root!=main_root:
        #                 remotepath = options.input_fname + main_root.split(root)[1]+localpath.split('/')[-1]
        #             else:
        #                 remotepath = options.input_fname + localpath.split('/')[-1]
        #             class_my_ftp().my_ftplib(server_address_com, USERNAME, PASSWORD, localpath, remotepath,session)
        #         if dir2


        deleteAfterCopy = False 	#set to true if you want to clean out the remote directory
        onlyNewFiles = False			#set to true to grab & overwrite all files locally
        # moveFTPFiles(server_address_com,USERNAME,PASSWORD,remotepath,localpath,deleteAfterCopy,onlyNewFiles)
        upload_to_FTPFiles(server_address_com,USERNAME,PASSWORD,remotepath,localpath,deleteAfterCopy,onlyNewFiles)
        # class_my_ftp().my_ftplib(server_address_com, USERNAME, PASSWORD, localpath, remotepath)
        os.remove(localpath)

    # class_my_ftp().my_fabric(server_address_com, USERNAME, PASSWORD, localpath, remotepath)
    # class_my_ftp().paramiko_ftp(server_address_com, USERNAME, PASSWORD, localpath, remotepath)




#
# server_address_com = 'call-info.tk'
# server_address_com = '31.170.166.100'
# USERNAME = 'u391528959';
# server_address_com = 'http://irancall.tk'
# USERNAME = 'u967933577'
# PASSWORD = 'ss123456';
#
# localpath = os.getcwd().replace("\\", "/") + '/small_test_file.txt';
# # remotepath = '/ss/' + localpath.split('/')[-1]
# remotepath = '/sd/s/ss/' + localpath.split('/')[-1]
# fh = open("small_test_file.txt", "w")
# fh.write("Small test file")
# fh.close()
# class_my_ftp().my_ftplib(server_address_com, USERNAME, PASSWORD, localpath, remotepath)
#
# # class_my_ftp().my_fabric(server_address_com, USERNAME, PASSWORD, localpath, remotepath)
# # class_my_ftp().paramiko_ftp(server_address_com, USERNAME, PASSWORD, localpath, remotepath)
#

EOF
#wget http://test-22.4rog.in/tmp/rapiech/files/elec-lab.zip
#${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python ftp_lib.py  --url 'http://test-22.4rog.in/tmp/rapiech/files/elec-lab.zip' -f '216.218.192.170' --user 'soheils5:ss123456' -i '/public_html/test'
# ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python ftp_lib.py   -f 'http://azmon.fulba.com' --user 'u981025896:ss123456' --File_name 'elec-lab.zip'
#rm -rf elec-lab.zip