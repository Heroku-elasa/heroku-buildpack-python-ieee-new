#!/usr/bin/env python
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
import os
from sets import Set
class class_my_ftp(object):
    def paramiko_ftp(self, hostname, username, password, localpath, remotepath):

        import os
        import crypto
        import sys

        sys.modules['Crypto'] = crypto
        import paramiko

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(hostname, username=username, password=password)
            sftp = ssh.open_sftp()
            # localpath = '/home/e100075/python/ss.txt'
            # remotepath = '/home/developers/screenshots/ss.txt'
            sftp.put(localpath, remotepath)
            sftp.close()
            ssh.close()
            return remotepath
        except:

            return 'None'

    def my_fabric(self, ftp_host_name, username, password, localpath, remotepath):
        from fabric.api import run, env, put

        env.user = username
        env.hosts = ftp_host_name     # such as ftp.google.com

        # assuming i have wong_8066.zip in the same directory as this script
        # put('wong_8066.zip', '/www/public/wong_8066.zip')
        # put(localpath, remotepath + localpath.split('/')[-1])
        put(localpath, remotepath)

    def my_ftplib(self, server_address_com_0, USERNAME, PASSWORD, localpath, remotepath):
        import ftplib
        # session = ftplib.FTP('server.address.com','USERNAME','PASSWORD')
        server_address_com = server_address_com_0.replace('http://', '').replace('https://', '')
        # session = ftplib.FTP(server_address_com, USERNAME, PASSWORD)
        # with open(localpath, 'rb') as file:
        #
        #     file_2 = remotepath.split('/')[-1]
        #     dir = remotepath.split(file_2)[0]
        #     cuurent_dir=session.pwd()
        #     print(cuurent_dir) # Get the current path - this does work either
        #     mkdir=session.mkd(cuurent_dir+'/s25/')
        #     ftp_list=session.retrlines('LIST')
        #     test=session.cwd(cuurent_dir+'/s25/')
        #     print(session.pwd()) # Get the current path - this does work either
        #     do=session.storbinary('STOR ' + remotepath.split('/')[-1], file,8192)     # send the file
        try:
            session = ftplib.FTP(server_address_com, USERNAME, PASSWORD)
            print session.getwelcome()

            # file = open('kitten.jpg','rb')                  # file to send
            # session.storbinary('STOR kitten.jpg', file)     # send the file
            file = open(localpath, 'rb')                  # file to send
            # dirs = session.dir('-a -l ')
            file_2 = remotepath.split('/')[-1]
            dir_main = remotepath.split(file_2)[0]
            dir = dir_main[1:]
            # try:
            #     dir2 = dir.split('/')[0]
            # except:
            #     dir2 = dir
            # try:
            #     dir_r = dir.split('/')[1]
            # except:
            #     dir_r=''
            dir2=dir;dir_r=dir
            cuurent_dir = session.pwd()
            f0 = 0;
            try:
                test = session.cwd(cuurent_dir + '/' + dir)
                do=False
            except:
                do=True
            while do:
                try:
                    dir2 = dir_r.split('/',1)[0]
                except:
                    dir2 = ''
                try:
                    dir_r = dir_r.split('/',1)[1]
                except:
                    dir_r=''
                cuurent_dir = session.pwd()
                print(cuurent_dir) # Get the current path - this does work either
                filelist = [] #to store all files
                session.retrlines('LIST', filelist.append)    # append to list
                f0 = 0;
                if dir2!='':
                    for f in filelist:
                        if dir2  in f:
                            f0 = 1
                            break
                    if f0==0:
                        mkdir = session.mkd(dir2)
                    test = session.cwd(cuurent_dir + '/' + dir2)
                else:
                    do = False


            if f0 == 0:
                # test = session.cwd(cuurent_dir + '/' + dir)
                do = session.storbinary('STOR ' + file_2, file)     # send the file
                # session.storbinary('RETR %s' % remotepath, file)     # send the file
                file.close()                                    # close file and FTP
                session.quit()
                return server_address_com_0 + remotepath

        except:
            return 'None'

    def my_ftplib_tofolder(self, server_address_com_0, USERNAME, PASSWORD, localpath, remotepath):
        import ftplib
        # session = ftplib.FTP('server.address.com','USERNAME','PASSWORD')
        server_address_com = server_address_com_0.replace('http://', '').replace('https://', '')
        # session = ftplib.FTP(server_address_com, USERNAME, PASSWORD)
        # with open(localpath, 'rb') as file:
        #
        #     file_2 = remotepath.split('/')[-1]
        #     dir = remotepath.split(file_2)[0]
        #     cuurent_dir=session.pwd()
        #     print(cuurent_dir) # Get the current path - this does work either
        #     mkdir=session.mkd(cuurent_dir+'/s25/')
        #     ftp_list=session.retrlines('LIST')
        #     test=session.cwd(cuurent_dir+'/s25/')
        #     print(session.pwd()) # Get the current path - this does work either
        #     do=session.storbinary('STOR ' + remotepath.split('/')[-1], file,8192)     # send the file
        try:
            session = ftplib.FTP(server_address_com, USERNAME, PASSWORD)
            print session.getwelcome()

            # file = open('kitten.jpg','rb')                  # file to send
            # session.storbinary('STOR kitten.jpg', file)     # send the file
            # file = open(localpath, 'rb')                  # file to send
            # dirs = session.dir('-a -l ')
            file_2 = remotepath.split('/')[-1]
            dir_main = remotepath.split(file_2)[0]
            dir = dir_main[1:]
            # try:
            #     dir2 = dir.split('/')[0]
            # except:
            #     dir2 = dir
            # try:
            #     dir_r = dir.split('/')[1]
            # except:
            #     dir_r=''
            dir2=dir;dir_r=dir
            cuurent_dir = session.pwd()
            f0 = 0;
            try:
                test = session.cwd(cuurent_dir + '/' + dir)
                do=False
            except:
                do=True
            while do:
                try:
                    dir2 = dir_r.split('/',1)[0]
                except:
                    dir2 = ''
                try:
                    dir_r = dir_r.split('/',1)[1]
                except:
                    dir_r=''
                cuurent_dir = session.pwd()
                print(cuurent_dir) # Get the current path - this does work either
                filelist = [] #to store all files
                session.retrlines('LIST', filelist.append)    # append to list
                f0 = 0;
                if dir2!='':
                    for f in filelist:
                        if dir2  in f:
                            f0 = 1
                            break
                    if f0==0:
                        mkdir = session.mkd(dir2)
                    test = session.cwd(cuurent_dir + '/' + dir2)
                else:
                    do = False



            if f0 == 0:
                from sets import Set
                localPath=localpath
                lFileSet = Set(os.listdir(localPath))

                file = open(localpath, 'rb')                  # file to send
                # test = session.cwd(cuurent_dir + '/' + dir)
                do = session.storbinary('STOR ' + file_2, file)     # send the file
                # session.storbinary('RETR %s' % remotepath, file)     # send the file
                file.close()                                    # close file and FTP
                session.quit()
                return server_address_com_0 + remotepath

        except:
            return 'None'



    def my_ftplib_folder(self, server_address_com_0, USERNAME, PASSWORD, localpath, remotepath,session):
        import ftplib
        # session = ftplib.FTP('server.address.com','USERNAME','PASSWORD')
        server_address_com = server_address_com_0.replace('http://', '').replace('https://', '')
        # session = ftplib.FTP(server_address_com, USERNAME, PASSWORD)
        # with open(localpath, 'rb') as file:
        #
        #     file_2 = remotepath.split('/')[-1]
        #     dir = remotepath.split(file_2)[0]
        #     cuurent_dir=session.pwd()
        #     print(cuurent_dir) # Get the current path - this does work either
        #     mkdir=session.mkd(cuurent_dir+'/s25/')
        #     ftp_list=session.retrlines('LIST')
        #     test=session.cwd(cuurent_dir+'/s25/')
        #     print(session.pwd()) # Get the current path - this does work either
        #     do=session.storbinary('STOR ' + remotepath.split('/')[-1], file,8192)     # send the file


        try:
            # session = ftplib.FTP(server_address_com, USERNAME, PASSWORD)
            print session.getwelcome()

            # file = open('kitten.jpg','rb')                  # file to send
            # session.storbinary('STOR kitten.jpg', file)     # send the file

            # file = open(localpath, 'rb')                  # file to send
            # dirs = session.dir('-a -l ')
            file_2 = remotepath.split('/')[-1]
            dir_main = remotepath.split(file_2)[0]
            dir = dir_main[1:]
            # try:
            #     dir2 = dir.split('/')[0]
            # except:
            #     dir2 = dir
            # try:
            #     dir_r = dir.split('/')[1]
            # except:
            #     dir_r=''
            dir2=dir;dir_r=dir
            cuurent_dir = session.pwd()
            f0 = 0;
            try:
                test = session.cwd(cuurent_dir + '/' + dir)
                do=False
            except:
                do=True
            while do:
                try:
                    dir2 = dir_r.split('/',1)[0]
                except:
                    dir2 = ''
                try:
                    dir_r = dir_r.split('/',1)[1]
                except:
                    dir_r=''
                cuurent_dir = session.pwd()
                print(cuurent_dir) # Get the current path - this does work either
                filelist = [] #to store all files
                session.retrlines('LIST', filelist.append)    # append to list
                f0 = 0;
                if dir2!='':
                    for f in filelist:
                        if dir2  in f:
                            f0 = 1
                            break
                    if f0==0:
                        mkdir = session.mkd(dir2)
                    test = session.cwd(cuurent_dir + '/' + dir2)
                else:
                    do = False


            # if f0 == 0:
            #     # test = session.cwd(cuurent_dir + '/' + dir)
            #     do = session.storbinary('STOR ' + file_2, file)     # send the file
            #     # session.storbinary('RETR %s' % remotepath, file)     # send the file
            #     file.close()                                    # close file and FTP
            #     session.quit()
            #     return server_address_com_0 + remotepath
            return server_address_com_0 + remotepath

        except:
            return 'None'





