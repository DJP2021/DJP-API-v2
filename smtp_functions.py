### Importing necessary libraries
import smtplib
from smtplib import SMTP_SSL as SMTP
import ssl
import datetime

### SMTP details
smtp = smtplib.SMTP('smtp-mail.outlook.com', 587)

from_addr = ""
password = ""
smtp.ehlo()
smtp.starttls()
smtp.login(from_addr, password)

async def send_password_mail(name, to_addr, newpassword):
    date = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )
    message_text = f"Hello {name}, \nYou are receiving this mail because you have requested a password change due to either a password leak or because you lost your password. \n Your new password looks like the following:\n\n {newpassword} \n \n We are happy to help you if you have any questions left regarding your password change.\n Greetings \n The DJP-API Support Team \n You have not requested a password change? Open a support ticket immediately to ensure that your account is safe. \n\n This is an automated message. Please do not answer this email. If you have any questions regarding this email, please open a ticket."
    subj = "Your Password has been reset successfully"
    msg = f"From: {from_addr} \nTo: {to_addr} \nSubject: {subj} \nDate: {date} \n\n {message_text}" 
    smtp.sendmail(from_addr, to_addr, msg)
    
async def send_key_mail(name, to_addr, newkey):
    date = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )
    message_text = f"Hello {name}, \nYou are receiving this mail because you have requested an API Key change due to either a api key leak or because you lost your Key. \n Your new API Key looks like the following:\n\n {newkey} \n \n We are happy to help you if you have any questions left regarding your API Key change.\n Greetings \n The DJP-API Support Team \n You have not requested an API Key change? Open a support ticket immediately to ensure that your account is safe. \n\n This is an automated message. Please do not answer this email. If you have any questions regarding this email, please open a ticket."
    subj = "Your API Key has been reset successfully"
    msg = f"From: {from_addr} \nTo: {to_addr} \nSubject: {subj} \nDate: {date} \n\n {message_text}" 
    smtp.sendmail(from_addr, to_addr, msg)
