'''
本文件为处理微信端的访问，
1.对于微信后台，验证后台地址有效性、验证js安全域名
2.对于微信用户，处理用户关注、用户消息、点击菜单等事件
'''
from lxml import etree
import time
from flask import request,render_template,redirect,url_for
from index import app,sql
from config.autoreply import AutoReply
AutoReply=AutoReply()

#验证微信后台可用性，处理微信接受的文本消息推送、事件推送
@app.route('/WeChatServer',methods=['GET','POST'])
def WeChatServer():
    if request.method=='GET':
        return request.values.get('echostr')
    else:       
        str_xml = request.get_data()
        xml = etree.fromstring(str_xml) #XML解析
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        print(f"from {fromUser}")
        if msgType=='text':
            returnContent=AutoReply.ReplyText(message=xml.find("Content").text,fromUser=fromUser)
            if returnContent:
                return render_template('WeChatMessage/ReturnText.xml',toUser=fromUser,fromUser=toUser,createTime=int(time.time()),content=returnContent)
            else:
                return 'success'
        elif msgType == 'event':
            eventType=xml.find("Event").text
            if eventType == 'subscribe':
                return render_template('WeChatMessage/ReturnText.xml',toUser=fromUser,fromUser=toUser,createTime=int(time.time()),content=AutoReply.ReplySubscribe())
            elif eventType == 'CLICK':
                returnContent=AutoReply.ReplyEvent(ClickType=xml.find("EventKey").text,fromUser=fromUser)
                if returnContent:
                    return render_template('WeChatMessage/ReturnText.xml',toUser=fromUser,fromUser=toUser,createTime=int(time.time()),content=returnContent)
                else:
                    return 'success'
        else:
            return 'success'

#绑定学生信息
@app.route('/BindStudentInfo/<wxid>',methods=['GET','POST'])
def BindStudentInfo(wxid=None):
    if 'MicroMessenger' in str(request.headers):
        pass
    else :
        return "请在微信浏览器中打开"
    if request.method == 'GET':
        arealy = sql.selectStudentAll(wxid)
        if (arealy[0]=='success') and (len(arealy[1]) >= 1) :
            return render_template('WeChatClientWeb/BindStudentInfo.html',url='UpdataStudentInfo',st='更新',wxid=wxid,StudentName=arealy[1][0][2],ParentName=arealy[1][0][3],ParentTel=arealy[1][0][4],MealCard=arealy[1][0][6],HomeAddress=arealy[1][0][5])
        else:
            return render_template('WeChatClientWeb/BindStudentInfo.html',url='BindStudentInfo',st='绑定',wxid=wxid,StudentName='',ParentName='',ParentTel='',MealCard='',HomeAddress='')
    else:
        try:
            studentDict={
                'WeChatID':wxid,
                'StudentName':request.form['StudentName'],
                'ParentName':request.form['ParentName'],
                'ParentTel':request.form['ParentTel'],
                'HomeAddress':request.form['HomeAddress'],
                'MealCard':request.form['MealCard']
            }
        except Exception as e:
            return render_template('WeChatClientWeb/Result.html',text=str(e),errcode="1001") 
        else:
            mess=sql.insertStudent(studentDict=studentDict)
            if mess[0] == 'success':
                return render_template('WeChatClientWeb/Result.html',text='绑定完成！')
            else:
                return render_template('WeChatClientWeb/Result.html',text=str(mess[1]),errcode="1002") 
#更新绑定信息
@app.route('/UpdataStudentInfo/<wxid>',methods=['GET','POST'])
def UpdataStudentInfo(wxid=None):
    if 'MicroMessenger' in str(request.headers):
        pass
    else :
        return "请在微信浏览器中打开"
    if request.method == 'GET':
        arealy = sql.selectStudentAll(wxid)
        if (arealy[0]=='success') and (len(arealy[1]) >= 1) :
            return render_template('WeChatClientWeb/BindStudentInfo.html',st='更新',url='UpdataStudentInfo',wxid=wxid,StudentName=arealy[1][0][2],ParentName=arealy[1][0][3],ParentTel=arealy[1][0][4],MealCard=arealy[1][0][6],HomeAddress=arealy[1][0][5])
        else:
            return render_template('WeChatClientWeb/BindStudentInfo.html',st='绑定',url='BindStudentInfo',wxid=wxid,StudentName='',ParentName='',ParentTel='',MealCard='',HomeAddress='')
    else:
        try:
            studentDict={
               'WeChatID':wxid,
               'StudentName':request.form['StudentName'],
               'ParentName':request.form['ParentName'],
               'ParentTel':request.form['ParentTel'],
               'HomeAddress':request.form['HomeAddress'],
               'MealCard':request.form['MealCard']
            }
        except Exception as e:
            return render_template('WeChatClientWeb/Result.html',text=str(e),errcode="1001") 
        else:
            mess=sql.updateStudent(studentDict=studentDict)
            if mess[0] == 'success':
                return render_template('WeChatClientWeb/Result.html',text='修改成功！')
            else:
                return render_template('WeChatClientWeb/Result.html',text=str(mess[1]),errcode="1002") 

#查询饭卡消费详情
@app.route('/selectMealCardMoney/<cardid>',methods=['GET'])
def selectMealCardMoney(cardid=None):
    if cardid :
        pass
    else:
        return "hi"
    ms=sql.selectMealCardRecord(cardid)
    if ms[0] == 'success':
        return render_template('WeChatClientWeb/SelectMealCardRecord.html',record=list(ms[1])[::-1][:30])
    else:
        return render_template('WeChatClientWeb/Result.html',text=str(ms[1]),errcode="1002") 
#微信js安全域名校验
@app.route('/MP_verify_2lbwKqYZfbwACVRF.txt',methods=['GET'])
def MP_verify_2lbwKqYZfbwACVRF():
    return '2lbwKqYZfbwACVRF'
  