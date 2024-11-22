import requests
import json
import time

# https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=105ad1a05c26d22477283846e582d198&redirect_uri=https://example.com/oauth
url = 'https://kauth.kakao.com/oauth/token'
rest_api_key = '105ad1a05c26d22477283846e582d198'
redirect_uri = 'https://example.com/oauth'
authorize_code = 'ihGKlcExrUP3BQGvw8KaiNFUd2Vf53bUDxyEUAxA4ou5SEhaNY04AEPHYHL67enpbJIS6wo9dZwAAAGIn09VIA'

# with open("kakao_code.json", "r") as fp:
#     ts = json.load(fp)
# authorize_code = ts["access_token"]

def f_auth():
    data = {
        'grant_type': 'authorization_code',
        'client_id': rest_api_key,
        'redirect_uri': redirect_uri,
        'code': authorize_code,
    }

    response = requests.post(url, data=data)
    tokens = response.json()

    with open("kakao_code.json", "w") as fp:
        json.dump(tokens, fp)
    with open("kakao_code.json", "r") as fp:
        ts = json.load(fp)
    r_token = ts["refresh_token"]
    return r_token

def f_auth_refresh(r_token):
    with open("kakao_code.json", "r") as fp:
        ts = json.load(fp)
    data = {
        "grant_type": "refresh_token",
        "client_id": rest_api_key,
        "refresh_token": r_token
    }
    response = requests.post(url, data=data)
    tokens = response.json()

    with open("kakao_code.json", "w") as fp:
        json.dump(tokens, fp)
    with open("kakao_code.json", "r") as fp:
        ts = json.load(fp)
    token = ts["access_token"]
    return token

def f_send_talk(token, text):
    header = {'Authorization': 'Bearer ' + token}
    url = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'  
    post = {
        'object_type': 'text',
        'text': text,
        'link': {
            'web_url': 'https://developers.kakao.com',
            'mobile_web_url': 'https://developers.kakao.com'
        },
        'button_title': '확인'
    }
    data = {'template_object': json.dumps(post)}
    return requests.post(url, headers=header, data=data)

r_token = f_auth()

while(1):
    token = f_auth_refresh(r_token)  
    # kapi.kakao.com/v2/api/talk/memo/default/send 
    response = f_send_talk(token, "Hello World!")
    response.status_code
    print("I'm OK!")
    print(token)
    time.sleep(60)
    


