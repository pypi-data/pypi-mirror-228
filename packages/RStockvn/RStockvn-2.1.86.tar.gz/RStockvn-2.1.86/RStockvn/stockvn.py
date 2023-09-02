# Copyright 2023 Nguyen Phuc Binh @ GitHub
# See LICENSE for details.
__version__ = "2.1.6"
__author__ ="Nguyen Phuc Binh"
__copyright__ = "Copyright 2023, Nguyen Phuc Binh"
__license__ = "MIT"
__email__ = "nguyenphucbinh67@gmail.com"
__website__ = "https://github.com/NPhucBinh"

import pandas as pd
import requests
import requests
import json
from bs4 import BeautifulSoup
from .user_agent import random_user
from .cafef_test import browser_get_data
import datetime as dt


def report_finance_cf(symbol,report,year,timely): ### HAM LAY BAO CAO TAI CHINH TU TRANG CAFEF 4
    symbol=symbol.upper()
    report=report.upper()
    year=int(year)
    timely= timely.upper()
    if report =="CDKT" or 'BS' or 'BALANCESHEET':
        x='BSheet'
        if timely=='YEAR':
            y='0'
        elif timely=='QUY' or 'QUARTER':
            y='4'
    elif report=='KQKD' or 'P&L':
        x='IncSta'
        if timely=='YEAR':
            y='0'
        elif timely=='QUY' or 'QUARTER':
            y='4'
    elif report=="CFD":
        x='CashFlowDirect'
        if timely=='YEAR':
            y='0'
        elif timely=='QUY' or 'QUARTER':
            y='4'
    elif report=="CF":
        x='CashFlow'
        if timely=='YEAR':
            y='0'
        elif timely=='QUY' or 'QUARTER':
            y='4'
    repl=pd.read_html('https://s.cafef.vn/BaoCaoTaiChinh.aspx?symbol={}&type={}&year={}&quarter={}'.format(symbol,x,year,y))
    lst=repl[-2].values.tolist()
    df=pd.DataFrame(repl[-1])
    df.columns=list(lst[0])
    df.drop('Tăng trưởng',axis=1,inplace=True)
    return df


def exchange_currency(current,cover_current,from_date,to_date): ###HAM LAY TY GIA 7
    url = 'https://api.exchangerate.host/timeseries?'
    payload={'base':current,"start_date":from_date,'end_date':to_date}
    response = requests.get(url, params=payload)
    data = response.json()
    dic={}
    lid=[]
    for item in data['rates']:
        de=item
        daa=data['rates'][item][cover_current]
        dic[de]=[daa]
        lid.append(daa)
        a=pd.DataFrame(dic).T
        a=round(a,2)
        a.columns=['{}/{}'.format(current,cover_current)]
        d=a.sort_index(ascending=False)
    return d

        
###HAM GET DATA VIETSTOCK 
def token():
    urltoken='https://finance.vietstock.vn/du-lieu-vi-mo/53-64/ty-gia-lai-xuat.htm#'
    head={'User-Agent':random_user()}
    loadlan1=requests.get(urltoken,headers=head)
    soup=BeautifulSoup(loadlan1.content,'html.parser')
    stoken=soup.body.input
    stoken=str(stoken)
    listtoken=stoken.split()
    xre=[]
    for i in listtoken[1:]:
        i=i.replace('=',':')
        i=i.replace('"','')
        xre.append(i)
    token=str(xre[2])
    token=token.replace('value:','')
    token=token.replace('/>','')
    dic=dict(loadlan1.cookies.get_dict())
    revtoken=dic['__RequestVerificationToken']
    revasp=dic['ASP.NET_SessionId']
    return revasp, revtoken, token

