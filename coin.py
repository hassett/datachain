import hashlib
import json
from time import time
from textwrap import dedent
from uuid import uuid4
from urllib.parse import urlparse
from flask import Flask, jsonify, request
import requests

class Block():

    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.users = {'jayhawk': 1000, 'alpha': 1000}
        self.usernames = ['jayhawk', 'alpha']

        # MUST CREATE GENESIS BLOCK!!
        self.new_block(proof = 0, previous_hash = 1)

    def new_block(self, proof, previous_hash = None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        self.current_transactions = []
        self.chain.append(block)

        return block

    def new_transaction(self, sender, recipient, amount):
        '''
        TODO:
            1. Check to make sure the sender has enough to cover the amount

        '''

        if self.valid_user(sender, recipient):
            sender_bal = self.users[sender]
        else:
            raise ValueError('User does not exist')
        if (sender_bal >= amount):
            self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
            })
            self.send(sender, recipient, amount)

            return self.last_block['index'] + 1
        else:
            raise ValueError("Sender does not have enough funds")

    def 

    def send(self, sender, recipient, amount):
        self.users[sender] -= amount
        self.users[recipient] += amount


    def get_balance(self, user):
        for indiv in self.users:
            balance = indiv[user]

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    def create_user(self, user, balance = 0):
        self.usernames.append(user)
        self.users[user] = balance
        return len(self.users)

    def clear_users(self):
        self.users = []

    def valid_user(self, sender, recipient):
        if(sender == recipient):
            return False
        count = 0
        for indiv in self.usernames:
            if(indiv == sender):
                count += 1
            if(indiv == recipient):
                count += 1

        return count == 2

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:6] == '730285'

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys = True).encode()
        block_hash = hashlib.sha256(block_string).hexdigest()
        return block_hash

    @property
    def last_block(self):
        return self.chain[-1]
#'''
app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

block = Block()

@app.route('/mine', methods = ['GET'])
def mine():
    last_block = block.last_block
    last_proof = last_block['proof']
    proof = block.proof_of_work(last_proof)

    previous_hash = block.hash(last_block)
    new_block = block.new_block(proof, previous_hash)

    response = {
    'message': "New Block Forged",
    'index': new_block['index'],
    'transactions': new_block['transactions'],
    'proof': new_block['proof'],
    'previous_hash': new_block['previous_hash'],
    }

    return jsonify(response), 200

@app.route('/new/transaction', methods = ['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    index = block.new_transaction(values['sender'], values['recipient'],
                                values['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/mine/send', methods = ['POST'])
def mine_send():
    _ = mine()
    values = request.get_json()
    required = ['username']

@app.route('/new/user', methods = ['POST'])
def new_user():
    values = request.get_json()

    required = ['username']
    if not all(k in values for k in required):
        return 'Missing values', 400

    index = block.create_user(values['username'])
    response = {'message': f'You are user #{index}'}

    return jsonify(response), 201

@app.route('/get/balance', methods = ['GET'])
def get_balance():
    response = {
        'balance': block.users
    }
    return jsonify(response), 200

@app.route('/chain', methods = ['GET'])
def full_chain():
    response = {
        'chain': block.chain,
        'length': len(block.chain)
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)
'''
block = Block()
block1 = block.new_block(proof = 100, previous_hash = 1)
print(block1)
print(block.hash(block1))
print(block.proof_of_work(last_proof = 100))
block.create_user(user = 'jackhassett', balance = 1000)
print(block.users)
print("Transaction #: {}".format(block.new_transaction(sender = 'jayhawk', recipient = 'alpha', amount = 500)))
print("Transaction #: {}".format(block.new_transaction(sender = 'alpha', recipient = 'jackhassett', amount = 250)))
print(block.current_transactions)
print(block.users)
block2 = block.new_block(proof = 10000, previous_hash = 2)
print(block2)
block.create_user(user = 'katehassett', balance = 1000)
print(print("Transaction #: {}".format(block.new_transaction(sender = 'jayhawk', recipient = 'alpha', amount = 500))))
print(block.current_transactions)
print(block.users)
#print("Transaction #: {}".format(block.new_transaction(sender = 'dude', recipient = 'jackhassett', amount = 500)))
'''
