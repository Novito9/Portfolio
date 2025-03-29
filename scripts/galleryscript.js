// ======= DEBUG HELPER =======
    function log(msg) {
      console.log("[DEBUG]:", msg);
    }

    // ======= MOBILE MENU TOGGLE =======
    const menuBtn = document.querySelector('.menu-btn');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    menuBtn.addEventListener('click', function() {
      this.classList.toggle('active');
      mobileMenu.classList.toggle('active');
      document.body.style.overflow = this.classList.contains('active') ? 'hidden' : '';
    });
    
    // Close mobile menu when clicking on a link
    document.querySelectorAll('.mobile-nav-links a').forEach(link => {
      link.addEventListener('click', () => {
        menuBtn.classList.remove('active');
        mobileMenu.classList.remove('active');
        document.body.style.overflow = '';
      });
    });

    // ======= DYNAMIC QUOTE & WELCOME MESSAGE =======
    const quotes = [
      "Creativity is allowing yourself to make mistakes. Art is knowing which ones to keep. - Scott Adams",
      "Art enables us to find ourselves and lose ourselves at the same time. - Thomas Merton",
      "A true artist is not one who is inspired, but one who inspires others. - Salvador Dalí"
    ];
    let currentQuote = 0;
    const dynamicQuote = document.getElementById('dynamic-quote');
    const welcomeMessage = document.getElementById('welcome-message');

    function showNextQuote() {
      dynamicQuote.style.opacity = 0;
      setTimeout(() => {
        currentQuote = (currentQuote + 1) % quotes.length;
        dynamicQuote.textContent = quotes[currentQuote];
        dynamicQuote.style.opacity = 1;
      }, 1000);
    }
    
    // ======= PORTFOLIO IMAGES LOADER =======
    // Fallback images array
    const fallbackImages = [
      { 
        url: "images/Anubis.jpg", 
        alt: "Anubis Artwork", 
        title: "Egypt Ai", 
        desc: "Anubis, jackal-headed god, towering in judgment hall with scales and ankh." 
      },
      { 
        url: "images/PharaohHound.jpg", 
        alt: "Pharaoh Hound Artwork", 
        title: "Quantum Flow", 
        desc: "A stylized Pharaoh Hound with a jeweled collar next to an Egyptian artifact." 
      }
    ];

    // Validate image file extension
    function isValidImage(url) {
      if (!url) return false;
      const validExtensions = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg'];
      const extension = url.split('.').pop().split('?')[0].toLowerCase();
      return validExtensions.includes(extension);
    }

    async function loadRandomImages() {
      try {
        const response = await fetch('images/image-list.json');
        if (response.ok) {
          const imageData = await response.json();
          const validImages = imageData.filter(item => isValidImage(item.url));
          if (validImages.length > 0) {
            log("Images loaded from JSON.");
            return validImages;
          }
        }
      } catch (e) {
        log("Error loading JSON, using fallback images.");
      }
      return fallbackImages;
    }

    // Shuffle array for randomness
    function shuffleArray(array) {
      for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
      }
      return array;
    }

    // Display images in the portfolio grid
    function displayImages(imageData) {
      const grid = document.getElementById('portfolio-grid');
      grid.innerHTML = "";
      const validImages = shuffleArray(imageData.filter(item => item.url && item.alt && isValidImage(item.url)));

      validImages.forEach(item => {
        const portfolioItem = document.createElement('div');
        portfolioItem.className = "portfolio-item";
        
        // Create image element
        const img = document.createElement('img');
        img.src = item.url;
        img.alt = item.alt || "Artwork Image";
        img.loading = "lazy";
        img.onerror = () => {
          log("Failed to load image: " + item.url);
          portfolioItem.style.display = "none";
        };

        // Overlay for title and description
        const overlay = document.createElement('div');
        overlay.className = "item-overlay";
        overlay.innerHTML = `<strong>${item.title || "Untitled"}</strong><br>${item.desc || ""}`;
        
        // Like Button
        const likeBtn = document.createElement('button');
        likeBtn.className = 'like-btn';
        likeBtn.innerHTML = '♥';
        likeBtn.addEventListener('click', handleLike);
        portfolioItem.appendChild(likeBtn);

        // Like Count Display
        const likeCount = document.createElement('div');
        likeCount.className = 'like-count';
        likeCount.textContent = '0';
        portfolioItem.appendChild(likeCount);

        // Click event to open image modal
        portfolioItem.addEventListener('click', () => {
          openModal(item);
        });

        portfolioItem.appendChild(img);
        portfolioItem.appendChild(overlay);
        grid.appendChild(portfolioItem);
      });

      if (validImages.length === 0) {
        grid.innerHTML = '<p style="grid-column:1/-1;text-align:center;color:white;">No images found in the gallery</p>';
      }
    }

    // ======= MODAL FUNCTIONALITY =======
    const modal = document.getElementById("imageModal");
    const modalImg = document.getElementById("modalImage");
    const modalTitle = document.getElementById("modalTitle");
    const modalDesc = document.getElementById("modalDesc");
    const closeModalSpan = document.querySelector(".close-modal");
    const closeModalBtn = document.getElementById("closeModalBtn");

    function openModal(item) {
      log("Opening modal for: " + item.title);
      modalImg.src = item.url;
      modalImg.alt = item.alt || "Modal Image";
      modalTitle.textContent = item.title || "";
      modalDesc.textContent = item.desc || "";
      modal.style.display = "flex";
      document.body.style.overflow = "hidden";
    }

    function closeImageModal() {
      modal.style.display = "none";
      document.body.style.overflow = "";
      log("Modal closed.");
    }

    closeModalSpan.addEventListener("click", closeImageModal);
    closeModalBtn.addEventListener("click", closeImageModal);

    // Stop propagation on modal content clicks
    document.querySelector(".modal-content").addEventListener("click", e => e.stopPropagation());
    modal.addEventListener("click", closeImageModal);

    // ======= SOCIAL ENGAGEMENT (LIKE BUTTON) =======
    let isLoggedIn = false;

    function handleLike(e) {
      e.stopPropagation();
      if (!isLoggedIn) {
        openLoginModal();
        return;
      }
      const btn = e.target;
      const countElement = btn.parentElement.querySelector('.like-count');
      btn.classList.toggle('liked');
      const currentCount = parseInt(countElement.textContent);
      countElement.textContent = btn.classList.contains('liked') ? currentCount + 1 : currentCount - 1;
    }

    // ======= COMMENT SYSTEM =======
    let currentImageId = null; // Use your logic to track image IDs

    document.getElementById('openCommentsBtn').addEventListener('click', () => {
      closeImageModal();
      openCommentSystem(1); // Replace 1 with the actual image ID if needed
    });

    document.getElementById('closeComments').addEventListener('click', () => {
      document.getElementById('commentModal').classList.remove('active');
    });

    document.getElementById('commentForm').addEventListener('submit', e => {
      e.preventDefault();
      if (!isLoggedIn) {
        openLoginModal();
        return;
      }
      postComment();
    });

    function openCommentSystem(imageId) {
      currentImageId = imageId;
      document.getElementById('commentModal').classList.add('active');
      loadComments(imageId);
    }

    function loadComments(imageId) {
      const commentList = document.getElementById('commentList');
      commentList.innerHTML = '<p>Loading comments...</p>';
      // Simulate an async load
      setTimeout(() => {
        commentList.innerHTML = `
          <div class="comment-item">
            <div class="comment-author">CyberUser42</div>
            <div class="comment-text">This artwork is amazing! Love the colors.</div>
          </div>
          <div class="comment-item">
            <div class="comment-author">NeonDreamer</div>
            <div class="comment-text">The composition is perfect 👌</div>
          </div>
        `;
      }, 500);
    }

    function postComment() {
      const commentInput = document.getElementById('commentInput');
      const commentText = commentInput.value.trim();
      if (commentText) {
        const commentList = document.getElementById('commentList');
        const newComment = document.createElement('div');
        newComment.className = 'comment-item';
        newComment.innerHTML = `
          <div class="comment-author">You</div>
          <div class="comment-text">${commentText}</div>
        `;
        commentList.prepend(newComment);
        commentInput.value = '';
      }
    }

    // ======= LOGIN SYSTEM =======
    document.getElementById('loginClose').addEventListener('click', () => {
      document.getElementById('loginModal').style.display = 'none';
    });

    document.getElementById('loginForm').addEventListener('submit', e => {
      e.preventDefault();
      isLoggedIn = true;
      document.getElementById('loginModal').style.display = 'none';
      alert('Login successful! You can now comment and like images.');
    });

    function openLoginModal() {
      document.getElementById('loginModal').style.display = 'block';
    }

    // ======= INITIALIZATION =======
    document.addEventListener('DOMContentLoaded', async () => {
      // Start dynamic quote rotation
      setTimeout(() => {
        welcomeMessage.style.opacity = 0;
      }, 4000);
      showNextQuote();
      setInterval(showNextQuote, 8000);

      // Load images and display them in grid
      const images = await loadRandomImages();
      displayImages(images);
      log("Images displayed.");
    });

