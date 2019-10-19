import nexmo

# Load in configuration from environment variables:
# NEXMO_API_KEY = env_var('NEXMO_API_KEY')
# NEXMO_API_SECRET = env_var('NEXMO_API_SECRET')
# NEXMO_NUMBER = env_var('NEXMO_NUMBER')
NEXMO_API_KEY = '3ee5cdd5'
NEXMO_API_SECRET = 'lgzsdgI4cP9eZl7J'
NEXMO_NUMBER = '35799599819'
 
# Create a new Nexmo Client object:
nexmo_client = nexmo.Client(key=NEXMO_API_KEY, secret=NEXMO_API_SECRET)
 
to_number = '35799359864'
message = 'hi.ganimides'

# Send the SMS message:
result = nexmo_client.send_message({
    'from': NEXMO_NUMBER,
    'to': to_number,
    'text': message,
})

print(result)
#{'message-count': '1', 'messages': [{'to': 'YOUR-PHONE-NUMBER', 'message-id': '0D00000039FFD940', 'status': '0', 'remaining-balance': '14.62306950', 'message-price': '0.03330000', 'network': '12345'}]}

response = nexmo_client.start_verification(number='35799359864', brand="GanimidesTechnology")

if response["status"] == "0":
    print("Started verification request_id is %s" % (response["request_id"]))
else:
    print("Error: %s" % response["error_text"])
