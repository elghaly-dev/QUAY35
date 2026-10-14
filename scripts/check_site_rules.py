#!/usr/bin/env python3
"""House-rule checks for published HTML (stdlib only).

    python3 scripts/check_site_rules.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

FOOTER_URLS = [
    "https://chatting.elghaly.dev",
    "https://elghaly.dev/about.html",
    "https://elghaly.dev/contact.html",
    "https://elghaly.dev/delivery.html",
    "https://elghaly.dev/terms.html",
    "https://elghaly.dev/privacy.html",
]

FORBIDDEN_WORDS = re.compile(r"\b(live|profit|guarantee|audit|launched)\b", re.I)
FORBIDDEN = [
    (re.compile(r"qq\.com", re.I), "qq.com"),
    (re.compile(r"telegram", re.I), "Telegram"),
    (re.compile(r"t\.me/", re.I), "t.me link"),
    (re.compile(r"facebook\.com", re.I), "Facebook"),
]

SKIP_DIRS = {".git", ".github", "node_modules", "_templates", "scripts"}


def visible_html(raw: str) -> str:
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    raw = re.sub(r"<script[\s\S]*?</script>", "", raw, flags=re.I)
    raw = re.sub(r"<style[\s\S]*?</style>", "", raw, flags=re.I)
    return raw


def html_files():
    for path in sorted(ROOT.rglob("*.html")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def main():
    errors = []
    pages = list(html_files())
    if not pages:
        errors.append("no HTML pages found")

    index = ROOT / "index.html"
    if index.exists():
        index_text = index.read_text(encoding="utf-8")
        for url in FOOTER_URLS:
            if url not in index_text:
                errors.append("index.html missing footer URL %s" % url)
        if "elghaly, LLC" not in index_text:
            errors.append("index.html missing elghaly, LLC")
        if 'data-page-menu' not in index_text:
            errors.append("index.html missing page-menu slot")
        if "page-menu.js" not in index_text:
            errors.append("index.html missing page-menu.js script")

    for path in pages:
        rel = path.relative_to(ROOT)
        raw = path.read_text(encoding="utf-8")
        vis = visible_html(raw)
        for pat, label in FORBIDDEN:
            if pat.search(vis):
                errors.append("%s: forbidden %s" % (rel, label))
        for match in FORBIDDEN_WORDS.finditer(vis):
            errors.append("%s: forbidden word %r" % (rel, match.group(0)))

    for msg in errors:
        print("FAIL", msg)
    if errors:
        sys.exit(1)
    print("ok: %d HTML file(s), footer URLs on index" % len(pages))


if __name__ == "__main__":
    main()
