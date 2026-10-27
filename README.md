# AI News Daily Archive

A small automated archive of AI news. GitHub Actions runs every day and creates or refreshes a date-based Markdown digest in `news/YYYY-MM-DD.md`.

## How it works

- Collects recent headlines from configured AI and technology RSS feeds.
- Saves each day's digest under `news/` using the Asia/Kolkata date.
- Includes article title, source, publication date, link, and a short feed-provided summary when available.
- Removes duplicate links and skips articles without a usable title or URL.
- Can also be run manually from the **Actions** tab.

## Run locally

Python 3.10 or newer is recommended.

```bash
python -m pip install -r requirements.txt
python scripts/fetch_ai_news.py
```

The script creates `news/YYYY-MM-DD.md` for the current date in India time. If feeds are temporarily unavailable, it writes a note in the dated file instead of failing silently.

## Automatic schedule

The workflow in `.github/workflows/daily-ai-news.yml` runs daily at 02:30 UTC (08:00 India Standard Time). GitHub Actions can delay scheduled jobs during busy periods. You can also run it manually using **Actions → Daily AI News → Run workflow**.

## Sources

The script reads public RSS feeds from technology and AI publishers. Each item links to its original publisher; summaries are based on feed descriptions and should be read in context at the source.

## Important

This is a headline digest, not a guarantee of exhaustive coverage or independent fact-checking. Always open the original article for full details.