/**
 * Real-time refresh for leaderboard and winner list
 * Refreshes the page every 30 seconds to show updated scores
 */

(function () {
  // Only run on public pages (leaderboard and winner list)
  const isPublicPage =
    window.location.pathname === "/leaderboard" ||
    window.location.pathname === "/events" ||
    window.location.pathname === "/";

  if (!isPublicPage) {
    return;
  }

  // Refresh interval in milliseconds (30 seconds)
  const REFRESH_INTERVAL = 30000;

  // Store scroll position before refresh
  function saveScrollPosition() {
    sessionStorage.setItem("scrollPosition", window.scrollY);
  }

  // Restore scroll position after refresh
  function restoreScrollPosition() {
    const scrollPosition = sessionStorage.getItem("scrollPosition");
    if (scrollPosition) {
      window.scrollTo(0, parseInt(scrollPosition));
      sessionStorage.removeItem("scrollPosition");
    }
  }

  // Restore scroll position on page load
  window.addEventListener("load", restoreScrollPosition);

  // Set up auto-refresh
  setInterval(function () {
    saveScrollPosition();
    window.location.reload();
  }, REFRESH_INTERVAL);

  // Add visual indicator that auto-refresh is active
  function addRefreshIndicator() {
    const indicator = document.createElement("div");
    indicator.id = "refresh-indicator";
    indicator.innerHTML = "🔄 Auto-updating every 30s";
    indicator.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            color: rgba(255, 255, 255, 0.9);
            padding: 0.5rem 1rem;
            border-radius: 12px;
            font-size: 0.85rem;
            z-index: 9999;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
            animation: fadeIn 0.5s ease-in;
        `;
    document.body.appendChild(indicator);

    // Add fade in animation
    const style = document.createElement("style");
    style.textContent = `
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
        `;
    document.head.appendChild(style);
  }

  // Add indicator when page loads
  window.addEventListener("load", function () {
    setTimeout(addRefreshIndicator, 1000);
  });
})();
