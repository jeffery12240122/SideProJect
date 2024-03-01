from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import reptile as rep
import requests
from flask import Flask, request, abort
from flask import send_from_directory
import logging
app = Flask(__name__)

line_bot_api = LineBotApi('TOttUtUSAZnZgHzeuQiEOAfEYemiyRStXIN2FtfP4cwDKrLK/5FymCAQgnLtf79Do7GyzGL4gINYPS6+BtbgAaayn3LuRb2uc0x6ONLbq7zzbOKyyeJuhgJYrLDqEGy88L7qO6v6Tq3Mx02r+1eLRgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('52691829ff3c9df4e39162fc403b0a9e')

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
    user_input = event.message.text  

    # Log user input
    logging.info(f"Received message from user: {user_input}")

    # Get stock information
    tree = rep.getUrl(user_input)
    logging.info(f"Retrieved stock information: {tree}")

    # Extract stock details
    name = rep.getName(tree)
    price = rep.getPrice(tree)
    up_down = rep.getUpDown(tree)
    percentage = rep.getPercentage(tree)

    # Generate reply message
    reply_message = f"股票名稱：{name}\n當前價格：{price}\n漲跌額：{up_down}\n漲跌幅：{percentage}%"
    logging.info(f"Generated reply message: {reply_message}")

    # Reply to user
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000) 
