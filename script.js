// ---------------------------------------------------------
// Config
// ---------------------------------------------------------
const API_BASE = ""; // point this at your deployed backend

const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

// ---------------------------------------------------------
// Theme toggle (persisted in localStorage)
// ---------------------------------------------------------
const root = document.documentElement;
const themeToggle = document.getElementById("theme-toggle");

function applyTheme(theme) {
  root.setAttribute("data-theme", theme);
  themeToggle.setAttribute(
    "aria-label",
    theme === "dark" ? "Switch to light mode" : "Switch to dark mode"
  );
}

const savedTheme = localStorage.getItem("theme");
if (savedTheme) {
  applyTheme(savedTheme);
} else {
  // default to dark regardless of system preference, per the site's design
  applyTheme("dark");
}

themeToggle.addEventListener("click", () => {
  const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
  applyTheme(next);
  localStorage.setItem("theme", next);
});

// ---------------------------------------------------------
// Mobile nav
// ---------------------------------------------------------
const navBurger = document.getElementById("nav-burger");
const navLinks = document.querySelector(".nav-links");

navBurger.addEventListener("click", () => {
  const isOpen = navLinks.classList.toggle("open");
  navBurger.setAttribute("aria-expanded", String(isOpen));
});

navLinks.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => {
    navLinks.classList.remove("open");
    navBurger.setAttribute("aria-expanded", "false");
  });
});

// ---------------------------------------------------------
// Hero role typing effect
// ---------------------------------------------------------
const roles = [
  "Full-Stack Developer",
  "Python & FastAPI Backend Builder",
  "Generative AI Enthusiast",
  "SQL & Data-Driven Apps",
];

const roleEl = document.getElementById("role-text");

if (prefersReducedMotion) {
  roleEl.textContent = roles[0];
} else {
  let roleIndex = 0;
  let charIndex = roles[0].length;
  let deleting = false;

  function tick() {
    const current = roles[roleIndex];

    if (!deleting) {
      charIndex++;
      if (charIndex > current.length) {
        deleting = true;
        setTimeout(tick, 1400);
        return;
      }
    } else {
      charIndex--;
      if (charIndex < 0) {
        deleting = false;
        roleIndex = (roleIndex + 1) % roles.length;
        charIndex = 0;
      }
    }

    roleEl.textContent = current.slice(0, charIndex);
    setTimeout(tick, deleting ? 35 : 60);
  }

  setTimeout(tick, 1400);
}

// ---------------------------------------------------------
// Scroll reveal for sections
// ---------------------------------------------------------
const revealEls = document.querySelectorAll(".reveal");

if (prefersReducedMotion || !("IntersectionObserver" in window)) {
  revealEls.forEach((el) => el.classList.add("in-view"));
} else {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("in-view");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15 }
  );
  revealEls.forEach((el) => observer.observe(el));
}

// ---------------------------------------------------------
// Contact form -> FastAPI -> SQL database
// ---------------------------------------------------------
const form = document.getElementById("contact-form");
const statusEl = document.getElementById("form-status");
const submitBtn = document.getElementById("submit-btn");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const payload = {
    name: form.name.value.trim(),
    email: form.email.value.trim(),
    message: form.message.value.trim(),
  };

  submitBtn.disabled = true;
  submitBtn.textContent = "Sending…";
  statusEl.textContent = "";
  statusEl.className = "form-status";

  try {
    const res = await fetch(`${API_BASE}/api/contact`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) throw new Error("Request failed");

    statusEl.textContent = "Message sent — thanks for reaching out!";
    statusEl.classList.add("ok");
    form.reset();
  } catch (err) {
    statusEl.textContent = "Couldn't send that. Try emailing directly instead.";
    statusEl.classList.add("err");
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Send message";
  }
});

// ---------------------------------------------------------
// Footer year
// ---------------------------------------------------------
document.getElementById("year").textContent = new Date().getFullYear();
