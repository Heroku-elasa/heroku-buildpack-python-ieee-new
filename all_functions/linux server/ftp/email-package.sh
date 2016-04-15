#!/bin/bash 
#cd /tmp
#Ho to use lamson
cat << "EOF" >> lasmon_openshift.sh
~/app-root/runtime/srv/python/bin/lamson gen -project mymailserver && cd mymailserver/config
#change host and port in settings.py
~/app-root/runtime/srv/python/bin/lamson start -pid ./run/smtp.pid -FORCE False -chroot False -chdir "/var/lib/openshift/542d073fe0b8cd5b58000115/app-root/runtime/tmp/mymailserver" \
        -umask False -uid False -gid False -boot config.boot
~/app-root/runtime/srv/python/bin/lamson send -sender me@mydomain.com -to test@test.com -subject “My test.” -body “Hi there.” -port 8823
~/app-root/runtime/srv/python/bin/lamson send -port 15009 -host '127.7.15.1' \
-debug 1 -sender ss3@elec-lab.tk -to soheil_paper@yahoo.com -subject "STR" -body "STR" -attach False
EOF
${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install lamson 

#
${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install secure_smtpd 
${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install smtplib