def moveFTPFiles(serverName,userName,passWord,remotePath,localPath,deleteRemoteFiles=False,onlyDiff=False):
    """Connect to an FTP server and bring down files to a local directory"""
    import os
    from sets import Set
    from ftplib import FTP
    # import ftplib
    server_address_com = serverName.replace('http://', '').replace('https://', '')
    # ftp = ftplib.FTP(serverName, userName, passWord)
    # ftp = FTP(serverName, userName, passWord)
    try:
        ftp = FTP(server_address_com)
    except:
        print "Couldn't find server"
    ftp.login(userName,passWord)
    print ftp.getwelcome()


    file_2 = remotepath.split('/')[-1]
    dir_main = remotepath.split(file_2)[0]
    dir = dir_main[1:]

    dir2=dir;dir_r=dir
    cuurent_dir = ftp.pwd()
    f0 = 0;
    try:
        test = ftp.cwd(cuurent_dir + '/' + dir)
        do=False
    except:
        do=True
        ftp.cwd(cuurent_dir)
    try:
        print "Connecting..."
        if onlyDiff:
            lFileSet = Set(os.listdir(localPath))
            rFileSet = Set(ftp.nlst())
            transferList = list(rFileSet - lFileSet)
            print "Missing: " + str(len(transferList))
        else:
            transferList = ftp.nlst()
        delMsg = ""
        filesMoved = 0
        for fl in transferList:
            # create a full local filepath
            localFile = localPath + fl
            grabFile = True
            if grabFile:
                #open a the local file
                fileObj = open(localFile, 'wb')
                # Download the file a chunk at a time using RETR
                ftp.retrbinary('RETR ' + fl, fileObj.write)
                # Close the file
                fileObj.close()
                filesMoved += 1

            # Delete the remote file if requested
            if deleteRemoteFiles:
                ftp.delete(fl)
                delMsg = " and Deleted"

        print "Files Moved" + delMsg + ": " + str(filesMoved) + " on " + timeStamp()
    except:
        print "Connection Error - " + timeStamp()
    ftp.close() # Close FTP connection
    ftp = None


