import requests
from lxml import html

stock_num = (input("請輸入股價代碼:"))
url = 'https://tw.stock.yahoo.com/q/q?s='+stock_num

# 發送 GET 請求並獲取內容
response = requests.get(url)

if response.status_code == 200:
    # 使用 lxml 解析頁面內容
    tree = html.fromstring(response.content)
    
    #股價XPATH
    price_element = tree.xpath('//*[@id="main-0-QuoteHeader-Proxy"]/div/div[2]/div[1]/div/span[1]/text()')
    #股名XPATH
    name_element = tree.xpath('//*[@id="main-0-QuoteHeader-Proxy"]/div/div[1]/h1/text()')
    #漲跌
    highlow = tree.xpath('//*[@id="main-0-QuoteHeader-Proxy"]/div/div[2]/div[1]/div/span[2]/text()')
    #漲跌幅
    percentage = tree.xpath('//*[@id="main-0-QuoteHeader-Proxy"]/div/div[2]/div[1]/div/span[3]/text()')

    if name_element:
        
        # 提取股價和股價名稱
        price = price_element[0].strip()
        name = name_element[0].strip()
        high = highlow[0].strip()
        percent = percentage[0].strip()[1:-1]
        
        
        print(name + '股價：', price)
        print('漲跌:', high)
        print('漲跌幅:', percent)
    else:
        print('無法找到此股。')
else:
    print('404 Error!!!。')