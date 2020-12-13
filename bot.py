#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import (Updater, CommandHandler, ConversationHandler,
MessageHandler, Filters)
from urllib import request

PORT = int(os.environ.get('PORT', 5000))
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

token='REPLACE_WITH_YOUR_TOKEN'

updater = Updater(token,use_context=True)
dp = updater.dispatcher

qry = range(1)

def predict(update, context):
    update.message.reply_text("""Input your Pregnancies,Glucose,Bloodpressure,Skinthickness,Insulin,BodyMassIndex,DiabetesPedigreeFunction, and Age with this format

Pregnancies/Glucose/Bloodpressure/Skinthickness/Insulin/BodyMassIndex/DiabetesPedigreeFunction/Age

For Example

1/89/66/23/94/28.1/0.167/21

    """)
    return qry

def result(update, context):
    # Gunakan huruf besar saat pencarian
    query = update.message.text.strip()
    a = query
    inp = a.split('/')
    a = inp[0]
    b = inp[1]
    c = inp[2]
    d = inp[3]
    e = inp[4]
    f = inp[5]
    g = inp[6]
    h = inp[7]
    url = f'http://feelfree10.pythonanywhere.com/api?pregnancies={a}&glucose={b}&bloodpressure={c}&skinthickness={d}&insulin={e}&bmi={f}&dbf={g}&age={h}'
    response = request.urlopen(url)
    data = json.loads(response.read())
    c = data['result']

    if c == str(0):
        c = 'You dont have potential to get have diabetes. Keep up your good health. '
    elif c == str(1):
        c = 'You have potential to get diabetes.Please take medical check up.'

    text = f'{str(c)}'
    update.message.reply_text(text)
    return ConversationHandler.END

obrolan = ConversationHandler(
    entry_points = [CommandHandler('predict', predict)],
    states = {
        qry: [MessageHandler(Filters.text, result)]
    },
    fallbacks = []
)

def main():
    """Start the bot."""
    dp.add_handler(obrolan)
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=token)
    updater.bot.setWebhook('https://yourappname.herokuapp.com/' + token)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
