async function getApiToken() {
  return new Promise(resolve => {
    chrome.storage.sync.get(['apiToken'], (data) => {
      resolve(data.apiToken);
    });
  });
}

async function getClassName() {
  return new Promise(resolve => {
    chrome.storage.sync.get(['className'], (data) => {
      resolve(data.className);
    });
  });
}

async function getCamera() {
  return new Promise(resolve => {
    chrome.storage.sync.get(['camera'], (data) => {
      resolve(data.camera);
    });
  });
}

async function getAmount() {
  return new Promise(resolve => {
    chrome.storage.sync.get(['amount'], (data) => {
      resolve(data.amount);
    });
  });
}

const openTabsSequentially = async (links, delayMs = 1000) => {
  let successCount = 0;
  let errorCount = 0;

  for (const [index, link] of links.result.entries()) {
    try {
      await chrome.tabs.create({ url: link, active: false });
      successCount++;
      console.log(`Opened tab ${index + 1}/${links.result.length}: ${link}`);

      // Only delay if not the last tab
      if (index < links.result.length - 1) {
        await new Promise(resolve => setTimeout(resolve, delayMs));
      }
    } catch (error) {
      errorCount++;
      console.error(`Failed to open ${link}:`, error);
    }
  }

  console.log(`Finished: ${successCount} tabs opened, ${errorCount} failed`);
  return { successCount, errorCount };
};

chrome.action.onClicked.addListener(async () => {
  // entrypoint for the extension - is triggered when clicking the extension button
  try {
    const apiToken = await getApiToken();
    const amount = await getAmount();
    const className = await getClassName();
    const camera = await getCamera();
    const response = await fetch(`https://vat.berlin-united.com/api/annotation-task/?amount=${amount}&class_name=${className}&camera=${camera}`, {
      headers: { 'Authorization': `Token ${apiToken}` }
    });
    const links = await response.json();

    // Open tabs with delay between each - helps to not overwhelm the server and browser
    await openTabsSequentially(links, 800);

  } catch (error) {
    console.error('Failed to fetch links:', error);
  }
});

