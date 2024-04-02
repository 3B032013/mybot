# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 15:04:03 2024

@author: user
"""

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import bot_info

app = Flask(__name__)

# LINE Bot Basic Profile
line_bot_api = LineBotApi(bot_info.line_bot_token)
handler = WebHookHandler(bot_info.line_bot_secret)

# Post Request from LINE Platform
@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info('Request body:' + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def echo(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

if __name__ == '__main__':
    app.run()