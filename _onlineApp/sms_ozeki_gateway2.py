###########################################
## Ozeki NG - SMS Gateway Python example ##
###########################################

import requests

############################
### Ozeki NG information ###
############################

host = "http://127.0.0.1"

user_name = "admin"
user_password = "abc123"

recipient = "+36304080332"

message_body = "Hello World from Python"

############################
#### Sending the message ###
############################

response = requests.get(host + ":9501/api",
                        params={"action": "sendmessage",
                                "username": user_name,
                                "password": user_password,
                                "recipient": recipient,
                                "messagetype": "SMS:TEXT",
                                "messagedata": message_body})

##############################
### Verifying the response ###
##############################

if response.text.find("Message accepted for delivery") > 1:
    print("Message successfully sent")
else:
    print("Message not sent! Please check your settings!")