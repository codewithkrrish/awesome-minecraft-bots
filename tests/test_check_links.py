"""Tests for scripts/check_links.py.

Only the parsing and the status logic are tested here — the live network is
not a test dependency. Where a fetch is involved, urlopen is mocked.
"""

from __future__ import annotations

import sys
import urllib.error
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import check_links  # noqa: E402


def test_extract_links_finds_markdown_links() -> None:
    text = "- [mineflayer](https://github.com/PrismarineJS/mineflayer) — the one.\n"
    assert check_links.extract_links(text) == [
        "https://github.com/PrismarineJS/mineflayer"
    ]


def test_extract_links_dedupes_and_keeps_order() -> None:
    text = (
        "[a](https://example.com/one) [b](https://example.com/two) "
        "[a again](https://example.com/one)"
    )
    assert check_links.extract_links(text) == [
        "https://example.com/one",
        "https://example.com/two",
    ]


def test_extract_links_skips_images_anchors_and_mailto() -> None:
    text = (
        "![badge](https://example.com/badge.svg)\n"
        "[section](#my-setup)\n"
        "[mail](mailto:someone@example.com)\n"
        "[real](https://example.com/real)\n"
    )
    assert check_links.extract_links(text) == ["https://example.com/real"]


def test_extract_links_ignores_non_http() -> None:
    assert check_links.extract_links("[local](CONTRIBUTING.md)") == []


def test_check_url_ok_on_200() -> None:
    response = MagicMock()
    response.status = 200
    response.__enter__.return_value = response
    with patch.object(check_links.urllib.request, "urlopen", return_value=response):
        result = check_links.check_url("https://example.com")
    assert result.status == "ok"
    assert "200" in result.detail


def test_check_url_broken_on_404() -> None:
    with patch.object(
        check_links.urllib.request,
        "urlopen",
        side_effect=urllib.error.HTTPError("https://example.com", 404, "nope", {}, None),
    ):
        result = check_links.check_url("https://example.com/missing")
    assert result.status == "broken"
    assert "404" in result.detail


def test_check_url_falls_back_to_get_when_head_is_refused() -> None:
    head_error = urllib.error.HTTPError(
        "https://example.com", 405, "no head", {}, None
    )
    response = MagicMock()
    response.status = 200
    response.__enter__.return_value = response
    with patch.object(
        check_links.urllib.request,
        "urlopen",
        side_effect=[head_error, response],
    ):
        result = check_links.check_url("https://example.com")
    assert result.status == "ok"
    assert "GET" in result.detail


def test_check_url_403_retried_with_get_then_unreachable() -> None:
    error = urllib.error.HTTPError("https://example.com", 403, "denied", {}, None)
    with patch.object(
        check_links.urllib.request,
        "urlopen",
        side_effect=[error, error],
    ):
        result = check_links.check_url("https://example.com")
    assert result.status == "unreachable"
    assert "403" in result.detail


def test_check_url_unreachable_on_dns_failure() -> None:
    with patch.object(
        check_links.urllib.request,
        "urlopen",
        side_effect=urllib.error.URLError("no such host"),
    ):
        result = check_links.check_url("https://does-not-exist.example")
    assert result.status == "unreachable"


def test_main_dry_run_lists_links_and_does_not_fetch(tmp_path: Path) -> None:
    doc = tmp_path / "list.md"
    doc.write_text("[a](https://example.com/one)\n[b](https://example.com/two)\n")
    with patch.object(
        check_links.urllib.request, "urlopen", side_effect=AssertionError("no net")
    ):
        assert check_links.main(["--file", str(doc), "--dry-run"]) == 0


def test_main_missing_file_exits_2(capsys) -> None:
    assert check_links.main(["--file", "no-such-file.md"]) == 2
    assert "can't read" in capsys.readouterr().err


def test_main_broken_link_exits_1(tmp_path: Path) -> None:
    doc = tmp_path / "list.md"
    doc.write_text("[a](https://example.com/gone)\n")
    with patch.object(
        check_links.urllib.request,
        "urlopen",
        side_effect=urllib.error.HTTPError("https://example.com", 404, "no", {}, None),
    ):
        assert check_links.main(["--file", str(doc)]) == 1


def test_main_unreachable_is_warning_by_default_but_fails_strict(
    tmp_path: Path,
) -> None:
    doc = tmp_path / "list.md"
    doc.write_text("[a](https://example.com/)\n")
    with patch.object(
        check_links.urllib.request,
        "urlopen",
        side_effect=urllib.error.URLError("blocked"),
    ):
        assert check_links.main(["--file", str(doc)]) == 0
        assert check_links.main(["--file", str(doc), "--strict"]) == 1


def test_readme_has_no_duplicate_links() -> None:
    readme = Path(__file__).resolve().parents[1] / "README.md"
    links = check_links.extract_links(readme.read_text(encoding="utf-8"))
    assert len(links) == len(set(links))
    # Sanity: the list should actually be a list.
    assert len(links) >= 30
