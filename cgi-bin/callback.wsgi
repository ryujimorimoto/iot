#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, sys, json
from eventlet import wsgi
import eventlet

from builtins import bytes
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)
from linebot.utils import PY3

# Get instance
line_bot_api = LineBotApi("a/uAEBYh63G6o2DwRhaHIwOqkmrbTIDBcAf2NgFi1qMx96W4jeN0BPigF8Kz/T/fWZaMHSeCCx7SxRFyOEtYksUy364uBmFYiShcJrdb27jZzkaxudEAVR+zHE6KVQMsEQ/kkECP44D6Wo4FfaDIrgdB04t89/1O/w1cDnyilFU=")
parser = WebhookParser("7dd4c5047391b622ddbac1c78166be21")

def create_body(text):
    if PY3:
        return [bytes(text, 'utf-8')]
    else:
        return text

# application
def application(env, start_response):

    # check request method
    if env['REQUEST_METHOD'] != 'POST':
        start_response('405 Method Not Allowed', [('Content-Type', 'text/plain')])
        return create_body('Method Not Allowed')

    # get X-Line-Signature header value
    signature = env['HTTP_X_LINE_SIGNATURE']

    # get request body as text
    wsgi_input = env['wsgi.input']
    content_length = int(env['CONTENT_LENGTH'])
    body = wsgi_input.read(content_length).decode('utf-8')

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        start_response('400 Bad Request', [('Content-Type', 'text/plain')])
        return create_body('Bad Request')

    # analytics
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        replyMessage = ''
        text = event.message.text

        # line で on と入力したら、暖房を入れ、"on ok" とlineを返す 
        if( text == "on" ):
            replyMessage = 'on ok'
            os.system("irsend SEND_ONCE aircon hoton")
        # off と入力したら、エアコンを止め、"aircon off ok" とlineを返す
        elif( text == "off" ):
            replyMessage = 'aircon off ok'
            os.system("irsend SEND_ONCE aircon off")
        else:
            replyMessage = text

        try:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=replyMessage))
        except LineBotApiError as e:

    start_response('200 OK', [('Content-Type', 'text/plain')])
    return create_body('200 OK')