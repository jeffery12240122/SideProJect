from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import reptile as rep
import requests
from flask import Flask, request, abort
from flask import send_from_directory
import logging
import sqlite3
from flask import g

app = Flask(__name__)

line_bot_api = LineBotApi('TOttUtUSAZnZgHzeuQiEOAfEYemiyRStXIN2FtfP4cwDKrLK/5FymCAQgnLtf79Do7GyzGL4gINYPS6+BtbgAaayn3LuRb2uc0x6ONLbq7zzbOKyyeJuhgJYrLDqEGy88L7qO6v6Tq3Mx02r+1eLRgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('52691829ff3c9df4e39162fc403b0a9e')

# 建立 SQLite 資料庫連接的函數
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('stock_reminder.db')
    return g.db

# 在請求完成後關閉資料庫連接的函數
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
        
        
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 連接到 SQLite 資料庫
    try:
        conn = sqlite3.connect('stock_reminder.db')
        print("Database connection established successfully.")
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
    c = conn.cursor()

    # 建立股票提醒資料表
    c.execute('''CREATE TABLE IF NOT EXISTS reminders
             (id INTEGER PRIMARY KEY AUTOINCREMENT, stock_code TEXT, target_price REAL)''')

    message_text = event.message.text.lower()  # 將使用者輸入轉換為小寫
    tokens = message_text.split(' ')
    db = get_db()  # 獲取資料庫連接
    
    if tokens[0] == 'add' and len(tokens) == 3:
        stock_code = tokens[1]
        target_price = float(tokens[2])
        
        # 使用 reptile.py 中的函數解析 HTML 並獲取解析樹對象
        tree = rep.getUrl(stock_code)
        
        current_price = rep.getPrice(tree)
        
        if current_price is not None:
            if current_price >= target_price:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=f"股票 {stock_code} 已達到目標價格 {target_price}，請注意。")
                )
            else:
                c.execute("INSERT INTO reminders (stock_code, target_price) VALUES (?, ?)", (stock_code, target_price))
                conn.commit()
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=f"已添加提醒：當股票 {stock_code} 達到 {target_price} 時將通知您。\n目前股價為{current_price}")
                )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"無法獲取股票 {stock_code} 的價格，請稍後再試。")
            )

    
    elif tokens[0] == 'del' and len(tokens) == 2:
        stock_code = tokens[1]
        c = db.cursor()
        c.execute("DELETE FROM reminders WHERE stock_code=?", (stock_code,))
        db.commit()

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"已刪除股票 {stock_code} 的提醒。")
        )
        conn = sqlite3.connect('stock_reminder.db')
        c = conn.cursor()
        c.execute("SELECT stock_code, target_price FROM reminders")
        reminders = c.fetchall()
        
    elif tokens[0] == 'list' and len(tokens) == 1:
        c.execute("SELECT stock_code, target_price FROM reminders")
        reminders = c.fetchall()
        if reminders:
            # 將查詢結果格式化成文字訊息
            message = "已加入的股票及通知股價：\n"
            for stock_code, target_price in reminders:
                message += f"股票代碼：{stock_code}，通知股價：{target_price}\n"
        else:
            message = "目前沒有任何股票提醒"
        
        # 回覆訊息給使用者
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
        )
    elif tokens[0] == 'help':
        message = '-add stock_num notice_price\n'
        message += '-del stock_num\n'
        message += '-list\n\n'
        message += 'Example1 : add 0050 130\n'
        message += 'Example2 : del 0050\n'
        message += 'Example3 : list '
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
        )
    
    # 在這裡關閉資料庫連接
    conn.close()
        

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000) 
