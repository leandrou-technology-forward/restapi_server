import smtplib
carriers = {
	'att':    '@mms.att.net',
	'tmobile':' @tmomail.net',
	'verizon':  '@vtext.com',
	'sprint':   '@page.nextel.com'
}

def send(message):
    # Replace the number with your own, or consider using an argument\dict for multiple people.
    to_number = '+35799359864{}'.format(carriers['att'])
    auth = ('spithas@leandrou.com', 'spithas3116')
    GOOGLE_MAIL_USERNAME = 'akamas2020@gmail.com'
    GOOGLE_MAIL_PASSWORD = 'philea13'
    GOOGLE_MAIL_USERNAME = 'bstarr131@gmail.com'
    GOOGLE_MAIL_PASSWORD = 'bstarr13'
    GOOGLE_MAIL_USERNAME = 'spithas@leandrou.com'
    GOOGLE_MAIL_PASSWORD = 'spithas3116'
    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP( "smtp.gmail.com", 587 )
    server.starttls()
    server.login(auth[0], auth[1])

    # Send text message through SMS gateway of destination number
    res = server.sendmail(auth[0], to_number, message)

    print(res)

#import SMS

some_text = 'Blah, blah'

send(some_text)