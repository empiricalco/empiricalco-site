/* Empirical Co — small progressive enhancements. The page works without this file. */
(function () {
  "use strict";

  var root = document.documentElement;
  var nav = document.querySelector("[data-nav]");
  var toggle = document.querySelector(".nav__toggle");
  var panel = document.getElementById("nav-panel");

  /* Nav: solid background once the page scrolls */
  function onScroll() {
    nav.toggleAttribute("data-scrolled", window.scrollY > 8);
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* Nav: mobile menu */
  function setMenu(open) {
    toggle.setAttribute("aria-expanded", String(open));
    toggle.textContent = open ? "Close" : "Menu";
    nav.toggleAttribute("data-open", open);
  }
  toggle.addEventListener("click", function () {
    setMenu(toggle.getAttribute("aria-expanded") !== "true");
  });
  panel.addEventListener("click", function (e) {
    if (e.target.closest("a")) setMenu(false);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && nav.hasAttribute("data-open")) {
      setMenu(false);
      toggle.focus();
    }
  });

  /* Section rules draw across as they enter view (decorative only) */
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!reduce && "IntersectionObserver" in window) {
    var rules = document.querySelectorAll(".rule[data-rule]");
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-in");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    rules.forEach(function (r) {
      var box = r.getBoundingClientRect();
      if (box.top < window.innerHeight) r.classList.add("is-in");
      io.observe(r);
    });
    root.classList.add("motion");
  }

  /* Footer year */
  var year = document.querySelector("[data-year]");
  if (year) year.textContent = String(new Date().getFullYear());

  /* Enquiry form */
  var form = document.getElementById("enquiry");
  var done = document.getElementById("form-done");
  var status = document.getElementById("form-status");
  if (!form) return;
  var button = form.querySelector('button[type="submit"]');

  var messages = {
    "f-name": "Please add your name.",
    "f-email": "Please add an email address we can reply to.",
    "f-type": "Please choose a project type.",
    "f-brief": "Please add a short brief."
  };

  function clearError(field) {
    field.removeAttribute("aria-invalid");
    var err = document.getElementById(field.id + "-error");
    if (err) err.remove();
    var hint = document.getElementById(field.id + "-hint");
    field.setAttribute("aria-describedby", hint ? hint.id : "");
    if (!hint) field.removeAttribute("aria-describedby");
  }

  function showError(field) {
    clearError(field);
    var msg = field.type === "email" && field.value ? "Please check the email address." : messages[field.id];
    var err = document.createElement("p");
    err.className = "field__error";
    err.id = field.id + "-error";
    err.textContent = msg || "Please fill in this field.";
    field.parentNode.appendChild(err);
    field.setAttribute("aria-invalid", "true");
    var described = [err.id];
    if (document.getElementById(field.id + "-hint")) described.unshift(field.id + "-hint");
    field.setAttribute("aria-describedby", described.join(" "));
  }

  form.addEventListener("input", function (e) {
    if (e.target.hasAttribute("aria-invalid") && e.target.checkValidity()) clearError(e.target);
  });
  form.addEventListener("change", function (e) {
    if (e.target.hasAttribute("aria-invalid") && e.target.checkValidity()) clearError(e.target);
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    status.textContent = "";
    status.removeAttribute("data-error");

    var invalid = Array.prototype.filter.call(form.querySelectorAll("[required]"), function (f) {
      return !f.checkValidity();
    });
    form.querySelectorAll("[aria-invalid]").forEach(clearError);
    if (invalid.length) {
      invalid.forEach(showError);
      invalid[0].focus();
      return;
    }

    button.disabled = true;
    button.textContent = "Sending…";

    var finish = function () {
      var first = (document.getElementById("f-name").value || "").trim().split(/\s+/)[0];
      document.getElementById("form-done-title").textContent = first ? "Thank you, " + first + "." : "Thank you.";
      form.hidden = true;
      done.hidden = false;
      done.focus();
    };

    if (window.EMPIRICAL_PREVIEW) { setTimeout(finish, 500); return; }

    fetch(form.action, {
      method: "POST",
      body: new FormData(form),
      headers: { Accept: "application/json" }
    }).then(function (res) {
      if (!res.ok) throw new Error("Request failed: " + res.status);
      finish();
    }).catch(function () {
      button.disabled = false;
      button.textContent = "Send enquiry";
      status.setAttribute("data-error", "");
      status.textContent = "Your enquiry didn’t send. Please try again, or email hello@empiricalco.com.";
    });
  });
})();
