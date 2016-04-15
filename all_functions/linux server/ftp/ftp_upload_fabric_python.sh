#!/bin/sh
~/app-root/runtime/srv/python/bin/pip install fabric
${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install fabric
wget http://test-22.4rog.in/tmp/rapiech/files/elec-lab.zip
cd /tmp
cat <<'EOF'  >> ftp_fabric.py
#http://elec-lab.4rog.in
#~/app-root/runtime/srv/python/bin/python  ftp_fabric.py
from fabric.api import run, env, sudo, put
host='s.id.ai:21';port='21'
env.user = 'u707539103'
# Set the password [NOT RECOMMENDED]
env.password = "ss123456"

env.hosts = [host]     # such as ftp.google.com
run("hostname -f")
def copy():
    # assuming i have wong_8066.zip in the same directory as this script
    put('elec-lab.zip', '/public_html/elec-lab/elec-lab.zip')
	
EOF

${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python ftp_fabric.py