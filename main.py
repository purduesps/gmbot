from flask import Flask, request
import requests
import random
import re
import numpy as np
from json import loads

class bot:

    def __init__(self, name):
        self.NAME = name
        self.TESTBOTID = '8c470e6280d30e292d42f64a91'
        self.SPSBOTID = 'caefd5601535a6e6924f38efb8'
        self.URL = 'https://api.groupme.com/v3/bots/post'

        self.loungeStatus = 'closed'
        self.wellStatus = 'closed'

        self.app = Flask(__name__)

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
            botid = self.TESTBOTID
            request.form = parseData(request.data)
            request.form['text'] = request.form['text'].lower()
            if shouldRespond(request):
                print('should respond to '+request.form['text'])
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
                try:
                    r = requests.post(URL, data={
                            'bot_id':botid,
                            'text':response
                            })
                except NameError:
                    return "spstest didn't say anything"
        return 'spstest'

    #
    # SPSBOT
    # group: Official SPS Members 2017-2018
    # make sure stuff works before you put it here
    #
    @app.route('/spsbot', methods=['GET','POST'])
    def spsbot():
        if request.method == 'POST':
            botid = self.SPSBOTID
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
                try:
                    r = requests.post(URL, data={
                            'bot_id':botid,
                            'text':response
                            })
                except NameError:
                    return "spsbot didn't say anything"
        return 'spsbot'

    #
    # handle ping for lounge status
    #
    @app.route('/spsbot/lounge', methods=['GET','POST'])
    def lounge():
        if request.method == 'POST':
            data = loads(request.get_data().decode('utf-8'))
            if 'lounge' in data:
                self.loungeStatus = ['closed','open'][data['lounge']]
            else:
                self.loungeStatus = 'closed'
        else:
            if self.loungeStatus == 'open':
                self.loungeStatus = 'closed'
            elif self.loungeStatus == 'closed':
                self.loungeStatus = 'open'
        return 'lounge'

    #
    # handle ping for well status
    #
    @app.route('/spsbot/well', methods=['GET','POST'])
    def well():
        if self.wellStatus == 'open':
            self.wellStatus = 'closed'
        elif self.wellStatus == 'closed':
            self.wellStatus = 'open'
        return 'well'

    #
    # support functions
    #

    def parseData(data):
        s = str(data)
        s = s[3:len(s)-2]
        parsed = {'text':findText(s)}
        s = s.replace('"text":"'+parsed['text']+'"','')
        arr = s.split(',')
        for keyval in arr:
            keyval = keyval.replace('"','')
            idx = keyval.find(':')
            parsed[keyval[:idx]] = keyval[idx+1:len(keyval)]
        return parsed

    def findText(string):
        idx = string.find('"text":')
        idx += len('"text":')
        string = string[idx:]
        idx = string.find('","')
        string = string[1:idx]
        return string

    def shouldRespond(request):
        print(request.form['sender_type'])
        print(re.search(r'\b'+BOTNAME+r'\b', request.form['text']))
        return ((request.form['sender_type'] == 'user')
            and ((re.search(r'\b'+BOTNAME+r'\b', request.form['text']) != None)
            or (request.form['text'] == 'good bot')
            or (request.form['text'] == 'bad bot')))

    def isGreeting(msg):
        greetings = ['hi','hey','hello','sup','hai',
                'wazzup','wassup','howdy','yo']
        for g in greetings:
            if re.search(r'\b'+g+r'\b', msg) != None:
                return True
        return False

    def isFratGreeting(msg):
        return re.search(r'\basuh\b', msg) != None

    def isLoungeRequest(msg):
        return re.search(r'\blounge\b', msg) != None

    def isWellRequest(msg):
        return re.search(r'\bwell\b', msg) != None

bot('spsbot')
