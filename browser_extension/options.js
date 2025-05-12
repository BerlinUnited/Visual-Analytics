document.addEventListener('DOMContentLoaded', () => {
  // Load saved settings
  chrome.storage.sync.get(['apiToken', 'amount'], (data) => {
    document.getElementById('apiToken').value = data.apiToken || '';
    document.getElementById('amount').value = data.amount || '';
  });

  // Save settings
  document.getElementById('save').addEventListener('click', () => {
    const apiToken = document.getElementById('apiToken').value.trim();
    const amount = document.getElementById('amount').value.trim();
    chrome.storage.sync.set({ apiToken, amount }, () => {
      const status = document.getElementById('status');
      status.textContent = 'Settings saved!';
      setTimeout(() => status.textContent = '', 2000);
    });
  });
});