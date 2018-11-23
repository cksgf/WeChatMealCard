# encoding: utf-8
import sqlite3
import time
import os
import hashlib
from decimal import getcontext, Decimal
class sqldb:
    def __init__(self):
        sqlpath =(os.path.dirname(os.path.realpath(__file__)))
        studentdb ='student.db'
        mealcarddb ='mealcard.db'
        updatadb='updatadb.db'
        if studentdb in os.listdir(sqlpath):
            print(f"{studentdb} was already")
            self.st_conn = sqlite3.connect(sqlpath+os.sep+studentdb,check_same_thread=False)
        else:
            print(f"{studentdb} is done , creat now...")
            self.st_conn = sqlite3.connect(sqlpath+os.sep+studentdb,check_same_thread=False)
            self.st_conn.execute('''CREATE TABLE STUDENT
               (WeChatID           TEXT,
               StudentID           TEXT,
               StudentName         TEXT,
               ParentName          TEXT,
               ParentTel           TEXT,
               HomeAddress         TEXT,
               MealCard            TEXT,
               TIM                 TEXT);''')
            self.st_conn.execute('''CREATE TABLE MEALCARD
               (MealCard            TEXT,
               MealCardMoney       TEXT);''')
        if mealcarddb in os.listdir(sqlpath):
            print(f"{mealcarddb} was already")
        else:
            print(f"{mealcarddb} is done , creat now...")
        self.mc_conn = sqlite3.connect(sqlpath+os.sep+mealcarddb,check_same_thread=False)
        if updatadb in os.listdir(sqlpath):
            print(f"{updatadb} was already")
        else:
            print(f"{updatadb} is done , creat now...")
        self.up_conn = sqlite3.connect(sqlpath+os.sep+updatadb,check_same_thread=False)
    def getTime(self):
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    def getId(self,WeChatID):
        return hashlib.md5(WeChatID.encode()).hexdigest()
    def getDate(self):
        return str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
    #创建饭卡号码及金额，创建饭卡消费记录表
    def creatMealcard(self,mealCard,mealcardmoney):
        mealCard=str(mealCard)
        mealcardmoney=str(mealcardmoney)
        self.st_conn.execute("INSERT INTO MEALCARD (MealCard,MealCardMoney ) VALUES (?,?)", (mealCard,mealcardmoney))
        self.st_conn.commit()
        try :
            self.mc_conn.execute(f'''CREATE TABLE '{mealCard}'
               (TIM                    TEXT,
               RECORD                  TEXT,
               ReduceMealCardMoney     TEXT,
               Number                  TEXT,
               MoneyNow                TEXT,
               ReduceMealCardId        TEXT,
               p                       TEXT);''')
        except Exception as e:
            return ['error',str(e)]
        else:
            return ['success','success']

    #绑定微信ID和用户信息
    def insertStudent(self,studentDict):
        try:
            #先查重
            _wxid=studentDict['WeChatID']
            arealy = self.selectStudentAll(_wxid)
            if (arealy[0]=='success') and (len(arealy[1]) >= 1) :
                return ['error',arealy[1]]
            print('查重通过')
            _MealCard=studentDict['MealCard']
            _stid=self.getId(_wxid)
            #检查绑定的饭卡是否存在
            temp = list(self.st_conn.execute('SELECT MealCardMoney from MEALCARD WHERE MealCard=?',(_MealCard,)).fetchall())
            if len(temp)>=1:
                pass
            else:
                return ['error','绑定的饭卡不存在']
            trpm=[(_wxid,_stid,studentDict['StudentName'],studentDict['ParentName'],studentDict['ParentTel'],studentDict['HomeAddress'],_MealCard,self.getTime())]
            self.st_conn.executemany("INSERT INTO STUDENT (WeChatID,StudentID,StudentName,ParentName,ParentTel,HomeAddress,MealCard,TIM ) VALUES (?,?,?,?,?,?,?,?)", trpm)
            self.st_conn.commit()
        except Exception as e:
            print(e)
            return ['error',str(e)]
        else:
            return ['success',trpm]
    #查询学生所有信息，除饭卡金额
    def selectStudentAll(self,WeChatID):
        try:
            temp=self.st_conn.execute("select * from STUDENT WHERE WeChatID=?",(WeChatID,)).fetchall()
        except Exception as e:
            return ['error',e]
        else:
            return ['success',list(temp)]
    #查询所有学生
    def selectStudentTable(self):
        try:
            temp=self.st_conn.execute("select * from STUDENT").fetchall()
        except Exception as e:
            return ['error',e]
        else:
            return ['success',temp]
    #查询学生信息指定项
    def selectStudentOne(self,WeChatID,types):
        try:
            temp=self.st_conn.execute("select ? from STUDENT WHERE WeChatID=?",(types,WeChatID)).fetchall()[0]
        except Exception as e:
            return ['error',e]
        else:
            return ['success',temp]
    #更新微信绑定的学生信息
    def updateStudent(self,studentDict):
        _MealCard=studentDict['MealCard']
        arealy = self.selectStudentAll(studentDict['WeChatID'])
        #检查是否未绑定过学生信息
        if (arealy[0]=='success') and (len(arealy[1]) == 0) :
            return ['error','未绑定信息']
        #检查绑定的饭卡是否存在
        temp = list(self.st_conn.execute('SELECT MealCardMoney from MEALCARD WHERE MealCard=?',(_MealCard,)).fetchall())
        if len(temp)>=1:
            pass
        else:
            return ['error','绑定的饭卡不存在']
        try:
            self.st_conn.execute('UPDATE STUDENT set StudentName=?, ParentName=?, ParentTel=?, HomeAddress=?, MealCard=? where WeChatID=?',(studentDict['StudentName'],studentDict['ParentName'],studentDict['ParentTel'],studentDict['HomeAddress'],_MealCard,studentDict['WeChatID']))
            self.st_conn.commit()
            return ['success','success']
        except Exception as e:
            return ['error',str(e)]
    #更新饭卡余额
    def updateStudentReduceMealCardMoney(self,MealCard,ReduceMealCardMoney):
        try:
            ReduceMealCardMoney=float(ReduceMealCardMoney)
            _old_m=float(list(self.st_conn.execute("SELECT MealCardMoney from MEALCARD WHERE MealCard=?",(MealCard,)).fetchone())[0])
            print(f'原金额{_old_m}')
            if (ReduceMealCardMoney > 0) and (ReduceMealCardMoney > _old_m):
                return ['error','金额不足']

            _now_m=str((int(_old_m*1000)-int(ReduceMealCardMoney*1000))/1000)
            print(f'现金额{_now_m}')
            self.st_conn.execute('UPDATE MEALCARD set MealCardMoney=? where MealCard=?',(_now_m,MealCard))
            self.st_conn.commit()
            return ['success',_now_m,_old_m]
        except Exception as e:
            return ['error',str(e)]

    #饭卡产生消费记录
    def insertMealCard(self,MealCardDict):
        try:
            _MealCard=MealCardDict['MealCard']
            p=MealCardDict['p']
            updatereduce=self.updateStudentReduceMealCardMoney(MealCard=_MealCard,ReduceMealCardMoney=MealCardDict['ReduceMealCardMoney'])
            if updatereduce[0] == 'success' :
                if MealCardDict['Number']:
                    number=MealCardDict['Number']
                else:
                    number=self.getId(str(time.time())+MealCardDict['RECORD'])
                _ReduceMealCardMoney=MealCardDict['ReduceMealCardMoney']
                trpm=[(self.getTime(),MealCardDict['RECORD'],_ReduceMealCardMoney,number,updatereduce[1],_MealCard,p)]
                self.mc_conn.executemany(f"INSERT INTO '{_MealCard}' (TIM,RECORD,ReduceMealCardMoney,Number,MoneyNow,ReduceMealCardId,p) VALUES (?,?,?,?,?,?,?)", trpm)
                self.mc_conn.commit()
                self.insertMealLog(types=('rechange' if '-' in str(_ReduceMealCardMoney) else 'pay'),trpm=trpm,MoneyOld=updatereduce[2])
            else:
                return ['error',updatereduce[1]]
        except Exception as e:
            print(e)
            return ['error',str(e)]
        else:
            return ['success',trpm]
    #查询饭卡余额
    def selectMealCardMoney(self,MealCard):
        try:
            _now_money=list(self.st_conn.execute("SELECT MealCardMoney from MEALCARD WHERE MealCard=?",(MealCard,)).fetchall())[0][0]
            return ['success',_now_money]
        except Exception as e:
            return ['error',str(e)]

    #查询饭卡消费记录
    def selectMealCardRecord(self,MealCard):
        try:
            return ['success',self.mc_conn.execute(f"SELECT * from '{MealCard}'").fetchall()]
        except Exception as e:
            return ['error',str(e)]
        #--------------------业务类------------------------
        '''
         1.查询充值记录
         2.查询消费记录
        '''
    #插入充值/消费记录
    def insertMealLog(self,types,trpm,MoneyOld):
        date=self.getDate()
        try:
            self.up_conn.execute(f'''CREATE TABLE '{date}'
               (TIM                    TEXT,
               RECORD                  TEXT,
               ReduceMealCardMoney     TEXT,
               Number                  TEXT,
               MoneyNow                TEXT,
               ReduceMealCardId        TEXT,
               types                   TEXT,
               MoneyOld                TEXT);''')
        except:
            pass
        trpm=list(trpm[0])[:6]
        trpm[2]=abs(float(trpm[2]))
        trpm.append(types)
        trpm.append(MoneyOld)
        self.up_conn.executemany(f"INSERT INTO '{date}' (TIM,RECORD,ReduceMealCardMoney,Number,MoneyNow,ReduceMealCardId,types,MoneyOld) VALUES (?,?,?,?,?,?,?,?)", [trpm])
        self.up_conn.commit()

    #按日期查询充值/消费记录
    def selectMealLog(self,date,types):
        try:
            self.up_conn.execute(f'''CREATE TABLE '{date}'
               (TIM                    TEXT,
               RECORD                  TEXT,
               ReduceMealCardMoney     TEXT,
               Number                  TEXT,
               MoneyNow                TEXT,
               ReduceMealCardId        TEXT,
               types                   TEXT,
               MoneyOld                TEXT);''')
        except:
            pass
        if types != 'all':
            ret=self.up_conn.execute(f"SELECT * FROM '{date}' WHERE types=?",(types,)).fetchall()
        else:
            ret=self.up_conn.execute(f"SELECT * FROM '{date}'").fetchall()
        return ['success',ret]

if __name__=='__main__':
    pass