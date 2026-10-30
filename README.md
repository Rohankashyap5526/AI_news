# AI Pulse — Daily AI News

An automated AI news archive with a responsive website. GitHub Actions collects daily headlines, stores Markdown and JSON digests, and deploys the AI Pulse website with GitHub Pages.

## How it works

- Collects recent headlines from configured AI and technology RSS feeds.
- Saves each day's digest under `news/` using the Asia/Kolkata date.
- Publishes JSON files for the website and a searchable archive index.
- Deploys the responsive AI Pulse website to GitHub Pages after each successful daily collection.
- Includes article title, source, publication date, link, and a short feed-provided summary when available.
- Removes duplicate links and skips articles without a usable title or URL.
- Can also be run manually from the **Actions** tab.

## Run locally

Python 3.10 or newer is recommended.

```bash
python -m pip install -r requirements.txt
python scripts/fetch_ai_news.py
```

The script creates `news/YYYY-MM-DD.md`, `news/YYYY-MM-DD.json`, and refreshes `news/index.json`. If no articles are collected, it exits with an error so the workflow does not publish an empty digest.

## Automatic schedule

The workflow in `.github/workflows/daily-ai-news.yml` runs daily at 02:30 UTC (08:00 India Standard Time). GitHub Actions can delay scheduled jobs during busy periods. You can also run it manually using **Actions → Daily AI News → Run workflow**.

## Website

The site uses plain HTML, CSS, and JavaScript. It includes headline search, topic filters, date selection, a featured story, responsive layouts, and a light/dark theme toggle. GitHub Actions deploys it to GitHub Pages after each successful daily collection.

## Sources

The script reads public RSS feeds from technology and AI publishers. Each item links to its original publisher; summaries are based on feed descriptions and should be read in context at the source.

## Important

This is a headline digest, not a guarantee of exhaustive coverage or independent fact-checking. Always open the original article for full details.