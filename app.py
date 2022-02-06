import flask
import sqlite3
from eth_account import Account
import secrets
conn = sqlite3.connect('tmp.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS Wallets
              (UserID VARCHAR(126), PrivateKey TEXT)''')
conn.commit()
conn.close()
app = flask.Flask(__name__)
app.config["DEBUG"] = True




@app.route('/wallet', methods=['POST', 'GET'])
def wallet():
    user_id = flask.request.args['userid']
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    account = Account.from_key(private_key)
    return flask.jsonify(private_key=private_key, account=account.address)

@app.route('/', methods=['GET'])
def home():
    return flask.jsonify(input="Hello World")

app.run()