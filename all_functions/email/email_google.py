import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# Specifying the from and to addresses

fromaddr = 'soheilpaper@gmail.com'
toaddrs  = 'soheil_paper@yahoo.com'

# Writing the message (this message will appear in the email)

msg1 = 'Enter you message here'

msg = MIMEMultipart()
msg['Subject'] = 'Python emaillib Test'
msg['To'] = toaddrs
msg['From'] = fromaddr
file = MIMEImage(open('06180383.pdf', 'rb').read(), _subtype="pdf")
file.add_header('Content-Disposition', 'attachment', filename='06180383.pdf')
msg.attach(file)

# Gmail Login

username = 'soheilpaper'
password = 'ss32913291'

# Sending the mail  
headers = ["from: " + fromaddr,
           "subject: " + 'your file have been downloaded',
           "to: " + toaddrs,
           "mime-version: 1.0",
           "content-type: text/html"]

# server = smtplib.SMTP('smtp.gmail.com:587')
server = smtplib.SMTP('127.0.0.1:1025')
server.sendmail(fromaddr, toaddrs,headers, msg1)
server.ehlo()
server.starttls()
server.login(username,password)
headers = "\r\n".join(headers)
server.sendmail(fromaddr, toaddrs,headers, msg1)
server.sendmail(fromaddr, toaddrs,headers,msg.as_string())
server.quit()