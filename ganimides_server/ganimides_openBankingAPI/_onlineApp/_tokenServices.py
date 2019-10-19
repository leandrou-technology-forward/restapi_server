# token_services/token_services.py
#import sys
import random
from itsdangerous import URLSafeTimedSerializer
#from myApp import app
from _utilities import get_rand_string

def generate_token(parWhat):
    secret_key='spithas'
    salt_password='chaos490px!'
    serializer = URLSafeTimedSerializer(secret_key)
    token=serializer.dumps(parWhat, salt_password)
    return token

def generate_confirmation_token(parWhat):
    #MAIL_userName = os.environ['APP_MAIL_userName']
    #MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']
    #secret_key=app.config['SECRET_KEY']
    #salt_password=app.config['SECURITY_PASSWORD_SALT']
    secret_key='spithas'
    salt_password='chaos490px!'
    serializer = URLSafeTimedSerializer(secret_key)
    token=serializer.dumps(parWhat, salt_password)
    return token
    
def generate_sms_friendly_confirmation_token(what):
    s1 = get_rand_string(length=12, allowed_chars='0123456789ABCDEF')
    # for ix in range(0,len(what)):
    #     a = random.randint(ord('A'), ord('Z'))
    #     c = str(chr(a))
    return s1

def generate_otp():
    n = random.randint(100000, 999999)
    return (str(n))

def confirm_token(parToken, parExpiration=3600):
    #MAIL_userName = os.environ['APP_MAIL_userName']
    #MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']
    #secret_key=app.config['SECRET_KEY']
    #salt_password=app.config['SECURITY_PASSWORD_SALT']
    secret_key='spithas'
    salt_password='chaos490px!'
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        what = serializer.loads(
            parToken,
            salt=salt_password,
            max_age=parExpiration
        )
    except:
        return None
    return what

def token_is_valid(parToken, parExpiration=3600):
    #MAIL_userName = os.environ['APP_MAIL_userName']
    #MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']
    #secret_key=app.config['SECRET_KEY']
    #salt_password=app.config['SECURITY_PASSWORD_SALT']
    secret_key='spithas'
    salt_password='chaos490px!'
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        serializer.loads(
            parToken,
            salt=salt_password,
            max_age=parExpiration
        )
        
    except:
        return False
    return True
def decrypted_token(parToken):
    #MAIL_userName = os.environ['APP_MAIL_userName']
    #MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']
    #secret_key=app.config['SECRET_KEY']
    #salt_password=app.config['SECURITY_PASSWORD_SALT']
    secret_key='spithas'
    salt_password='chaos490px!'
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        what = serializer.loads(
            parToken,
            salt=salt_password,
            max_age=999999
        )
    except:
        return None
    return what

def generate_mobileconfirmation_code(parWhat):
    codeInt=random.randint(100000,999999)
    codeStr=str(codeInt)
    return codeStr
if __name__ == '__main__':
    #tests/research
    what = '1111ssssssss111222a222222222233333AAAAAAAAAA33333333333'
    what={'x':2,'y':3}
    r = generate_token(what)
    print(r)
    what = '1111ssssssss111222222222222233333AAAAAAAAAA33333333333'
    r = generate_token(what)
    print(r)
    #print(confirm_token('eyJ4IjoxLCJ5IjoyfQ.EBB-0Q.NriDfz1LBt1Nsb_h7dI7ysWOxXU', parExpiration=1))
    

    


