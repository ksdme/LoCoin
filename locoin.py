"""
	@author ksdme
	the locoin server executer
"""
from txns import *
from wallet import *
from base64 import b64decode
from flask_cors import CORS
from flask import Flask, jsonify

# obviously
app = Flask(__name__)
CORS(app)

# new endpoints
@app.route("/new/identity/<int:name>")
def newIdentity(name):
	identity = Identity.new()
	Identity.saveWallet(identity, str(name))

	return jsonify({
		"pk": Identity.getPublicKey(identity) })

# wallet identity
@app.route("/new/wallet/<int:name>")
def newWallet(name):
	wallet = Wallet.new()
	Wallet.saveWallet(wallet, str(name))

	return jsonify({
		"pk": Wallet.getPublicKey(wallet) })

# simply add lotxn
@app.route("/txn/identity/<pubkey>/<location>/<int:difficulty>")
def makeLocationUpdate(pubkey, location, difficulty):
	location = str(location) + "="*(len(location)%4)
	location = b64decode(location)

	return jsonify(LoTxn(location, difficulty, pubkey).raw)

if __name__ == "__main__":
	app.run()
