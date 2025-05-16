document.addEventListener('DOMContentLoaded', () => {
  // Load saved settings and display it when loading the options page
  chrome.storage.sync.get(['apiToken', 'amount'], (data) => {
    document.getElementById('apiToken').value = data.apiToken || '';
    document.getElementById('amount').value = data.amount || 2;
    document.getElementById('className').value = data.className || 'ball';
  });

  // Save settings in chrome extension storage
  document.getElementById('save').addEventListener('click', () => {
    const apiToken = document.getElementById('apiToken').value.trim();
    const amount = document.getElementById('amount').value.trim();
    const className = document.getElementById('className').value.trim();

    chrome.storage.sync.set({ apiToken, amount, className }, () => {
      const status = document.getElementById('status');
      status.textContent = 'Settings saved!';
      setTimeout(() => status.textContent = '', 2000);
    });
  });
});