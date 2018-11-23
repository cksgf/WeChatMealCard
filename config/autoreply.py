from config.config import reply_text,replysubscribe,replyBindJson,replySecectJson
import time 
import requests
import json
from index import sql,AccessToken
class AutoReply:
    def __init__(self):
        self.reply_text=reply_text
        self.replysubscribe=replysubscribe
        self.replyBindJson=replyBindJson
        self.replySecectJson=replySecectJson
    def ReplyText(self,message=None,fromUser=None):
        if message == '绑定':
            weChatAccessToken=AccessToken.GetToken()
            arealy = sql.selectStudentAll(fromUser)
            if (arealy[0]=='success') and (len(arealy[1]) >= 1) :
                #已绑定过
                self.replyBindJson['touser']=fromUser
                self.replyBindJson['url']=f'http://wxgl.wenrui.work/UpdataStudentInfo/{fromUser}'
                self.replyBindJson['data']['first']['value']="您已绑定为"+arealy[1][0][2]
                self.replyBindJson['data']['keyword1']['value']="已绑定"
                self.replyBindJson['data']['keyword2']['value']=str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
                self.replyBindJson['data']['remark']['value']="点击前往更改"
            else:
                #未绑定
                self.replyBindJson['touser']=fromUser
                self.replyBindJson['url']=f'http://wxgl.wenrui.work/BindStudentInfo/{fromUser}'
                self.replyBindJson['data']['first']['value']="您还没有绑定信息"
                self.replyBindJson['data']['keyword1']['value']="未绑定"
                self.replyBindJson['data']['keyword2']['value']=str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
                self.replyBindJson['data']['remark']['value']="点击前往绑定"
            requests.post(f'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={weChatAccessToken}',data=json.dumps(self.replyBindJson))
            return None
        elif message == '查询':
            arealy = sql.selectStudentAll(fromUser)
            weChatAccessToken=AccessToken.GetToken()
            if (arealy[0]=='success') and (len(arealy[1]) >= 1) :
                #已绑定过
                card=arealy[1][0][6]
                _now_money=sql.selectMealCardMoney(card)[1]
                print(sql.selectMealCardMoney(card))
                self.replySecectJson['touser']=fromUser
                self.replySecectJson['url']=f'http://wxgl.wenrui.work/selectMealCardMoney/{card}'
                self.replySecectJson['data']['first']['value']=f"饭卡号码为{card}的余额"
                self.replySecectJson['data']['keyword1']['value']=arealy[1][0][2]
                self.replySecectJson['data']['keyword2']['value'] = f"您的饭卡余额为{_now_money}"
                self.replySecectJson['data']['keyword3']['value']=str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
                self.replySecectJson['data']['remark']['value']="点击查看详情记录"
                requests.post(f'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={weChatAccessToken}',data=json.dumps(self.replySecectJson))
                return None
            else:
                #未绑定
                self.replyBindJson['touser']=fromUser
                self.replyBindJson['url']=f'http://wxgl.wenrui.work/BindStudentInfo/{fromUser}'
                self.replyBindJson['data']['first']['value']="您还没有绑定信息"
                self.replyBindJson['data']['keyword1']['value']="未绑定"
                self.replyBindJson['data']['keyword2']['value']=str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
                self.replyBindJson['data']['remark']['value']="点击前往绑定"
                requests.post(f'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={weChatAccessToken}',data=json.dumps(self.replyBindJson))
                return None
        elif message == 'wenrui':
            return f'http://wxgl.wenrui.work/pay/{fromUser}'
        elif message in self.reply_text:
            return self.reply_text[message]
        else:
            return None
    def ReplySubscribe(self):
        return replysubscribe
    def ReplyEvent(self,ClickType,fromUser):
        if ClickType == 'wssc':
            return '网上商城功能建设中...'
        elif ClickType == 'cjcx':
            return '成绩查询功能建设中...'
        elif ClickType == 'bdgl':
            self.ReplyText(message='绑定',fromUser=fromUser)
            return None
        elif ClickType == 'fkcz':
            arealy = sql.selectStudentAll(fromUser)
            weChatAccessToken=AccessToken.GetToken()
            if (arealy[0]=='success') and (len(arealy[1]) >= 1) :
                #已绑定过
                card=arealy[1][0][6]
                _now_money=sql.selectMealCardMoney(card)[1]
                print(sql.selectMealCardMoney(card))
                self.replySecectJson['touser']=fromUser
                self.replySecectJson['url']=f'http://wxgl.wenrui.work/pay/{fromUser}'
                self.replySecectJson['data']['first']['value']=f"饭卡号码为{card}的余额"
                self.replySecectJson['data']['keyword1']['value']=arealy[1][0][2]
                self.replySecectJson['data']['keyword2']['value'] = f"您的饭卡余额为{_now_money}"
                self.replySecectJson['data']['keyword3']['value']=str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
                self.replySecectJson['data']['remark']['value']="【点击进行充值】"
                requests.post(f'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={weChatAccessToken}',data=json.dumps(self.replySecectJson))
                return None
            else:
                #未绑定
                self.replyBindJson['touser']=fromUser
                self.replyBindJson['url']=f'http://wxgl.wenrui.work/BindStudentInfo/{fromUser}'
                self.replyBindJson['data']['first']['value']="您还没有绑定信息"
                self.replyBindJson['data']['keyword1']['value']="未绑定"
                self.replyBindJson['data']['keyword2']['value']=str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
                self.replyBindJson['data']['remark']['value']="点击前往绑定"
                requests.post(f'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={weChatAccessToken}',data=json.dumps(self.replyBindJson))
                return None
        elif ClickType == 'yecx':
            self.ReplyText(message='查询',fromUser=fromUser)
            return None
        return None
if __name__ == '__main__':
    pass