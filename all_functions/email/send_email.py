#!"E:/Program Files win 7 2nd/python27/python.exe"
#!/usr/bin/python
# coding: utf-8

# This script asks your name, email, password, SMTP server and destination
# name/email. It'll send an email with this script's code as attachment and
# with a plain-text message. You can also pass `message_type='html'` in
# `Email()` to send HTML emails instead of plain text.
# You need email_utils.py to run it correctly. You can get it on:
# https://gist.github.com/1455741
#  Copyright 2011 Alvaro Justen [alvarojusten@gmail.com]
# License: GPL <http://www.gnu.org/copyleft/gpl.html>
__author__ = ' Alvaro Justen [alvarojusten@gmail.com]'
import sys
from getpass import getpass
from email_utils import EmailConnection, Email


# print 'I need some information...'
# name = raw_input(' - Your name: ')
# email = raw_input(' - Your e-mail: ')
# password = getpass(' - Your password: ')
# mail_server = raw_input(' - Your mail server: ')
# to_email = raw_input(' - Destination email: ')
# to_name = raw_input(' - Name of destination: ')
# subject = 'Sending mail easily with Python'
# message = 'here is the message body'
# attachments = [sys.argv[0]]
def main_server(**kwargs):
    # main(mail_server=,email = ,password=,name =,to_name =,subject = , message =,attachments = ,to_email = )
    print 'I need some information...'
    mail_server=kwargs['mail_server']
    user =  kwargs['user']
    password=kwargs['password']

    name =  kwargs['name']
    to_name =  kwargs['to_name']
    to_email =  kwargs['to_email']
    subject =  kwargs['subject']
    message =  kwargs['message']
    attachments =  kwargs['attachments']




    print 'Connecting to server...'
    server = EmailConnection(mail_server, user, password)
    print 'Preparing the email...'
    email = Email(from_='"%s" <%s>' % (name, user), #you can pass only email
                  to='"%s" <%s>' % (to_name, to_email), #you can pass only email
                  subject=subject, message=message, attachments=attachments)
    print 'Sending...'
    server.send(email)
    print 'Disconnecting...'
    server.close()
    print 'Done!'
if __name__ == "__main__":

     #main_server( mail_server='127.0.0.1:15030',user ='soheilpaper' ,password='ss32913291',name =options.name,to_name =options.to_name,to_email ='soheil_paper@yahoo.com',subject ='Download succesfully' , message ='This is your file requested',attachments =['06180383.pdf'])
	from optparse import OptionParser
    parser = OptionParser(description=__doc__)
    parser.add_option('-m','--server',type='string', dest='smpt',
                      help='please insert your mail server to send request on it like:smtp.gmail.com:587',default='smtp.gmail.com:587' )
    parser.add_option('-s','--user', dest='user', help='user name of your email like  admin:admin' )
    parser.add_option('-p','--pass', dest='Pass', help='pass of your email like  admin:admin ')
    parser.add_option('-e','--to', dest='to_email', help='send to  ')
    parser.add_option('-n','--name', dest='name', help='Name of email sender',default='Dummy')
    parser.add_option('-t','--to_name', dest='to_name', help='name of receiver',default='Dummy')
    parser.add_option('-T','--title', dest='title', help='title of message',default=' You have a Message' )
    parser.add_option('-g','--msg', dest='msg', help='body message',default='This is a default body message' )
    parser.add_option('-a','--attach', dest='attachment', help='file list for attaching like ["test.pdf"]',default=None)
    parser.add_option('-H','--HELP', dest='HELP', help='For Getting Help')
    options, args = parser.parse_args()
    # main_server(mail_server=options.smpt,user ='soheilpaper' ,
    #             password='ss32913291',name =options.name,to_name =options.to_name,to_email ='soheil_paper@yahoo.com',
    #             subject ='Download succesfully' , message ='This is your file requested',attachments =['06180383.pdf'])
    main_server(mail_server='mx1.elec-lab.tk:2525',user ='ssy1' ,
         password='ss123456',name =options.name,to_name =options.to_name,to_email ='soheil_paper@yahoo.com',
         subject ='Download succesfully' , message ='This is your file requested',attachments =['06180383.pdf'])
    if  options.user and options.Pass and  options.to and options.ms and options.From :
        main_server(mail_server=options.smpt,user =options.user ,
             password=options.Pass,name =options.name,to_name =options.to_name,to_email =options.to_email,
        subject =options.sub , message =options.msg,attachments =options.attachment)
    else:

            print 'we could not send email beacuse you must enter your user pass  and receiver email at least'

            parser.print_help()


