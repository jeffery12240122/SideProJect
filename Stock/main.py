
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import reptile as rep
import requests
from flask import Flask, request, abort

app = Flask(__name__)
handler = WebhookHandler('52691829ff3c9df4e39162fc403b0a9e')
line_bot_api = LineBotApi('TOttUtUSAZnZgHzeuQiEOAfEYemiyRStXIN2FtfP4cwDKrLK/5FymCAQgnLtf79Do7GyzGL4gINYPS6+BtbgAaayn3LuRb2uc0x6ONLbq7zzbOKyyeJuhgJYrLDqEGy88L7qO6v6Tq3Mx02r+1eLRgdB04t89/1O/w1cDnyilFU=')


@app.route("/callback", methods=['POST'])

def callback():
    
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:

        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
        
        
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_input = event.message.text  
    tree = rep.getUrl(user_input)
    
    name = rep.getName(tree)
    price = rep.getPrice(tree)
    up_down = rep.getUpDown(tree)
    percentage = rep.getPercentage(tree)
    
    reply_message = f"股票名稱：{name}\n當前價格：{price}\n漲跌額：{up_down}\n漲跌幅：{percentage}%"
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

if __name__ == "__main__":
    app.run(debug=True)    
