async function fetchFilter(url) {
  try {
    const response = await fetch(url);
    const text = await response.text();
    return text.split("\n")
      .map(line => line.trim())
      .filter(line => line && !line.startsWith("#"));
  } catch (err) {
    console.error("Arkas: Failed to fetch", url, err);
    return [];
  }
}

async function loadBlocklists() {
  return new Promise(resolve => {
    chrome.runtime.sendMessage({ type: "getFilters" }, async (response) => {
      if (!response || !response.urls) {
        console.error("Arkas: No filter URLs received");
        resolve([]);
        return;
      }
      const urls = response.urls;
      const allUsers = [];
      for (const url of urls) {
        const users = await fetchFilter(url);
        allUsers.push(...users);
      }
      console.log("Arkas: Active filters", urls);
      resolve(allUsers);
    });
  });
}

function applyRules(users) {
  users.forEach(entry => {
    let mode = "both";
    let user = entry;

    if (entry.endsWith(":c")) {
      mode = "c";
      user = entry.slice(0, -2);
    } else if (entry.endsWith(":d")) {
      mode = "d";
      user = entry.slice(0, -2);
    }

    if (mode !== "d") {
      document.querySelectorAll(`.Comment .Username[href="/profile/${user}"]`)
        .forEach(el => el.closest(".Comment")?.remove());
    }
    if (mode !== "c") {
      document.querySelectorAll(`.ItemDiscussion .DiscussionAuthor a[href="/profile/${user}"]`)
        .forEach(el => el.closest(".ItemDiscussion")?.remove());
    }
  });
}

function startObserver(users) {
  const observer = new MutationObserver(() => {
    applyRules(users);
  });

  const tryObserve = () => {
    if (document.body) {
      observer.observe(document.body, { childList: true, subtree: true });
      applyRules(users); // run once immediately
    } else {
      requestAnimationFrame(tryObserve);
    }
  };

  tryObserve();
}

(async () => {
  const users = await loadBlocklists();
  startObserver(users);
})();