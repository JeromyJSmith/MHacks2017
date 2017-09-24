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

def dummy_func():
    pass

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

class User(object):

    """
    Mock of database for quicker hackathon app creation.
    Dictionary holds account information.
    """
    database = {
		'admin': {'username': 'admin', 'password': 'password', 'is_active': True, 'get_id': dummy_func },
		'austin': {'username': 'austin', 'password': 'meyer24', 'is_active': True}
    }



    def __init__(self, username, password, id):
        self.id = id
        self.username = username
        self.password = password

    def is_authenticated(self):
        pass

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    @classmethod
    def get(cls, id):
        log.debug('classmethod: %s' % (id))
        log.debug(cls.database)
        try:
            log.debug(cls.database[id])
            return cls.database[id]
        except KeyError:
            return None

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
    try:
        return User.get(id)
    except KeyError:
        return None

@app.before_request
def before_request():
    g.user = current_user
    # session['admin'] = User('admin', 'password', 'admin')
    #log.debug('made: %s' % (g.users['admin']))


@app.route('/user/<username>')
@login_required
def user(username):
    print('in user function')
    if username != g.user.id:
        return '<h1>You are not authorized to access that page</h1>'
    return render_template('account.html',
                            username=username)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        log.debug('test')
        return render_template('login.html')
    json = request.get_json()
    log.debug('login json: %s' %(json))
    username = json['username']
    password = json['password']
    user = User.get(username)
    if not user:
        log.error('No user found with username: %s' % (username))
        return 'Fail', 401
    log.debug('usr: %s' % user)
    d = AttrDict()
    d.update(user)
    login_user(d)
    log.debug('Logged in %s' %(user))
    return redirect(request.args.get('next') or url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8000)
