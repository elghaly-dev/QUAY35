/* page-menu.js — QUAY35: Chatting header link, EN/AR/RU/ZH contact lines, home hero swap.
 * No third-party AI menu, no tracking. QUAY-only fork of the shared elghaly
 * page-menu on this site only.
 */
(function () {
  "use strict";

  var CHAT_URL = "https://chatting.elghaly.dev/";
  var CHAT_LABEL = "\uD83D\uDCAC Chatting by elghaly";
  var STORAGE_KEY = "quay-lang";
  var LANGS = ["en", "ar", "ru", "zh"];
  var MAIL = "support@elghaly.dev";

  var CONTACT = {
    en: "Email first: " + MAIL + ". Calls only by appointment.",
    ar:
      "\u0627\u0644\u0628\u0631\u064A\u062F \u0623\u0648\u0644\u0627\u064B: " +
      MAIL +
      ". \u0627\u0644\u0645\u0643\u0627\u0644\u0645\u0627\u062A \u0628\u0645\u0648\u0639\u062F \u0645\u0633\u0628\u0642 \u0641\u0642\u0637.",
    ru:
      "\u0421\u043D\u0430\u0447\u0430\u043B\u0430 \u043F\u043E \u043F\u043E\u0447\u0442\u0435: " +
      MAIL +
      ". \u0417\u0432\u043E\u043D\u043A\u0438 \u0442\u043E\u043B\u044C\u043A\u043E \u043F\u043E \u0434\u043E\u0433\u043E\u0432\u043E\u0440\u0451\u043D\u043D\u043E\u0441\u0442\u0438.",
    zh:
      "\u8BF7\u5148\u53D1\u90AE\u4EF6\uFF1A" + MAIL + "\u3002\u7535\u8BDD\u4EC5\u9650\u9884\u7EA6\u3002"
  };

  var HERO = {
    en: {
      h: "Reports a desk can sell. Not another empty chart.",
      l:
        "QUAY works from public data and the text you send — signatures, a mint, a feed — and sends back a page, a card or a ping. You buy a file, a card or a watch, not a token. We never hold keys."
    },
    ar: {
      h: "\u062A\u0642\u0627\u0631\u064A\u0631 \u0644\u0644\u0645\u0643\u062A\u0628.",
      l: "\u0645\u0644\u0641 \u0623\u0648 \u0643\u0627\u0631\u062A. \u0645\u0634 \u062A\u0648\u0643\u0646."
    },
    ru: {
      h: "\u041E\u0442\u0447\u0451\u0442\u044B \u0434\u043B\u044F \u0441\u0442\u043E\u043B\u0430.",
      l: "\u0424\u0430\u0439\u043B \u0438\u043B\u0438 \u043A\u0430\u0440\u0442\u0430. \u041D\u0435 \u0442\u043E\u043A\u0435\u043D."
    },
    zh: {
      h: "\u80FD\u5356\u7684\u62A5\u544A.",
      l: "\u6587\u4EF6\u6216\u5361\uFF0C\u4E0D\u662F\u4EE3\u5E01\u3002"
    }
  };

  function addFocusStyle() {
    if (document.getElementById("quay-pm-focus")) return;
    var s = document.createElement("style");
    s.id = "quay-pm-focus";
    s.textContent =
      ".btn:focus-visible{outline:2px solid #2ee6c7;outline-offset:2px}";
    document.head.appendChild(s);
  }

  function ensureChatLink() {
    document.querySelectorAll(".header-right").forEach(function (hr) {
      var link = hr.querySelector("[data-quay-chatting]");
      if (!link) {
        link = hr.querySelector('a[href*="chatting.elghaly.dev"]');
        if (link) link.setAttribute("data-quay-chatting", "");
      }
      if (!link) {
        link = document.createElement("a");
        link.className = "btn";
        link.setAttribute("data-quay-chatting", "");
        hr.insertBefore(link, hr.firstChild);
      }
      link.href = CHAT_URL;
      link.textContent = CHAT_LABEL;
      link.setAttribute("aria-label", CHAT_LABEL);
    });
  }

  function contactHtml(lang) {
    var text = CONTACT[lang] || CONTACT.en;
    var mailPos = text.indexOf(MAIL);
    if (mailPos === -1) {
      return "elghaly, LLC \u00B7 " + text;
    }
    var before = text.slice(0, mailPos);
    var after = text.slice(mailPos + MAIL.length);
    return (
      "elghaly, LLC \u00B7 " +
      before +
      '<a href="mailto:' +
      MAIL +
      '">' +
      MAIL +
      "</a>" +
      after
    );
  }

  function applyContact(lang) {
    document.querySelectorAll("[data-quay-contact]").forEach(function (el) {
      el.innerHTML = contactHtml(lang);
    });
  }

  function readStoredLang() {
    try {
      var v = localStorage.getItem(STORAGE_KEY);
      if (LANGS.indexOf(v) !== -1) return v;
    } catch (e) { /* private mode */ }
    return "en";
  }

  function storeLang(lang) {
    try {
      localStorage.setItem(STORAGE_KEY, lang);
    } catch (e) { /* ignore */ }
  }

  function applyHero(lang) {
    var h1 = document.querySelector("main h1");
    var lede = document.querySelector("main .lede");
    if (!h1 || !lede || !HERO[lang]) return;
    if (lang === "en" && h1.hasAttribute("data-quay-en-h")) {
      h1.textContent = h1.getAttribute("data-quay-en-h");
      lede.textContent = lede.getAttribute("data-quay-en-l");
      return;
    }
    h1.textContent = HERO[lang].h;
    lede.textContent = HERO[lang].l;
  }

  function setLang(lang, activeBtn) {
    if (LANGS.indexOf(lang) === -1) lang = "en";
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === "ar" ? "rtl" : "ltr";
    applyContact(lang);
    applyHero(lang);
    storeLang(lang);
    document.querySelectorAll(".lang-btn").forEach(function (btn) {
      var on = activeBtn
        ? btn === activeBtn
        : btn.getAttribute("data-lang") === lang;
      btn.classList.toggle("on", on);
    });
  }

  function initLangSwitch() {
    var root = document.getElementById("langs");
    if (!root) {
      setLang(readStoredLang(), null);
      return;
    }
    root.querySelectorAll(".lang-btn").forEach(function (btn) {
      var code = btn.getAttribute("data-lang");
      if (LANGS.indexOf(code) === -1) btn.hidden = true;
    });
    var h1 = document.querySelector("main h1");
    var lede = document.querySelector("main .lede");
    if (h1 && lede && !h1.hasAttribute("data-quay-en-h")) {
      h1.setAttribute("data-quay-en-h", h1.textContent);
      lede.setAttribute("data-quay-en-l", lede.textContent);
    }
    setLang(readStoredLang(), null);
    root.addEventListener("click", function (e) {
      var btn = e.target.closest("[data-lang]");
      if (!btn || btn.hidden) return;
      setLang(btn.getAttribute("data-lang"), btn);
    });
  }

  addFocusStyle();
  ensureChatLink();
  initLangSwitch();
})();
