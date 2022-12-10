from flask import Flask, request, abort
from key import WEBHOOK_URL,WEBHOOK_PORT,API_TOKEN
import telebot
from bot import bot

app = Flask(__name__)

# return OK
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''

# process webhook calls
@app.route('/{}'.format(API_TOKEN), methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)

bot.set_webhook('{URL}:{PORT}/{HOOK}/'.format(URL=WEBHOOK_URL, PORT=WEBHOOK_PORT, HOOK=API_TOKEN))

if __name__ == '__main__':
    app.run(port=WEBHOOK_PORT,threaded=True)
