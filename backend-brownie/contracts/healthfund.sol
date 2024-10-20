// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MedicalCrowdfunding {
    address public owner;

    struct Hospital {
        string name;
        address hospitalAddress;
        string email;
        bool isApproved;
    }

    struct Campaign {
        string patientName;
        string description;
        uint goalAmount;
        uint currentAmount;
        address payable creator;
        address hospital;
        bool approved;
        bool fundsReleased;
        bool closed;
    }

    mapping(address => Hospital) public hospitals;  // Stores hospitals by address
    address[] public hospitalAddresses;  // Track all hospital addresses

    mapping(uint => Campaign) public campaigns;  // Stores campaigns by ID
    uint public campaignCount;  // Campaign counter

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the contract owner can perform this action.");
        _;
    }

    event HospitalAdded(string name, address hospitalAddress, string email);
    event CampaignCreated(uint campaignId, string patientName, address creator, address hospital);
    event CampaignApproved(uint campaignId);
    event DonationReceived(uint campaignId, address donor, uint amount);
    event FundsReleased(uint campaignId, address hospital, uint amount);
    event CampaignClosed(uint campaignId);

    constructor() {
        owner = msg.sender;  // Set the contract deployer as the owner
    }

    // Add a new hospital (only the owner can call this function)
    function addHospital(
        string memory _name,
        address _hospitalAddress,
        string memory _email
    ) public onlyOwner {
        require(_hospitalAddress != address(0), "Invalid hospital address.");
        require(!hospitals[_hospitalAddress].isApproved, "Hospital already exists.");

        hospitals[_hospitalAddress] = Hospital(_name, _hospitalAddress, _email, true);
        hospitalAddresses.push(_hospitalAddress);  // Store hospital address

        emit HospitalAdded(_name, _hospitalAddress, _email);
    }

    // Get the total number of hospitals
    function getHospitalCount() public view returns (uint) {
        return hospitalAddresses.length;
    }

    // Get the address of a hospital by its index in the array
    function getHospitalAddress(uint index) public view returns (address) {
        require(index < hospitalAddresses.length, "Invalid index.");
        return hospitalAddresses[index];
    }

    // Create a new campaign linked to a specific hospital
    function createCampaign(
        string memory _patientName,
        string memory _description,
        uint _goalAmount,
        address _hospital
    ) public {
        require(hospitals[_hospital].isApproved, "Invalid hospital.");

        campaignCount++;
        campaigns[campaignCount] = Campaign(
            _patientName,
            _description,
            _goalAmount,
            0,
            payable(msg.sender),
            _hospital,
            false,
            false,
            false
        );

        emit CampaignCreated(campaignCount, _patientName, msg.sender, _hospital);
    }

    // Approve the campaign (only the assigned hospital can approve it)
    function approveCampaign(uint _campaignId) public {
        Campaign storage campaign = campaigns[_campaignId];
        require(campaign.hospital == msg.sender, "Only the assigned hospital can approve this campaign.");
        require(!campaign.approved, "Campaign is already approved.");
        require(!campaign.closed, "Campaign is closed.");

        campaign.approved = true;
        emit CampaignApproved(_campaignId);
    }

    // Donate to a campaign (anyone can donate)
    function donate(uint _campaignId) public payable {
        Campaign storage campaign = campaigns[_campaignId];
        require(campaign.approved, "Campaign is not approved.");
        require(msg.value > 0, "Donation amount must be greater than zero.");
        require(!campaign.fundsReleased, "Funds already released.");
        require(!campaign.closed, "Campaign is closed.");

        campaign.currentAmount += msg.value;
        emit DonationReceived(_campaignId, msg.sender, msg.value);

        // Automatically release funds and close the campaign if the goal is reached
        if (campaign.currentAmount >= campaign.goalAmount) {
            releaseFunds(_campaignId);
            closeCampaign(_campaignId);
        }
    }

    // Release funds to the hospital automatically once the goal is reached
    function releaseFunds(uint _campaignId) internal {
        Campaign storage campaign = campaigns[_campaignId];
        require(campaign.currentAmount >= campaign.goalAmount, "Funding goal not reached.");
        require(!campaign.fundsReleased, "Funds already released.");

        campaign.fundsReleased = true;  // Mark funds as released

        uint amount = campaign.currentAmount;
        campaign.currentAmount = 0;  // Reset the campaign's current amount

        payable(campaign.hospital).transfer(amount);  // Transfer the funds to the hospital

        emit FundsReleased(_campaignId, campaign.hospital, amount);
    }

    // Mark a campaign as closed
    function closeCampaign(uint _campaignId) internal {
        Campaign storage campaign = campaigns[_campaignId];
        require(!campaign.closed, "Campaign is already closed.");

        campaign.closed = true;  // Mark the campaign as closed
        emit CampaignClosed(_campaignId);
    }
}
