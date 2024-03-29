import requests
from lxml import html
import re
def structure(url):
    response = requests.get(url)
    tree = html.fromstring(response.content)
    company = tree.xpath('//*[@id="index"]/div[2]/div[1]/div[3]/div/div[1]/div[2]/div[1]/div[1]/div/div[4]/div/button[2]/text()')
    num = re.findall(r'\d+', company[0])
    return int(num[0].replace(',', ''))


def M():
    url = 'https://www.104.com.tw/company/search/?keyword=%E8%81%AF%E7%99%BC%E7%A7%91&jobsource=index_s_cs&mode=s&page=1'
    return structure(url)

def R():
    url = 'https://www.104.com.tw/company/search/?keyword=%E7%91%9E%E6%98%B1&jobsource=index_s_cs&mode=s&page=1'
    return structure(url)

def N():
    url = 'https://www.104.com.tw/company/search/?keyword=%E8%81%AF%E8%A9%A0&jobsource=index_s_cs&mode=s&page=1'
    return structure(url)

def P():
    url = 'https://www.104.com.tw/company/search/?keyword=%E7%BE%A4%E8%81%AF&jobsource=index_s_cs&mode=s&page=1'
    return structure(url)
def A():
    url = 'https://www.104.com.tw/company/search/?keyword=%E9%81%94%E7%99%BC&jobsource=index_s_cs&mode=s&page=1'
    return structure(url)






print("MTK : " + str(M()))
print("Novatek : " + str(N()))
print("Realtek : " + str(R()))
print("Phison : " + str(P()))
print("Airoha : " + str(A()))
