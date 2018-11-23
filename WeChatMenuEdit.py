# encoding: utf-8

import json
import urllib
import urllib2
import requests
appid=""
secret=""
access_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(appid,secret)
menu_url = "https://api.weixin.qq.com/cgi-bin/menu/create?%s"
def generate_menu(token):
    menus = {
     "button":[
     {    
          "type":"click",
          "name":"网上商城",
          "key":"wssc"
      },
     {    
          "type":"click",
          "name":"成绩查询",
          "key":"cjcx"
      },
      {
           "name":"饭卡管理",
           "sub_button":[
           {    
               "type":"click",
               "name":"饭卡充值",
               "key":"fkcz"
            },
            {
               "type":"click",
               "name":"绑定管理",
               "key":"bdgl"
            },
            {
               "type":"click",
               "name":"余额及详情",
               "key":"yecx"
            }]
       }]
 
    }
    params = {'access_token': urllib.quote(token)}
    url = menu_url % urllib.urlencode(params)
    request = urllib2.Request(url, json.dumps(menus, ensure_ascii=False))
    response = urllib2.urlopen(request)
    print(response.read())
if __name__ == '__main__':
    req=requests.get(access_url).text
    a=json.loads(req)
    generate_menu(a['access_token'])