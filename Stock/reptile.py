import requests
from lxml import html

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
    if upDown(tree) == 2:
        return 0 + float(tree.xpath('//*[@id="main-0-QuoteHeader-Proxy"]/div/div[2]/div[1]/div/span[2]/text()')[0].strip())    
    elif upDown(tree) == 3:
        return 0 - float(tree.xpath('//*[@id="main-0-QuoteHeader-Proxy"]/div/div[2]/div[1]/div/span[2]/text()')[0].strip())
    else:
        return float(tree.xpath('//*[@id="main-0-QuoteHeader-Proxy"]/div/div[2]/div[1]/div/span[2]/text()')[0].strip())

def getPercentage(tree):
    percentage = tree.xpath('//*[@id="main-0-QuoteHeader-Proxy"]/div/div[2]/div[1]/div/span[3]/text()')
    if upDown(tree) == 2:
        return float(0) + float(percentage[0].replace('%', '')[1:-1])
    elif upDown(tree) == 3:
        return float(0) - float(percentage[0].replace('%', '')[1:-1])
    else:
        return float(percentage[0].replace('%', '')[1:-1])

def upDown(tree):
     up = tree.xpath('//*[@id="main-0-QuoteHeader-Proxy"]/div/div[2]/div[1]/div/span[2]/span/@style')
     if up == []:
         return 1
     elif '#ff333a' in up[0]:
         return 2
     elif '#00ab5e' in up[0]:
         return 3

    
     


