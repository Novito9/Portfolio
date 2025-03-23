// Smooth scroll function
function scrollToPortfolio() {
  const portfolioSection = document.getElementById('portfolio');
  if (portfolioSection) {
    portfolioSection.scrollIntoView({ behavior: 'smooth' });
  }
}
