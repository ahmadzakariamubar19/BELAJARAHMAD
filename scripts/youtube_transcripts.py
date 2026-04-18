#!/usr/bin/env python3
"""Download YouTube captions (no API key) and save as Markdown.

Uses the public caption tracks that YouTube exposes; requires
``youtube-transcript-api`` (see requirements.txt).
"""

from __future__ import annotations

import argparse
import re
import sys
import textwrap
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import CouldNotRetrieveTranscript, YouTubeTranscriptApi

DEFAULT_URL = "https://www.youtube.com/watch?v=L2baqhX1sMg"
DEFAULT_TITLE = "Chris Walker Transcript"
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = REPO_ROOT / "research" / "youtube-transcripts" / "chris-walker-video1.md"


def extract_video_id(url_or_id: str) -> str:
    """Return 11-character video id from a watch URL, short URL, or raw id."""
    s = url_or_id.strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", s):
        return s

    parsed = urlparse(s)
    host = (parsed.hostname or "").lower()

    if host in ("youtu.be", "www.youtu.be"):
        seg = parsed.path.strip("/").split("/")[0]
        if len(seg) == 11:
            return seg

    if "youtube" in host:
        if parsed.path.rstrip("/") == "/watch":
            v = parse_qs(parsed.query).get("v", [None])[0]
            if v and len(v) >= 11:
                return v[:11]
        parts = [p for p in parsed.path.split("/") if p]
        if len(parts) >= 2 and parts[0] in ("embed", "v", "shorts", "live"):
            cand = parts[1]
            if len(cand) == 11:
                return cand

    raise ValueError(f"Could not parse a YouTube video id from: {url_or_id!r}")


def transcript_to_paragraphs(snippets, width: int = 92) -> str:
    """Join caption snippets into wrapped prose for readable Markdown."""
    words = " ".join(sn.text.strip() for sn in snippets if sn.text and sn.text.strip())
    if not words:
        return ""
    return textwrap.fill(words, width=width)


def build_markdown(*, title: str, page_url: str, video_id: str, body: str) -> str:
    lines = [
        f"# {title}",
        "",
        f"- **Source:** {page_url}",
        f"- **Video ID:** `{video_id}`",
        "",
        body.strip(),
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Save a YouTube transcript as Markdown.")
    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help="Full YouTube URL or 11-character video id (default: Chris Walker video)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output .md path (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--title",
        default=DEFAULT_TITLE,
        help="Heading text for the Markdown file",
    )
    parser.add_argument(
        "--one-line-per-snippet",
        action="store_true",
        help="Write each caption segment on its own line instead of wrapped prose",
    )
    args = parser.parse_args()

    try:
        video_id = extract_video_id(args.url)
    except ValueError as e:
        print(e, file=sys.stderr)
        return 1

    watch_url = args.url if "youtube" in args.url or "youtu.be" in args.url else f"https://www.youtube.com/watch?v={video_id}"

    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)
    except CouldNotRetrieveTranscript as e:
        print(f"Could not load transcript: {e}", file=sys.stderr)
        return 1

    if args.one_line_per_snippet:
        body = "\n".join(sn.text for sn in transcript)
    else:
        body = transcript_to_paragraphs(transcript)

    markdown = build_markdown(
        title=args.title,
        page_url=watch_url,
        video_id=video_id,
        body=body,
    )

    out: Path = args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(markdown, encoding="utf-8")
    print(f"Wrote {out} ({len(transcript)} segments)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
