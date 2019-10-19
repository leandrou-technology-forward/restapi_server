# python script for sending message update 

import time 
from time import sleep 
from sinchsms import SinchSMS 

# function for sending SMS 
def sendSMS(): 

	# enter all the details 
	# get app_key and app_secret by registering 
	# a app on sinchSMS 
	number = 'your_mobile_number'
	app_key = 'your_app_key'
	app_secret = 'your_app_secret'
    
	SMS_SERVER_SINCH_API_KEY = 'c44ef77212934112a20363646cc88d5c'
	SMS_SERVER_SINCH_API_SECRET = '4c44f46fc5294ac4981610233390b79f'
	SMS_SERVER_SINCH_FROM_NUMBER = '35799599819'

	app_key = SMS_SERVER_SINCH_API_KEY
	app_secret = SMS_SERVER_SINCH_API_SECRET

	number = '35799359864'
	
	# enter the message to be sent 
	message = 'Hello Message!!!'

	client = SinchSMS(app_key, app_secret) 
	print("Sending '%s' to %s" % (message, number)) 

	response = client.send_message(number, message) 
	message_id = response['messageId'] 
	response = client.check_status(message_id) 

	# keep trying unless the status retured is Successful 
	while response['status'] != 'Successful': 
		print(response['status']) 
		time.sleep(1) 
		response = client.check_status(message_id) 

	print(response['status']) 

if __name__ == "__main__": 
	sendSMS() 