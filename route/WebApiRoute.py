'''
本文件为网页端处理饭卡信息
'''
import json
from flask import request,render_template,redirect,send_file, send_from_directory,url_for,session,make_response
from index import app,sql
from config.config import wenrui
import re
import os
import xlwt
import time
from functools import wraps
pwd={'ADMIN':'password'}

#验证登录的修饰器
def cklogin(**kw):
    def ck(func):
        @wraps(func)
        def _ck(*args, **kwargs):
            password=session.get('password')
            name=session.get('username')
            if name in pwd:
                if password == pwd[name]:
                    return func(*args, **kwargs)
                else:
                    return redirect(url_for('login'))
            else:
                return redirect(url_for('login'))
        return _ck
    return ck


#--------------------API类处理-----------------------------
#首页框架
@app.route('/',methods=['GET','POST'])
@cklogin()
def admin():
    date=time.localtime(time.time())
    week={0:'一',1:'二',2:'三',3:'四',4:'五',5:'六',6:'日'}
    if request.method=='POST':
        redpath=request.form['path']
        return render_template('WebApi/index.html',date=f"{date[0]}年{date[1]}月{date[2]}日",week=week[date[6]],url=redpath)
    return render_template('WebApi/index.html',date=f"{date[0]}年{date[1]}月{date[2]}日",week=week[date[6]],url='/main')

#登陆
@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=='POST':
        if request.form['username'] in pwd:
            if request.form['password'] == pwd[request.form['username']]:
                try:
                    session['json']=request.form['json']
                except:
                    session['json']='None'  
                session['password']=request.form['password']
                session['username']=request.form['username']
                if session['json'] == 'True':
                    return json.dumps({
                                   'code':'success',
                                   'errorcode': 'None',
                                   'value': {'result':"LoginSuccess"}
                                  })
                return redirect(url_for('admin'))
            else:
                return render_template('WebApi/Login.html',message='密码错误')
        else:
                return render_template('WebApi/Login.html',message='账号不存在')
    else:
        return render_template('WebApi/Login.html',message='')

#登出
@app.route("/loginout",methods=["POST","GET"])
def loginout():
    session['password']=None
    session['username']=None
    session['json']=None
    return redirect(url_for('admin'))

#创建饭卡档案
@app.route('/CreatMealCard',methods=['GET','POST'])
@cklogin()
def CreatMealCard():
    if request.method == 'GET':
        return render_template('WebApi/CreatMealCard.html')
    else:
        try:
           mealCard=request.form['MealCard']
           mealcardmoney=request.form['MealCardMoney']
           if request.form['pwd'] == wenrui:
               pass
           else:
               return render_template('WebApi/Result.html',text='口令错误',errcode='1001')
        except Exception as e:
            if session['json']=='True':
                return json.dumps({
                                   'code':'error',
                                   'errorcode': '1001',
                                   'value': {'result':str(e)}
                                  })
            return render_template('WebApi/Result.html',text=str(e),errcode='1002')
        else:
            mess=sql.creatMealcard(mealCard=mealCard,mealcardmoney=mealcardmoney)
            if mess[0] == 'success':
                if session['json']=='True':
                    return json.dumps({'code':'success','errorcode': 'None','value': {'result':'success'}})
                return render_template('WebApi/Result.html',text='提交成功')
            else:
                if session['json']=='True':
                    return json.dumps({
                                       'code':'error',
                                       'errorcode': '1002',
                                       'value': {'result':mess[1]}
                                       })
                return render_template('WebApi/Result.html',text=mess[1],errcode='1002')


#更新金额
@app.route('/ReduceMealCardMoney',methods=['GET','POST'])
@cklogin()
def ReduceMealCardMoney():
    if request.method == 'GET':
        return render_template('WebApi/ReduceMealCardMoney.html')
    else:
        if request.form['pwd'] == wenrui:
            pass
        else:
            return render_template('WebApi/Result.html',text='口令错误',errcode='1001')
        try:
            ReduceMealCardMoney={
               'MealCard':request.form['MealCard'],
               'RECORD':request.form['RECORD'],
               'ReduceMealCardMoney':request.form['ReduceMealCardMoney'],
               'Number':False,
               'p':'0'
            }
        except Exception as e:
            if session['json']=='True':
                return json.dumps({
                                   'code':'error',
                                   'errorcode': '1001',
                                   'value': {'result':e}
                                   })
            return render_template('WebApi/Result.html',text=str(e),errcode='1001')
        else:
            mess=sql.insertMealCard(MealCardDict=ReduceMealCardMoney)
            if mess[0] == 'success':
                if session['json']=='True':
                    return json.dumps({
                                        'code':'success',
                                        'errorcode': 'None',
                                        'value': {'result':'success'}
                                     })
                return render_template('WebApi/Result.html',text='提交成功')
            else:
                if session['json']=='True':
                    return json.dumps({
                                       'code':'error',
                                       'errorcode': '1002',
                                       'value': {'result':mess[1]}
                                      })
                return render_template('WebApi/Result.html',text=mess[1],errcode='1002')


