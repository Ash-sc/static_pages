from bs4 import BeautifulSoup
import requests
import time
import sys


# 保持会话
# 新建一个session对象
sess = requests.session()

# 添加headers（header为自己登录的企查查网址，输入账号密码登录之后所显示的header，此代码的上方介绍了获取方法）
afterLogin_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'}

# post请求(代表着登录行为，登录一次即可保存，方便后面执行查询指令)
login = {}
sess.post('https://www.qcc.com',data=login,headers=afterLogin_headers)

def get_company_message(company):
    # 获取查询到的网页内容（全部）
    search = sess.get('https://www.qcc.com/web/search?key={}'.format(company),headers=afterLogin_headers,timeout=10)
    search.raise_for_status()
    search.encoding = 'utf-8' #linux utf-8
    soup = BeautifulSoup(search.text,features="html.parser")
    href = soup.find_all('a',{'class': 'title'})[0].get('href')
    time.sleep(4)
    # 获取查询到的网页内容（全部）
    details = sess.get(href,headers=afterLogin_headers,timeout=10)
    details.raise_for_status()
    details.encoding = 'utf-8' #linux utf-8
    details_soup = BeautifulSoup(details.text,features="html.parser")
    message = details_soup.text
    time.sleep(2)
    return message

import pandas as pd

def message_to_df(message,company):
    list_companys = []
    Date_of_Establishment = []
    registered_capital = []
    Unified_social_credit_code = []
    Taxpayer_Identification_Number = []
    sub_Industry = []
    enterprise_type = []
    qualification_num = []
    Registration_Authority = []
    Business_Scope = []

    list_companys.append(company)
    Date_of_Establishment.append(message.split('成立日期')[1].split('\n')[1].replace(' ',''))
    registered_capital.append(message.split(' 注册资本 ')[1].split('元人民币')[0].replace(' ',''))
    try:
        credit = '"' + message.split('统一社会信用代码')[1].split('\n')[1].replace(' ','') + '"'
        Unified_social_credit_code.append(credit)
    except:
        credit = '"' + message.split('统一社会信用代码')[3].split('\n')[1].replace(' ','') + '"'
        Unified_social_credit_code.append(credit)
    Taxpayer_Identification_Number.append(message.split('纳税人识别号')[1].split('\n')[1].replace(' ',''))
    try:
        sub = message.split('所属行业')[1].split('\n')[1].replace(' ','')
        sub_Industry.append(sub)
    except:
        sub = message.split('所属行业')[1].split('为')[1].split('，')[0]
        sub_Industry.append(sub)
    enterprise_type.append(message.split('企业类型')[1].split('\n')[1].replace(' ',''))
    qualification_num.append(message.split('纳税人资质')[1].split('\n')[2].replace(' ',''))
    Registration_Authority.append(message.split('登记机关')[1].split('\n')[1].replace(' ',''))
    Business_Scope.append(message.split('经营范围')[1].split('功能')[0].split('{}'.format(company))[0])
    df = pd.DataFrame({'企业名称':company,\
                      '统一社会信用代码':Unified_social_credit_code,\
                      '注册资本':registered_capital,\
                      '企业类型':enterprise_type,\
                      '纳税人资质':qualification_num,\
                      '成立日期':Date_of_Establishment,\
                      '登记机关':Registration_Authority,\
                      '经营范围':Business_Scope})
    
    return df

# 测试所用
companys = sys.argv[1:]

# 实际所用
# df_companys = pd.read_csv('自己目录的绝对路径/某某.csv')
# companys = df_companys['公司名称'].tolist()

for company in companys:
    try:
        messages = get_company_message(company)
    except:
        pass
    else:
        df = message_to_df(messages,company)
        if(company==companys[0]):
            df.to_csv('/Users/shenchuang/Documents/static_pages/download/dist/result.csv',index=False,header=True,encoding="utf_8_sig")
        else:
            df.to_csv('/Users/shenchuang/Documents/static_pages/download/dist/result.csv',mode='a+',index=False,header=False,encoding="utf_8_sig")
    time.sleep(1)