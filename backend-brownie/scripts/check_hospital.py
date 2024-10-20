from brownie import MedicalCrowdfunding, accounts, network, config
#from scripts.helpful_scripts import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def check_hospital():
    crowdfunding = MedicalCrowdfunding[-1]  
    print(f"Contract address: {crowdfunding.address}")

    # Get the total number of hospitals
    hospital_count = crowdfunding.getHospitalCount()
    print(f"Total Hospitals: {hospital_count}")

    # Loop through all hospital addresses and print their details
    for i in range(hospital_count):
        hospital_address = crowdfunding.getHospitalAddress(i)
        hospital_data = crowdfunding.hospitals(hospital_address)

        print(f"\nHospital Details for {hospital_address}:")
        print(f"  Name: {hospital_data[0]}")
        print(f"  Address: {hospital_data[1]}")
        print(f"  Email: {hospital_data[2]}")
        print(f"  Approved: {hospital_data[3]}")


def main():
    check_hospital()