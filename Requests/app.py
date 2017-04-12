import requests
from bs4 import BeautifulSoup
import bs4
import time
import re
from http import cookiejar
import os
import json
import sys
import sendmail

login_url  = 'http://Login'
session_url    = 'http://token='
sign_url   = 'http://index/signin'
points_url = 'http://UserInfo2'
pwd_url    = 'http://Password'

tokenlist_n = []
tokenlist = []

j_login     =  {"device":"2","password":"8ce22d4188dca4e013f33cf5f7c43ddf","os":"10.2","deviceid":"C-31E0393942C9","api":"1","username":"","version":"3.4.0"}

j_pwd       =  {"device":"2","password":"","os":"10.2","passwordNew":" ","deviceid":"1E0393942C9","api":"1","version":"3.4.0","token":""}  

# %22 = ",%3A= , ,%7D = } ,%7B = {

headers_sign= {
            'Host': '',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cookie': 'session=; _zg=014904592%22%3A%20%22bf0e0f33b%22%7D; Hm_lvt_9009849caed7e6fee87308f63a777730=1488902225,1490459307,1490530005,1490869108',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
            }

headers_get = {
            'Host': '',
             'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-cn',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': '',
            'Content-Length': '0',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92',
            'Referer': 'http://token=4030aa8d299063f',
            }

headers_login = {
             'Host': '',
             'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
             'Connection': 'keep-alive',
             'Connection': 'keep-alive',
             'Accept': '*/*',
             'User-Agent': 'sxsx/3400 (iPhone; iOS 10.2; Scale/2.00)',
             'Accept-Language': 'zh-Hans-CN;q=1, ja-JP;q=0.9',
             'Accept-Encoding': 'gzip, deflate',
             'Content-Length': '266'
            }

headers_points = {
            'Host': '',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            'Connection': 'keep-alive',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': 'sxsx/3400 (iPhone; iOS 10.2; Scale/2.00)',
            'Accept-Language': 'zh-Hans-CN;q=1, ja-JP;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Length': '230'
            }

headers_pwd = {
                'Host': '',
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                'Connection': 'keep-alive',
                'Connection': 'keep-alive',
                'Accept': '*/*',
                'User-Agent': 'sxsx/3400 (iPhone; iOS 10.2; Scale/2.00)',
                'Accept-Language': 'zh-Hans-CN;q=1, ja-JP;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'Content-Length': '306'
                }

def open_file():
    phone_list = []
    if os.path.exists("phone.txt"):
        fp = open("phone.txt","r")
        for phone_num in (fp):
            if phone_num != '\n':
                phone_num = phone_num.strip()
                phone_list.append(phone_num)
        print(phone_list)
    else:
        print("\nError: open phone number file error!!\n")
        Logfile.write("\nError: open phone number file error!!\n")
    return phone_list

# input phone ,get token
def login(phone):
    token = ''
    password = '8ce22d4188dca4e013f33cf5f7c43ddf'
    username = phone
    #repstr = "username%22%3A%22"+str(phone)+"%22%2C%22"
    #data = re.sub("username%22%3A%22%22%2C%22",repstr,j_login)
    j_login['username'] = username
    j_login['password'] = password
    data = {
        'json':json.dumps(j_login)
        }

    print('\nPhone number:\t%s\n'%phone)
    Logfile.write('\nPhone number:\t%s\n'%phone)

    try:
        r = requests.post(login_url ,data = data,headers=headers_login)
        r.raise_for_status
        token = (r.text.split(',')[3]).split(':')[1].replace("\"","")
    except:
        print("\nError: Login error ,\tPhone number:%s.\n"%phone)
        Logfile.write("\nError: Login error ,\tPhone number:%s.\n"%phone)
    #print('\nToken:\t%s\n'%token)
    #Logfile.write('\nToken:\t%s\n'%token)
    return token

# input token ,get session id
def getSession(phone,token):
    try:
        r = requests.get(session_url+token ,headers=headers_get)
        r.raise_for_status
        session = r.headers['Set-Cookie'].split(';')
        wechat_session = session[0]
    except:
        print("\nError: Get session_id error,\tPhone number:%s.\n"%phone)
        Logfile.write("\nError: Get session_id error,\tPhone number:%s.\n"%phone)
    #print('\nWechat_Session:\t%s\n'%wechat_session)
    #Logfile.write('\nWechat_Session:\t%s\n'%wechat_session)
    return wechat_session

