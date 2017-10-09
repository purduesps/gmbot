from flask import Flask, request
import requests
import random

TESTBOTID = '8c470e6280d30e292d42f64a91'
SPSBOTID = 'caefd5601535a6e6924f38efb8'
BOTNAME = 'spsbot'
URL = 'https://api.groupme.com/v3/bots/post'

loungeStatus = 'closed'
wellStatus = 'closed'

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
    if request.method == 'POST':
        botid = TESTBOTID
        request.form = parseData(request.data)
        request.form['text'] = request.form['text'].lower()
        if shouldRespond(request):
            if isGreeting(request.form['text']):
                response = 'Hi ' + request.form['name']
            elif isFratGreeting(request.form['text']):
                response = 'Asuh brah'
            elif request.form['text'] == 'good bot':
                response = random.choice((':)','<3'))
            elif request.form['text'] == 'bad bot':
                response = 'bad person'
            elif isLoungeRequest(request.form['text']):
                response = 'The lounge is ' + loungeStatus
            elif isWellRequest(request.form['text']):
                response = 'The well is ' + wellStatus
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
    if request.method == 'POST':
        botid = SPSBOTID
        request.form = parseData(request.data)
        request.form['text'] = request.form['text'].lower()
        if shouldRespond(request):
            if isGreeting(request.form['text']):
                response = 'Hi ' + request.form['name']
            elif isFratGreeting(request.form['text']):
                response = 'Asuh brah'
            elif request.form['text'] == 'good bot':
                response = random.choice((':)','<3'))
            elif request.form['text'] == 'bad bot':
                response = 'bad person'
            r = requests.post(URL, data={
                    'bot_id':botid,
                    'text':response
                    })
    return 'spsbot'

#
# handle ping for lounge status
#
@app.route('/spsbot/lounge', methods=['GET','POST'])
def lounge():
    global loungeStatus
    if loungeStatus == 'open':
        loungeStatus = 'closed'
    if loungeStatus == 'closed':
        loungeStatus = 'open'
    return 'lounge'

#
# handle ping for well status
#
@app.route('/spsbot/well', methods=['GET','POST'])
def well():
    global wellStatus
    if wellStatus == 'open':
        wellStatus = 'closed'
    if wellStatus == 'closed':
        wellStatus = 'open'
    return 'well'

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
        and ((BOTNAME in request.form['text'])
        or (request.form['text'] == 'good bot')
        or (request.form['text'] == 'bad bot')))

def isGreeting(msg):
    greetings = ['hi','hey','hello','sup','hai','wazzup','howdy','yo']
    for g in greetings:
        if g in msg:
            return True
    return False

def isFratGreeting(msg):
    return 'asuh' in msg

def isLoungeRequest(msg):
    return 'lounge' in msg

def isWellRequest(msg):
    return 'well' in msg
