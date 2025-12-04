chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "getFilters") {
    chrome.storage.sync.get(["extraFilter", "useDefault"], (data) => {
      const urls = [];
      if (data.useDefault !== false) {
        // Default filter is active unless explicitly disabled
        urls.push("https://arkas.quest/post_your_invoice_number.txt");
      }
      if (data.extraFilter) {
        urls.push(data.extraFilter);
      }
      sendResponse({ urls });
    });
    return true; // keep channel open for async sendResponse
  }
});