// main.js

document.addEventListener("DOMContentLoaded", () => {
  const overlay = document.getElementById("overlay");
  const closeOverlayButton = document.getElementById("close-overlay");
  const overlayContent = document.getElementById("overlay-content");

  // Function to load content into the overlay
  function loadOverlayContent(sectionId) {
    // Example of loading content from the server
    // For demonstration, we're using static HTML content
    overlayContent.innerHTML = `
            <iframe src="${sectionId.replace(
              "#",
              ""
            )}.html" frameborder="0" style="width: 100%; height: 100%; border: none;"></iframe>
        `;
  }

  // Handle box button clicks
  document.querySelectorAll(".box-button").forEach((button) => {
    button.addEventListener("click", (event) => {
      const sectionId = event.target.getAttribute("data-section");
      loadOverlayContent(sectionId);
      overlay.style.display = "flex"; // Show the overlay
    });
  });

  // Handle overlay close button
  closeOverlayButton.addEventListener("click", () => {
    overlay.style.display = "none"; // Hide the overlay
  });

  // Handle clicking outside of the overlay to close it
  overlay.addEventListener("click", (event) => {
    if (event.target === overlay) {
      overlay.style.display = "none"; // Hide the overlay
    }
  });
});
