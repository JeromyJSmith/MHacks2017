from flask import Flask, request, render_template
from twilio.twiml.messaging_response import Message, MessagingResponse
import logging as log
import text

app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def sms_handler():
    body = request.form['Body']
    from_num = request.form['From']
    log.debug('Text from: %s says: (%s)' % (from_num, body))
    new_body = text.get_response_text(body)

    resp = MessagingResponse()
    resp.message(new_body)
    return str(resp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8000)
