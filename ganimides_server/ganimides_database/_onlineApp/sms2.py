import smtplib
from email.mime.text import MIMEText

# # Replace the number with your own, or consider using an argument\dict for multiple people.
# to_number = '0035799359864{}'.format(carriers['att'])
# auth = ('spithas@leandrou.com', 'spithas3116')
GOOGLE_MAIL_USERNAME = 'akamas2020@gmail.com'
GOOGLE_MAIL_PASSWORD = 'philea13'
GOOGLE_MAIL_USERNAME = 'bstarr131@gmail.com'
GOOGLE_MAIL_PASSWORD = 'bstarr13'
GOOGLE_MAIL_USERNAME = 'spithas@leandrou.com'
GOOGLE_MAIL_PASSWORD = 'spithas3116'
# # Establish a secure session with gmail's outgoing SMTP server using your gmail account
# server = smtplib.SMTP( "smtp.gmail.com", 587 )
# server.starttls()
# server.login(auth[0], auth[1])


username = GOOGLE_MAIL_USERNAME
password = GOOGLE_MAIL_PASSWORD

vtext = "+35799359864@vtext.com"
message = "this is the message to be sent"

msg = MIMEText("""From: %s
To: %s
Subject: text-message
%s""" % (username, vtext, message))

server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(username,password)
server.sendmail(username, vtext, msg.as_string())
server.quit()