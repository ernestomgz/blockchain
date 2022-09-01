# For timestamp
import datetime
 
import hashlib
import json
from textwrap import dedent
from uuid import uuid4

from flask import Flask, jsonify, request

 
# Flask is for creating the web
# app and jsonify is for
# displaying the blockchain
from flask import Flask, jsonify, request
 
 
class Blockchain:
   
    # This function is created
    # to create the very first
    # block and set its hash to "0"
    def __init__(self):
        self.chain = []
        
        self.current_transactions = []
        self.create_block(previous_hash='0',proof=1)
 
    # This function is created
    # to add further blocks
    # into the chain
    def create_block(self,  previous_hash, proof):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'trasctions':self.current_transactions,
                 'proof': proof,
                 'previous_hash': previous_hash}
        #reset transaction list
        self.current_transactions = []

        #add the block to the chain
        self.chain.append(block)
        return block



    def new_transaction(self, sender, recipient, amount):

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1



    # This function is created
    # to display the previous block
    def print_previous_block(self):
        return self.chain[-1]
       
    # This is the function for proof of work
    # and used to successfully mine the block
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
         
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[-4:] == '4242':
                check_proof = True
            else:
                new_proof += 1
                 
        return new_proof
 
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
 
    def chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
         
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
               
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(proof**2 - previous_proof**2).encode()).hexdigest()
             
            if hash_operation[-4:] != '4242':
                return False
            previous_block = block
            block_index += 1
         
        return True
 
 
# Creating the Web
# App using flask
app = Flask(__name__)
 
# Create the object
# of the class blockchain
blockchain = Blockchain()
 
# Mining a new block
@app.route('/mine', methods=['GET'])
def mine_block():
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
     
    response = {'message': 'A block is MINED',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
     
    return jsonify(response), 200
 
# Display blockchain in json format
@app.route('/chain', methods=['GET'])
def display_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200
 
# Check validity of blockchain
@app.route('/valid', methods=['GET'])
def valid():
    valid = blockchain.chain_valid(blockchain.chain)
     
    if valid:
        response = {'message': 'The Blockchain is valid.'}
    else:
        response = {'message': 'The Blockchain is not valid.'}
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    # Check that the required fields are in the POST'ed data

    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return jsonify('Missing values'), 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201
 
# Run the flask server locally
app.run(host='127.0.0.1', port=5000)

