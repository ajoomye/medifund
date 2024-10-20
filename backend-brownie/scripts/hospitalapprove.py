from brownie import MedicalCrowdfunding, accounts, network, config
#from scripts.helpful_scripts import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS

def approve():
    crowdfunding = MedicalCrowdfunding[-1]
    print(f"Contract address: {crowdfunding.address}")

    # Define the campaign ID to approve
    campaign_id = 1  # Change this value as needed

    # Fetch the campaign details to ensure the correct hospital is used
    campaign = crowdfunding.campaigns(campaign_id)
    hospital_address = campaign[5]  # The hospital assigned to the campaign

    print(f"Approving Campaign ID: {campaign_id}")
    print(f"Assigned Hospital Address: {hospital_address}")

    # Use the assigned hospital's account to approve the campaign
    tx = crowdfunding.approveCampaign(campaign_id, {"from": hospital_address})
    tx.wait(1)  # Wait for the transaction to complete

    # Display the event details
    event = tx.events["CampaignApproved"]
    print(f"Campaign Approved: ID {event['campaignId']}")

def main():
    approve()