import requests
from lxml import html
stock_num = (input("請輸入股價代碼:"))
def getUrl():
    url = 'https://tw.stock.yahoo.com/q/q?s='+stock_num
    # 發送 GET 請求並獲取內容
    response = requests.get(url)
    tree = html.fromstring(response.content)
    return response,tree

def getPrice():
    return getUrl()[1].xpath('//*[@id="main-0-QuoteHeader-Proxy"]/div/div[2]/div[1]/div/span[1]/text()')
    

def getName():
    return getUrl()[1].xpath('//*[@id="main-0-QuoteHeader-Proxy"]/div/div[1]/h1/text()')


def getUpDown():
    return getUrl()[1].xpath('//*[@id="main-0-QuoteHeader-Proxy"]/div/div[2]/div[1]/div/span[2]/text()')

def getPercentage():
    return getUrl()[1].xpath('//*[@id="main-0-QuoteHeader-Proxy"]/div/div[2]/div[1]/div/span[3]/text()')

if getUrl()[0].status_code == 200:    
    if  getName():
        price = getPrice()[0].strip()
        name = getName()[0].strip()
        up = getUpDown()[0].strip()
        percent = getPercentage()[0].strip()[1:-1]
        print(name + '股價：', price)
        print('漲跌:', up)
        print('漲跌幅:', percent)
    else:
        print('無法找到此股。')
else:
    print('404 Error!!!。')