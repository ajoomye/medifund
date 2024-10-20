from brownie import MedicalCrowdfunding, accounts, network

def deploy_contract():
    # Load the deployment account (Ensure your account is funded on Base Sepolia)
    if network.show_active() == "base-sepolia":
        deployer_account = accounts.load("MetaMaskD6")  # Ensure you have this account stored in Brownie
    else:
        deployer_account = accounts[0]  # Use default account for development networks

    # Deploy the MedicalCrowdfunding contract
    crowdfunding_contract = MedicalCrowdfunding.deploy(
        {"from": deployer_account}
    )

    print(f"Contract deployed at: {crowdfunding_contract.address}")
    return crowdfunding_contract

def main():
    # Set the network to Base Sepolia v3 and deploy the contract
    if network.show_active() != "base-sepolia":
        print("Please select the Base Sepolia network.")
    deploy_contract()
