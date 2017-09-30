from flask import Flask, request
import requests

BOTID = '8c470e6280d30e292d42f64a91'
BOTNAME = 'spsbot'
URL = 'https://api.groupme.com/v3/bots/post'

app = Flask(__name__)

@app.route('/')
def root():
    return 'Hello world'

@app.route('/spstest', methods=['GET','POST'])
def spstest():
    request.form = parseData(request.data)
    if request.method == 'POST':
        if request.data['sender_type'] == 'user':
            r = requests.post(URL, data={
                    'bot_id':BOTID,
                    'text':'response'
                    })
    return 'spstest'

def parseData(data):
    # parse the data string into a dictionary
    return parsed