#-------------------------业务类-------------
#查询今日流水
@app.route('/SelectMealLog',methods=['GET','POST'])
@cklogin()
def selectMealLog():
    if request.method=='GET':
        types=request.values.get('types')
        date=request.values.get('date')
        if not types:
            types='pay'
        if not date:
            date=str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
        ckd={"pay":'',"rechange":''}
        ckd[types]='checked="checked"'
        record = sql.selectMealLog(date=date,types=types)
        moneys = abs(sum(int(float(i[2])*1000) for i in record[1]))/1000
        return render_template('WebApi/SelectMealLog.html',ckd=ckd,date=date,record=record[1][::-1][:30],moneys=moneys,types=('消费' if types=='pay' else '充值'))
    else:
        try:
            date=request.form['day']
        except:
            date=str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
        record = sql.selectMealLog(date=date,types='all')
        if record[0] == 'success':
            workbook = xlwt.Workbook(encoding = 'ascii')
            worksheet = workbook.add_sheet('sheet')
            worksheet.write(0, 0, label = '饭卡号')
            worksheet.write(0, 1, label = '时间')
            worksheet.write(0, 2, label = '消费前金额')
            worksheet.write(0, 3, label = '本次消费金额')
            worksheet.write(0, 4, label = '消费后金额')
            worksheet.write(0, 5, label = '消费详情')
            worksheet.write(0, 6, label = '订单号')
            worksheet.write(0, 7, label = '订单类型')
            _nowSheet=1
            for i in record[1]:
                temp=0
                for t in [5,0,7,2,4,1,3,6]:
                    worksheet.write(_nowSheet, temp, label = i[t])
                    temp+=1
                _nowSheet+=1
            filename = f'{date}.xls'
            workbook.save(filename)
            response = make_response(send_from_directory(os.getcwd() ,filename,as_attachment=True))
            response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
            return response
        else:
            return render_template('WebApi/Result.html',text=record[1],errcode='1002')


#查询全部用户
@app.route('/selectStudentTable',methods=['GET','POST'])
@cklogin()
def selectStudentTable():
    if request.method == 'GET':
        ms=sql.selectStudentTable()
        if ms[0] == 'success':
            return render_template('WebApi/SelectStudentTable.html',record=ms[1][::-1])
        else:
            return render_template('WebApi/Result.html',text=str(ms[1]),errcode='1002')
    else:
        ms=sql.selectStudentTable()
        keys=request.form['keys']
        mss=[]
        if ms[0] == 'success':
            for i in ms[1]:
                if keys in str(i):
                    temp=[]
                    for s in i:
                        s=re.sub(keys,f'<span style="color:red    ">{keys}</span>',s)
                        temp.append(s)
                    mss.append(temp)
            return render_template('WebApi/SelectStudentTable.html',record=mss[::-1])
        else:
            return render_template('WebApi/Result.html',text=str(ms[1]),errcode='1002')
#网页输入卡号查询记录
@app.route('/selectMealCardMoneyForWeb',methods=['GET'])
@cklogin()
def selectMealCardMoneyForWeb():
    _seachKey=request.values.get('cardid')
    '''try:
        page=int(request.values.get('page'))
    except:
        page=1
    page=(1 if not page else page)'''
    if not _seachKey:
        return render_template('WebApi/SelectMealCardRecord.html',record=[],seachKey='')#,page_len=[],now_page=1
    else:
        ms=sql.selectMealCardRecord(_seachKey)
        if ms[0] == 'success':
            if session['json']=='True':
                return json.jumps({'code':'success',
                                   'errorcode':'None',
                                   'value':{'result':list(ms[1])[::-1]}
                                 })
            '''temp_page=[]
            page_l=ms[1][::-1]
            for i in range(page*10-10,page*10):
                try:
                    temp_page.append(page_l[i])
                except:
                    pass
            page_len=range(1,int(len(page_l)/10)+2)'''
            return render_template('WebApi/SelectMealCardRecord.html',record=ms[1][::-1][:50],seachKey=_seachKey)#,page_len=page_len,now_page=page
        else:
            return render_template('WebApi/Result.html',text=str(ms[1]),errcode='1002') 