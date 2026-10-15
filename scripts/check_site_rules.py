#!/usr/bin/env python3
"""House-rule checks for published HTML (stdlib only).

    python3 scripts/check_site_rules.py
"""
import pathlib
import re
import sys
from html.parser import HTMLParser

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


class _VisibleStrip(HTMLParser):
    __slots__ = ("_skip", "out")

    def __init__(self) -> None:
        super().__init__()
        self._skip = 0
        self.out: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag.lower() in ("script", "style"):
            self._skip += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in ("script", "style") and self._skip:
            self._skip -= 1

    def handle_data(self, data: str) -> None:
        if not self._skip:
            self.out.append(data)


def visible_text(raw: str) -> str:
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    parser = _VisibleStrip()
    parser.feed(raw)
    parser.close()
    return re.sub(r"\s+", " ", " ".join(parser.out))


def is_redirect(raw: str) -> bool:
    head = raw.split("</head>", 1)[0] if re.search(r"</head>", raw, re.I) else raw[:4000]
    return bool(re.search(r'<meta[^>]+http-equiv=["\']refresh["\']', head, re.I))


def is_full_page(path: pathlib.Path, raw: str) -> bool:
    if not re.search(r"<!DOCTYPE\s+html|<html\b", raw, re.I):
        return False
    if is_redirect(raw):
        return False
    return True


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
        if is_full_page(path, raw) and "elghaly, LLC" not in raw:
            errors.append("%s: missing elghaly, LLC" % rel)
        vis = visible_text(raw)
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
