import smtpd
import asyncore,os

class CustomSMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data):
        print 'Receiving message from:', peer
        print 'Message addressed from:', mailfrom
        print 'Message addressed to  :', rcpttos
        print 'Message length        :', len(data)
        return;
s='s'

try:
    ip=(os.environ['OPENSHIFT_DIY_IP'])
    port=int('15030')
except:
    ip=('127.0.0.1')
    port=15030


server = CustomSMTPServer((ip, port), None)

asyncore.loop()