import flask
import secrets
import json
import os
from eth_account import Account
from collections import defaultdict
from web3 import Web3

compiled = {}
with open('nft/build/contracts/SimpleCollectible.json') as f:
    data = f.read()
    compiled = json.loads(data)
# get bytecode
bytecode = compiled["bytecode"]
# get abi
abi = compiled["abi"]

w3 = Web3(Web3.HTTPProvider(os.getenv("https://rinkeby.infura.io/v3/068039844ea54f41a84e0e4550a72819")))
chain_id = 4
#
# # For connecting to ganache
# w3 = Web3(Web3.HTTPProvider("http://0.0.0.0:8545"))
# chain_id = 1337
# my_address = "0xdbB4A708755dfD59f9c4b100B2BE23a6d2EB7D57"
# private_key = "ffdd7a010ab8c089d95a9c2ff24e75b21744b5db26c3cd66d14f8e91c46afcc4"

# # Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# # Get the latest transaction
# nonce = w3.eth.getTransactionCount(my_address)
# # Submit the transaction that deploys the contract
# transaction = SimpleStorage.constructor().buildTransaction(
#     {
#         "chainId": chain_id,
#         "gasPrice": w3.eth.gas_price,
#         "from": my_address,
#         "nonce": nonce,
#     }
# )
# # Sign the transaction
# signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# print("Deploying Contract!")
# # Send it!
# tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# # Wait for the transaction to be mined, and get the transaction receipt
# print("Waiting for transaction to finish...")
# tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
# print(f"Done! Contract deployed to {tx_receipt.contractAddress}")


# # Working with deployed Contracts
# simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# print(f"Initial Stored Value {simple_storage.functions.retrieve().call()}")
# greeting_transaction = simple_storage.functions.store(15).buildTransaction(
#     {
#         "chainId": chain_id,
#         "gasPrice": w3.eth.gas_price,
#         "from": my_address,
#         "nonce": nonce + 1,
#     }
# )
# signed_greeting_txn = w3.eth.account.sign_transaction(
#     greeting_transaction, private_key=private_key
# )
# tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
# print("Updating stored Value...")
# tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)

# print(simple_storage.functions.retrieve().call())
# # from brownie import accounts, SimpleCollectible
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