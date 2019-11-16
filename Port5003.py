# -*- coding: utf-8 -*-

#####

#Importing libraries
import datetime  # each block will need a timestap
import hashlib # To allow hashing the blocks
import json # To encode before hashing 
from flask import Flask, jsonify, request, send_file# To make object of the Flask class, jsonify allows to interact with postman, request gets blockchain data
import requests
from uuid import uuid4  # will generate a unique web address
from urllib.parse import urlparse

# Part 1 : Building the blockchain
# This class will create a blockchain
class Blockchain:
    def __init__(self):
        self.chain = []
        self.data = []
        self.create_block(proof = 1, previous_hash = '0') # 0 in '' because hashlib (SHA256) library only reads encoded strings
        self.nodes = set()
    
    # Create a new block - A new block has 4 keys and values
    def create_block(self, proof, previous_hash):
        block = {'index' : len(self.chain) + 1,
                 'timestamp' : str(datetime.datetime.now()),
                 'proof' : proof,
                 'previous_hash': previous_hash,
                 'data': self.data}
        self.data = []
        self.chain.append(block)
        return block
    
    # This method gets the previous block from the blockchain
    def get_previous_block(self):
        return self.chain[-1]
    
    # Proof of Work - hard to find, easy to verify
    def proof_of_work(self, previous_proof):
        new_proof = 1 # Initializing to 1 beacuse, to slove the problem for each itteration of while loop
        check_proof = False
        
        #while loop continues until the correct proof is met
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    # this method gives the hash of the current block
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        
        while block_index < len(chain):
            block = chain[block_index]
            
            #Checking the previous block is same as the hash
            if block['previous_hash'] != self.hash(previous_block):
                return False
            
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation [:4] != '0000':
                return False
            
            previous_block = block
            block_index += 1
        return True
    
    def add_record(self, bank, branch, date, account_number, account_holder_name, account_type,file_name):
        self.data.append({'bank': hashlib.sha256(bank).hexdigest(),
                          'branch': branch,
                          'date': date,
                           'account_number': account_number,
                           'account_holder_name': account_holder_name,
                           'account_type': account_type,
                           'file_name': file_name})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
    
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
    
    # The consensus to change to the longest chain
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length_of_chain']
                chain = response.json() ['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
        
        
# Part 2 - Mining the blockchain
# Creating a webapp in Flask
app = Flask(__name__)

# Creating an address for the node on Port 5000
node_address = str(uuid4()).replace('-', '')

# Creating a blockchain
blockchain = Blockchain() # instance of the class Blockchain

# Mining a new block
@app.route('/mine_block', methods = ['GET']) #flask commands
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    
    response = {'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'current_hash' : blockchain.hash(block),
                'previous_hash': block['previous_hash'],
                'data': block['data']}
    
    return jsonify(response), 200

# Getting the full blockchain
@app.route('/get_chain', methods = ['GET']) # flask commands
def get_chain():
    response = {'chain': blockchain.chain,
                'length_of_chain': len(blockchain.chain)}
    return jsonify(response), 200

# Checking if the blockchain is valid
@app.route('/is_valid', methods = ['GET']) # flask commands
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'Message': 'Valid Chain. All blocks are valid.'}
    else:
        response = {'Message': 'Not a Valid Chain. Alert!'}
    
    return jsonify(response), 200

# Adding a new trasaction to the blockchain
@app.route('/add_record', methods=['POST'])
def add_record():
    json = request.get_json(force=True)
    transaction_keys = ['bank', 'branch', 'date', 'account_number', 'account_holder_name', 'account_type','file_name']
    if not all (key in json for key in transaction_keys):
        return 'Some elements of te transaction are missing', 400
    index = blockchain.add_record (json['bank'],json['branch'], json['date'], json['account_number'], json['account_holder_name'], json['account_type'], json['file_name'])
    response = {'Message': f'This transaction will be added to Block {index}'}
    return jsonify(response), 201
    

# Part 3 - Decentralizing our Blockchain
# Connecting new nodes
@app.route('/connect_node', methods=['POST'])  
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return 'No Node', 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'Message': 'All the Nodes are now connected. The Unoone Blockchain now containts the following nodes.',
                'Total_nodes' : list(blockchain.nodes)}
    return jsonify(response), 201
    
# Replacing the chain by the longest chain if needed
@app.route('/replace_chain', methods = ['GET']) # flask commands
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'Message': 'The Nodes had difference chains so the chain was replaced by the longest chain',
                    'new_chain': blockchain.chain}
    else:
        response = {'Message': 'All good. Change is a longest one',
                    'Actual_chain': blockchain.chain}
    return jsonify(response), 200


def process_file(file_to_send):
    output = file_to_send
    return send_file(output)

@app.route('/get_files', methods=["POST"])
def file_handler():
    if request.method == "POST":
        response = request.get_json(force=True)
        return jsonify(response), 200
    

#Running the flask app
app.config['JSON_AS_ASCII'] = False
app.run(host='0.0.0.0', port = 5003) #Use "http://127.0.0.1:5001/get_chain" in postman to see the blockchain       