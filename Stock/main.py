import reptile

name = reptile.getName()[0].strip()
price = reptile.getPrice()[0].strip()
up = reptile.getUpDown()[0].strip()
percent = reptile.getPercentage()[0].strip()[1:-1]

if reptile.getUrl()[0].status_code == 200:
    if reptile.getName():
        print(name + '股價：', price)
        print('漲跌:', up)
        print('漲跌幅:', percent)
    else:
        print('無法找到此股。')
else:
    print('404 Error!!!。')


