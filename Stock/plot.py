import pandas as pd
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates

# 读取CSV文件
df = pd.read_csv('2330.csv')

# 将日期转换为matplotlib可识别的格式
df['Date'] = pd.to_datetime(df['Date'])
df['Date'] = df['Date'].apply(mdates.date2num)

# 创建子图
fig, ax = plt.subplots()

# 绘制K线图
candlestick_ohlc(ax, df[['Date', 'Open', 'High', 'Low', 'Close']].values, width=0.6, colorup='g', colordown='r')

# 设置x轴日期格式
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# 自动旋转日期标签
plt.xticks(rotation=45)



# 设置图表标题和标签
plt.title('Stock K-Line')
plt.xlabel('Date')
plt.ylabel('Price')

# 显示网格
plt.grid(True)

# 显示图表
plt.show()