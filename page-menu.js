/* page-menu.js — the "Ask ChatGPT | ⌄" button at the top of a content page.
 *
 * One split button: the main half opens this page in ChatGPT; the ⌄ half
 * opens a menu with Ask Cursor and Copy page. Plain JS. No tracking, no
 * cookies, no network calls: the Markdown is built from the page in this tab,
 * so it is always the page as it is now.
 *
 * Use: put <div class="page-menu" data-page-menu></div> where the button
 * goes (reserve 44px of height inline, so nothing moves when it fills in),
 * and load this file with <script src="/page-menu.js" defer></script>.
 * One copy of this file is shared by every elghaly site; edit them together.
 */
(function () {
  "use strict";

  var slots = document.querySelectorAll("[data-page-menu]");
  if (!slots.length) return;

  // 44px tall: a full touch target, the size of the buttons beside it.
  var CSS =
    ".pm{position:relative;display:inline-flex;align-items:stretch;min-height:44px;" +
    "border:1px solid rgba(127,127,127,.45);border-radius:14px;font-size:1rem;line-height:1.2;" +
    "font-weight:600;background:rgba(127,127,127,.06)}" +
    ".pm-main,.pm-more>summary{display:inline-flex;align-items:center;justify-content:center;" +
    "color:inherit;cursor:pointer;-webkit-user-select:none;user-select:none;white-space:nowrap}" +
    // Logical corners: the browser picks the outer edge from the text
    // direction, so a language switch to Arabic needs no script to follow it.
    ".pm-main{gap:.55rem;padding:0 1.1rem;border-start-start-radius:13px;" +
    "border-end-start-radius:13px;text-decoration:none}" +
    ".pm-more{display:flex;border-inline-start:1px solid rgba(127,127,127,.45)}" +
    ".pm-more>summary{list-style:none;width:44px;border-start-end-radius:13px;" +
    "border-end-end-radius:13px}" +
    ".pm-more>summary::-webkit-details-marker{display:none}" +
    ".pm-main:hover,.pm-more>summary:hover,.pm-more[open]>summary{background:rgba(127,127,127,.16)}" +
    ".pm-main:focus-visible,.pm-more>summary:focus-visible{outline:2px solid currentColor;outline-offset:2px}" +
    ".pm-ico{width:18px;height:18px;flex:none}" +
    ".pm-more[open] .pm-chev{transform:rotate(180deg)}" +
    ".pm-panel{position:absolute;inset-inline-end:0;top:calc(100% + 6px);z-index:60;width:17rem;" +
    "max-width:calc(100vw - 32px);padding:.35rem;border:1px solid rgba(127,127,127,.45);" +
    "border-radius:14px;box-shadow:0 12px 32px rgba(0,0,0,.38);text-align:start;font-weight:500}" +
    ".pm-panel a,.pm-panel button{display:flex;flex-direction:column;justify-content:center;" +
    "gap:.15rem;width:100%;min-height:44px;margin:0;padding:.5rem .75rem;border:0;" +
    "border-radius:10px;background:none;color:inherit;font:inherit;text-align:start;" +
    "text-decoration:none;cursor:pointer}" +
    ".pm-panel a:hover,.pm-panel button:hover,.pm-panel a:focus-visible,.pm-panel button:focus-visible" +
    "{background:rgba(127,127,127,.18);outline:none}" +
    ".pm-panel .pm-sub{font-size:.8rem;font-weight:400;opacity:.75}" +
    ".pm-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}";

  // Drawn inline, so the button needs no image request and takes the text
  // colour of whatever page it sits on.
  var SPARK =
    '<svg class="pm-ico" viewBox="0 0 24 24" aria-hidden="true" fill="currentColor">' +
    '<path d="M12 2.5l1.9 5.6 5.6 1.9-5.6 1.9L12 17.5l-1.9-5.6L4.5 10l5.6-1.9z"/>' +
    '<path d="M19 15.5l.8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8z"/></svg>';
  var CHEV =
    '<svg class="pm-ico pm-chev" viewBox="0 0 24 24" aria-hidden="true" fill="none" ' +
    'stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">' +
    '<path d="M6 9l6 6 6-6"/></svg>';

  function addStyle() {
    if (document.getElementById("pm-style")) return;
    var s = document.createElement("style");
    s.id = "pm-style";
    s.textContent = CSS;
    document.head.appendChild(s);
  }

  // ── the page's own address ──────────────────────────────────────────────
  function pageUrl() {
    var link = document.querySelector('link[rel="canonical"]');
    var href = link && link.getAttribute("href");
    if (href) {
      try {
        return new URL(href, location.href).href;
      } catch (e) { /* fall through */ }
    }
    return location.origin + location.pathname;
  }

  function prompt() {
    return "Read " + pageUrl() + " and help me with it";
  }

  // ── HTML → Markdown ─────────────────────────────────────────────────────
  var SKIP = {
    SCRIPT: 1, STYLE: 1, NOSCRIPT: 1, TEMPLATE: 1, SVG: 1, CANVAS: 1, IFRAME: 1,
    BUTTON: 1, INPUT: 1, SELECT: 1, TEXTAREA: 1, FORM: 1, NAV: 1, DIALOG: 1,
    VIDEO: 1, AUDIO: 1, OBJECT: 1, EMBED: 1, LINK: 1, META: 1
  };
  var INLINE = {
    A: 1, ABBR: 1, B: 1, BDI: 1, BDO: 1, CITE: 1, CODE: 1, DATA: 1, DFN: 1, EM: 1,
    I: 1, KBD: 1, LABEL: 1, MARK: 1, Q: 1, S: 1, SAMP: 1, SMALL: 1, SPAN: 1,
    STRONG: 1, SUB: 1, SUP: 1, TIME: 1, U: 1, VAR: 1, WBR: 1, BR: 1, IMG: 1, DEL: 1, INS: 1
  };

  function hidden(el) {
    if (el.hidden || el.getAttribute("aria-hidden") === "true") return true;
    if (el.hasAttribute("data-page-menu") || el.hasAttribute("data-md-skip")) return true;
    if (el.classList && (el.classList.contains("skip-link") || el.classList.contains("lic-badges"))) {
      return true;
    }
    var cs = window.getComputedStyle(el);
    return cs.display === "none" || cs.visibility === "hidden";
  }

  // True when el is on screen and not inside anything the conversion skips:
  // hidden() looks at one element, this looks at the whole way up.
  function shown(el) {
    if (!el.getClientRects().length) return false;
    for (var e = el; e && e !== document.documentElement; e = e.parentElement) {
      if (SKIP[e.tagName] || hidden(e)) return false;
    }
    return true;
  }

  function abs(url) {
    try {
      return new URL(url, location.href).href;
    } catch (e) {
      return url;
    }
  }

  function squash(s) {
    return s.replace(/[ \t\r\n\f]+/g, " ");
  }

  function inline(node) {
    if (node.nodeType === 3) return squash(node.nodeValue);
    if (node.nodeType !== 1) return "";
    var el = node, tag = el.tagName;
    if (SKIP[tag] || hidden(el)) return "";
    if (tag === "BR") return "\n";
    if (tag === "IMG") {
      var alt = (el.getAttribute("alt") || "").trim();
      return alt ? "![" + alt + "](" + abs(el.getAttribute("src") || "") + ")" : "";
    }
    var text = "";
    for (var c = el.firstChild; c; c = c.nextSibling) text += inline(c);
    var t = text.trim();
    if (!t) return text.indexOf("\n") >= 0 ? "\n" : (text ? " " : "");
    var lead = /^\s/.test(text) ? " " : "", tail = /\s$/.test(text) ? " " : "";
    switch (tag) {
      case "A": {
        var href = el.getAttribute("href") || "";
        if (!href || /^\s*javascript:/i.test(href) || href.charAt(0) === "#") return text;
        var url = abs(href);
        return lead + (url === t ? "<" + url + ">" : "[" + t + "](" + url + ")") + tail;
      }
      case "STRONG": case "B": return lead + "**" + t + "**" + tail;
      case "EM": case "I": return lead + "*" + t + "*" + tail;
      case "CODE": case "KBD": case "SAMP": return lead + "`" + t + "`" + tail;
      case "DEL": case "S": return lead + "~~" + t + "~~" + tail;
      default: return text;
    }
  }

  function inlineOf(el) {
    var s = "";
    for (var c = el.firstChild; c; c = c.nextSibling) s += inline(c);
    return s.replace(/ *\n */g, "\n").replace(/ {2,}/g, " ").trim();
  }

  function list(el, depth) {
    var ordered = el.tagName === "OL", n = 1, lines = [];
    var pad = new Array(depth + 1).join("   ");
    for (var li = el.firstElementChild; li; li = li.nextElementSibling) {
      if (li.tagName !== "LI" || hidden(li)) continue;
      var text = "", nested = [];
      for (var c = li.firstChild; c; c = c.nextSibling) {
        if (c.nodeType === 1 && (c.tagName === "UL" || c.tagName === "OL")) {
          if (!hidden(c)) nested.push(list(c, depth + 1));
        } else if (c.nodeType === 1 && !INLINE[c.tagName]) {
          if (!SKIP[c.tagName] && !hidden(c)) text += " " + inlineOf(c) + " ";
        } else {
          text += inline(c);
        }
      }
      text = text.replace(/\s+/g, " ").trim();
      if (!text && !nested.length) continue;
      lines.push(pad + (ordered ? n++ + ". " : "- ") + text);
      for (var k = 0; k < nested.length; k++) lines.push(nested[k]);
    }
    return lines.join("\n");
  }

  function table(el) {
    var rows = [], width = 0;
    var trs = el.querySelectorAll("tr");
    for (var i = 0; i < trs.length; i++) {
      if (hidden(trs[i])) continue;
      var cells = [];
      for (var c = trs[i].firstElementChild; c; c = c.nextElementSibling) {
        if (c.tagName === "TD" || c.tagName === "TH") {
          cells.push(
            inlineOf(c)
              .replace(/\n/g, " ")
              .replace(/\\/g, "\\\\")
              .replace(/\|/g, "\\|")
          );
        }
      }
      if (cells.length) {
        rows.push(cells);
        width = Math.max(width, cells.length);
      }
    }
    if (!rows.length) return "";
    var out = [];
    for (var r = 0; r < rows.length; r++) {
      while (rows[r].length < width) rows[r].push("");
      out.push("| " + rows[r].join(" | ") + " |");
      if (r === 0) out.push("|" + new Array(width + 1).join(" --- |"));
    }
    return out.join("\n");
  }

  function blocks(root, out) {
    var para = "";
    function flush() {
      var p = para.replace(/ *\n */g, "\n").replace(/ {2,}/g, " ").trim();
      if (p) out.push(p);
      para = "";
    }
    for (var node = root.firstChild; node; node = node.nextSibling) {
      if (node.nodeType === 3) {
        para += squash(node.nodeValue);
        continue;
      }
      if (node.nodeType !== 1) continue;
      var el = node, tag = el.tagName;
      if (SKIP[tag] || hidden(el)) continue;
      if (INLINE[tag]) {
        para += inline(el);
        continue;
      }
      flush();
      var m = /^H([1-6])$/.exec(tag);
      // A logo <h1> is the site's name, not this page's heading.
      if (m && m[1] === "1" && isLogo(el)) continue;
      if (m) {
        var h = inlineOf(el).replace(/\n/g, " ");
        if (h) out.push(new Array(+m[1] + 1).join("#") + " " + h);
      } else if (tag === "P") {
        var p = inlineOf(el);
        if (p) out.push(p);
      } else if (tag === "UL" || tag === "OL") {
        var l = list(el, 0);
        if (l) out.push(l);
      } else if (tag === "PRE") {
        var code = (el.textContent || "").replace(/\n+$/, "");
        if (code.trim()) out.push("```\n" + code + "\n```");
      } else if (tag === "BLOCKQUOTE") {
        var inner = [];
        blocks(el, inner);
        if (inner.length) out.push(inner.join("\n\n").replace(/^/gm, "> "));
      } else if (tag === "TABLE") {
        var t = table(el);
        if (t) out.push(t);
      } else if (tag === "HR") {
        out.push("---");
      } else if (tag === "DT") {
        var dt = inlineOf(el);
        if (dt) out.push("**" + dt + "**");
      } else if (tag === "SUMMARY") {
        var s = inlineOf(el);
        if (s) out.push("**" + s + "**");
      } else if (tag === "FIGCAPTION") {
        var f = inlineOf(el);
        if (f) out.push("*" + f + "*");
      } else {
        blocks(el, out);
      }
    }
    flush();
  }

  function contentRoot() {
    var marked = document.querySelector("[data-md-root]");
    if (marked) return marked;
    var mains = document.querySelectorAll("main");
    if (mains.length === 1) return mains[0];
    // An <article> is only the page when it is the only one: on a page of
    // cards, the first card is not the page.
    var articles = document.querySelectorAll("article");
    if (!mains.length && articles.length === 1) return articles[0];
    return document.body;
  }

  function text(el) {
    return (el.textContent || "").replace(/\s+/g, " ").trim();
  }

  // An <h1> that is all link or all image is a site logo, not a page title.
  // So is one inside a link (<a href="/"><h1>Brand</h1></a>).
  function isLogo(h) {
    if (h.parentElement && h.parentElement.closest("a[href]")) return true;
    var t = text(h), links = h.querySelectorAll("a[href]");
    for (var i = 0; i < links.length; i++) if (text(links[i]) === t) return true;
    return !t && !!h.querySelector("img, svg");
  }

  // A visible <h1> that is not a logo: the page's own title.
  function isTitleH1(h) {
    return shown(h) && !isLogo(h);
  }

  // The page's own title: the first visible <h1> that is not a logo and not
  // in site chrome (it is called while chrome is marked), else the document
  // title. On these sites a hero <h1> often sits in a page-level <header>
  // above <main>. On a page of cards (two or more <article>s) a card's <h1>
  // is that card's title, not the page's, unless the content root is that
  // card.
  function pageTitle(root) {
    var cards = document.querySelectorAll("article").length > 1;
    var hs = document.querySelectorAll("h1");
    for (var i = 0; i < hs.length; i++) {
      var h = hs[i];
      if (!isTitleH1(h)) continue;
      if (cards) {
        var card = h.closest("article");
        if (card && card !== root && !card.contains(root)) continue;
      }
      var t = inlineOf(h).replace(/\s+/g, " ").trim();
      if (t) return t;
    }
    return (document.title || "").trim();
  }

  // Site chrome: a page-level <header>/<footer> (HTML's own landmark rule:
  // inside an <article> or <section> it carries that block's title or
  // date), every <nav>, and the banner/navigation/contentinfo roles. A
  // page-level <header> that holds the page's own title (a visible <h1>
  // that is not a logo) is the page's hero and is not chrome. Everything is
  // decided before anything is marked, so one mark cannot change the next
  // decision.
  function siteChrome() {
    var found = document.body.querySelectorAll(
      "footer, nav, header, [role=banner], [role=navigation], [role=contentinfo]");
    var chrome = [];
    for (var i = 0; i < found.length; i++) {
      var el = found[i], tag = el.tagName;
      if (tag === "HEADER" || tag === "FOOTER") {
        var up = el.parentElement;
        if (up && up.closest("article, aside, main, nav, section")) continue;
        if (tag === "HEADER" && [].some.call(el.querySelectorAll("h1"), isTitleH1)) continue;
      }
      chrome.push(el);
    }
    return chrome;
  }

  function toMarkdown() {
    var root = contentRoot(), out = [], title = "";
    // Chrome stays marked while the body is converted and while the title
    // is chosen, so neither can come from a footer, a nav or a logo banner.
    // Outside a <body> root the marks only touch elements the root does not
    // contain.
    var chrome = siteChrome();
    for (var k = 0; k < chrome.length; k++) chrome[k].setAttribute("data-md-skip", "");
    try {
      blocks(root, out);
      title = pageTitle(root);
    } finally {
      for (var j = 0; j < chrome.length; j++) chrome[j].removeAttribute("data-md-skip");
    }
    // The copy always opens with the page's own title. If the first <h1>
    // that came out is something else (a card's, say), the title goes on
    // top; if it is the title, nothing is added.
    var first = "";
    for (var b = 0; b < out.length; b++) {
      if (/^# /.test(out[b])) { first = out[b].slice(2).trim(); break; }
    }
    var md = out.join("\n\n").replace(/\n{3,}/g, "\n\n").trim();
    if (title && first !== title) md = "# " + title + "\n\n" + md;
    return md + "\n\n---\nSource: " + pageUrl() + "\n";
  }

  // ── actions ─────────────────────────────────────────────────────────────
  function legacyCopy(text) {
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.cssText = "position:fixed;top:0;left:0;width:1px;height:1px;opacity:0;font-size:16px";
    document.body.appendChild(ta);
    ta.focus();
    ta.select();
    try { ta.setSelectionRange(0, text.length); } catch (e) { /* older engines */ }
    var ok = false;
    try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
    document.body.removeChild(ta);
    return ok;
  }

  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text).then(
        function () { return true; },
        function () { return legacyCopy(text); }
      );
    }
    return Promise.resolve(legacyCopy(text));
  }

  function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  // Opens a plain-text view of the Markdown in a new tab. A tab written from
  // here works the same in iPhone Safari as on a desktop; a blob: link in a
  // new tab does not always.
  function viewMarkdown(text) {
    var w = window.open("", "_blank");
    if (!w) return false;
    var d = w.document;
    d.open();
    d.write(
      '<!doctype html><html lang="en"><head><meta charset="utf-8">' +
      '<meta name="viewport" content="width=device-width,initial-scale=1">' +
      '<meta name="robots" content="noindex"><title>' +
      escapeHtml((document.title || "page") + ".md") + "</title></head>" +
      '<body style="margin:0;background:#fff;color:#111">' +
      '<pre style="margin:0;padding:16px;white-space:pre-wrap;word-wrap:break-word;' +
      'font:14px/1.55 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">' +
      escapeHtml(text) + "</pre></body></html>"
    );
    d.close();
    return true;
  }

  function panelBackground(from) {
    for (var el = from; el && el.nodeType === 1; el = el.parentElement) {
      var bg = window.getComputedStyle(el).backgroundColor;
      if (bg && bg !== "transparent" && !/rgba\(\s*0,\s*0,\s*0,\s*0\s*\)/.test(bg)) return bg;
    }
    var root = window.getComputedStyle(document.documentElement).backgroundColor;
    return root && root !== "rgba(0, 0, 0, 0)" ? root : "#111";
  }

  // ── render ──────────────────────────────────────────────────────────────
  function chatgptUrl(q) { return "https://chatgpt.com/?q=" + q; }

  // The ⌄ menu: Cursor, then Copy. ChatGPT is the button itself.
  var ITEMS = [
    { href: function (q) { return "https://cursor.com/link/prompt?text=" + q; }, label: "Ask Cursor" },
    { act: "copy", label: "Copy page", sub: "Markdown for AI tools" }
  ];

  function build(slot) {
    var q = encodeURIComponent(prompt());
    var box = document.createElement("div");
    box.className = "pm";
    box.setAttribute("role", "group");
    box.setAttribute("aria-label", "Ask AI about this page");

    var main = document.createElement("a");
    main.className = "pm-main";
    main.href = chatgptUrl(q);
    main.target = "_blank";
    main.rel = "noopener noreferrer";
    main.innerHTML = SPARK + "<span>Ask ChatGPT</span>";

    var details = document.createElement("details");
    details.className = "pm-more";
    var summary = document.createElement("summary");
    summary.setAttribute("aria-label", "More AI options: Ask Cursor, copy page");
    summary.innerHTML = CHEV;
    var panel = document.createElement("div");
    panel.className = "pm-panel";
    var live = document.createElement("span");
    live.className = "pm-sr";
    live.setAttribute("aria-live", "polite");

    ITEMS.forEach(function (it) {
      var el;
      if (it.act) {
        el = document.createElement("button");
        el.type = "button";
        el.setAttribute("data-pm", it.act);
      } else {
        el = document.createElement("a");
        el.href = it.href(q);
        el.target = "_blank";
        el.rel = "noopener noreferrer";
      }
      var label = document.createElement("span");
      label.textContent = it.label + (it.href ? " ↗" : "");
      el.appendChild(label);
      if (it.sub) {
        var sub = document.createElement("span");
        sub.className = "pm-sub";
        sub.textContent = it.sub;
        el.appendChild(sub);
      }
      panel.appendChild(el);
    });

    details.appendChild(summary);
    // The panel hangs off the whole button (.pm is the positioned box), so
    // it lines up with the button's edge rather than the ⌄ half.
    details.appendChild(panel);
    box.appendChild(main);
    box.appendChild(details);
    slot.appendChild(box);
    slot.appendChild(live);

    details.addEventListener("toggle", function () {
      if (!details.open) return;
      panel.style.background = panelBackground(slot);
    });

    panel.addEventListener("click", function (e) {
      var target = e.target.closest ? e.target.closest("a,button") : null;
      if (!target) return;
      var act = target.getAttribute("data-pm");
      if (act === "copy") {
        var first = target.firstChild;
        copyText(toMarkdown()).then(function (ok) {
          first.textContent = ok ? "Copied ✓" : "Copy failed";
          live.textContent = ok ? "Page copied as Markdown" : "Copy failed";
          setTimeout(function () {
            first.textContent = "Copy page";
            live.textContent = "";
            details.open = false;
          }, 1400);
        });
        return;
      }
      if (act === "md") {
        if (!viewMarkdown(toMarkdown())) {
          live.textContent = "The browser blocked the new tab";
        }
      }
      details.open = false;
    });

    document.addEventListener("click", function (e) {
      if (details.open && !details.contains(e.target)) details.open = false;
    });
    document.addEventListener("keydown", function (e) {
      if (details.open && (e.key === "Escape" || e.key === "Esc")) {
        details.open = false;
        summary.focus();
      }
    });
  }

  addStyle();
  for (var i = 0; i < slots.length; i++) build(slots[i]);

  // For tests and for anyone curious: the same Markdown the menu copies.
  window.pageMenuMarkdown = toMarkdown;
})();

/* QUAY35 — Chatting link, EN/AR/RU/ZH contact lines, home hero (runs after page menu). */
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
    if (mailPos === -1) return "elghaly, LLC \u00B7 " + text;
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

  ensureChatLink();
  initLangSwitch();
})();
