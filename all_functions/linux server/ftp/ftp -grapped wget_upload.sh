#http://techblog.rezitech.com/how-to-use-wget-to-download-all-filesfolders-via-ftp/
# Replace USERNAME and PASSWORD with the FTP credentials to be used
# Replace ftp://domainname.com/subfolder with the domain to connect to (remove subfolder to download the root)
#wget --ftp-user=USERNAME --ftp-password=PASSWORD -r ftp://domainname.com/subfolder/*

# To exclude directories, include --exclude-directories=
#wget --ftp-user=USERNAME --ftp-password=PASSWORD --exclude-directories=blog -r ftp://domainname.com/subfolder/*
if [ ! -d ${OPENSHIFT_HOMEDIR}/app-root/runtime/repo ]; then	
    mkdir ${OPENSHIFT_HOMEDIR}/app-root/runtime/repo
	mkdir ${OPENSHIFT_HOMEDIR}/app-root/runtime/repo/php
fi


nohup sh -c " wget  -P ${OPENSHIFT_HOMEDIR}/app-root/runtime/repo/php --mirror --user=u220290147 --password=ss123456 ftp://93.188.160.83:21/"> $OPENSHIFT_LOG_DIR/python_modules_install_1_1.log /dev/null 2>&1 &  
tail -f  $OPENSHIFT_LOG_DIR/python_modules_install_1_1.log
cd ${OPENSHIFT_HOMEDIR}/app-root/runtime/repo/php/*
nohup sh -c "zip -r elec-lab.zip . "> $OPENSHIFT_LOG_DIR/zip.log /dev/null 2>&1 &  
tail -f  $OPENSHIFT_LOG_DIR/zip.log


#nohup sh -c "wget http://dl1.sarzamindownload.com/sdlftpuser/92/07/10/Android.Bootcamp_Part2.rar "> $OPENSHIFT_LOG_DIR/zip2.log /dev/null 2>&1 &  
#tail -f  $OPENSHIFT_LOG_DIR/zip2.log


${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install pyftpsync
#${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/pyftpsync upload ${OPENSHIFT_HOMEDIR}/app-root/runtime/repo/php/ ftp://u882460391:ss123456@31.170.167.80:21/ --delete -x

cat <<'EOF'  >> ftp_sync.py
#http://elec-lab.4rog.in
from ftpsync.synchronizers import DownloadSynchronizer, UploadSynchronizer,BiDirSynchronizer

from ftpsync.targets import FsTarget # UploadSynchronizer, DownloadSynchronizer
from ftpsync.ftp_target import FtpTarget
import os

env_var = os.environ['OPENSHIFT_HOMEDIR']
local = FsTarget(env_var+"/app-root/runtime/tmp/")
user ="u220290147"
passwd = "ss123456"
ip='s.id.ai';user='u707539103';# ss-22.4rog.in
#ip='31.170.167.90';user='u929884673';# iran-balabar.tk master@tb-simple.heliohost.org
#remote = FtpTarget("/public_html", "93.188.160.83", user, passwd)
remote = FtpTarget("/public_html", ip, user, passwd)
opts = {"force": False, "delete_unmatched": False, "verbose": 3, "execute": True, "dry_run" : False}
#opts = {"force": True, "delete_unmatched": True, "verbose": 3, "execute": True, "dry_run" : False}
s = UploadSynchronizer(local, remote, opts)
#s = DownloadSynchronizer(local, remote, opts)
s.run()
stats = s.get_stats()
print(stats)
EOF

nohup sh -c " ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python ftp_sync.py"> $OPENSHIFT_LOG_DIR/python_ftp_sync.log /dev/null 2>&1 &  
tail -f  $OPENSHIFT_LOG_DIR/python_ftp_sync.log
