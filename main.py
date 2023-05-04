import re
from config import *
from flask import Flask, request
import requests
app = Flask(__name__)
class pycc:
    def __init__(self):
        self.session=requests.session()
        self.baseurl="https://iscc.isclab.org.cn/"
        self.session.post(url=self.baseurl+"login",headers=HEADERS,data={"name":USERNAME,"password":PASSWORD})
    def submitFlag(self,massage):
        flag = re.search(r'ISCC{.+}', massage)
        quest = massage.split()[0]
        for i in self.chals:
            if i['name']==quest:
                match = re.search(r"value=([a-fA-F\d]+)>", self.session.get(self.baseurl+"challenges").text)
                nonce=(match.group(1))
                statu=self.session.post(self.baseurl + f"chal/{i['id']}", headers=HEADERS,
                                        data={"key": flag, "nonce": nonce}).text
                if statu=='0':
                    return(f"题目名：{i['name']}\nflag：{flag}\n提交失败，请检查flag是否过期或flag是否正确")
                elif statu=='1' or statu=='2':
                    requests.post("http://happypy.skyman.cloud/index.php",data={"flag":flag,"name":i['name']})
                    return(f"{i['name']}提交成功")
                else:
                    return("返回值怪怪的，请自己检查哦")
        for i in self.arenas:
            if i['name']==quest:
                match = re.search(r"value=([a-fA-F\d]+)>", self.session.get(self.baseurl+"arena").text)
                nonce=(match.group(1))
                statu=self.session.post(self.baseurl + f"are/{i['id']}", headers=HEADERS,
                                        data={"key": flag, "nonce": nonce}).text
                if statu=='0':
                    return(f"题目名：{i['name']}\nflag：{flag}\n提交失败，请检查flag是否过期或flag是否正确")
                elif statu=='1' or statu=='2':
                    return(f"{i['name']}提交成功")
                else:
                    return("返回值怪怪的，请自己检查哦")
    def getRanking(self):
        "https://iscc.isclab.org.cn/arenasolves"
        "https://iscc.isclab.org.cn/solves"
    def getAllQuests(self):
        #获取所有题目信息
        self.arenas=self.getArenas()
        self.chals=self.getChallenges()
    def getArenas(self):
        chals=[]
        #获取擂台题信息
        for i in self.session.get(url=self.baseurl+"arenas",headers=HEADERS).json()['game']:
            chals.append(self.session.get(url=self.baseurl+"arenas/"+str(i['id']),headers=HEADERS).json())
        return chals
    def getChallenges(self):
        #获取练武题信息
        chals=[]
        #获取擂台题信息
        for i in self.session.get(url=self.baseurl+"chals",headers=HEADERS).json()['game']:
            chals.append(self.session.get(url=self.baseurl+"chals/"+str(i['id']),headers=HEADERS).json())
        return chals
def sendMessage(QID,message):
    requests.post("http://127.0.0.1:5700/send_msg",data={"user_id":str(QID),"message":message})
@app.route('/', methods=["POST"])
def post_data():
    if request.get_json().get('message_type')=='private':
        uid = request.get_json().get('sender').get('user_id')
        message = request.get_json().get('raw_message')
        if "ISCC{" in message:
            mes=PYCC.submitFlag(message)
            print(mes)
            sendMessage(ADMINQQ,mes)
        # print(request.get_json())
        # api.keywordForPerson(message,uid)
    if request.get_json().get('message_type')=='group':
        print(request.get_json())
        gid = request.get_json().get('group_id')
        uid = request.get_json().get('sender').get('user_id')
        message = request.get_json().get('raw_message')
        nick=request.get_json().get('sender').get('nickname')
        if "ISCC{" in message:
            mes=PYCC.submitFlag(message)
            print(mes)
            sendMessage(ADMINQQ,mes)
        # print(gid)
        # print(locals())
        # api.keywordForGroup(message, gid, uid,nick)
    return 'OK'


if __name__ == '__main__':
    PYCC=pycc()
    PYCC.getAllQuests()
    for i in PYCC.chals:
        print(i)
    app.run(debug=True, host='127.0.0.1', port=5701)