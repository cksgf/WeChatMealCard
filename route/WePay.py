
'''
处理微信支付，包括回调处理
'''

from flask import request,render_template,redirect,send_file, send_from_directory,url_for,session,make_response
from index import app,sql,AccessToken
import qrcode
import time
import hashlib
from config.config import *
from lxml import etree
import json
from config.wxpay import WxPay, get_nonce_str, dict_to_xml, xml_to_dict
pay_list_nor=[]

#请求支付-扫码/旧版
@app.route('/payqr/<openid>',methods=['GET','POST'])
def create_pay(openid=None):
    if not openid :
        return 'Who are you'
    if request.method == 'GET':
        return render_template('WePay/payfor.html',openid=openid)
    else:
        money=request.form['money']
        if money == '0.01':
            money='1'
        else:
            money=str(abs(int(request.form['money']))*100)
        nonce_str=hashlib.md5((openid+str(time.time())).encode()).hexdigest()
        #pay_list_nor.append(nonce_str)
        data = {
            'appid': appid,
            'mch_id': mch_id,
            'nonce_str': nonce_str,
            'body': '测试——饭卡充值',                              # 商品描述
            'out_trade_no': str(int(time.time())),       # 商户订单号
            'total_fee': money,                              #价格
            'spbill_create_ip': '59.110.217.126',
            'notify_url': notify_url,
            'attach': '测试支付订单',
            'trade_type': 'NATIVE',
            'openid': openid
        }

        wxpay = WxPay(merchant_key, **data)
        pay_info = wxpay.get_pay_info()
        if pay_info:
            xml = etree.fromstring(pay_info)
            qrcodeurl=xml.find("code_url").text
            qrcodeurl=qrcode.make(qrcodeurl)
            pic='static/payqr/'+openid+str(time.time())+'.png'
            qrcodeurl.save(pic)
            return render_template('WePay/payforqr.html',pic=pic)
        return str({'errcode': 40001, 'errmsg': '请求支付失败'})
#公众号调用JS拉起微信支付页面
@app.route("/payss/",methods=["POST","GET"])
def test():
    if request.method=='GET' :
        return 'Who are you'
    else:
        money=request.form['money']
        if money == '0.01':
            money='1'
        else:
            money=str(abs(int(request.form['money']))*100)
        openid=request.form['openid']
        nonce_str=hashlib.md5((openid+str(time.time())).encode()).hexdigest()
        timestamp=str(int(time.time()))
        #pay_list_nor.append(nonce_str)
        data = {
            'appid': appid,
            'mch_id': mch_id,
            'nonce_str': nonce_str,
            'body': '饭卡充值',              # 商品描述
            'out_trade_no': timestamp,       # 商户订单号
            'total_fee': money,              #价格
            'spbill_create_ip': '123.207.137.254',
            'notify_url': notify_url,
            'attach': '支付订单',
            'trade_type': 'JSAPI',
            'openid': openid
        }

        wxpay = WxPay(merchant_key, **data)
        pay_info = wxpay.get_pay_info()
        if not pay_info:
            return '请求支付失败'
        xml = etree.fromstring(pay_info)
        prepay_id=xml.find("prepay_id").text
        nonce_str=xml.find("nonce_str").text
        pay_data={'appId':appid,
  'nonceStr':nonce_str,
  'package':f'prepay_id={prepay_id}',
  'signType':'MD5',
  'timeStamp':timestamp
  }
        stringA = '&'.join(["{0}={1}".format(k, pay_data.get(k))for k in sorted(pay_data)])
        stringSignTemp = '{0}&key={1}'.format(stringA, merchant_key)
        paySign = hashlib.md5(stringSignTemp.encode()).hexdigest()
        #paySign=f'appId={appid}&nonceStr={nonce_str}&package=prepay_id={prepay_id}&signType="MD5"&timeStamp={timestamp}'
        signature=hashlib.md5(paySign.encode()).hexdigest()
        return render_template('WePay/payPassword.html',appid=appid,timestamp=timestamp,nonceStr=nonce_str,signature=signature,openid=openid,prepay_id=prepay_id,paySign=paySign)
#选择金额，跳转支付页面
@app.route('/pay/<openid>')
def payTemp(openid=None):  
    return render_template('WePay/payTemp.html',openid=openid)
  
#支付回调通知
@app.route('/qrpay', methods=['POST'])
def wxpay():
    if request.method == 'POST':
        d=request.get_data()
        xml = etree.fromstring(d)
        _pay_su=xml.find("result_code").text
        if _pay_su == 'SUCCESS':
            _openid=xml.find("openid").text
            _total_fee=int(xml.find("total_fee").text)/100
            _transaction_id=xml.find("transaction_id").text
            #查询饭卡号码
            _card=sql.selectStudentAll(WeChatID=_openid)[1][0][6]
            #充值
            insertMealCardDict={
                 'MealCard':_card,
                 'ReduceMealCardMoney':-_total_fee,
                 'RECORD':f'饭卡充值',
                 'Number':_transaction_id,
                 'p':d
            }         
            paynb=sql.insertMealCard(MealCardDict=insertMealCardDict)
            if paynb[0] == 'success':
                print(str(paynb[1]))
            else:
                print(str(paynb[1]))
        result_data = {
            'return_code': 'SUCCESS',
            'return_msg': 'OK'
        }
        return dict_to_xml(result_data), {'Content-Type': 'application/xml'}  