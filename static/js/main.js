(function () {
  "use strict";

  /* ---------------- Theme ---------------- */
  const root = document.documentElement;
  const stored = localStorage.getItem("theme");
  setTheme(stored === "dark" ? "dark" : "light");

  function setTheme(mode) {
    root.setAttribute("data-theme", mode);
    localStorage.setItem("theme", mode);
    const btn = document.getElementById("themeToggle");
    if (btn) {
      btn.innerHTML = mode === "dark" ? sun() : moon();
      btn.setAttribute("aria-pressed", String(mode === "dark"));
      btn.setAttribute("aria-label", mode === "dark" ? "Switch to light theme" : "Switch to dark theme");
    }
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

  /* ---------------- Pointer-responsive liquid glass ---------------- */
  const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)");
  let glassFrame = 0;
  let glassTarget = null;
  let glassPoint = null;

  document.addEventListener("pointermove", function (e) {
    if (!finePointer.matches) return;
    const glass = e.target.closest(".glass");
    if (!glass) {
      if (glassTarget) glassTarget.classList.remove("glass-active");
      glassTarget = null;
      return;
    }
    if (glassTarget && glassTarget !== glass) glassTarget.classList.remove("glass-active");
    glassTarget = glass;
    glassPoint = { x: e.clientX, y: e.clientY };
    if (glassFrame) return;
    glassFrame = requestAnimationFrame(function () {
      glassFrame = 0;
      if (!glassTarget || !glassPoint) return;
      const rect = glassTarget.getBoundingClientRect();
      glassTarget.style.setProperty("--glass-x", `${glassPoint.x - rect.left}px`);
      glassTarget.style.setProperty("--glass-y", `${glassPoint.y - rect.top}px`);
      glassTarget.classList.add("glass-active");
    });
  }, { passive: true });

  document.addEventListener("pointerout", function (e) {
    const glass = e.target.closest(".glass");
    if (!glass || glass.contains(e.relatedTarget)) return;
    glass.classList.remove("glass-active");
    if (glassTarget === glass) glassTarget = null;
  });

  /* ---------------- Expandable navigation and contact menus ---------------- */
  const setExpanded = (button, panel, open) => {
    if (!button || !panel) return;
    button.setAttribute("aria-expanded", String(open));
    button.setAttribute("aria-label", open
      ? (button.id === "navToggle" ? "Close navigation" : "Close contact options")
      : (button.id === "navToggle" ? "Open navigation" : "Open contact options"));
    panel.hidden = !open;
  };

  const closeMobileNav = (restoreFocus) => {
    const button = document.getElementById("navToggle");
    const panel = document.getElementById("primaryLinks");
    const nav = document.querySelector(".nav");
    if (!button || !panel || !nav) return;
    nav.classList.remove("menu-open");
    setExpanded(button, panel, false);
    if (restoreFocus) button.focus();
  };

  const closeFab = (restoreFocus) => {
    const wrap = document.getElementById("fabWrap");
    const button = document.getElementById("fabBtn");
    const panel = document.getElementById("fabMenu");
    if (!wrap || !button || !panel) return;
    wrap.classList.remove("open");
    setExpanded(button, panel, false);
    if (restoreFocus) button.focus();
  };

  document.addEventListener("click", function (e) {
    const wrap = document.getElementById("fabWrap");
    const fabButton = document.getElementById("fabBtn");
    const fabMenu = document.getElementById("fabMenu");
    const navButton = document.getElementById("navToggle");
    const mobileNav = document.getElementById("primaryLinks");
    const nav = document.querySelector(".nav");

    if (e.target.closest("#fabBtn") && wrap && fabButton && fabMenu) {
      const open = fabButton.getAttribute("aria-expanded") !== "true";
      wrap.classList.toggle("open", open);
      setExpanded(fabButton, fabMenu, open);
      return;
    }
    if (wrap && !e.target.closest("#fabWrap")) closeFab(false);

    if (e.target.closest("#navToggle") && navButton && mobileNav && nav) {
      const open = navButton.getAttribute("aria-expanded") !== "true";
      nav.classList.toggle("menu-open", open);
      setExpanded(navButton, mobileNav, open);
      return;
    }
    if (e.target.closest("#primaryLinks a")) closeMobileNav(false);
    else if (nav && !e.target.closest(".nav")) closeMobileNav(false);
  });

  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    if (document.getElementById("fabBtn")?.getAttribute("aria-expanded") === "true") closeFab(true);
    if (document.getElementById("navToggle")?.getAttribute("aria-expanded") === "true") closeMobileNav(true);
  });

  window.addEventListener("resize", function () {
    if (window.innerWidth > 960) closeMobileNav(false);
  });

  /* ---------------- Analytics (no-op unless gtag exists) ---------------- */
  function track(name, params) {
    if (typeof window.gtag === "function") {
      window.gtag("event", name, params || {});
    }
  }

  document.addEventListener("click", function (e) {
    const cta = e.target.closest("[data-cta]");
    if (cta) {
      track("select_content", { content_type: "cta", item_id: cta.getAttribute("data-cta") });
    }
    const project = e.target.closest("a.project");
    if (project) {
      track("click", { event_category: "outbound", event_label: project.href, outbound: true });
    }
  });

  /* ---------------- Smooth-scroll active nav ---------------- */
  const navLinks = Array.from(document.querySelectorAll('.nav-links a[href^="#"]'));
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener("click", (e) => {
      const id = a.getAttribute("href");
      if (id.length > 1) {
        const el = document.querySelector(id);
        if (el) {
          e.preventDefault();
          const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
          el.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
        }
      }
    });
  });
  if (navLinks.length && "IntersectionObserver" in window) {
    const setCurrent = (id) => {
      navLinks.forEach((link) => {
        if (link.getAttribute("href") === id) link.setAttribute("aria-current", "true");
        else link.removeAttribute("aria-current");
      });
    };
    const sectionIo = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) setCurrent("#" + en.target.id);
      });
    }, { rootMargin: "-40% 0px -50% 0px", threshold: 0 });
    navLinks.forEach((link) => {
      const target = document.querySelector(link.getAttribute("href"));
      if (target) sectionIo.observe(target);
    });
  }

  /* ---------------- Reveal on scroll ---------------- */
  const revealItems = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) {
          en.target.classList.add("in");
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.1, rootMargin: "0px 0px -5% 0px" });
    revealItems.forEach((el, index) => {
      el.style.setProperty("--reveal-delay", `${Math.min(index % 4, 3) * 55}ms`);
      io.observe(el);
    });
  } else {
    revealItems.forEach((el) => el.classList.add("in"));
  }

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
        status.textContent = "Thanks — I will reply with next steps within one business day.";
        form.reset();
        track("generate_lead", { method: "contact_form" });
        track("form_submit", { form_id: "contact" });
      } catch (err) {
        // Fallback for local preview / no API: open the user's mail client
        const email = document.body.getAttribute("data-email");
        const subject = encodeURIComponent(`Portfolio enquiry from ${data.name || "website"}`);
        const body = encodeURIComponent(`${data.message || ""}\n\nFrom: ${data.name || ""} (${data.email || ""})`);
        window.location.href = `mailto:${email}?subject=${subject}&body=${body}`;
        status.textContent = "Opening your email app so you can send the same note…";
        track("form_submit", { form_id: "contact", method: "mailto_fallback" });
      }
    });
  }

  /* ---------------- Icons ---------------- */
  function moon() { return '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'; }
  function sun() { return '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>'; }
})();