def getCPI_vietstock(fromdate,todate): ###HAM GET CPI 10
    asp,rtoken,tken=token()
    fromdate=pd.to_datetime(fromdate)
    todate=pd.to_datetime(todate)
    tungay=str(fromdate.strftime('%Y-%m-%d'))
    denngay=str(todate.strftime('%Y-%m-%d'))
    url='https://finance.vietstock.vn/data/reportdatatopbynormtype'
    header={'User-Agent':random_user(),'Cookie': 'language=vi-VN; ASP.NET_SessionId={}; __RequestVerificationToken={}; Theme=Light; _ga=GA1.2.521754408.1675222361; _gid=GA1.2.2063415792.1675222361; AnonymousNotification='.format(asp,rtoken)}
    payload={'type':'2','fromYear':fromdate.year,'toYear':todate.year,'from':fromdate.month,'to':todate.month,'normTypeID':'52','__RequestVerificationToken': '{}'.format(tken)}
    ls=requests.post(url,headers=header,data=payload)
    cov1=dict(ls.json())
    bangls=pd.DataFrame(cov1['data'])
    bangls.drop(['ReportDataID','TermID','TermYear','TernDay','NormID','GroupName','CssStyle','NormTypeID','NormGroupID'], axis=1, inplace=True)
    return bangls

def solieu_sanxuat_congnghiep(fromdate,todate): #HAMSOLIEUSANXUAT 11
    asp,rtoken,tken=token()
    fromdate=pd.to_datetime(fromdate)
    todate=pd.to_datetime(todate)
    tungay=str(fromdate.strftime('%Y-%m-%d'))
    denngay=str(todate.strftime('%Y-%m-%d'))
    url='https://finance.vietstock.vn/data/reportdatatopbynormtype'
    header={'User-Agent':random_user(),'Cookie': 'language=vi-VN; ASP.NET_SessionId={}; __RequestVerificationToken={}; Theme=Light; _ga=GA1.2.521754408.1675222361; _gid=GA1.2.2063415792.1675222361; AnonymousNotification='.format(asp,rtoken)}
    payload={'type':'2','fromYear':fromdate.year,'toYear':todate.year,
             'from':fromdate.month,'to':todate.month,'normTypeID':'46','__RequestVerificationToken': '{}'.format(tken)}
    ls=requests.post(url,headers=header,data=payload)
    cov1=dict(ls.json())
    bangls=pd.DataFrame(cov1['data'])
    bangls.drop(['ReportDataID','TermID','TermYear','TernDay','NormID','GroupName','CssStyle','NormTypeID','NormGroupID','FromSource'], axis=1, inplace=True)
    return bangls

def solieu_banle_vietstock(fromdate,todate):###HAMSOLIEUBANLE 12 
    asp,rtoken,tken=token()
    fromdate=pd.to_datetime(fromdate)
    todate=pd.to_datetime(todate)
    tungay=str(fromdate.strftime('%Y-%m-%d'))
    denngay=str(todate.strftime('%Y-%m-%d'))
    url='https://finance.vietstock.vn/data/reportdatatopbynormtype'
    header={'User-Agent':random_user(),'Cookie': 'language=vi-VN; ASP.NET_SessionId={}; __RequestVerificationToken={}; Theme=Light; _ga=GA1.2.521754408.1675222361; _gid=GA1.2.2063415792.1675222361; AnonymousNotification='.format(asp,rtoken)}
    payload={'type':'2','fromYear':fromdate.year,'toYear':todate.year,
             'from':fromdate.month,'to':todate.month,'normTypeID':'47','__RequestVerificationToken': '{}'.format(tken)}
    ls=requests.post(url,headers=header,data=payload)
    cov1=dict(ls.json())
    bangls=pd.DataFrame(cov1['data'])
    bangls.drop(['ReportDataID','TermID','TermYear','TernDay','NormID','GroupName','CssStyle','NormTypeID','NormGroupID',], axis=1, inplace=True)
    return bangls

def solieu_XNK_vietstock(fromdate,todate):###HAMSOLIEUXNK 13
    asp,rtoken,tken=token()
    fromdate=pd.to_datetime(fromdate)
    todate=pd.to_datetime(todate)
    tungay=str(fromdate.strftime('%Y-%m-%d'))
    denngay=str(todate.strftime('%Y-%m-%d'))
    url='https://finance.vietstock.vn/data/reportdatatopbynormtype'
    header={'User-Agent':random_user(),'Cookie': 'language=vi-VN; ASP.NET_SessionId={}; __RequestVerificationToken={}; Theme=Light; _ga=GA1.2.521754408.1675222361; _gid=GA1.2.2063415792.1675222361; AnonymousNotification='.format(asp,rtoken)}
    payload={'type':'2','fromYear':fromdate.year,'toYear':todate.year,
             'from':fromdate.month,'to':todate.month,'normTypeID':'48','__RequestVerificationToken': '{}'.format(tken)}
    ls=requests.post(url,headers=header,data=payload)
    cov1=dict(ls.json())
    bangls=pd.DataFrame(cov1['data'])
    bangls.drop(['ReportDataID','TermID','TermYear','TernDay','NormID','GroupName','CssStyle','NormTypeID','NormGroupID',], axis=1, inplace=True)
    return bangls

