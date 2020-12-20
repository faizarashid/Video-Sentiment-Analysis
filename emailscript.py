import smtplib
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders

def send_mail_gmail(username,password,toaddrs_list,msg_text,fromaddr=None,subject="Test mail",attachment_path_list=None):

    s = smtplib.SMTP('smtp.gmail.com:587')
    s.starttls()
    s.login(username, password)
    #s.set_debuglevel(1)
    msg = MIMEMultipart()
    sender = fromaddr
    recipients = toaddrs_list
    msg['Subject'] = subject
    if fromaddr is not None:
        msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    if attachment_path_list is not None:
        for each_file_path in attachment_path_list:
            try:
                file_name=each_file_path.split("/")[-1]
                part = MIMEBase('application', "octet-stream")
                part.set_payload(open(each_file_path, "rb").read())

                Encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment' ,filename=file_name)
                msg.attach(part)
            except:
                print "could not attache file"
    msg.attach(MIMEText(msg_text,'html'))
    s.sendmail(sender, recipients, msg.as_string())