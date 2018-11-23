#coding:utf-8
appid=''                                  #公众号appid
secret=''                   #公众号secret
wenrui=''                                             #网页API验证口令
mch_id = ''                                       # 商户号
total_fee = ''                                              # 总金额
spbill_create_ip = ''                         # 终端IP
notify_url = ''                # 通知回调地址
trade_type = 'JSAPI'                                        # 交易类型
merchant_key = ''           # 商户KEY

'''---------------------------------------------------------------------------------------'''
replysubscribe='欢迎关注！'                                 #公众号受到关注后回复的文本
#关键词回复
reply_text={
'你好':'你好呀',
'你是谁':'测试用例'
}

#绑定/更新模版json
replyBindJson={
"touser":'发送人',
"template_id":"9x-JkVT2SR7kI-1e3dzHJfN9UU2ozuKXuig5yWPF_7c",
"url":'点击跳转URL',
"topcolor":"#FF0000",
"data":{
"first": {
"value":"标题",
"color":"#173177"
},
"keyword1":{
"value":"是否绑定",
"color":"#173177"
},
"keyword2":{
"value":'当前时间',
"color":"#173177"
},
"remark":{
"value":"前往绑定或前往修改",
"color":"#173177"
}
}
}

#查询模版json
replySecectJson={
"touser":'发送人',
"template_id":"Q4ppZgSzdLS55mb6VMEcYIeuHhc2SwLbQ6AgBctUsqc",
"url":'点击跳转URL',
"topcolor":"#FF0000",
"data":{
"first": {
"value":"饭卡号码",
"color":"#173177"
},
"keyword1":{
"value":"绑定的学生姓名",
"color":"#173177"
},
"keyword2":{
"value":'卡上余额',
"color":"#173177"
},
"keyword3":{
"value":'当前时间',
"color":"#173177"
},
"remark":{
"value":"点击查看消费详情",
"color":"#173177"
}
}
}

