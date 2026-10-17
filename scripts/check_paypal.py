"""Check the PayPal Payments Standard links on this site.

Parses the HTML (stdlib only). A locked-price PayPal Payment Link
(paypal.com/ncp/payment/...) must be one listed in LOCKED, on the card whose
price matches that product. A plain Payments Standard link (cgi-bin/webscr)
fails when it pays the wrong account, the wrong amount or currency, uses the
wrong cmd for a one-time or monthly item, sends the buyer back to another
site, or disagrees with the price printed on its own card.

    python3 scripts/check_paypal.py
"""
import pathlib
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urlsplit, parse_qs

ROOT = pathlib.Path(__file__).resolve().parent.parent
# Payments Standard (cgi-bin/webscr) links are no longer used; any one found fails.
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Node:
    def __init__(self, tag, attrs, parent):
        self.tag, self.attrs, self.parent, self.children = tag, dict(attrs), parent, []

    def text(self):
        return "".join(c if isinstance(c, str) else c.text() for c in self.children)

    def classes(self):
        return (self.attrs.get("class") or "").split()

    def walk(self):
        for c in self.children:
            if isinstance(c, Node):
                yield c
                yield from c.walk()


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = self.cur = Node("#root", {}, None)

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur)
        self.cur.children.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.children.append(data)


def card_of(a):
    n = a.parent
    while n is not None and n.tag not in ("article", "section"):
        n = n.parent
    return n


def shown_price(card):
    for n in card.walk():
        if any(c in ("price", "seat-price") for c in n.classes()):
            t = n.text()
            m = re.search(r"\$\s*([\d,]+(?:\.\d\d)?)", t)
            if m:
                return "%.2f" % float(m.group(1).replace(",", "")), t
    return None, ""


def check(site, expected, pages, locked=None):
    locked = locked or {}
    host = urlsplit(site).hostname
    errors, seen = [], {}
    for rel in pages:
        tree = Tree()
        tree.feed((ROOT / rel).read_text(encoding="utf-8"))
        for a in tree.root.walk():
            href = a.attrs.get("href") or ""
            if a.tag != "a" or "paypal.com" not in href:
                continue
            where = "%s %s" % (rel, a.attrs.get("id") or a.text().strip())

            def bad(msg):
                errors.append("%s: %s" % (where, msg))

            u = urlsplit(href)
            if u.path.startswith("/ncp/payment/"):
                sku = locked.get(href)
                if u.scheme != "https" or u.hostname != "www.paypal.com" or sku is None:
                    bad("Payment Link not in LOCKED: " + href)
                    continue
                seen[sku] = seen.get(sku, 0) + 1
                amount, cycle = expected[sku]
                card = card_of(a)
                price, text = shown_price(card) if card else (None, "")
                if price != amount:
                    bad("card shows %r but %s is locked at %s" % (text.strip(), sku, amount))
                if "month" in text or cycle != "once":
                    bad("Payment Links here are one-time; %s is %s" % (sku, cycle))
                continue
            if u.scheme != "https" or u.hostname != "www.paypal.com" or u.path != "/cgi-bin/webscr":
                bad("not a PayPal Payments Standard URL: " + href)
                continue
            bad("Payments Standard link is not allowed; use a locked Payment Link or email ordering")
            q = {k: v[0] for k, v in parse_qs(u.query, keep_blank_values=True).items()}
            sku = q.get("item_number", "")
            if sku not in expected:
                bad("unknown item_number %r" % sku)
                continue
            seen[sku] = seen.get(sku, 0) + 1
            amount, cycle = expected[sku]
            if q.get("currency_code") != "USD":
                bad("currency_code is not USD")
            if not q.get("item_name"):
                bad("item_name missing")
            if cycle == "once":
                if q.get("cmd") != "_xclick":
                    bad("one-time item needs cmd=_xclick")
                got = q.get("amount")
            else:
                if q.get("cmd") != "_xclick-subscriptions":
                    bad("monthly item needs cmd=_xclick-subscriptions")
                if (q.get("p3"), q.get("t3"), q.get("src")) != ("1", "M", "1"):
                    bad("monthly item needs p3=1&t3=M&src=1")
                got = q.get("a3")
            if got != amount:
                bad("amount %s, expected %s" % (got, amount))
            for key in ("return", "cancel_return"):
                r = urlsplit(q.get(key, ""))
                if r.scheme != "https" or r.hostname != host:
                    bad("%s must be an https URL on %s" % (key, host))
            card = card_of(a)
            price, text = shown_price(card) if card else (None, "")
            if price != got:
                bad("card shows %r but the link pays %s" % (text.strip(), got))
            monthly_text = "month" in text
            if monthly_text != (cycle == "monthly"):
                bad("card says %r but the link is %s" % (text.strip(), cycle))
    for sku in expected:
        if sku not in seen:
            errors.append("no PayPal link for %s" % sku)
    for e in errors:
        print("FAIL", e)
    if errors:
        sys.exit(1)
    print("ok: %d PayPal links, %d products" % (sum(seen.values()), len(seen)))


SITE = "https://quay-35.elghaly.dev"
# sku: (amount, "once" | "monthly") — must match the prices on the product cards.
EXPECTED = {
    # quay-land and node-watch are ordered by email (mailto:support@elghaly.dev).
    "score-report": ("49.00", "once"),
    "flex-card-pack": ("29.00", "once"),
    "fee-review": ("199.00", "once"),
}
# Locked-price PayPal Payment Links: URL -> sku. The amount is fixed in PayPal.
LOCKED = {
    "https://www.paypal.com/ncp/payment/B27KHRX83CNP6": "fee-review",
    "https://www.paypal.com/ncp/payment/TA9ZAXCAGNUYY": "score-report",
    "https://www.paypal.com/ncp/payment/DDNVRBHA4952N": "flex-card-pack",
}
PAGES = ["index.html", "quay/fees.html"]

if __name__ == "__main__":
    check(SITE, EXPECTED, PAGES, LOCKED)
