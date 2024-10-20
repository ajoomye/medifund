from brownie import MedicalCrowdfunding, accounts, network, config
#from scripts.helpful_scripts import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS

def addhospital():
    # Replace with your deployed contract address and owner account
    owner = accounts[0]  # Use the first Ganache account (owner)
    contract = MedicalCrowdfunding[-1]  # Get the latest deployed contract instance

    # Define hospital data to add
    hospitals = [
        {"name": "General Hospital", "address": accounts[1], "email": "contact@generalhospital.com"},
        {"name": "City Clinic", "address": accounts[2], "email": "info@cityclinic.com"},
    ]

    # Add hospitals
    for hospital in hospitals:
        tx = contract.addHospital(
            hospital["name"],
            hospital["address"],
            hospital["email"],
            {"from": owner}
        )
        tx.wait(1)  # Wait for the transaction to confirm
        print(f"Added hospital: {hospital['name']} at {hospital['address']}")

def main():
    addhospital()