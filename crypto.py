import flask
import sqlite3
import secrets
from eth_account import Account
from collections import defaultdict
# from brownie import accounts, SimpleCollectible
walletsDB = defaultdict(lambda:"")

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route("/nft_post", methods=['POST', 'GET'])
def nft_post():
    user_id = flask.request.args['userid']
    
@app.route('/wallet_get', methods=['GET'])
def wallet_add():
    user_id = flask.request.args['userid']
    pkey = walletsDB[user_id]
    if pkey == "":
        return flask.jsonify(error="Error: No user id exists.")
    account = Account.from_key(pkey)

    return flask.jsonify(private_key=pkey, account=account.address)


@app.route('/wallet', methods=['POST', 'GET'])
def wallet():
    user_id = flask.request.args['userid']
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    account = Account.from_key(private_key)
    walletsDB[user_id] = private_key
    return flask.jsonify(private_key=private_key, account=account.address)

@app.route('/', methods=['GET'])
def home():
    return flask.jsonify(input="Hello World")


app.run()