import config
from flask import Flask, render_template, request
from twilio.rest import Client
from twilio.twiml.messaging_response import Message, MessagingResponse

app = Flask(__name__)

def send_text(body, to_num, from_num):
    client = Client(config.ACCOUNT_SID, config.AUTH_TOKEN)
    message = client.api.account.messages.create(to=to_num,
						from_=from_num,
						body=body)

def get_response_text(body):
    return 'response text'

@app.route('/sms', methods=['POST'])
def sms_handler():
    # hierarchy of responses, help at the top
    body = request.form['Body']
    from_num = request.form['From']

    text = get_response_text(body)
    resp = MessagingResponse()
    resp.message(text)
    return str(resp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
