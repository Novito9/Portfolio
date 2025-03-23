// Smooth scroll function for index page
function scrollToPortfolio() {
  const portfolioSection = document.getElementById("portfolio-preview");
  if (portfolioSection) {
    portfolioSection.scrollIntoView({ behavior: "smooth" });
  }
}
