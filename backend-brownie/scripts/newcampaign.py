from brownie import MedicalCrowdfunding, accounts, network, config
#from scripts.helpful_scripts import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def newcampaign():
    crowdfunding = MedicalCrowdfunding[-1]
    print(f"Contract address: {crowdfunding.address}")

    # Use the first hospital's address for the campaign (assuming one is added)
    hospital_address = crowdfunding.getHospitalAddress(0)  # Fetch the first hospital address

    # Create a new campaign linked to the hospital
    tx = crowdfunding.createCampaign(
        "John Doe",  # Patient name
        "Heart surgery needed",  # Description
        10 ** 18,  # Goal amount in wei (1 ETH)
        hospital_address,  # Linked hospital address
        {"from": accounts[0]}  # Transaction sent from account[0]
    )
    tx.wait(1)  # Wait for the transaction to be mined

    # Display the campaign creation event details
    print(f"Campaign created: {tx.events['CampaignCreated']}")


def main():
    newcampaign()