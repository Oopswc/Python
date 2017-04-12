import email
import smtplib
import io
import os
import re
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def send_mail(file1,file2 = ''):
    #add attachment1
    msg = MIMEMultipart()

    if file1 !='Error':
        # mail text body
        msg.attach(MIMEText('Signin Success!', 'plain', 'utf-8'))

        with open(file1, 'r') as f1:
            att1 = MIMEText(f1.read(), 'plain', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="Log.txt"'  
        msg.attach(att1)
        
        with open(file2, 'r') as f2:
            att2 = MIMEText(f2.read(), 'plain', 'utf-8')
        att2["Content-Type"] = 'application/octet-stream'
        att2["Content-Disposition"] = 'attachment; filename="Points.txt"'  
        msg.attach(att2)
    else:
        msg.attach(MIMEText('Send Error,No find Log file!', 'plain', 'utf-8'))
    
    #mail info
    msg['to'] = 'XXX'
    msg['from'] = 'XXX'
    msg['subject'] = r'XXX'

    try:
        server = smtplib.SMTP()
        code,ms = server.connect('smtp.163.com','25')
        server.login('XXX','XXX')
        server.sendmail(msg['from'], msg['to'],msg.as_string())
        server.quit()
        print("Send success")
    except Exception:  
        print('Error: Sendmail error')


if __name__ == "__main__":
    if os.path.exists('Log.txt')and os.path.exists('Log.txt'):
        path1 = os.path.join(os.getcwd(),'Log.txt')
        path2 = os.path.join(os.getcwd(),'Points.txt')
        send_mail(path1,path2)
    else:
        send_mail('Error','Error')
