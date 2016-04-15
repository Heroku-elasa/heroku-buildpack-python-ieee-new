sendmail -f "elsa.group@gmail.com" -t "soheil_paper@yahoo.com" -m "backup" -u "communiuty"   -a "/tmp/Forum-*.sql.gz" 

mkdir /tmp/email
cd /tmp/email
#mkdir /tmp/email/db
#cd /tmp/email/db
#mysql  -u $OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD  p1resta4shop3 > p1resta4shop3new.sql
nohup sh -c " mysql -f -u $OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD  p1resta4shop3 > p1resta4shop3.sql"  > $OPENSHIFT_LOG_DIR/mysql.log /dev/null 2>&1 & 
nohup sh -c " mysql -f -u $OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD  dr2omnia > dr2omnia.sql"  > $OPENSHIFT_LOG_DIR/mysql.log /dev/null 2>&1 & 

cd /tmp
zip -r    p1resta4shop34new3.zip  p1resta4shop34new3.sql

cd /tmp/email
zip -r    p1resta4shop3.zip  p1resta4shop3.sql
zip -r sites.zip  $HOME/app-root/data/sites/
nohup sh -c " zip -r shopping.zip $HOME/app-root/runtime/repo/php/"  > $OPENSHIFT_LOG_DIR/zipping_conf.log /dev/null 2>&1 &  
 #zip -r -s 10m vbuletin-4-1-2.zip $HOME/app-root/runtime/repo/php/
 
 #cat vbuletin-4-1-2* vbuletin-4-1-2* vbuletin-4-1-2* >vbuletin-4-1-2-final.zip
#gzip -c vbuletin-4-1-2.zip | split -b 10MiB - vbuletin-4-1-2.gz_


mkdir /tmp/db
cd /tmp/db
mysql  -u $OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD  p1resta4shop3 > p1resta4shop3.sql
mysql  -u $OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD  dr2omnia > dr2omnia.sql

cd


#sendmail -f "elsa.group@gmail.com" -t "soheil_paper@yahoo.com" -m "backup" -u "communiuty"   -a "/tmp/Forum-*.sql.gz" 

