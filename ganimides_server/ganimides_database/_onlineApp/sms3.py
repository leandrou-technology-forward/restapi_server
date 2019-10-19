import requests
resp = requests.post('https://textbelt.com/text', {
  'phone': '+35799359864',
  'message': 'Hello world',
  'key': 'textbelt',
})
print(resp.json())