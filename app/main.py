from flask import Flask, render_template, request

app = Flask(__name__)

#def send_text(body, to_num, from_num):
#    client = Client(config.ACCOUNT_SID, config.AUTH_TOKEN)
#    message = client.api.account.messages.create(to=to_num,
#						from_=from_num,
#						body=body)

@app.route('/sms')
def sms_handler():
   return "Hello from sms"
 
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
