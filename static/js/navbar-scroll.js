/**
 * Auto-hide navbar on scroll down for mobile devices
 */

(function () {
  // Only run on mobile devices
  function isMobile() {
    return window.innerWidth <= 768;
  }

  // Only run on public pages
  const navbar = document.querySelector(".navbar.glass-nav");
  if (!navbar) {
    return;
  }

  let lastScrollTop = 0;
  let scrollThreshold = 50; // Minimum scroll distance to trigger hide/show
  let isScrolling;

  function handleScroll() {
    // Only apply on mobile
    if (!isMobile()) {
      navbar.classList.remove("nav-hidden");
      return;
    }

    const currentScroll =
      window.pageYOffset || document.documentElement.scrollTop;

    // Ignore small scroll movements
    if (Math.abs(currentScroll - lastScrollTop) < 5) {
      return;
    }

    // Show navbar at the top of the page
    if (currentScroll <= scrollThreshold) {
      navbar.classList.remove("nav-hidden");
    }
    // Hide navbar when scrolling down
    else if (currentScroll > lastScrollTop && currentScroll > scrollThreshold) {
      navbar.classList.add("nav-hidden");
    }
    // Show navbar when scrolling up
    else if (currentScroll < lastScrollTop) {
      navbar.classList.remove("nav-hidden");
    }

    lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;
  }

  // Debounce scroll events for better performance
  window.addEventListener(
    "scroll",
    function () {
      window.clearTimeout(isScrolling);
      isScrolling = setTimeout(handleScroll, 10);
    },
    false
  );

  // Handle window resize
  window.addEventListener("resize", function () {
    if (!isMobile()) {
      navbar.classList.remove("nav-hidden");
    }
  });

  // Initial check
  handleScroll();
})();
