from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib
import os


### need to change the username and th passowrd
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT =  587
SMTP_USERNAME = "testingpurpose217@gmail.com"
SMTP_PASSWORD = "pjmflkjtxckkafgw"


def send_mail(EMAIL_TO ,EMAIL_FROM, EMAIL_SUBJECT ,MESSAGE_BODY ,  FILE_NAME ,PATH_TO_FILE ):
    # Create a multipart message
    try:
        msg = MIMEMultipart()
        
        body_part = MIMEText(MESSAGE_BODY, 'plain')

        msg['Subject'] = EMAIL_SUBJECT
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO

        ###   Add body to email
        msg.attach(body_part)

        if os.path.exists(PATH_TO_FILE):
            # open and read the CSV file in binary
            with open(PATH_TO_FILE,'rb') as file:
                # Attach the file with filename to the email
                msg.attach(MIMEApplication(file.read(), Name=FILE_NAME))
        
            # Create SMTP object and then Login to the server
            smtp_obj = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            smtp_obj.starttls()
            smtp_obj.login(SMTP_USERNAME, SMTP_PASSWORD)

            # Convert the message to a string and send it
            smtp_obj.sendmail(msg['From'], msg['To'], msg.as_string())
            smtp_obj.quit()

            context = {
                "Status" : "Success" ,
                "Message" : "Mail Sent Successfully "
            }
            return context
        else:
            context = {
                "Status" : "Failure" ,
                "Message" : "File Not found to attached into the mail"
            }
            return context

    
    except Exception as e:
        context = {
            "Status" : "Failure" ,
            "Message" : f"Exception while sending the mail:- {e}"
        }
        return context