def solieu_FDI_vietstock(fromdate,todate):###HAMSOLIEUVONFDI 14
    asp,rtoken,tken=token()
    fromdate=pd.to_datetime(fromdate)
    todate=pd.to_datetime(todate)
    url='https://finance.vietstock.vn/data/reportdatatopbynormtype'
    header={'User-Agent':random_user(),'Cookie': 'language=vi-VN; ASP.NET_SessionId={}; __RequestVerificationToken={}; Theme=Light; _ga=GA1.2.521754408.1675222361; _gid=GA1.2.2063415792.1675222361; AnonymousNotification='.format(asp,rtoken)}
    payload={'type':'2','fromYear':fromdate.year,'toYear':todate.year,
             'from':fromdate.month,'to':todate.month,'normTypeID':'50','__RequestVerificationToken': '{}'.format(tken)}
    ls=requests.post(url,headers=header,data=payload)
    cov1=dict(ls.json())
    bangls=pd.DataFrame(cov1['data'])
    bangls.drop(['ReportDataID','TermID','TermYear','TernDay','NormID','GroupName','CssStyle','NormTypeID','NormGroupID',], axis=1, inplace=True)
    return bangls

def tygia_vietstock(fromdate,todate):###HAMGETTYGIAVIETSTOCK 15
    asp,rtoken,tken=token()
    fromdate=pd.to_datetime(fromdate)
    todate=pd.to_datetime(todate)
    tungay=str(fromdate.strftime('%Y-%m-%d'))
    denngay=str(todate.strftime('%Y-%m-%d'))
    url='https://finance.vietstock.vn/data/reportdatatopbynormtype'
    header={'User-Agent':random_user(),'Cookie': 'language=vi-VN; ASP.NET_SessionId={}; __RequestVerificationToken={}; Theme=Light; _ga=GA1.2.521754408.1675222361; _gid=GA1.2.2063415792.1675222361; AnonymousNotification='.format(asp,rtoken)}
    payload={'type':'1','fromYear':fromdate.year,'toYear':todate.year,'from':tungay,'to':denngay,'normTypeID':'53','__RequestVerificationToken': '{}'.format(tken)}
    ls=requests.post(url,headers=header,data=payload)
    cov1=dict(ls.json())
    bangls=pd.DataFrame(cov1['data'])
    bangls.drop(['ReportDataID','TermID','TermYear','TernDay','NormID','GroupName','CssStyle','NormTypeID','NormGroupID'], axis=1, inplace=True)
    return bangls

def solieu_tindung_vietstock(fromdate,todate):###HAMGETDATATINDUNG 16
    asp,rtoken,tken=token()
    fromdate=pd.to_datetime(fromdate)
    todate=pd.to_datetime(todate)
    url='https://finance.vietstock.vn/data/reportdatatopbynormtype'
    header={'User-Agent':random_user(),'Cookie': 'language=vi-VN; ASP.NET_SessionId={}; __RequestVerificationToken={}; Theme=Light; _ga=GA1.2.521754408.1675222361; _gid=GA1.2.2063415792.1675222361; AnonymousNotification='.format(asp,rtoken)}
    payload={'type':'2','fromYear':fromdate.year,'toYear':todate.year,
             'from':fromdate.month,'to':todate.month,'normTypeID':'51','__RequestVerificationToken': '{}'.format(tken)}
    ls=requests.post(url,headers=header,data=payload)
    cov1=dict(ls.json())
    bangls=pd.DataFrame(cov1['data'])
    bangls.drop(['ReportDataID','TermID','TermYear','TernDay','NormID','GroupName','CssStyle','NormTypeID','NormGroupID',], axis=1, inplace=True)
    return bangls

