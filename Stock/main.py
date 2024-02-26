import reptile
stock_code = reptile.stockNum()
tree = tree = reptile.getUrl(stock_code)


print(reptile.getName(tree) + '股價：', reptile.getPrice(tree))
print('漲跌:', reptile.getUpDown(tree))
print('漲跌幅:', reptile.getPercentage(tree))