// ======= IMAGE DATA STRUCTURE =======
// Update your image data to include categories and metadata
const fallbackImages = [
  { 
    url: "images/Anubis.jpg", 
    alt: "Anubis Artwork", 
    title: "Egypt Ai", 
    desc: "Anubis, jackal-headed god, towering in judgment hall with scales and ankh.",
    category: "cyberpunk",
    date: "2024-05-15",
    views: 1245,
    likes: 89
  },
  { 
    url: "images/PharaohHound.jpg", 
    alt: "Pharaoh Hound Artwork", 
    title: "Quantum Flow", 
    desc: "A stylized Pharaoh Hound with a jeweled collar next to an Egyptian artifact.",
    category: "abstract",
    date: "2024-04-22",
    views: 876,
    likes: 64
  }
];

// ======= FILTERING & SORTING =======
let currentCategory = 'all';
let currentSearchTerm = '';
let currentSort = 'random';

// Category filter
document.querySelectorAll('.category-btn').forEach(btn => {
  btn.addEventListener('click', function() {
    document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
    this.classList.add('active');
    currentCategory = this.dataset.category;
    filterAndSortImages();
  });
});

// Search functionality
document.getElementById('searchBtn').addEventListener('click', () => {
  currentSearchTerm = document.getElementById('searchInput').value.toLowerCase();
  filterAndSortImages();
});

