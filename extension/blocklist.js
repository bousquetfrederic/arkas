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
      const allEntries = [];
      for (const url of urls) {
        const entries = await fetchFilter(url);
        allEntries.push(...entries);
      }
      console.log("Arkas: Active filters", urls);
      resolve(allEntries);
    });
  });
}

function removeDiscussionById(id) {
  // Listing tiles: <li id="Discussion_<id>" class="ItemDiscussion ...">
  const tile = document.getElementById(`Discussion_${id}`);
  if (tile) {
    console.log(`Arkas: Removing listing tile Discussion_${id}`);
    tile.remove();
  }

  // Discussion page itself
  if (window.location.href.includes(`/discussion/${id}/`)) {
    document.querySelectorAll(".Discussion").forEach(el => {
      console.log(`Arkas: Removing discussion page content for ${id}`);
      el.remove();
    });
  }
}

function applyRules(entries) {
  entries.forEach(entry => {
    // --- Discussion ID filter ---
    if (entry.startsWith("$")) {
      const discussionId = entry.slice(1);
      if (/^\d+$/.test(discussionId)) {
        removeDiscussionById(discussionId);
      }
      return;
    }

    // --- User filter ---
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
      document.querySelectorAll(`.Comment .Username[href="/profile/${CSS.escape(user)}"]`)
        .forEach(el => el.closest(".Comment")?.remove());
    }
    if (mode !== "c") {
      document.querySelectorAll(`.ItemDiscussion .DiscussionAuthor a[href="/profile/${CSS.escape(user)}"]`)
        .forEach(el => el.closest(".ItemDiscussion")?.remove());
    }
  });
}

function startObserver(entries) {
  const observer = new MutationObserver(() => {
    applyRules(entries);
  });

  const tryObserve = () => {
    if (document.body) {
      observer.observe(document.body, { childList: true, subtree: true });
      applyRules(entries); // initial pass
    } else {
      requestAnimationFrame(tryObserve);
    }
  };

  tryObserve();
}

(async () => {
  const entries = await loadBlocklists();
  startObserver(entries);
})();