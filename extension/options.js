document.getElementById("saveBtn").addEventListener("click", () => {
  const extraUrl = document.getElementById("extraUrl").value.trim();
  const useDefault = document.getElementById("useDefault").checked;

  chrome.storage.sync.set({ extraFilter: extraUrl, useDefault });
});

// Load saved values when opening options
chrome.storage.sync.get(["extraFilter", "useDefault"], (data) => {
  if (data.extraFilter) {
    document.getElementById("extraUrl").value = data.extraFilter;
  }
  document.getElementById("useDefault").checked = data.useDefault !== false;
});