# input session id ,sign in ,get points.
def signin(phone):
    get_points = ''
    try:
        r = requests.get(sign_url ,headers=headers_sign)
        r.raise_for_status
        sign_code = r.json()
        for key,value in sign_code.items():
            print('%-20s:%-s'%(key,value))
            Logfile.write('%-8s:%-s\t'%(key,value))
    except:
        print("\nError: Signin error,\tPhone number:%s.\n"%phone)
        Logfile.write("\nError: Signin error,\tPhone number:%s.\n"%phone)   


def get_userInfo():
    if os.path.exists('Points.txt'):
        os.remove('Points.txt')
    Pointsfile = open("Points.txt","w")
    Pointsfile.write('\n----- Time:%s.\n'%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())))
    Pointsfile.write("%-13s,%-6s,%-7s,%-6s\n"%('Nickname','Points','Collect','Freeze'))
    for token in tokenlist:         #open("Token.txt","r")
        j_getpoints['token'] = token
        data = {
            'json':json.dumps(j_getpoints)
            }
        try:
            r = requests.post(points_url ,data = data,headers=headers_points)
            r.raise_for_status
            text =eval(r.text)
            userdata = text.get('data')
            nickname = userdata.get('nickname')
            points   = userdata.get('integration')
            collect  = userdata.get('collect')
            order    = userdata.get('order')
            freeze   = userdata.get('freeze')
            print("Nickname:%-s,Points:%-s,Collect:%-s,Freeze:%-s"%(nickname,points,collect,freeze))
            Pointsfile.write("%-13s,%-6s,%-7s,%-6s\n"%(nickname,points,collect,freeze))
        except:
            print('Error: Get User Info Error')
            Pointsfile.close()
    Pointsfile.close()


def change_pwd(pwdOld,pwdNew,file):
    if os.path.exists(file):
        with open(file,'r') as f:
            Tklist = f.readlines()
        j_pwd['password'] = pwdOld
        j_pwd['passwordNew'] = pwdNew

        for token in Tklist:
            j_pwd['token'] = token

            data = {
                'json':json.dumps(j_pwd)
                }
            r = requests.post(pwd_url ,data = data,headers=headers_pwd)
            if (r.status_code != 200):
                print("Change pwd Error!")
    else:
         print("Change pwd Error!")
    print("Change pwd Success!")

def sendemail():
    if os.path.exists('Log.txt')and os.path.exists('Log.txt'):
        path1 = os.path.join(os.getcwd(),'Log.txt')
        path2 = os.path.join(os.getcwd(),'Points.txt')
        sendmail.send_mail(path1,path2)
    else:
        sendmail.send_mail('Error','Error')

def run(phone):
    iphone = phone
    #setp1
    token = login(iphone)
    #step2
    if token == '':
        return
    tokenlist_n.append(token+"\n")
    tokenlist.append(token)
    new_cookie= getSession(iphone,token)
    cookies = 'responseTimeline=;session=;_zg=%7B%2aaa582f90f1A%201491057027.156%2C%22updated%22%3A%22C%222%3A%c6491312%22%7D; Hm_lvt_9009849caed7e6fe488902225,14907,5,1490869108'
    cookies = re.sub(r'session=',new_cookie,cookies)
    headers_sign['Cookie'] = cookies
    #step3
    signin(iphone)
    print("\n------------------------------------\n")
    Logfile.write("\n------------------------------------\n")

if __name__ == "__main__":
    if os.path.exists('Log.txt'):
        os.remove('Log.txt')
    Logfile = open('Log.txt','w')
    Logfile.write("\n---Work Start:\n")
    Logfile.write('\n-----Start Time:%s.\n'%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())))

    for phone in open_file():
        run(phone)

    Logfile.write('\n-----End Time:%s.\n'%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())))
    Logfile.close()    # if not close,Log.txt will lose data.
    
    get_userInfo()
    sendemail()

    #save token for change pwd
    Tokenfile = open("Token.txt","w")
    Tokenfile.writelines(tokenlist_n)
    Tokenfile.close()
    



