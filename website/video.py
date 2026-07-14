"""Helpers for normalizing product video URLs into embeddable sources."""

from __future__ import annotations

import re
from urllib.parse import parse_qs, urlparse


_IFRAME_SRC_RE = re.compile(
    r"""src\s*=\s*["']([^"']+)["']""",
    re.IGNORECASE,
)
_YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be", "www.youtu.be"}
_VIMEO_HOSTS = {"vimeo.com", "www.vimeo.com", "player.vimeo.com"}


def _host(netloc: str) -> str:
    return (netloc or "").lower().split(":")[0]


def youtube_embed_url(url: str) -> str | None:
    """Return a youtube.com/embed/ URL, or None if not a YouTube link."""
    parsed = urlparse(url.strip())
    host = _host(parsed.netloc)
    if host not in _YOUTUBE_HOSTS:
        return None

    video_id = ""
    if host in {"youtu.be", "www.youtu.be"}:
        video_id = parsed.path.strip("/").split("/")[0]
    elif parsed.path.startswith("/embed/"):
        video_id = parsed.path.split("/embed/", 1)[-1].split("/")[0]
    elif parsed.path.startswith("/shorts/"):
        video_id = parsed.path.split("/shorts/", 1)[-1].split("/")[0]
    else:
        video_id = parse_qs(parsed.query).get("v", [""])[0]

    video_id = video_id.strip()
    if not video_id:
        return None
    return f"https://www.youtube.com/embed/{video_id}"


def vimeo_embed_url(url: str) -> str | None:
    """Return a player.vimeo.com/video/ URL, or None if not a Vimeo link."""
    parsed = urlparse(url.strip())
    host = _host(parsed.netloc)
    if host not in _VIMEO_HOSTS:
        return None

    if host == "player.vimeo.com" and parsed.path.startswith("/video/"):
        video_id = parsed.path.split("/video/", 1)[-1].split("/")[0]
    else:
        parts = [p for p in parsed.path.split("/") if p]
        video_id = parts[-1] if parts else ""

    video_id = video_id.strip()
    if not video_id.isdigit():
        return None
    return f"https://player.vimeo.com/video/{video_id}"


def resolve_video_embed_url(value: str) -> str:
    """
    Accept a YouTube/Vimeo watch URL, short link, embed URL, or legacy iframe HTML.
    Returns an embeddable src URL, or "" when nothing usable is found.
    """
    raw = (value or "").strip()
    if not raw:
        return ""

    # Reason: older admin rows may still store full <iframe> markup.
    if "<iframe" in raw.lower():
        match = _IFRAME_SRC_RE.search(raw)
        if not match:
            return ""
        raw = match.group(1).strip()

    for resolver in (youtube_embed_url, vimeo_embed_url):
        embed = resolver(raw)
        if embed:
            return embed

    parsed = urlparse(raw)
    if parsed.scheme in {"http", "https"} and parsed.netloc:
        return raw
    return ""
