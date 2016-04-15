#!/usr/bin/pythonimport smtpd
import smtpd
import asyncore

class CustomSMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data):
        print 'Receiving message from:', peer
        print 'Message addressed from:', mailfrom
        print 'Message addressed to  :', rcpttos
        print 'Message length        :', len(data)
        return
try:
    ip=(os.environ['OPENSHIFT_DIY_IP'])
    port=int('15030')
except:
    ip=('127.0.0.1')
    port=15030
server = CustomSMTPServer((ip, 15030), None)

asyncore.loop()
#nohup sh -c "${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python emserver.py" > $OPENSHIFT_LOG_DIR/python_ftp_sync.log /dev/null 2>&1 &
#tail -f $OPENSHIFT_LOG_DIR/python_ftp_sync.log