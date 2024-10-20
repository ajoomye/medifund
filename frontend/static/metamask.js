let web3;
let selectedAccount;

// Function to connect the wallet
async function connectWallet() {
  if (typeof window.ethereum !== 'undefined') {
    try {
      // Request account access from MetaMask
      const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
      selectedAccount = accounts[0];
      console.log('Connected account:', selectedAccount);

      // Store the connected wallet address in sessionStorage
      sessionStorage.setItem('connectedWallet', selectedAccount);

      // Initialize Web3 instance
      web3 = new Web3(window.ethereum);

      // Display the connected wallet address in the button
      document.getElementById('connect-wallet').textContent =
        `Connected: ${selectedAccount.substring(0, 6)}...${selectedAccount.substring(38)}`;

      // Send the connected wallet address to Flask back-end
      await fetch('/connect_wallet', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ wallet_address: selectedAccount })
      });
    } catch (error) {
      console.error('Error connecting to MetaMask', error);
      alert('Failed to connect to MetaMask');
    }
  } else {
    console.log('MetaMask is not installed');
    alert('Please install MetaMask!');
  }
}

// Function to check if the wallet is already connected on page load
function checkWalletConnection() {
  const storedWallet = sessionStorage.getItem('connectedWallet');
  if (storedWallet) {
    selectedAccount = storedWallet;
    console.log('Wallet already connected:', selectedAccount);

    // Initialize Web3 instance
    web3 = new Web3(window.ethereum);

    // Display the connected wallet address in the button
    document.getElementById('connect-wallet').textContent =
      `Connected: ${selectedAccount.substring(0, 6)}...${selectedAccount.substring(38)}`;
  }
}

// Call the checkWalletConnection function on page load
document.addEventListener('DOMContentLoaded', function() {
  checkWalletConnection();  // Check if the wallet is already connected when the page loads

  // Add event listener for the connect button
  document.getElementById('connect-wallet').addEventListener('click', connectWallet);
});
