import flask
import sqlite3
import secrets
from eth_account import Account
# import eth_account

conn = sqlite3.connect('tmp.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS Wallets
              (UserID VARCHAR(126), PrivateKey TEXT)''')
conn.commit()
conn.close()
app = flask.Flask(__name__)
app.config["DEBUG"] = True



# @app.route('/wallet_get', methods=['GET'])
# def wallet_add():
#     user_id = flask.request.args['userid']
#     conn = sqlite3.connect('tmp.db')
#     cursor = conn.cursor()
#     pkey = cursor.execute("Select PrivateKey from Wallets where UserID = %s limit 1", user_id)
#     conn.commit()
#     conn.close()
#     account = Account.from_key(pkey)

#     return flask.jsonify(private_key=pkey, account=account.address)


@app.route('/wallet', methods=['POST', 'GET'])
def wallet():
    user_id = flask.request.args['userid']
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    account = Account.from_key(private_key)
    conn = sqlite3.connect('tmp.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Wallets (UserID, PrivateKey) VALUES (%s, %s)", user_id, private_key)
    conn.commit()
    conn.close()
    return flask.jsonify(private_key=private_key, account=account.address)

@app.route('/', methods=['GET'])
def home():
    return flask.jsonify(input="Hello World")


app.run()