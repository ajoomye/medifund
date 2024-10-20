from brownie import MedicalCrowdfunding, accounts, network, config
#from scripts.helpful_scripts import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS

def donate():
    crowdfunding = MedicalCrowdfunding[-1]  # Get the latest deployed instance
    print(f"Contract address: {crowdfunding.address}")

    tx = crowdfunding.donate(1, {"from": accounts[3], "value": 5 * 10**17})  # Donate 0.5 ETH
    tx.wait(1)
    print(f"Donation Received: {tx.events['DonationReceived']}")

def main():
    donate()