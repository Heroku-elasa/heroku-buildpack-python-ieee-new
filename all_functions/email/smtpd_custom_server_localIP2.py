# pip install secure_smtpd
from datetime import datetime
import asyncore,os,sys
from smtpd import SMTPServer

class EmlServer(SMTPServer):
    no = 0
    def process_message(self, peer, mailfrom, rcpttos, data):
        filename = '%s-%d.eml' % (datetime.now().strftime('%Y%m%d%H%M%S'),
                                  self.no)
        f = open(filename, 'w')
        f.write(data)
        f.close
        # print '%s saved.' % filename
        print 'Email received at %s and saved as %s' % (datetime.now().strftime('%H:%M:%S'), filename)
        self.no += 1


def run():
    print 'Python SMTP server'
    print 'Quit the server with CONTROL-C.'
    try:
        ip=(os.environ['OPENSHIFT_DIY_IP'])
        port=int('15030')
    except:
        ip=('127.0.0.1')
        port=15030
    # foo = EmlServer(('localhost', 25), None)
    foo = EmlServer((ip, port), None)
    try:
        asyncore.loop()
    except KeyboardInterrupt or IndexError:
        sys.exit("Usage: smtpsink.py <port>")





if __name__ == '__main__':
    run()