#!/usr/bin/env python3
"""Check every link in the awesome list still returns a healthy status.

An awesome list is only useful if its links work, so this script re-checks
them all. It runs weekly in CI (see .github/workflows/links.yml) and I run
it by hand before adding new entries.

Usage:
    python scripts/check_links.py               # check README.md
    python scripts/check_links.py --file X.md   # check another file
    python scripts/check_links.py --dry-run     # list links, don't fetch
    python scripts/check_links.py --strict      # also fail on unreachable hosts

Exit codes: 0 = all links fine, 1 = at least one link is broken (4xx/5xx),
2 = usage error (missing file, bad flags).

Unreachable hosts (DNS failure, timeout, TLS error) are warnings, not
failures, unless --strict is passed. Some hosts block datacenter IPs or
rate-limit HEAD requests, and a link that is merely unreachable from here
is not the same as a dead link.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass

DEFAULT_TIMEOUT_SECONDS = 10
MAX_WORKERS = 8
USER_AGENT = "awesome-minecraft-bots-link-checker/1.0"

# Matches [text](url) but not ![alt](url) image links, and not bare anchors.
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


@dataclass
class LinkResult:
    """One checked link and what happened when we fetched it."""

    url: str
    status: str  # "ok" | "broken" | "unreachable"
    detail: str


def extract_links(text: str) -> list[str]:
    """Pull unique http(s) URLs out of markdown link syntax, in order.

    Skips image links, same-page anchors (#...) and mailto: links.
    """
    seen: set[str] = set()
    links: list[str] = []
    for match in LINK_PATTERN.finditer(text):
        url = match.group(1)
        if url.startswith("#") or url.startswith("mailto:"):
            continue
        if not url.startswith(("http://", "https://")):
            continue
        if url not in seen:
            seen.add(url)
            links.append(url)
    return links


def _fetch(url: str, method: str, timeout: float) -> int:
    """One request; returns the HTTP status code, raising on transport errors."""
    request = urllib.request.Request(
        url, method=method, headers={"User-Agent": USER_AGENT}
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.status


def check_url(url: str, timeout: float = DEFAULT_TIMEOUT_SECONDS) -> LinkResult:
    """Check a single URL. HEAD first, GET as a fallback for servers that
    reject HEAD (some hosts answer 405 to HEAD but serve GET fine)."""
    try:
        status = _fetch(url, "HEAD", timeout)
        return LinkResult(url, "ok", f"HTTP {status}")
    except urllib.error.HTTPError as error:
        if error.code in (405, 501):
            try:
                status = _fetch(url, "GET", timeout)
                return LinkResult(url, "ok", f"HTTP {status} (via GET)")
            except urllib.error.HTTPError as get_error:
                return LinkResult(url, "broken", f"HTTP {get_error.code}")
            except urllib.error.URLError as get_error:
                return LinkResult(url, "unreachable", str(get_error.reason))
        if error.code == 403:
            # 403 from a HEAD usually means bot-blocking, not a dead link:
            # retry with GET, and treat a second 403 as unreachable, since
            # the server is clearly alive and answering.
            try:
                status = _fetch(url, "GET", timeout)
                return LinkResult(url, "ok", f"HTTP {status} (via GET)")
            except urllib.error.HTTPError:
                return LinkResult(url, "unreachable", "HTTP 403 (bot-blocked?)")
            except urllib.error.URLError as get_error:
                return LinkResult(url, "unreachable", str(get_error.reason))
        return LinkResult(url, "broken", f"HTTP {error.code}")
    except urllib.error.URLError as error:
        return LinkResult(url, "unreachable", str(error.reason))
    except (TimeoutError, OSError) as error:
        return LinkResult(url, "unreachable", str(error))


def check_links(
    urls: list[str],
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    workers: int = MAX_WORKERS,
) -> list[LinkResult]:
    """Check all URLs concurrently, keeping the results in input order."""
    if not urls:
        return []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(lambda url: check_url(url, timeout), urls))


def main(argv: list[str] | None = None) -> int:
    """Parse args, check links, print a report, return an exit code."""
    parser = argparse.ArgumentParser(
        description="Check every link in a markdown file still works."
    )
    parser.add_argument("--file", default="README.md", help="markdown file to check")
    parser.add_argument(
        "--dry-run", action="store_true", help="list links without fetching them"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="also fail when a host is unreachable (default: warn only)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT_SECONDS,
        help="seconds to wait per link",
    )
    parser.add_argument("--workers", type=int, default=MAX_WORKERS)
    args = parser.parse_args(argv)

    try:
        with open(args.file, encoding="utf-8") as handle:
            text = handle.read()
    except OSError as error:
        print(f"error: can't read {args.file}: {error.strerror}", file=sys.stderr)
        return 2

    urls = extract_links(text)
    print(f"{len(urls)} links in {args.file}")
    if args.dry_run:
        for url in urls:
            print(f"  {url}")
        return 0

    results = check_links(urls, timeout=args.timeout, workers=args.workers)
    broken = [r for r in results if r.status == "broken"]
    unreachable = [r for r in results if r.status == "unreachable"]

    for result in results:
        mark = {"ok": "OK ", "broken": "BAD", "unreachable": "???"}[result.status]
        print(f"[{mark}] {result.url} — {result.detail}")

    print(f"\n{len(results) - len(broken) - len(unreachable)} ok, "
          f"{len(broken)} broken, {len(unreachable)} unreachable")
    if unreachable:
        print("Unreachable links are warnings (host may block this network); "
              "re-run with --strict to fail on them.")
    if broken:
        return 1
    if unreachable and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
