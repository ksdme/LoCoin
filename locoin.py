"""
	@author ksdme
	the locoin server executer
"""
from txns import *
from wallet import *
from base64 import b64decode
from flask import Flask, jsonify

# obviously
app = Flask(__name__)

# new endpoints
@app.route("/new/identity")
def newIdentity():
	return jsonify(Identity.new())

# wallet identity
@app.route("/new/wallet")
def newWallet():
	return jsonify(Wallet.new())

# simply add lotxn
@app.route("/txn/identity/<pubkey>/<location>/<int:difficulty>")
def makeLocationUpdate(pubkey, location, difficulty):
	location = str(location) + "="*(len(location)%4)
	location = b64decode(location)

	return jsonify(LoTxn(location, difficulty, pubkey).raw)

if __name__ == "__main__":
	app.run()
