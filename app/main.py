from flask import Flask, request, render_template, url_for, redirect, g, session
from flask_login import LoginManager
from flask_login import LoginManager, UserMixin, login_required
from flask_login import login_user, logout_user, current_user
from twilio.twiml.messaging_response import Message, MessagingResponse
import logging as log
import text

app = Flask(__name__)
app.config['SECRET_KEY'] = 'A super secret key yahhhh!!!'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    database = {
        'AustinMeyer': ('AustinMeyer', 'hunter47'),
        'Admin': ('Admin', 'password')
    }

    def __init__(self, username, password):
        self.id = username
        self.password = password

    @classmethod
    def get(cls, id):
        return cls.database.get(id)


@app.route('/sms', methods=['POST'])
def sms_handler():
    body = request.form['Body']
    from_num = request.form['From']
    log.debug('Text from: %s says: (%s)' % (from_num, body))
    new_body = text.get_response_text(body)

    resp = MessagingResponse()
    resp.message(new_body)
    return str(resp)


@login_manager.user_loader
def load_user(id):
    return User.get(id)

@app.before_request
def before_request():
    g.user = current_user

@app.route('/user/<username>')
@login_required
def user(username):
    print('in user function')
    if username != g.user.id:
        return '<h1>You are not authorized to access that page</h1>'
    return '<h1>%s</h1>' % (username)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    user = User.get(username)
    if not user:
        log.error('No user found with username: %s' % (username))
        return redirect(url_for('login'))
    login_user(user)
    return redirect(request.args.get('next') or url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8000)
