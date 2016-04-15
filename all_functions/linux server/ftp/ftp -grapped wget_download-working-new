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
ip='ftp.ucq.me';user='ucq_17121158';#  http://ftp112.ucq.me soheil_paper@yahoo.om

remote = FtpTarget("/htdocs/community/", ip,21, user, passwd)

opts = {"force": True, "delete_unmatched": False, "verbose": 3, "execute": True, "dry_run" : False}

s = UploadSynchronizer(local, remote, opts)
#s = DownloadSynchronizer(local, remote, opts)
s.run()
stats = s.get_stats()
print(stats)
EOF

nohup sh -c " ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python ftp_sync2.py"> $OPENSHIFT_LOG_DIR/python_ftp_sync2.log /dev/null 2>&1 &  
tail -f  $OPENSHIFT_LOG_DIR/python_ftp_sync2.log
