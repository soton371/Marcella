from email.message import EmailMessage
import smtplib
import random
from core.constants import senderEmail, sendOTPPassword, smtpHost, smtpPort

def generateOTP():
    otpLength = 5
    myOtp = ''
    for i in range(otpLength):
        myOtp += str(random.randint(0,9))

    return myOtp


def sendOtpSmtp(otp: str, recipientMail: str):
    try:
        smtpServer = smtplib.SMTP(smtpHost, smtpPort)
        smtpServer.starttls()
        smtpServer.login(senderEmail, sendOTPPassword)

        msg = EmailMessage()
        msg['Subject'] = 'Otp Verification'
        msg['from'] = senderEmail
        msg['to'] = recipientMail
        msg.set_content(f"Your otp code is: {otp}")
        smtpServer.send_message(msg)
        return True
    except Exception as e:
        print(f"sendOtpSmtp e: {e}")
        return False