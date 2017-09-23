import config
from flask import Flask, render_template, request
from twilio.rest import Client
from twilio.twiml.messaging_response import Message, MessagingResponse
import difflib
import logging as log

DIFF_SENSITIVITY=0.6
app = Flask(__name__)

def send_text(body, to_num, from_num):
    log.debug('Sending text')
    client = Client(config.ACCOUNT_SID, config.AUTH_TOKEN)
    message = client.api.account.messages.create(to=to_num,
						from_=from_num,
						body=body)

def get_api_words():
    return [
        {'api': 'wikipedia', 'words': ['wiki', 'wikipedia']},
        {'api': 'news', 'words': ['news']},
        {'api': 'weather', 'words': ['rain', 'weather', 'sunny', 'snow']},
    ]

def pretend_wiki():
    return 'wikipedia function'

def pretend_news():
    return 'news function'

def run_api_function(api):
    options = {
        # 'wikipedia':
        'wikipedia': pretend_wiki,
        'news': pretend_news
        # 'weather':
    }
    return options[api]()

def has_word(string, good_words):
    return len(difflib.get_close_matches(string, good_words, 1,
                                        DIFF_SENSITIVITY)) > 0

def get_response_text(body):
    # hierarchy of responses, help at the top
    words = body.lower().split()
    api_words = get_api_words()
    chosen_api = ''
    for api in api_words:
        for word in words:
            if has_word(word, api['words']):
                chosen_api = api['api']

    if not chosen_api:
        log.error('No api found from body')
        return 'Nothing chosen'

    log.debug('api found: %s' % chosen_api)
    ret_string = run_api_function(chosen_api)
    if ret_string:
        return ret_string

@app.route('/sms', methods=['POST'])
def sms_handler():
    body = request.form['Body']
    from_num = request.form['From']
    log.debug('Text from: %s says: (%s)' % (from_num, body))
    text = get_response_text(body)

    resp = MessagingResponse()
    resp.message(text)
    return str(resp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
