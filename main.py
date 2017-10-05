from flask import Flask, request
import requests

TESTBOTID = '8c470e6280d30e292d42f64a91'
SPSBOTID = 'caefd5601535a6e6924f38efb8'
BOTNAME = 'spsbot'
URL = 'https://api.groupme.com/v3/bots/post'

app = Flask(__name__)

@app.route('/')
def root():
    return 'Hello world'

#
# TEST BOT
# group: bot testing
# test things here before deploying to sps member group
#
@app.route('/spstest', methods=['GET','POST'])
def spstest():
    botid = TESTBOTID
    request.form = parseData(request.data)
    request.form['text'] = request.form['text'].lower()
    if request.method == 'POST':
        if shouldRespond(request):
            if isGreeting(request.form['text']):
                response = 'Hi ' + request.form['name']
            elif isFratGreeting(request.form['text']):
                response = 'Asuh brah'
            r = requests.post(URL, data={
                    'bot_id':botid,
                    'text':response
                    })
    return 'spstest'

#
# SPSBOT
# group: Official SPS Members 2017-2018
# make sure stuff works before you put it here
#
@app.route('/spsbot', methods=['GET','POST'])
def spsbot():
    botid = SPSBOTID
    request.form = parseData(request.data)
    request.form['text'] = request.form['text'].lower()
    if request.method == 'POST':
        if shouldRespond(request):
            if isGreeting(request.form['text']):
                response = 'Hi ' + request.form['name']
            elif isFratGreeting(request.form['text']):
                response = 'Asuh brah'
            r = requests.post(URL, data={
                    'bot_id':botid,
                    'text':response
                    })
    return 'spsbot'

#
# support functions
#

def parseData(data):
    s = str(data)
    s = s[3:len(s)-2]
    s = s.replace('"','')
    arr = s.split(',')
    parsed = {}
    for keyval in arr:
        idx = keyval.find(':')
        parsed[keyval[:idx]] = keyval[idx+1:len(keyval)]
    return parsed

def shouldRespond(request):
    return ((request.form['sender_type'] == 'user')
        and (BOTNAME in request.form['text']))

def isGreeting(msg):
    greetings = ['hi','hey','hello','sup','hai','wazzup','howdy','yo']
    for g in greetings:
        if g in msg:
            return True
    return False

def isFratGreeting(msg):
    return 'asuh' in msg
