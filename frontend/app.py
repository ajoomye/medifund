#!/usr/bin/env python3

from flask import Flask, render_template, request, jsonify, session, redirect
from web3 import Web3
import json
import os
from config import CONTRACT_ADDRESS, NETWORK

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize Web3 and connect to the local Ganache network
web3 = Web3(Web3.HTTPProvider(NETWORK))

# Load the contract ABI
with open('abi/MedicalCrowdfunding.json') as f:
    contract_abi = json.load(f)['abi']

contract_abi_json = json.dumps(contract_abi)

# Initialize the contract
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)


# Home route
@app.route('/')
def index():
    # Load the contract ABI
    with open('abi/MedicalCrowdfunding.json') as f:
        contract_abi = json.load(f)['abi']

    return render_template('index.html', contract_address=CONTRACT_ADDRESS, contract_abi=contract_abi_json)


# Route for campaigns
@app.route('/campaigns')
def campaigns():
    try:
        campaign_count = contract.functions.campaignCount().call()
        campaigns = []
        for i in range(1, campaign_count + 1):
            campaign = contract.functions.campaigns(i).call()
            campaigns.append({
                'id': i,
                'patient_name': campaign[0],
                'description': campaign[1],
                'goal_amount': web3.from_wei(campaign[2], 'ether'),
                'current_amount': web3.from_wei(campaign[3], 'ether')
            })
        return render_template('campaigns.html', campaigns=campaigns, contract_address=CONTRACT_ADDRESS, contract_abi=contract_abi_json)
    except Exception as e:
        print(f"Error fetching campaigns: {e}")
        return render_template('error.html', message="Error fetching campaigns")




# MetaMask wallet connection route
@app.route('/connect_wallet', methods=['POST'])
def connect_wallet():
    try:
        data = request.get_json()
        session['wallet_address'] = data['wallet_address']
        return jsonify({'message': 'Wallet connected successfully'}), 200
    except Exception as e:
        print(f"Error connecting wallet: {e}")
        return jsonify({'message': 'Failed to connect wallet'}), 500


# Hospital Management route
@app.route('/hospital-management')
def hospital_management():
    
    # Load the contract ABI
    with open('abi/MedicalCrowdfunding.json') as f:
        contract_abi = json.load(f)['abi']

    return render_template('hospital_management.html', contract_address=CONTRACT_ADDRESS, contract_abi=contract_abi_json, owner_address="0xcbdc15ad58a24723e7764be613BF28cacC3A66D6")


# Approve Campaigns route
@app.route('/approve-campaigns')
def approve_campaigns():
    # Load the contract ABI
    with open('abi/MedicalCrowdfunding.json') as f:
        contract_abi = json.load(f)['abi']

    return render_template('approve_campaigns.html', contract_address=CONTRACT_ADDRESS, contract_abi=contract_abi_json)


if __name__ == '__main__':
    app.run(debug=True)