def laisuat_vietstock(fromdate,todate):###HAMGETLAISUAT 17
    asp,rtoken,tken=token()
    fromdate=pd.to_datetime(fromdate)
    todate=pd.to_datetime(todate)
    tungay=str(fromdate.strftime('%Y-%m-%d'))
    denngay=str(todate.strftime('%Y-%m-%d'))
    url='https://finance.vietstock.vn/data/reportdatatopbynormtype'
    header={'User-Agent':random_user(),'Cookie': 'language=vi-VN; ASP.NET_SessionId={}; __RequestVerificationToken={}; Theme=Light; _ga=GA1.2.521754408.1675222361; _gid=GA1.2.2063415792.1675222361; AnonymousNotification='.format(asp,rtoken)}
    payload={'type':'1','fromYear':fromdate.year,'toYear':todate.year,'from':tungay,'to':denngay,'normTypeID':'66','__RequestVerificationToken': '{}'.format(tken)}
    ls=requests.post(url,headers=header,data=payload)
    cov1=dict(ls.json())
    bangls=pd.DataFrame(cov1['data'])
    bangls.drop(['ReportDataID','TermID','TermYear','TernDay','NormID','GroupName','CssStyle','NormTypeID','NormGroupID'], axis=1, inplace=True)
    df_bang=bangls.pivot(index='ReportTime',columns='NormName',values='NormValue')
    df_bang.reset_index(inplace=True)
    df_bang.columns.name=None
    return df_bang

def solieu_danso_vietstock(fromdate,todate):###HAMGETSOLIEUDANSO 18
    asp,rtoken,tken=token()
    fromdate=pd.to_datetime(fromdate)
    todate=pd.to_datetime(todate)
    tungay=str(fromdate.strftime('%Y-%m-%d'))
    denngay=str(todate.strftime('%Y-%m-%d'))
    url='https://finance.vietstock.vn/data/reportdatatopbynormtype'
    header={'User-Agent':random_user(),'Cookie': 'language=vi-VN; ASP.NET_SessionId={}; __RequestVerificationToken={}; Theme=Light; _ga=GA1.2.521754408.1675222361; _gid=GA1.2.2063415792.1675222361; AnonymousNotification='.format(asp,rtoken)}
    payload={'type':'4','fromYear':fromdate.year,'toYear':todate.year,'from':tungay,'to':denngay,'normTypeID':'55','__RequestVerificationToken': '{}'.format(tken)}
    ls=requests.post(url,headers=header,data=payload)
    cov1=dict(ls.json())
    bangls=pd.DataFrame(cov1['data'])
    bangls.drop(['ReportDataID','TermID','TermYear','TernDay','NormID','GroupName','CssStyle','NormTypeID','NormGroupID'], axis=1, inplace=True)
    return bangls
def solieu_GDP_vietstock(fromyear,fromQ,toyear,toQ):###HAMGETGDP 19
    asp,rtoken,tken=token()
    url='https://finance.vietstock.vn/data/reportdatatopbynormtype'
    header={'User-Agent':random_user(),'Cookie': 'language=vi-VN; ASP.NET_SessionId={}; __RequestVerificationToken={}; Theme=Light; _ga=GA1.2.521754408.1675222361; _gid=GA1.2.2063415792.1675222361; AnonymousNotification='.format(asp,rtoken)}
    payload={'type':'3','fromYear':fromyear,'toYear':toyear,'from':fromQ,'to':toQ,'normTypeID':'43','__RequestVerificationToken': '{}'.format(tken)}
    ls=requests.post(url,headers=header,data=payload)
    cov1=dict(ls.json())
    bangls=pd.DataFrame(cov1['data'])
    bangls.drop(['ReportDataID','TermID','TermYear','TernDay','NormID','GroupName','CssStyle','NormTypeID','NormGroupID'], axis=1, inplace=True)
    return bangls

def get_data_history_cafef(symbol,fromdate,todate):### 20
    data=browser_get_data(symbol,fromdate,todate).getdata()
    return data
