#!/usr/bin/evn python

# -*- coding: utf-8 -*-

# Creator: Johnson Guan
# Date: 2018-12-21
# ses[4].select('tr')[5].select('td')[8].get_text().strip()

import requests
from bs4 import BeautifulSoup
import csv
import os
import schedule
import time

BASE_URL = 'http://www.gzcc.gov.cn/data/Category_177/Index.aspx'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}

def crawWeb(url):
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        print("con't connect this WebSite!")

def tableToTitle(table,datestr):
    title01 = []

    title00 = table.select('tr')[0].get_text().strip()
    title01raw = table.select('tr')[1].select('td')

    for i in range(len(title01raw)):
        if i == 0:
            title01.append(title01raw[i].get_text().strip())
        else:
            title01.append(title01raw[i].get_text().strip() + u'\u5957\u6570')
            title01.append(title01raw[i].get_text().strip() + u'\u9762\u79ef')
            #title01raw[i].get_text().strip() + title02raw

    title01.append(datestr)
    return title01

def tableToData(table,datestr):
    tbdata = []
    tbodytr = table.select('tr[bgcolor="#ffffff"]')
    for i in range(len(tbodytr)):
        tblist = []
        for j in range(len(tbodytr[i].select('td'))):
            tblist.append(tbodytr[i].select('td')[j].get_text().strip())
        tblist.append(datestr)
        tbdata.append(tblist)
    return tbdata


def csvToFile(file,datas,title):
    if not os.path.isfile(file):
        with open(file,"a") as tifile:
            writertitle = csv.writer(tifile)
            writertitle.writerows([title])
            writertitle.writerows(datas)
    else:
        with open(file,"a") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(datas)

def job():
    contents = crawWeb(BASE_URL)

    soup = BeautifulSoup(contents,features='html.parser')
    tables = soup.select('table')
    if len(tables) > 0:
        dateStrTemp = tables[1].select('tr')[0].select('td')[1].get_text().strip()

        dtTitle = tableToTitle(tables[0],dateStrTemp[0:2])
        dtDatas0 = tableToData(tables[0],dateStrTemp[3:])
        dtDatas1 = tableToData(tables[2],dateStrTemp[3:])
        dtDatas2 = tableToData(tables[4],dateStrTemp[3:])

        csvToFile("d:/Develop/Python/own/tempwintest0.csv",dtDatas0,dtTitle)
        csvToFile("d:/Develop/Python/own/tempwintest1.csv",dtDatas1,dtTitle)
        csvToFile("d:/Develop/Python/own/tempwintest2.csv",dtDatas2,dtTitle)
    else:
        print("WebSite contents is empty!")

if __name__ == "__main__":
    schedule.every().day.at("11:31").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
