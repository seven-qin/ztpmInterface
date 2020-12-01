# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     main2
   Description :
   Author :       seven
   date：          2020/11/20
-------------------------------------------------
   Change Activity:
                   2020/11/20:
-------------------------------------------------
"""
import os
import sys
import traceback
from urllib import parse

import requests

__author__ = 'seven'
import configparser
import json


from lxml import etree


import logging



import  time
import myhttpClient

logname="runlog" + time.strftime("%Y-%m-%d", time.localtime()) + ".log"
LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(pathname)s %(message)s "#配置输出日志格式
DATE_FORMAT = '%Y-%m-%d  %H:%M:%S %a ' #配置输出时间的格式，注意月份和天数不要搞乱了
logging.basicConfig(level=logging.DEBUG,
                    format=LOG_FORMAT,
                    datefmt = DATE_FORMAT ,
                    filename=logname #有了filename参数就不会直接输出显示到控制台，而是直接写入文件
                    )


header={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection":"keep-alive",
}


def login(client):
    url = 'http://ztpm.goldwind.com.cn:9898/pro/user-login-L3Byby9xYS5odG1s.html'
    rsp=client.get(url)
    html = rsp.read().decode()
    with open("loginpage.html", 'w', encoding='utf-8') as f:
        f.write(html)

    url='http://ztpm.goldwind.com.cn:9898/pro/user-login-L3Byby9xYS5odG1s.html'
    data={"account": "qinhailong",
             "password": "qhl12345",
             "referer": "/pro/qa.html"
    }
    data = parse.urlencode(data)
    rsp=client.post(url,data)
    html = rsp.read().decode()

def mainpage(client):
    url='http://ztpm.goldwind.com.cn:9898/pro/index.html'
    rsp = client.get(url)
    html = rsp.read().decode()

    html = rsp.read().decode()
    with open("index.html", 'w', encoding='utf-8') as f:
        f.write(html)
    url = 'http://ztpm.goldwind.com.cn:9898/pro/my/'
    rsp = client.get(url)
    html = rsp.read().decode()
    """
    with open("mymainpage.html", 'w', encoding='utf-8') as f:
        f.write(html)
    """
def bug_page(client,datatype,type):
    #请求搜索
    htmllist=[]

    url='http://ztpm.goldwind.com.cn:9898/pro/search-buildQuery.html'
    data='fieldtitle=&fieldkeywords=&fieldsteps=&fieldassignedTo=&fieldresolvedBy=&fieldstatus=&fieldconfirmed=ZERO&fieldproduct=21&fieldbranch=&fieldplan=&fieldmodule=0&fieldproject=&fieldseverity=0&fieldpri=0&fieldtype=&fieldos=&fieldbrowser=&fieldresolution=&fieldactivatedCount=&fieldtoTask=&fieldtoStory=&fieldopenedBy=&fieldclosedBy=&fieldlastEditedBy=&fieldmailto=&fieldopenedBuild=&fieldresolvedBuild=&fieldopenedDate=&fieldassignedDate=&fieldresolvedDate=&fieldclosedDate=&fieldlastEditedDate=&fielddeadline=&fieldid=&andOr1=AND&field1='+type+'&operator1=between&value1=%24'+datatype+'&andOr2=and&field2=id&operator2=%3D&value2=&andOr3=and&field3=keywords&operator3=include&value3=&groupAndOr=and&andOr4=AND&field4=steps&operator4=include&value4=&andOr5=and&field5=assignedTo&operator5=%3D&value5=&andOr6=and&field6=resolvedBy&operator6=%3D&value6=&module=bug&actionURL=%2Fpro%2Fbug-browse-21-0-bySearch-myQueryID.html&groupItems=3&queryID=&formType=lite'
    rsp=client.post(url,data)
    url='http://ztpm.goldwind.com.cn:9898/pro/bug-browse-21-0-bySearch-myQueryID.html'
    rsp = client.get(url)
    html=rsp.read().decode()
    """
    with open("bug" + type + ".html", 'w', encoding='utf-8') as f:
        f.write(html)
    """
    htmllist.append(html)
    content = etree.HTML(html)
    try:
        perpagenum = content.xpath("//a[@id='_recPerPage']/strong/text()")[0]
        sumnum=content.xpath("//form[@id='bugForm']//strong[1]/text()")[0]
    except:
        perpagenum = '1'
        sumnum='0'

    for i in range(int((int(sumnum)/int(perpagenum)))):

        url='http://ztpm.goldwind.com.cn:9898/pro/bug-browse-21-0-bySearch-myQueryID--'+sumnum+'-'+perpagenum+'-'+str(i+2)+'.html'
        rsp = client.get(url)
        html = rsp.read().decode()
        htmllist.append(html)
        """
        with open("bug" + type+str(i+2)+ ".html", 'w', encoding='utf-8') as f:
            f.write(html)
        """

    return htmllist
def testsuits_testing_page(client):
    #所有测试单
    url='http://ztpm.goldwind.com.cn:9898/pro/testtask-browse-21-0-local,doing.html'
    rsp = client.get(url)
    html = rsp.read().decode()
    """
    with open("testsuits_testing.html", 'w', encoding='utf-8') as f:
        f.write(html)
    """
    return html
def suitresults_page(client,datatype,testsuitID,perpagenum):
    print("开始请求时间：" + time.asctime(time.localtime(time.time())))
    htmllist=[]
    #testsuitID = urlencode(testsuitID)
    url='http://ztpm.goldwind.com.cn:9898/pro/search-buildQuery.html'
    data='fieldtitle=&fieldmodule=ZERO&fieldkeywords=&fieldlastEditedBy=&fieldtype=&fieldpri=3&fieldopenedBy=&fieldstatus=&fieldproduct=21&fieldstage=&fieldlastRunner=&fieldlastRunResult=n%2Fa&fieldlastRunDate=&fieldopenedDate=&fieldlastEditedDate=&fieldassignedTo=&fieldid=&andOr1=AND&field1=lastRunDate&operator1=between&dateValue1=&'\
         'value1=%24'+datatype+'&andOr2=and&field2=id&operator2=%3D&value2=&andOr3=and&field3=keywords&operator3=include&value3=&groupAndOr=and&andOr4=AND&field4=lastEditedBy&operator4=%3D&value4=&andOr5=and&field5=type&operator5=%3D&value5=&andOr6=and&field6=openedBy&operator6=%3D&value6=&module=testtask&actionURL=%2Fpro%2Ftesttask-cases-1461-bySearch-myQueryID.html&groupItems=3&queryID=&formType=lite'
    rsp = client.post(url, data)
    url='http://ztpm.goldwind.com.cn:9898/pro/testtask-cases-'+testsuitID+'-bySearch-myQueryID.html'
    rsp = client.get(url)
    html = rsp.read().decode()
    """

    with open("testsuits_" + testsuitID +"_result.html", 'w', encoding='utf-8') as f:
        f.write(html)
    """
    content = etree.HTML(html)
    try:
        sumnum = content.xpath("//form[@id='casesForm']//strong[1]/text()")[0]
    except:
        sumnum = '0'
    for i in range(int((int(sumnum) / int(perpagenum)))+1):
        url = 'http://ztpm.goldwind.com.cn:9898/pro/testtask-cases-'+testsuitID+'-bySearch-myQueryID-id_desc-'+sumnum+'-'+perpagenum+'-'+str(i+1)+'.html'
        rsp = client.get(url)
        html = rsp.read().decode()
        htmllist.append(html)
        print(url)
        """  

        with open("testsuits"+testsuitID+"_"+str(i+1) + ".html", 'w', encoding='utf-8') as f:
            f.write(html)
        """
    print("请求结束时间：" + time.asctime(time.localtime(time.time())))
    return htmllist
def suitresults_page1(client,type,testsuitID,testerlist):
    print("开始请求时间：" + time.asctime(time.localtime(time.time())))
    htmllist=[]
    for tester in testerlist:
        #testsuitID = urlencode(testsuitID)
        url='http://ztpm.goldwind.com.cn:9898/pro/search-buildQuery.html'
        if type=='all':
            data='fieldtitle=&fieldmodule=ZERO&fieldkeywords=&fieldlastEditedBy=&fieldtype=&fieldpri=3&fieldopenedBy=&fieldstatus=&fieldproduct=21&fieldstage=&fieldlastRunner=&fieldlastRunResult=n%2Fa&fieldlastRunDate=&fieldopenedDate=&fieldlastEditedDate=&fieldassignedTo=&fieldid=&andOr1=AND&field1=assignedTo&operator1=%3D&'\
                 'value1='+tester+'&andOr2=and&field2=title&operator2=include&value2=&andOr3=and&field3=keywords&operator3=include&value3=&groupAndOr=and&andOr4=AND&field4=type&operator4=%21%3D&value4=Auto&andOr5=and&field5=type&operator5=%3D&value5=&andOr6=and&field6=openedBy&operator6=%3D&value6=&module=testtask&'\
                                  'actionURL=%2Fpro%2Ftesttask-cases-'+testsuitID+'-bySearch-myQueryID.html&groupItems=3&queryID=&formType=more'
            #data='fieldtitle=&fieldmodule=ZERO&fieldkeywords=&fieldlastEditedBy=&fieldtype=&fieldpri=3&fieldopenedBy=&fieldstatus=&fieldproduct=21&fieldstage=&fieldlastRunner=&fieldlastRunResult=n%2Fa&fieldlastRunDate=&fieldopenedDate=&fieldlastEditedDate=&fieldassignedTo=&fieldid=&andOr1=AND&field1=assignedTo&operator1=%3D&'value1='+tester+'&andOr2=and&field2=id&operator2=%3D&value2=&andOr3=and&field3=keywords&operator3=include&value3=&groupAndOr=and&andOr4=AND&field4=title&operator4=include&value4=&andOr5=and&field5=type&operator5=%3D&value5=&andOr6=and&field6=openedBy&operator6=%3D&value6=&module=testtask&'actionURL=%2Fpro%2Ftesttask-cases-'+testsuitID+'-bySearch-myQueryID.html&groupItems=3&queryID=&formType=lite'
        else:
            data='fieldtitle=&fieldmodule=ZERO&fieldkeywords=&fieldlastEditedBy=&fieldtype=&fieldpri=3&fieldopenedBy=&fieldstatus=&fieldproduct=21&fieldstage=&fieldlastRunner=&fieldlastRunResult=n%2Fa&fieldlastRunDate=&fieldopenedDate=&fieldlastEditedDate=&fieldassignedTo=&fieldid=&andOr1=AND&field1=assignedTo&operator1=%3D&'\
                 'value1='+tester+'&andOr2=and&field2=lastRunResult&operator2=%3D&'\
                                  'value2='+type+'&andOr3=and&field3=keywords&operator3=include&value3=&groupAndOr=and&andOr4=AND&field4=type&operator4=%21%3D&value4=Auto&andOr5=and&field5=type&operator5=%3D&value5=&andOr6=and&field6=openedBy&operator6=%3D&value6=&module=testtask&'\
                                  'actionURL=%2Fpro%2Ftesttask-cases-'+testsuitID+'-bySearch-myQueryID.html&groupItems=3&queryID=&formType=more'
            #data='fieldtitle=&fieldmodule=ZERO&fieldkeywords=&fieldlastEditedBy=&fieldtype=&fieldpri=3&fieldopenedBy=&fieldstatus=&fieldproduct=21&fieldstage=&fieldlastRunner=&fieldlastRunResult=n%2Fa&fieldlastRunDate=&fieldopenedDate=&fieldlastEditedDate=&fieldassignedTo=&fieldid=&andOr1=AND&field1=assignedTo&operator1=%3D&value1='+tester+'&andOr2=and&field2=id&operator2=%3D&value2=&andOr3=and&field3=keywords&operator3=include&value3=&groupAndOr=and&andOr4=AND&field4=lastRunResult&operator4=%3D&value4='+type+'&andOr5=and&field5=type&operator5=%3D&value5=&andOr6=and&field6=openedBy&operator6=%3D&value6=&module=testtask&actionURL=%2Fpro%2Ftesttask-cases-'+testsuitID+'-bySearch-myQueryID.html&groupItems=3&queryID=&formType=lite'
        rsp = client.post(url, data)
        url='http://ztpm.goldwind.com.cn:9898/pro/testtask-cases-'+testsuitID+'-bySearch-myQueryID.html'
        rsp = client.get(url)
        html = rsp.read().decode()
        htmllist.append(html)
        #with open("testsuits_" + testsuitID +"_"+type+"_"+tester+ "_result.html", 'w', encoding='utf-8') as f:
        #  f.write(html)
    print("请求结束时间：" + time.asctime(time.localtime(time.time())))
    return htmllist

def  cases_page(client,datatype,type):
    htmllist=[]
    url='http://ztpm.goldwind.com.cn:9898/pro/search-buildQuery.html'
    data='fieldtitle=&fieldmodule=ZERO&fieldkeywords=&fieldlastEditedBy=&fieldtype=&fieldpri=3&fieldopenedBy=&fieldstatus=&fieldproduct=21&fieldbranch=&fieldstage=&fieldlastRunner=&fieldlastRunResult=n%2Fa&fieldlastRunDate=&fieldopenedDate=&fieldlastEditedDate=&fieldid=&andOr1=AND&field1='+type+'&operator1=between&value1=%24'+datatype+'&andOr2=and&field2=id&operator2=%3D&value2=&andOr3=and&field3=keywords&operator3=include&value3=&groupAndOr=and&andOr4=AND&field4=lastEditedBy&operator4=%3D&value4=&andOr5=and&field5=type&operator5=%3D&value5=&andOr6=and&field6=openedBy&operator6=%3D&value6=&module=testcase&actionURL=%2Fpro%2Ftestcase-browse-21-0-bySearch-myQueryID.html&groupItems=3&queryID=&formType=lite'
    rsp = client.post(url, data)
    url='http://ztpm.goldwind.com.cn:9898/pro/testcase-browse-21-0-bySearch-myQueryID.html'
    rsp = client.get(url)
    html = rsp.read().decode()
    """
    with open("testcase_" + type + "result.html", 'w', encoding='utf-8') as f:
        f.write(html)
    """
    htmllist.append(html)
    content = etree.HTML(html)
    try:
        perpagenum = content.xpath("//a[@id='_recPerPage']/strong/text()")[0]
        sumnum = content.xpath("//form[@id='batchForm']//strong[1]/text()")[0]
    except:
        perpagenum='1'
        sumnum='0'
    for i in range(int((int(sumnum) / int(perpagenum)))):

        url = 'http://ztpm.goldwind.com.cn:9898/pro/testcase-browse-21-0-bySearch-myQueryID-id_desc-'+sumnum+'-'+perpagenum+'-'+str(i+2)+'.html'
        rsp = client.post(url, data)
        html = rsp.read().decode()
        htmllist.append(html)

        #with open("testcases" + type + str(i+2) + ".html", 'w', encoding='utf-8') as f:
        #  f.write(html)

    return htmllist
def logout_page(client):
    #退出登录
    url='http://ztpm.goldwind.com.cn:9898/pro/user-logout.html'
    rsp = client.get(url)


def getBugResults(htmllist,xpth,testerlist):
    bugresults=[]
    testernamelist=[]
    for html in htmllist:
    #creater_Xpath="//form[@id='bugForm']/table/tbody/tr/td[6]/text()"
    #closer_Xpath="//form[@id='bugForm']/table/tbody/tr/td[8]"
        content=etree.HTML(html)
        testernamelist=testernamelist+content.xpath(xpth)
    for tester in testerlist:
        bugresults.append(testernamelist.count(tester))
    return  bugresults
def sum(testsuitsMap,testerlist):
    ALLSUMList = []
    SUMEXEdList = []
    RATE = []
    for i in range(len(testerlist)):

        ALLSUM = 0
        ALLUNEXECUTED = 0
        for testsuit in testsuitsMap:
            ALLSUM = ALLSUM + int(testsuitsMap[testsuit]["ALLCASE"][i])
            ALLUNEXECUTED = ALLUNEXECUTED + int(testsuitsMap[testsuit]["UnExecutedCase"][i])

        ALLEXECUTED = ALLSUM - ALLUNEXECUTED
        if ALLSUM == 0:
            RATE1 = 0
            RATE1='{:.2%}'.format(RATE1)
        else:
            RATE1 = ALLEXECUTED / ALLSUM
            RATE1 = '{:.2%}'.format(RATE1)
        ALLSUMList.append(ALLSUM)
        SUMEXEdList.append(ALLEXECUTED)
        RATE.append(RATE1)
    return {"ALL TEST SUITS RESUTLS":{"ALL":ALLSUMList,"ALLEXECUTED":SUMEXEdList,"RATE":RATE}}

def getSumNum(htmllist,xpath):
    print("开始解析时间：" + time.asctime(time.localtime(time.time())))
    sumResults=[]
    for html in htmllist:
        content = etree.HTML(html)
        try:
            sumResults.append(content.xpath(xpath)[0])
        except:
            sumResults.append("0")
    print("解析完成时间：" + time.asctime(time.localtime(time.time())))
    return sumResults

def writeFileFortestsuits(testsuitlist,namelist,filename):
    size1 = len(namelist) * 15 + 15
    with open(filename, "a+", encoding="UTF-8") as file:
        for testsuit in testsuitlist:
            file.write(testsuit.center(size1, "*"))
            file.write("\n")
            file.write("TYPE".ljust(15, " "))
            for name in namelist:
                file.write(name.ljust(15, " "))
            for type in testsuitlist[testsuit]:
                file.write("\n")
                file.write(type.ljust(15, " "))
                for ele in range(len(testsuitlist[testsuit][type])):
                    value=str(testsuitlist[testsuit][type][ele])
                    file.write(value.ljust(15, " "))
            file.write("\n")
def send_file(file_path,bot):
    file_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={bot}&type=file"
    file = {'file': open(file_path, 'rb')}
    result = requests.post(file_url, files=file)
    file_id = eval(result.text)['media_id']
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={bot}"
    data = {
        "msgtype": "file",
        "content": "测试",
        "file": {"media_id": file_id, }
    }
    r = requests.post(url, json=data)
def send_text(text,bot):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={bot}"
    headers = {"Content-Type": "text/plain"}
    data = {
          "msgtype": "text",
          "text": {
             "content": text,
          }
       }
    r = requests.post(url, headers=headers, json=data)

if __name__ == '__main__':
    myclient=myhttpClient.MyHttp(20,header)
    try:
        #定义结果文件名称
        filename = "result" + time.strftime("%Y-%m-%d", time.localtime()) + ".log"
        if os.path.exists(filename):
            os.remove(filename)

        #记录时间
        print("开始执行时间："+time.asctime(time.localtime(time.time())))
        #读取配置文件：
        config = configparser.ConfigParser()
        config.read("config.ini", encoding="utf-8-sig")
        testerlist = json.loads(config.get("testcase", "testers"))
        testerlist1 = json.loads(config.get("testcase", "testers1"))
        caseresults = json.loads(config.get("testcase", "caseresults"))
        datatype=config.get("testcase","datatype")
        dogid=config.get("testcase","dogid")
        perpagenum = config.get("testcase", "perpagenum")

        #保存数据
        bugresultsMap={}
        caseresultMap={}
        testsuitsMap={}


        #登陆禅道
        login(myclient)
        #获取用户主界面
        mainpage(myclient)
        #处理bug模块
        #openedDate,xapth=//form[@id='bugForm']/table/tbody/tr/td[6]/text()
        #closedDate,xpath=//form[@id='bugForm']/table/tbody/tr/td[8]/text()
        htmlopenedDate=bug_page(myclient,datatype,'openedDate')
        htmlclosedDate=bug_page(myclient,datatype,'closedDate')
        bugresultsMap['newbug']=getBugResults(htmlopenedDate,"//form[@id='bugForm']/table/tbody/tr/td[6]/text()",testerlist)
        bugresultsMap['colsebug']=getBugResults(htmlclosedDate, "//form[@id='bugForm']/table/tbody/tr/td[8]/text()", testerlist)


        print(bugresultsMap)

        #处理用例模块
        htmlopenedDate = cases_page(myclient,datatype, 'openedDate')
        htmlfixedDate = cases_page(myclient,datatype, 'lastEditedDate')
        caseresultMap['newcase'] = getBugResults(htmlopenedDate, "//form[@id='batchForm']/table/tbody/tr/td[6]/text()",
                                                testerlist)
        caseresultMap['fixedcase'] = getBugResults(htmlfixedDate, "//form[@id='batchForm']/table/tbody/tr/td[8]/text()",
                                                  testerlist)
        print(caseresultMap)
        #获取正在执行的测试单
        content=etree.HTML(testsuits_testing_page(myclient))
        testsuitsID_list=content.xpath("//table[@id='taskList']/tbody/tr/td[1]/a/text()")
        testsuitsName_list=content.xpath("//table[@id='taskList']/tbody/tr/td[2]/a/text()")
        for i in range(len(testsuitsID_list)):
            print(testsuitsName_list[i]+"开始处理测试单时间：" + time.asctime(time.localtime(time.time())))
            testsuitsName=testsuitsName_list[i]
            testsuitsMap[testsuitsName]={}
            htmllist=suitresults_page(myclient,datatype,testsuitsID_list[i],perpagenum)
            testsuitsMap[testsuitsName]["ExecutedCase"]=getBugResults(htmllist,"//form[@id='casesForm']/table/tbody/tr/td[6]/text()",testerlist)
            testsuitsMap[testsuitsName]['ALLCASE'] = getSumNum(suitresults_page1(myclient,"all", testsuitsID_list[i], testerlist1),
                                                               "//form[@id='casesForm']/table/tfoot/tr/td/div/strong[1]/text()")
            testsuitsMap[testsuitsName]['UnExecutedCase'] = getSumNum(
                suitresults_page1(myclient,"null", testsuitsID_list[i], testerlist1),
                "//form[@id='casesForm']/table/tfoot/tr/td/div/strong[1]/text()")
            print("处理测试单完成时间：" + time.asctime(time.localtime(time.time())))

        print(testsuitsMap)
        testSUM=sum(testsuitsMap,testerlist1)
        print(testSUM)
        #开始写文件
        writeFileFortestsuits(testsuitsMap,testerlist1,filename)
        writeFileFortestsuits({"缺陷统计":bugresultsMap,"用例统计":caseresultMap},testerlist1,filename)
        writeFileFortestsuits(testSUM,testerlist1,filename)
        print("结束执行时间：" + time.asctime(time.localtime(time.time())))
        logout_page(myclient)
    except Exception as e :
        logout_page(myclient)
        logging.debug(traceback.format_exc())
        traceback.print_exc()
        send_text("统计数据异常", dogid)
        sys.exit()

    send_text(datatype+"测试数据统计，请及时更新进度表与禅道任务", dogid)
    send_file(filename,dogid)
