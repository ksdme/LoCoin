"""
	@author ksdme
	the locoin server executer
"""
from wallet import *
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

if __name__ == "__main__":
	app.run()
