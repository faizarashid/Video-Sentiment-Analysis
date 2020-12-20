
# Python code to send email to a list of 
# emails from a spreadsheet 
  
# import the required libraries 
import pandas as pd 
import smtplib ,os,glob
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage

  
# change these as per use 
your_email = ''
your_password = ''
  
# establishing connection with gmail 
server = smtplib.SMTP_SSL('smtp.gmail.com', 465) 
server.ehlo() 
server.login(your_email, your_password) 
#### You email message here
mail_content = '''Hello,
This is a test mail.
In this mail we are sending some attachments.
The mail is sent using Python SMTP library.
Thank You
'''
# reading the spreadsheet 
email_list = pd.read_excel('D:/internship/test.xlsx') 

# getting the names and the emails 
names = email_list['Name'] 
emails = email_list['Email'] 
  
# iterate through the records 
for i in range(len(emails)): 
  
    # for every record get the name and the email addresses 
    name = names[i] 
    email = emails[i] 
   
    # the message to be emailed 
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = your_email
    message['To'] = emails[i]
    message['bcc']= ''     # sir's email address here
    message['Subject'] = '' #your subject here
    #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    
    ## images of certificates here
    attachment_path_list = r'd:/internship/images'

    
    ## images path for new courses here
    img_data1 = open('D:/internship/Code Maze/output-onlinepngtools.png', 'rb')
    ## image name here
    image1 = MIMEImage(img_data1.read(), name=os.path.basename('output-onlinepngtools.png'))
    message.attach(image1)
  
    
    for files in os.listdir(attachment_path_list):

        if files.startswith(name):
            print(files,name)
            img_data2 = open(attachment_path_list+'/'+files, 'rb').read()
            image1 = MIMEImage(img_data2, name=os.path.basename(files))
    message.attach(image1)    
    try:
        # sending the email 
        server.sendmail(your_email, email, message.as_string()) 
        print('Email to ',email,' successfully sent!')
    except Exception as e:
        print('Email to ',email,' could not be sent')
    print(i," iteration completed")
    # close the smtp server 
server.close() 
