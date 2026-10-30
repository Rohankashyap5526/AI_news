#!/usr/bin/env python3
"""Fetch a daily AI news digest from public RSS feeds."""

from __future__ import annotations

import calendar
import html
import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import urlparse

import feedparser

ROOT = Path(__file__).resolve().parents[1]
NEWS_DIR = ROOT / "news"
IST = timezone(timedelta(hours=5, minutes=30))
MAX_ITEMS_PER_FEED = 12
MAX_TOTAL_ITEMS = 50
TIMEOUT_NOTE = "Feeds can occasionally be unavailable or rate-limited. Run the workflow again later if this digest is incomplete."

FEEDS = [
    ("Google News — Artificial Intelligence", "https://news.google.com/rss/search?q=artificial+intelligence+OR+generative+AI+when:2d&hl=en-US&gl=US&ceid=US:en"),
    ("Google News — Machine Learning", "https://news.google.com/rss/search?q=machine+learning+OR+LLM+when:2d&hl=en-US&gl=US&ceid=US:en"),
    ("Google News — OpenAI", "https://news.google.com/rss/search?q=OpenAI+OR+ChatGPT+when:2d&hl=en-US&gl=US&ceid=US:en"),
    ("Google News — Google DeepMind", "https://news.google.com/rss/search?q=Google+DeepMind+OR+Gemini+AI+when:2d&hl=en-US&gl=US&ceid=US:en"),
    ("Google News — Anthropic", "https://news.google.com/rss/search?q=Anthropic+Claude+AI+when:2d&hl=en-US&gl=US&ceid=US:en"),
    ("MIT Technology Review", "https://www.technologyreview.com/feed/"),
    ("OpenAI News", "https://openai.com/news/rss.xml"),
]

def clean_text(value: str, limit: int = 500) -> str:
    value = html.unescape(value or "")
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value[:limit].rstrip()

def safe_url(value: str) -> bool:
    try:
        return urlparse(value).scheme in {"http", "https"} and bool(urlparse(value).netloc)
    except ValueError:
        return False

def entry_date(entry) -> str:
    for field in ("published_parsed", "updated_parsed", "created_parsed"):
        parsed = entry.get(field)
        if parsed:
            try:
                return datetime.fromtimestamp(calendar.timegm(parsed), timezone.utc).astimezone(IST).strftime("%Y-%m-%d %H:%M IST")
            except (OverflowError, OSError, ValueError):
                pass
    return "Date not provided by feed"

def fetch_items():
    items = []
    seen = set()
    feed_errors = []
    for source, url in FEEDS:
        try:
            parsed = feedparser.parse(url, request_headers={"User-Agent": "AI-News-Daily-Archive/1.0"})
            if getattr(parsed, "bozo", False) and not parsed.entries:
                feed_errors.append(source)
                continue
            for entry in parsed.entries[:MAX_ITEMS_PER_FEED]:
                title = clean_text(entry.get("title", ""), 220)
                link = (entry.get("link") or "").strip()
                if not title or not safe_url(link):
                    continue
                normalized = link.split("#", 1)[0].rstrip("/")
                if normalized in seen:
                    continue
                seen.add(normalized)
                summary = clean_text(entry.get("summary", entry.get("description", "")), 600)
                items.append({
                    "title": title,
                    "link": link,
                    "source": source,
                    "published": entry_date(entry),
                    "summary": summary,
                })
        except Exception as exc:
            print(f"Warning: could not read {source}: {exc}", file=sys.stderr)
            feed_errors.append(source)
    items.sort(key=lambda item: item["published"] == "Date not provided by feed")
    return items[:MAX_TOTAL_ITEMS], feed_errors

def build_markdown(day: str, items: list[dict], feed_errors: list[str]) -> str:
    lines = [
        f"# AI News — {day}",
        "",
        f"> Daily digest generated on {datetime.now(IST).strftime('%Y-%m-%d %H:%M IST')}.",
        "",
    ]
    if items:
        for index, item in enumerate(items, start=1):
            lines.extend([
                f"## {index}. {item['title']}",
                "",
                f"- **Source/feed:** {item['source']}",
                f"- **Published:** {item['published']}",
                f"- **Article:** [{item['link']}]({item['link']})",
            ])
            if item["summary"]:
                lines.extend(["", item["summary"]])
            lines.append("")
    else:
        lines.extend([
            "No articles were retrieved during this run.",
            "",
            "This can happen when feeds are unavailable or return no recent items. Run the workflow again later.",
            "",
        ])
    lines.extend(["---", "", "## Collection notes", ""])
    lines.append(f"- Articles collected: **{len(items)}**.")
    lines.append("- Headlines and summaries are supplied by publisher feeds or news search feeds; follow the original links for full reporting.")
    if feed_errors:
        lines.append(f"- Feeds that could not be read: {', '.join(feed_errors)}.")
    if not items or feed_errors:
        lines.append(f"- {TIMEOUT_NOTE}")
    lines.append("")
    return "\n".join(lines)

def main() -> int:
    now = datetime.now(IST)
    day = now.strftime("%Y-%m-%d")
    NEWS_DIR.mkdir(parents=True, exist_ok=True)
    items, feed_errors = fetch_items()
    output = NEWS_DIR / f"{day}.md"
    if not items:
        print("No articles collected; refusing to publish an empty digest.", file=sys.stderr)
        return 1

    output.write_text(build_markdown(day, items, feed_errors), encoding="utf-8")
    day_payload = {
        "date": day,
        "generated_at": datetime.now(IST).isoformat(),
        "articles": [{**item, "date": day} for item in items],
        "feed_errors": feed_errors,
    }
    (NEWS_DIR / f"{day}.json").write_text(
        json.dumps(day_payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    archived_articles = []
    for archive in sorted(NEWS_DIR.glob("*.json")):
        if archive.name == "index.json":
            continue
        try:
            archived_articles.extend(
                json.loads(archive.read_text(encoding="utf-8")).get("articles", [])
            )
        except (OSError, json.JSONDecodeError) as exc:
            print(f"Warning: could not read {archive.name}: {exc}", file=sys.stderr)
    archived_articles.sort(key=lambda item: item.get("published", ""), reverse=True)
    index_payload = {
        "generated_at": datetime.now(IST).isoformat(),
        "latest_date": day,
        "total_articles": len(archived_articles),
        "articles": archived_articles,
    }
    (NEWS_DIR / "index.json").write_text(
        json.dumps(index_payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Wrote {output.relative_to(ROOT)} and JSON index with {len(items)} articles.")
    if feed_errors:
        print(f"Feeds unavailable: {', '.join(feed_errors)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