document.getElementById('searchInput').addEventListener('keyup', (e) => {
  if (e.key === 'Enter') {
    currentSearchTerm = document.getElementById('searchInput').value.toLowerCase();
    filterAndSortImages();
  }
});

// Sort functionality
document.getElementById('sortSelect').addEventListener('change', function() {
  currentSort = this.value;
  filterAndSortImages();
});

function filterAndSortImages() {
  let filteredImages = [...fallbackImages]; // Use your actual image data source
  
  // Filter by category
  if (currentCategory !== 'all') {
    filteredImages = filteredImages.filter(img => img.category === currentCategory);
  }
  
  // Filter by search term
  if (currentSearchTerm) {
    filteredImages = filteredImages.filter(img => 
      img.title.toLowerCase().includes(currentSearchTerm) || 
      img.desc.toLowerCase().includes(currentSearchTerm)
    );
  }
  
  // Sort images
  switch(currentSort) {
    case 'newest':
      filteredImages.sort((a, b) => new Date(b.date) - new Date(a.date));
      break;
    case 'oldest':
      filteredImages.sort((a, b) => new Date(a.date) - new Date(b.date));
      break;
    case 'popular':
      filteredImages.sort((a, b) => b.likes - a.likes);
      break;
    case 'views':
      filteredImages.sort((a, b) => b.views - a.views);
      break;
    default: // random
      filteredImages = shuffleArray([...filteredImages]);
  }
  
  displayImages(filteredImages);
}

// ======= INITIALIZATION =======
document.addEventListener('DOMContentLoaded', async () => {
  // Start dynamic quote rotation
  setTimeout(() => {
    welcomeMessage.style.opacity = 0;
  }, 4000);
  showNextQuote();
  setInterval(showNextQuote, 8000);

  // Load images and display them in grid
  const images = await loadRandomImages();
  // Add default metadata to images if not present
  images.forEach(img => {
    if (!img.category) img.category = ['cyberpunk', 'abstract', 'portrait', 'landscape'][Math.floor(Math.random() * 4)];
    if (!img.date) img.date = new Date(Date.now() - Math.floor(Math.random() * 1000 * 60 * 60 * 24 * 30)).toISOString().split('T')[0];
    if (!img.views) img.views = Math.floor(Math.random() * 2000);
    if (!img.likes) img.likes = Math.floor(Math.random() * 150);
  });
  
  fallbackImages.push(...images);
  filterAndSortImages();
  log("Images displayed.");
});