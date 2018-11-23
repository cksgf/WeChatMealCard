import requests
import json
import time
from config.config import appid,secret
#维护微信的accesstoken，在保证其时效性的前提下，尽量少的进行更新，需要获取accesstoken时，调用token下的GetToken方法即可
class AccessToken:
    def __init__(self):
        self.real_token=[]
        self.real_ticket=[]
        self.url=f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}'
    def RequestToken(self):
        mess=json.loads(requests.get(self.url).content.decode())
        try:
            self.real_token = [mess['access_token'],time.time()+int(mess['expires_in'])-30]
        except Exception as e:
            print('error',e)
    def GetToken(self):
        if (self.real_token==[]) or (time.time() >= self.real_token[1]):
            self.RequestToken()
        else:
            pass
        return self.real_token[0]
    def RequestTicket(self):
        tic=json.loads(requests.get(f"https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={self.GetToken()}&type=jsapi").content.decode())
        try:
            self.real_ticket = [tic['ticket'],time.time()+int(tic['expires_in'])-30]
        except Exception as e:
            print('error',e)
    def GetTicket(self):
        if (self.real_ticket==[]) or (time.time() >= self.real_ticket[1]):
            self.RequestTicket()
        else:
            pass
        return self.real_ticket[0]

if __name__ == '__main__':
    pass