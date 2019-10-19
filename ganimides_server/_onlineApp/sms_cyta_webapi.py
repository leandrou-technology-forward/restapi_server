import requests

#https://www.cyta.com.cy/web-sms-api/en

mobile = '99359864'
message='Hello please verify your mobile'

request_xml=f"""<?xml version="1.0" encoding="UTF-8" ?> 
<websmsapi>
  <version>1.0</version>
  <username>Philippos</username>
  <secretkey>f69f0d4702814d1fa1768f397ce9b485</secretkey>
  <recipients>
    <count>1</count>
    <mobiles>
      <m>{mobile}</m>
    </mobiles>
  </recipients>
  <message>{message}</message>
  <language>en</language>
</websmsapi>"""

# POST https://www.cyta.com.cy/cytamobilevodafone/dev/websmsapi/sendsms.aspx HTTP/1.1
# Host: www.cyta.com.cy
# Content-Type: application/xml; charset="utf-8"
# Content-Length: 433
# Connection: close

url = 'https://www.cyta.com.cy/cytamobilevodafone/dev/websmsapi/sendsms.aspx'
headers = {'Content-Type': 'application/xml; charset=utf-8', 'Content-length': len(request_xml), 'Connection': 'close',}
headers = {'Content-Type': 'application/xml; charset=utf-8'}

r = requests.post(url, headers=headers, data=request_xml)
if r.status_code in (200, 201):
    if r.headers.get('Content-Type','')=='application/json':
        # log_message(f'{Fore.RED}server reply:{Fore.RESET}',json.dumps(r.json()),msgType='info-3',msgOffset='+1',msgColor=Fore.CYAN)
        # api_reply = r.json()
        print( r.json())
    else:
        # log_message(f'{Fore.RED}server reply:{Fore.RESET}', r.text, msgType='info-1', msgOffset='+1', msgColor=Fore.BLUE)
        # api_reply = {'data': r.text}
        print( r.text)
else:
    errormsg=f"{r.reason}:{r.text}"
    # log_message(f'{Fore.WHITE}server reply:{Fore.RESET}', errormsg, msgType='error', msgOffset='+1')
    # api_reply = {'api_status': 'system error', 'api_message': errormsg}        
    print(errormsg)