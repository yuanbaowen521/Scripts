#!/usr/bin/python
# -*- coding: utf-8 -*-  

desc='''
Function: Send emails from server to mailbox.

Cited from Chen Tong. 
'''
import sys
import os
from optparse import OptionParser as OP

def cmdparameter(argv):
    if len(argv) == 1:
        global desc
        print >>sys.stderr, desc
        cmd = 'python ' + argv[0] + ' -h'
        os.system(cmd)
        sys.exit(1)
    usages = "%prog -r receiver@smtp.com -s subjsct -c context -a attach1,attach2"
    parser = OP(usage=usages)
    parser.add_option("-r", "--receiver", dest='receiver',
            metavar="RECEIVER", default="yuanbaowen521@126.com", 
            help="The receiver for your mail. \
Default <yuanbaowen521@126.com>.")
    parser.add_option("-s", "--subject", dest='subject',
            metavar="SUBJECT", help="The subject for your mail")
    parser.add_option("-c", "--context", dest='context',
            metavar="CONTEXT", default="Hi, please check this email!",
            help="The main context for your mail. \
Symbol <-> should be given if you want SYS.STDIN as the mail content.")
    parser.add_option("-a", "--attachement", dest='attachment',
            metavar="ATTACHEMENT", help="The attachment for your mail. \
Multiple attachments should be separated by ','.")
    parser.add_option("-u", "--user", dest='user',
            metavar="USER", default='server_bak@126.com', 
            help="The username for mail sender.")
    parser.add_option("-p", "--passwd", dest='passwd',
            metavar="PASSWD", default='server.bak', 
            help="The passwd for mail sender.")
    parser.add_option("-S", "--smtp", dest='smtp',
            metavar="SMTP", default='smtp.126.com', 
            help="The mail send server, for 126 is \
smtp.126.com.")
    (options, args) = parser.parse_args()
    return (options, args)


import smtplib  
import mimetypes  
from email.MIMEMultipart import MIMEMultipart  
from email.MIMEBase import MIMEBase  
from email.MIMEText import MIMEText  
from email.MIMEAudio import MIMEAudio  
from email.MIMEImage import MIMEImage  
from email.Encoders import encode_base64  
  
def sendMail(subject, text, recipient, attachmentFilePaths, user,
        passwd, smtp):  
    gmailUser = user
    gmailPassword = passwd
  
    msg = MIMEMultipart()  
    msg['From'] = gmailUser  
    msg['To'] = recipient  
    msg['Subject'] = subject  
    msg.attach(MIMEText(text))  
  
    for attachmentFilePath in attachmentFilePaths:  
        if attachmentFilePath:
            msg.attach(getAttachment(attachmentFilePath))  
  
    mailServer = smtplib.SMTP(smtp)  
    mailServer.ehlo()  
    mailServer.starttls()  
    mailServer.ehlo()  
    mailServer.login(gmailUser, gmailPassword)  
    mailServer.sendmail(gmailUser, recipient, msg.as_string())  
    mailServer.close()  
  
    print('Sent email to %s' % recipient)  
  
def getAttachment(attachmentFilePath):  
    contentType, encoding = mimetypes.guess_type(attachmentFilePath)  
  
    if contentType is None or encoding is not None:  
        contentType = 'application/octet-stream'  
  
    mainType, subType = contentType.split('/', 1)  
    file = open(attachmentFilePath, 'rb')  
  
    if mainType == 'text':  
        attachment = MIMEText(file.read())  
    elif mainType == 'message':  
        attachment = email.message_from_file(file)  
    elif mainType == 'image':  
        attachment = MIMEImage(file.read(),_subType=subType)  
    elif mainType == 'audio':  
        attachment = MIMEAudio(file.read(),_subType=subType)  
    else:  
        attachment = MIMEBase(mainType, subType)  
    attachment.set_payload(file.read())  
    encode_base64(attachment)  
  
    file.close()  
  
    attachment.add_header('Content-Disposition', 'attachment',   filename=os.path.basename(attachmentFilePath))  
    return attachment  
  
  
# start to test  
def main():
    options, args = cmdparameter(sys.argv)
    subject = options.subject
    context = options.context
    if context != '-':
        content = context
    else:
        #fh = sys.stdin
        content = sys.stdin.read()
    recipient = options.receiver
    if options.attachment:
        attach = [i.strip() for i in options.attachment.split(',')]
    else:
        attach = []
    user = options.user
    passwd = options.passwd
    smtp = options.smtp

    sendMail(subject, content, recipient, attach, user, passwd, smtp) 

main()
