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

w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/068039844ea54f41a84e0e4550a72819"))
chain_id = 4
OPENSEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"
contractAddress = "0xECE0b56D4cbCaE1a1225C69fBB6254BAD78945Db"
NFTFactory = w3.eth.contract(address=contractAddress, abi=abi)

sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
dev_private_key = "0x0e10373c761cbe50eafe9798cb8df4ed9edeb13c1396684daa0f8eefd6022abc"
dev = Account.from_key(dev_private_key).address
print("Dev address {}".format(dev))
# # from brownie import accounts, SimpleCollectible
walletsDB = defaultdict(lambda:"")

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route("/nft_art", methods=['POST'])
def craft_nft_art():
    pass

@app.route("/nft_post", methods=['POST', 'GET'])
def nft_post():
    user_id = flask.request.args['userid']
    # token_id = NFTFactory.functions.tokenCounter().call()
    # print(token_id)
    pkey = walletsDB[user_id]
    addressOfNewUser = Account.from_key(pkey).address
    os.system("cd nft; brownie run scripts/simple_collectible/create_collectible.py create {} --network rinkeby".format(addressOfNewUser))
    return flask.jsonify(status=200)
    # addressOfUser = Account.from_key(pkey)
    
    # print("address of user {}".format(addressOfUser))
    # nonce = w3.eth.getTransactionCount(dev)
    # greeting_transaction = NFTFactory.functions.createCollectible(addressOfUser.address, sample_token_uri).buildTransaction(
    #     {
    #         "chainId": chain_id,
    #         "gasPrice": w3.eth.gas_price,
    #         "from": dev,
    #         "nonce": nonce + 1,
    #     }
    # )
    # signed_greeting_txn = w3.eth.account.sign_transaction(
    #     greeting_transaction, private_key=dev_private_key
    # )
    # tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
    # print(tx_greeting_hash)
    # print("Generating NFT...")
    # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
    # print(tx_receipt)
    # print(
    #         "Awesome! You can view your NFT at {}".format(
    #             OPENSEA_FORMAT.format(simple_collectible.address, token_id)
    #         )
    #     )
    
# @app.route('/wallet_get', methods=['GET'])
# def wallet_add():
#     user_id = flask.request.args['userid']
#     pkey = walletsDB[user_id]
#     if pkey == "":
#         return flask.jsonify(error="Error: No user id exists.")
#     account = Account.from_key(pkey)

#     return flask.jsonify(private_key=pkey, account=account.address)


@app.route('/wallet', methods=['POST', 'GET'])
def wallet():
    print(flask.request.data)
    user_id = flask.request.get_json()['user_id']
    if walletsDB[user_id] != "":
        pkey = walletsDB[user_id]
        account = Account.from_key(pkey)
        return flask.jsonify(private_key=pkey, account=account.address)
    print("Creating new account/private key for {}".format(user_id))
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    account = Account.from_key(private_key)
    walletsDB[user_id] = private_key
    return flask.jsonify(private_key=private_key, account=account.address)

@app.route('/', methods=['GET'])
def home():
    return flask.jsonify(input="Hello World")


app.run()