${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install pyftpsync

cd /tmp

cat << 'EOF' > ftp_sync2.py
from ftpsync.synchronizers import DownloadSynchronizer, UploadSynchronizer,BiDirSynchronizer

from ftpsync.targets import FsTarget #, UploadSynchronizer, DownloadSynchronizer
from ftpsync.ftp_target import FtpTarget
import os

env_var = os.environ['OPENSHIFT_HOMEDIR']
#local = FsTarget(env_var+"/app-root/runtime/repo/php/")
local = FsTarget('/tmp/')

passwd = "ss123456"

ip='f12-preview.atspace.me';user='2025575';#  sa1sss.atspace.cc soheil_paper@yahoo.om

#ip='s156.eatj.com';user='ssasa';#  sa1sss.atspace.cc soheil_paper@yahoo.om
ip='ftp.ucq.me';user='ucq_17120729';#  www.ftp22.ucq.me soheil_paper@yahoo.om
ip='s156.eatj.com';user='ssasa';#  http://s156.eatj.com soheil_paper@yahoo.om
ip='f13-preview.awardspace.net';user='2026604';passwd='@SSss123456'#  http://s156.eatj.com soheil_paper@yahoo.om


remote = FtpTarget("/home/www/", ip,21, user, passwd)
remote = FtpTarget("/s1", ip,21, user, passwd)
#remote = FtpTarget("/work", ip,21, user, passwd)

opts = {"force": False, "delete_unmatched": False, "verbose": 3, "execute": True, "dry_run" : False}

s = UploadSynchronizer(local, remote, opts)
#s = DownloadSynchronizer(local, remote, opts)

s.run()
stats = s.get_stats()
print(stats)
EOF

nohup sh -c " ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python ftp_sync2.py"> $OPENSHIFT_LOG_DIR/python_ftp_sync2.log /dev/null 2>&1 &  
#tail -f  $OPENSHIFT_LOG_DIR/python_ftp_sync2.log


cd /tmp
${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install -U setuptools
${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install dropbox
cd ~/app-root/runtime/repo/php
cat << 'EOF' > my_dropbox.py
class main_dropbox:
    def __init__(self,app_key,app_secret,access_token,loalpath,remotepath):
        self.app_key=app_key;self.app_secret=app_secret;
        self.access_token=access_token;
        self.loalpath=loalpath;self.remotepath=remotepath
    def main_dropbox(self,localpath,remotepath):

        import dropbox
        from dropbox import session
        # # from session import BaseSession
        # s=session.BaseSession

        # Get your app key and secret from the Dropbox developer website
        # app_key = 'INSERT_APP_KEY'
        # app_secret = 'INSERT_APP_SECRET'
        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(self.app_key, self.app_secret)

        # Have the user sign in and authorize this token
        authorize_url = flow.start()
        print '1. Go to: ' + authorize_url
        print '2. Click "Allow" (you might have to log in first)'
        print '3. Copy the authorization code.'

        # code = raw_input("Enter the authorization code here: ").strip()
        # # This will fail if the user enters an invalid authorization code
        # access_token, user_id = flow.finish(code)

        client = dropbox.client.DropboxClient(self.access_token)
        print 'linked account: ', client.account_info()

        # fh = open("small_test_file.txt","w")
        # fh.write("Small test file")
        # fh.write("Small test file")
        # fh.close()


        try:
	        CurrentDir=os.path.dirname(os.path.realpath(__file__))
	        Parent_Dir=os.path.abspath(os.path.join(CurrentDir, '..'))
        # Destination= os.path.abspath(os.path.join(Parent_Dir, '..'))

        except:
	        CurrentDir=os.getcwd()
	        Parent_Dir=os.path.abspath(os.path.join(CurrentDir, '..'))

        for root, dirs, files in os.walk(CurrentDir):
            curent_path0=root.split(Parent_Dir)[1]+'/'
            curent_path=curent_path0.replace('\\','/')
            root=root.replace('\\','/')
            for dir2 in dirs:
                # if os.path.isdir(Destination+ curent_path+dir2):
                # client.file_create_folder('/'+dir2)
                pass

        #uploading file
        f = open(localpath, 'rb')
        response = client.put_file(remotepath, f,True)
        print "/n uploaded:", response
        f.close()
        # link=dropbox.client.DropboxClient(access_token).share('/magnum-opus.txt')
        link=client.share(remotepath)
        print "/n share_link:", link
        return link

    def download(self):
        #downloading files
        f, metadata = client.get_file_and_metadata('/magnum-opus.txt')
        out = open('magnum-opus.txt', 'wb')
        out.write(f.read())
        out.close()
        print metadata


def my_dropbox(email, password, localpath, remotepath):
    from dbupload import DropboxConnection
    from getpass import getpass

    # email = raw_input("Enter Dropbox email address:")
    # password = getpass("Enter Dropbox password:")

    # Create a little test file
    # fh = open("small_test_file.txt","w")
    # fh = open("small_test_file.txt","w")
    # fh.write("Small test file")
    # fh.write("Small test file")
    # fh.close()
    remote_file=remotepath.split('/')[-1]
    remote_dir=remotepath.split(remote_file)[0]

    try:
    # Create the connection
        conn = DropboxConnection(email, password)

        # Upload the file
        uploader=conn.upload_file(localpath,remote_dir,remote_file)
        public_url=conn.get_download_url(remote_dir,remote_file)
    except:
        print("Upload failed")
    else:
        print("Uploaded small_test_file.txt to the root of your Dropbox")
if __name__ == '__main__':
    import os
    email='ss3@elec-lab.tk';password='ss123456';

    localpath=os.getcwd().replace("\\","/")+'/small_test_file.txt';
    # remotepath='/'+localpath.split('/')[-1]
    try:remotepath0="/"+os.environ('OPENSHIFT_APP_DNS')+'/'
    except:remotepath0="/"+'dr2omnia-diy4phantomjs.rhcloud.com/'
    # fh = open("small_test_file.txt","w")
    # fh.write("Small test file")
    # fh.close()
    # my_dropbox( email, password, localpath, remotepath)
    app_key='pzwtcqpfj5ih8p0'
    app_secret='s57axvy6ta0cdpd'
    access_token='Ap8LK01GJbsAAAAAAAAABpqZnhsSpLwvdFgL69ROiQ98N3S-PPwbylCf2Cc5Fxhc'
    # link=main_dropbox(app_key,app_secret,access_token,localpath,remotepath).main_dropbox(localpath,remotepath)


    from dropbox.client import DropboxClient
    # import dropbox
    # import dropbox.client
    # client=dropbox.client.DropboxClient(access_token)
    client = DropboxClient(access_token)

    try:
	    CurrentDir=os.path.dirname(os.path.realpath(__file__))
	    Parent_Dir=os.path.abspath(os.path.join(CurrentDir, '..'))
        # Destination= os.path.abspath(os.path.join(Parent_Dir, '..'))

    except:
	    CurrentDir=os.getcwd()
	    Parent_Dir=os.path.abspath(os.path.join(CurrentDir, '..'))
        # Destination= os.path.abspath(os.path.join(Parent_Dir, '..'))
    Destination= os.path.abspath(os.path.join(Parent_Dir, '..'))

    for root, dirs, files in os.walk(CurrentDir):
        # root=root.replace("/","\\")
        curent_path0=root.split(Parent_Dir)[1]+'/'
        curent_path=curent_path0.replace('\\','/')
        # root=root.replace('\\','/')
        for dir2 in dirs:
           # if os.path.isdir(Destination+ curent_path+dir2):
                try:client.file_create_folder(remotepath0+dir2)
                except:pass
                for root2, dirs2, files2 in os.walk(dir2):
                    for file22 in files2:

                        if os.path.isfile(root2+"/"+file22):
                            remotepath=remotepath0+dir2+'/'+file22
                            path = os.path.join(root2, file22)
                            link=main_dropbox(app_key,app_secret,access_token,path,remotepath).main_dropbox(path,remotepath)

                # remotepath=remotepath0+dir2+remotepath.replace('/','')
        for file2 in files:
            # if os.path.isfile(Destination+ curent_path+file2):
            if os.path.isfile(root+"/"+file2):
                path = os.path.join(root, file2)
                try:
                    remotepath=remotepath0+dir2+'/'+file2
                except:
                    remotepath=remotepath0+file2

                print "file is:"+file2
                link=main_dropbox(app_key,app_secret,access_token,path,remotepath).main_dropbox(path,remotepath)
                # except:pass
                # size_source = os.stat(path.replace('\\','/')).st_size # in bytes
                # size_target=os.stat(root+"\\"+file2).st_size
                # if size_source != size_target:
                    # replace(Parent_Dir+curent_path+file2,Destination+ curent_path+file2)
                    # pass
            else:
                pass

EOF

 ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python ~/app-root/runtime/repo/php/my_dropbox.py
 
 
 #cd  $HOME/app-root/runtime/repo/php/
#${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python my_dropbox.py

