from flask import Flask,render_template
from config.accesstoken import AccessToken
from sqlitedb.SqliteConnect import sqldb
AccessToken=AccessToken()
sql=sqldb()
app=Flask(__name__)
app.secret_key='1996-05-16'
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
if __name__ == '__main__':
    from route.WePay import *
    from route.WeChatRoute import *
    from route.WebApiRoute import *
    app.run(host='0.0.0.0',port=800,debug=True)