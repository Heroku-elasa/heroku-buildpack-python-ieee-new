__author__ = 'http://pymotw.com/2/smtpd/'
import smtplib
import email.utils,os
from email.mime.text import MIMEText

# Create the message
msg = MIMEText('This is the body of the message.')
msg['To'] = email.utils.formataddr(('Recipient', 'soheil_paper@yahoo.com'))
msg['From'] = email.utils.formataddr(('Author', 'soheilpaper@gmail.com'))
msg['Subject'] = 'Simple test message'

try:
    ip=(os.environ['OPENSHIFT_DIY_IP'])
    port=int('15030')
except:
    ip=('127.0.0.1')
    port=15030
server = smtplib.SMTP(ip, 15030)
#server = smtplib.SMTP(ip+':15030')
server.set_debuglevel(True) # show communication with the server
try:
    # server.sendmail(From, [To], msg.as_string())
    server.sendmail('soheilpaper@gmail.com', ['soheil_paper@yahoo.com'], msg.as_string())
finally:
    server.quit()
