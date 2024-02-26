import requests
from lxml import html
def stockNum():
    stock_num = (input("請輸入股價代碼:"))
    return stock_num
def getUrl(stock_num):
    url = 'https://tw.stock.yahoo.com/q/q?s='+stock_num
    # 發送 GET 請求並獲取內容
    response = requests.get(url)
    tree = html.fromstring(response.content)
    return tree

def getPrice(tree):
    price = tree.xpath('//*[@id="main-0-QuoteHeader-Proxy"]/div/div[2]/div[1]/div/span[1]/text()')
    return float(price[0].replace(',', ''))
    

def getName(tree):
    return tree.xpath('//*[@id="main-0-QuoteHeader-Proxy"]/div/div[1]/h1/text()')[0].strip()


def getUpDown(tree):
    return float(tree.xpath('//*[@id="main-0-QuoteHeader-Proxy"]/div/div[2]/div[1]/div/span[2]/text()')[0].strip())

def getPercentage(tree):

    percentage = tree.xpath('//*[@id="main-0-QuoteHeader-Proxy"]/div/div[2]/div[1]/div/span[3]/text()')
    updown = tree.xpath('//*[@id="main-0-QuoteHeader-Proxy"]/div/div[2]/div[1]/div/span[2]/span/@style')
    if '#ff333a' in updown:
        return float(0) + float(percentage[0].replace('%', '')[1:-1])
    elif '#00ab5e' in updown:
        return float(0) - float(percentage[0].replace('%', '')[1:-1])
    else:
        return float(percentage[0].replace('%', '')[1:-1])

    


