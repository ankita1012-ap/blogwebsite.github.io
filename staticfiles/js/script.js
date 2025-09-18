// Dark mode toggle
const darkModeBtn = document.getElementById("darkModeBtn");

// ✅ Load saved theme from localStorage
if (localStorage.getItem("theme") === "dark") {
  document.body.classList.add("dark-mode");
  darkModeBtn.textContent = "☀️";
} else {
  darkModeBtn.textContent = "🌙";
}

// ✅ Toggle and save
darkModeBtn.addEventListener("click", () => {
  document.body.classList.toggle("dark-mode");

  if (document.body.classList.contains("dark-mode")) {
    localStorage.setItem("theme", "dark");
    darkModeBtn.textContent = "☀️";
  } else {
    localStorage.setItem("theme", "light");
    darkModeBtn.textContent = "🌙";
  }
});

// Back to top + reading progress
const backToTop = document.getElementById("backToTop");
window.onscroll = function () {
  // Back to top
  if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
    backToTop.style.display = "block";
  } else backToTop.style.display = "none";
  // Reading progress
  let winScroll = document.body.scrollTop || document.documentElement.scrollTop;
  let height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  document.getElementById("readingProgress").style.width = (winScroll / height) * 100 + "%";
};
backToTop.addEventListener("click", () => { document.documentElement.scrollTop = 0; document.body.scrollTop = 0; });

// Hero animated text
const heroText = document.getElementById("heroText");
const heroPhrases = ["Discover Trending Stories", "Explore Creative Ideas", "Read Inspiring Articles"];
let heroIndex = 0;
function typeHero() {
  heroText.textContent = "";
  let phrase = heroPhrases[heroIndex];
  let i = 0;
  let interval = setInterval(() => {
    heroText.textContent += phrase[i];
    i++;
    if (i >= phrase.length) {
      clearInterval(interval);
      setTimeout(() => { heroIndex = (heroIndex + 1) % heroPhrases.length; typeHero(); }, 1000);
    }
  }, 100);
}
typeHero();




// Top authors
let topAuthorBlogs = JSON.parse(document.getElementById("top-author-data").textContent);
let grid = document.getElementById("topAuthorGrid");

if (!topAuthorBlogs || topAuthorBlogs.length === 0) {
  grid.innerHTML = "<p>No top author blogs found.</p>";
} else {
  topAuthorBlogs.forEach(item => {
    let card = document.createElement("div");
    card.className = "col-md-3 col-6 mb-3"; // 2 per row
    card.innerHTML =
      `<div class="card h-100 author-card text-center bg-light text-dark p-2">
    <img src="/media/${item.blog_image}" class="card-img-top mx-auto mt-3">
    <div class="card-body">
      <h5 class="card-title">${item.title}</h5>
      <p class="card-text">${item.short_description.substring(0, 100)}...</p>
    </div></div>`;
    grid.appendChild(card);
  });
}



// Categories}
let categories = JSON.parse(document.getElementById("categories-data").textContent);
let categoryList = document.getElementById("categoryList");
categories.forEach(c => {
  let span = document.createElement("span");
  span.className = "badge bg-transparent border border-secondary rounded me-2 p-2";
  span.innerHTML = `<a href="/category-blog/${c}">${c}</a>`;
  // a.textContent = c;
  categoryList.appendChild(span);
});


// Newsletter submit
// document.getElementById("newsletterForm").addEventListener("submit", e => {
//   e.preventDefault();
//   alert("Subscribed!");
// });

// let loggedInUser = JSON.parse(localStorage.getItem("loggedInUser")) || null;

// Signup Form
const signupForm = document.getElementById("signupForm");
signupForm && signupForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const name = document.getElementById("signupName").value;
  const email = document.getElementById("signupEmail").value;
  const password = document.getElementById("signupPassword").value;

  const users = JSON.parse(localStorage.getItem("users")) || [];
  if (users.find(u => u.email === email)) {
    alert("User already exists! Please login.");
    return;
  }

  users.push({ name, email, password });
  localStorage.setItem("users", JSON.stringify(users));
  alert("Signup successful! You can now login.");
  document.getElementById("signupForm").reset();
  const loginTab = new bootstrap.Tab(document.querySelector("#login-tab"));
  loginTab.show();
});





