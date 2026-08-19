(function () {
  "use strict";

  /* ---------------- Theme ---------------- */
  const root = document.documentElement;
  const stored = localStorage.getItem("theme");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  setTheme(stored || (prefersDark ? "dark" : "light"));

  function setTheme(mode) {
    root.setAttribute("data-theme", mode);
    localStorage.setItem("theme", mode);
    const btn = document.getElementById("themeToggle");
    if (btn) btn.innerHTML = mode === "dark" ? sun() : moon();
    syncGitHubTheme(mode);
  }

  document.addEventListener("click", function (e) {
    const t = e.target.closest("#themeToggle");
    if (t) setTheme(root.getAttribute("data-theme") === "dark" ? "light" : "dark");
  });

  /* ---------------- GitHub cards theme sync ---------------- */
  function syncGitHubTheme(mode) {
    const light = { title: "0078d4", text: "0f172a", ring: "0078d4", line: "6d28d9", pt: "0ea5a4" };
    const dark  = { title: "3ea0ff", text: "eef2ff", ring: "3ea0ff", line: "a78bfa", pt: "2dd4bf" };
    const c = mode === "dark" ? dark : light;
    const bg = "00000000"; // transparent so the glass card shows through
    const stats = document.getElementById("ghStats");
    const langs = document.getElementById("ghLangs");
    const chart = document.getElementById("ghChart");
    const user = document.body.getAttribute("data-gh") || "lloydismael";
    if (stats) stats.src =
      `https://github-readme-stats.vercel.app/api?username=${user}&show_icons=true&hide_border=true&count_private=true&bg_color=${bg}&title_color=${c.title}&text_color=${c.text}&icon_color=${c.ring}`;
    if (langs) langs.src =
      `https://github-readme-stats.vercel.app/api/top-langs/?username=${user}&layout=compact&hide_border=true&bg_color=${bg}&title_color=${c.title}&text_color=${c.text}`;
    // Original GitHub contribution calendar — native green tiles (GitHub's own colors).
    if (chart) chart.src = `https://ghchart.rshah.org/216e39/${user}`;
  }

  /* ---------------- Live project previews (mShots + retry) ---------------- */
  // mShots generates screenshots asynchronously and serves a small placeholder
  // (~400x300 grey) until ready. We poll by reloading the image until a real,
  // larger screenshot loads; then fall back to microlink; then to a styled tile.
  function initPreviews() {
    document.querySelectorAll(".preview-img").forEach(function (img) {
      var base = img.getAttribute("data-shot");
      var fallback = img.getAttribute("data-fallback");
      var maxTries = 10;

      img.addEventListener("load", function () {
        // mShots placeholder is ~400px wide; a real capture is much larger.
        var tries = parseInt(img.getAttribute("data-tries") || "0", 10);
        if (img.naturalWidth > 600 || img.naturalHeight > 400) {
          img.classList.add("loaded");
          img.closest(".preview").classList.remove("loading");
          return;
        }
        if (tries < maxTries) {
          tries += 1;
          img.setAttribute("data-tries", String(tries));
          img.closest(".preview").classList.add("loading");
          setTimeout(function () { img.src = base + "&reload=" + Date.now(); },
            1200 + tries * 600); // back off a little each attempt
        } else {
          img.src = fallback; // give microlink a shot
        }
      });

      img.addEventListener("error", function () {
        if (img.src.indexOf("microlink") === -1) {
          img.src = fallback;
        } else {
          img.closest(".preview").classList.add("noshot");
        }
      });

      // Kick the first load (in case it was cached before listeners attached)
      if (img.complete) img.dispatchEvent(new Event("load"));
    });
  }
  initPreviews();

  /* ---------------- Floating chat menu ---------------- */
  document.addEventListener("click", function (e) {
    const wrap = document.getElementById("fabWrap");
    if (!wrap) return;
    if (e.target.closest("#fabBtn")) { wrap.classList.toggle("open"); return; }
    if (!e.target.closest("#fabWrap")) wrap.classList.remove("open");
  });

  /* ---------------- Smooth-scroll active nav ---------------- */
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener("click", (e) => {
      const id = a.getAttribute("href");
      if (id.length > 1) {
        const el = document.querySelector(id);
        if (el) { e.preventDefault(); el.scrollIntoView({ behavior: "smooth" }); }
      }
    });
  });

  /* ---------------- Reveal on scroll ---------------- */
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
  }, { threshold: 0.12 });
  document.querySelectorAll(".reveal").forEach((el) => io.observe(el));

  /* ---------------- Contact form ---------------- */
  const form = document.getElementById("contactForm");
  if (form) {
    form.addEventListener("submit", async function (e) {
      e.preventDefault();
      const status = document.getElementById("formStatus");
      const data = Object.fromEntries(new FormData(form).entries());
      status.textContent = "Sending…";
      try {
        const res = await fetch("/api/contact", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data),
        });
        if (!res.ok) throw new Error("bad");
        status.textContent = "✓ Thanks! Your message was received.";
        form.reset();
      } catch (err) {
        // Fallback for local preview / no API: open the user's mail client
        const email = document.body.getAttribute("data-email");
        const subject = encodeURIComponent(`Portfolio enquiry from ${data.name || "website"}`);
        const body = encodeURIComponent(`${data.message || ""}\n\nFrom: ${data.name || ""} (${data.email || ""})`);
        window.location.href = `mailto:${email}?subject=${subject}&body=${body}`;
        status.textContent = "Opening your email app…";
      }
    });
  }

  /* ---------------- Icons ---------------- */
  function moon() { return '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'; }
  function sun() { return '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>'; }
})();