def upload_to_FTPFiles(ftp,remotePath,localPath,deleteRemoteFiles=False,onlyDiff=False):
    lFileSet = Set(os.listdir(localPath))
    # for root, dirs, files in os.walk('path/to/local/dir'):
    for root, dirs, files in os.walk(localPath):
        dr=[]
        for fname in files:
            full_fname = os.path.join(root, fname)
            ftp.storbinary('STOR remote/dir' + fname, open(full_fname, 'rb'))
        for dir in dirs:
            cuurent_dir = ftp.pwd()
            file_2 = remotepath.split('/')[-1]
            # test = ftp.cwd(cuurent_dir + '/' + dir)
            ftp.mkd(cuurent_dir + '/' + dir)
            dr.append(dir)

    return dir


def upload_to_FTPFiles(serverName,userName,passWord,remotePath,localPath,deleteRemoteFiles=False,onlyDiff=False):
    """Connect to an FTP server and bring down files to a local directory"""

    from ftplib import FTP
    # import ftplib
    server_address_com = serverName.replace('http://', '').replace('https://', '')
    # ftp = ftplib.FTP(serverName, userName, passWord)
    # ftp = FTP(serverName, userName, passWord)
    try:
        ftp = FTP(server_address_com)
    except:
        print "Couldn't find server"
    ftp.login(userName,passWord)
    print ftp.getwelcome()


    file_2 = remotepath.split('/')[-1]
    dir_main = remotepath.split(file_2)[0]
    dir = dir_main[1:]

    dir2=dir;dir_r=dir
    cuurent_dir = ftp.pwd()
    f0 = 0;
    try:
        test = ftp.cwd(cuurent_dir + '/' + dir)
        do=False
    except:
        do=True
        ftp.cwd(cuurent_dir)
    try:
        print "Connecting..."
        if onlyDiff:
            lFileSet = Set(os.listdir(localPath))
            rFileSet = Set(ftp.nlst())
            transferList = list(rFileSet - lFileSet)
            print "Missing: " + str(len(transferList))
        else:
            transferList = Set(os.listdir(localPath))
            # transferList = ftp.nlst()
        delMsg = ""
        filesMoved = 0
        do=True
        while do:
            transferList = Set(os.listdir(localPath))
            file_2 = remotepath.split('/')[-1]
            for fl in transferList:
                # create a full local filepath

                localFile = localPath +'/'+ fl
                if os.path.isfile(localFile):
                    grabFile = True
                    if grabFile:
                        #open a the local file
                        # fileObj = open(localFile, 'rb')
                        # # Download the file a chunk at a time using RETR
                        # ftp.retrbinary('RETR ' + fl, fileObj.write)
                        # # Close the file
                        # fileObj.close()

                        file = open(localFile, 'rb')
                        do = ftp.storbinary('STOR ' + file_2, file)     # send the file
                        # session.storbinary('RETR %s' % remotepath, file)     # send the file
                        file.close()                                    # close file and FTP
                if os.path.isdir(localFile):
                    dr=upload_to_FTPFiles(ftp,remotePath,localFile,deleteRemoteFiles=False,onlyDiff=False)
                    while True:
                        for d in dr:
                            da=upload_to_FTPFiles(ftp,remotePath,localFile,deleteRemoteFiles=False,onlyDiff=False)
                            if da!=[]:
                                localFile=localFile+'/'



                    filesMoved += 1

                        # Delete the remote file if requested
                    if deleteRemoteFiles:
                        ftp.delete(fl)
                        delMsg = " and Deleted"

        print "Files Moved" + delMsg + ": " + str(filesMoved) + " on " + timeStamp()
    except:
        print "Connection Error - " + timeStamp()
    ftp.close() # Close FTP connection
    ftp = None

def timeStamp():
    """returns a formatted current time/date"""
    import time
    return str(time.strftime("%a %d %b %Y %I:%M:%S %p"))



# from fabric.api import run
# def host_type():
#     run('uname -s')




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
    parser.add_option('-n','--File_name',type='string', dest='File_name', help=' File_name')#,default='http://irancall.tk')
    # parser.add_option('-s','--user', dest='user_name', help='user & password of ftp like (user:password)',default='u967933577:ss123456')


    parser.add_option('-f','--ftp', dest='ftp_url', help=' ftp url  name to be download like:121.121.21.21',default='http://azmon.fulba.com')
    parser.add_option('-s','--user', dest='user_name', help='user & password of ftp like (user:password)',default='u981025896:ss123456')

    parser.add_option('-i', dest='input_fname', help='folder name to file been uploaded',default='/test21/')
    options, args = parser.parse_args()
    # options.url='http://pr8ss.tk/web/tmp/present_sp_98.pdf'
    # options.File_name='d'
    if options.File_name:
        file_name=options.File_name

        USERNAME =options.user_name.split(':')[0]
        PASSWORD = options.user_name.split(':')[1]
    elif options.url:
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

    if True:
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
