from brownie import MedicalCrowdfunding, accounts, network, config
import sys

def donate(aaa):
    print(f"Argument received for donation: {aaa}")
    
    # Ensure that we are connected to the correct network
    active_network = network.show_active()
    print(f"Active network: {active_network}")
    
    # Get the latest deployed instance of MedicalCrowdfunding
    crowdfunding = MedicalCrowdfunding[-1]  
    print(f"Contract address: {crowdfunding.address}")

    # Example: Get campaign with ID 1
    campaign = crowdfunding.campaigns(1)  
    print(f"Campaign: {campaign}")
    
def main(aaa):
    # Check if we received enough arguments
    print(f"Inside main: {aaa}")
    donate(aaa)
