# AI Pulse — Daily AI News

<p align="center">
  <strong>Your daily signal in artificial intelligence.</strong><br>
  A searchable, image-led AI news briefing and automatically updated news archive.
</p>

<p align="center">
  <a href="https://rohankashyap5526.github.io/AI_news/"><strong>🌐 View Live Website →</strong></a>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white">
  <img alt="GitHub Actions" src="https://img.shields.io/badge/Automation-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white">
  <img alt="Frontend" src="https://img.shields.io/badge/Frontend-HTML%20%7C%20CSS%20%7C%20JavaScript-E34F26">
  <img alt="License" src="https://img.shields.io/badge/License-Not%20specified-lightgrey">
</p>

**AI Pulse** collects recent artificial intelligence and technology headlines from public RSS feeds, creates a daily Markdown and JSON digest, and publishes a responsive website. Browse stories by topic or date, search headlines, view publisher images when available, and follow each story to its original source.

**Repository:** [Rohankashyap5526/AI_news](https://github.com/Rohankashyap5526/AI_news)

---

## Contents

- [Highlights](#highlights)
- [How it works](#how-it-works)
- [News sources](#news-sources)
- [Website features](#website-features)
- [Project structure](#project-structure)
- [Run locally](#run-locally)
- [Generated files](#generated-files)
- [Automation and deployment](#automation-and-deployment)
- [Configuration](#configuration)
- [Limitations and attribution](#limitations-and-attribution)

## Highlights

- Automatically collects AI news from configured public RSS feeds.
- Generates a dated Markdown digest and a JSON file for each collection day.
- Maintains a combined JSON archive for the website.
- Collects up to 50 unique stories per run.
- Removes duplicate article links and skips entries without a valid title or URL.
- Extracts article images from RSS media fields and, when needed, the publisher page's Open Graph or Twitter image metadata.
- Uses Asia/Kolkata (IST) for digest dates and publication timestamps.
- Deploys the static website through GitHub Pages using GitHub Actions.

## How it works

1. GitHub Actions starts the collection workflow on its daily schedule, or when manually triggered.
2. The Python script reads the configured RSS feeds and normalizes the returned articles.
3. Duplicate links and invalid entries are filtered out.
4. The script attempts to find a relevant publisher image for each story.
5. It writes the daily Markdown and JSON files and rebuilds `news/index.json`.
6. The deployment job publishes the website and news archive to GitHub Pages.

The website reads `news/index.json` in the browser. It does not require a database or a separate backend server.

## News sources

The collector currently uses these feeds:

| Feed | Coverage |
|---|---|
| Google News — Artificial Intelligence | AI developments and generative AI |
| Google News — Machine Learning | Machine learning, LLMs and related research |
| Google News — OpenAI | OpenAI and ChatGPT updates |
| Google News — Google DeepMind | Google, DeepMind and Gemini updates |
| Google News — Anthropic | Anthropic and Claude updates |
| MIT Technology Review | Technology and AI reporting |
| OpenAI News | Official OpenAI announcements |

Feed availability and the number of stories returned can vary from day to day.

## Website features

### News discovery
- Search across story titles, summaries and publishers.
- Topic filters for AI, Machine Learning, OpenAI, Google / DeepMind and Anthropic.
- Date filtering and sorting by newest, oldest or title.
- Paginated results, with 12 stories per page.
- Featured story layout and readable news cards.

### Story reading
- Dedicated article-detail pages.
- Publisher, publication date and available article image.
- Feed-provided story summary when available.
- Direct link to the original publisher for the complete report.

### Reading experience
- Responsive layout for desktop and mobile screens.
- Light and dark themes, with the selected theme saved in the browser.
- Keyboard shortcut `/` to focus the search field.
- Newsroom statistics based on the loaded archive.

> **Note:** Article detail pages display a feed preview, not a copy of the full publisher article. Use the original-source link for complete reporting.

## Project structure

```text
AI_news/
├── .github/
│   └── workflows/
│       └── daily-ai-news.yml   # Collection and GitHub Pages deployment
├── news/
│   ├── YYYY-MM-DD.md           # Daily readable digest
│   ├── YYYY-MM-DD.json         # Daily structured article data
│   └── index.json              # Combined archive used by the website
├── scripts/
│   └── fetch_ai_news.py        # RSS collection and digest generator
├── article.html                # Individual story page
├── article.js                  # Loads and displays a selected story
├── app.js                      # Search, filters, sorting and pagination
├── index.html                  # AI Pulse homepage
├── styles.css                  # Website styling and responsive layouts
└── requirements.txt            # Python dependencies
```

The `news/YYYY-MM-DD.*` files are generated by the collection script. The `news/index.json` file is rebuilt from the available daily JSON archives.

## Run locally

### Requirements

- Python 3.10 or newer
- Git
- An internet connection to retrieve RSS feeds and publisher images

### 1. Clone the repository

```bash
git clone https://github.com/Rohankashyap5526/AI_news.git
cd AI_news
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

The current Python dependency is `feedparser`.

### 3. Generate the latest digest

```bash
python scripts/fetch_ai_news.py
```

The script creates or updates the daily digest and the combined archive in the `news/` directory. If no articles are collected, it exits with an error rather than publishing an empty digest.

### 4. View the website

From the repository root, start a local static server:

```bash
python -m http.server 8000
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

Run the collector before opening the site if `news/index.json` does not exist or you want to refresh the local data.

## Generated files

For a successful run on a given IST date, the collector generates:

| File | Purpose |
|---|---|
| `news/YYYY-MM-DD.md` | Human-readable daily digest |
| `news/YYYY-MM-DD.json` | Structured data for that day's stories |
| `news/index.json` | Combined archive consumed by the website |

Each article can include its title, source/feed, publication time, original URL, summary and image URL. Image extraction is best-effort, so some stories may not have an image.

## Automation and deployment

The workflow is defined in [`.github/workflows/daily-ai-news.yml`](.github/workflows/daily-ai-news.yml).

| Trigger | Behaviour |
|---|---|
| Daily schedule | Runs at **02:30 UTC (08:00 IST)** |
| Manual dispatch | Can be started from the GitHub Actions tab |
| Push to `main` | Runs the collection and deployment workflow |

### Run it manually

1. Open the repository on GitHub.
2. Select **Actions**.
3. Open **Daily AI News**.
4. Select **Run workflow** and confirm the `main` branch.

### GitHub Pages setup

To publish the website:

1. Open **Settings → Pages** in the repository.
2. Set the build and deployment source to **GitHub Actions**.
3. Ensure Actions are enabled and the workflow has the required Pages permissions.
4. Check the deployment job in the Actions tab for its result and published URL.

GitHub may delay scheduled workflow runs during periods of high load, so 08:00 IST is the configured schedule rather than a guaranteed exact publication time.

## Configuration

To change the news feeds, edit the `FEEDS` list in `scripts/fetch_ai_news.py`.

The collector's current limits are:

- Maximum 12 entries considered from each feed.
- Maximum 50 stories in a daily digest.
- Best-effort publisher image lookup for up to 50 stories.
- Publisher page image lookup timeout of 5 seconds.

After changing the feeds or collection logic, run the script locally to verify the output.

## Limitations and attribution

- AI Pulse is a news discovery and headline aggregation project, not a news publisher.
- Headlines, summaries, images and article links originate from third-party feeds or publisher pages.
- Summaries are feed-provided excerpts; they are not independently researched or fact-checked by this project.
- Publisher images may be unavailable, blocked, changed or removed. The site displays a fallback when an image cannot load.
- Feed outages, rate limits and publisher changes can affect collection results.
- Always visit the original publisher for the complete story, context and corrections.
- Third-party content remains the property of its respective publishers and rights holders.

---

<p align="center">
  Built with Python, HTML, CSS, JavaScript and GitHub Actions.<br>
  <strong>AI Pulse — Built for the AI-curious.</strong>
</p>
