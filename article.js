const root = document.getElementById("articleContent");
const params = new URLSearchParams(location.search);
const target = params.get("id");
function hashStory(story) {
 let h = 2166136261;
 for (const char of (story.link || story.title || "")) {
  h ^= char.charCodeAt(0);
  h = Math.imul(h, 16777619);
 }
 return (h >>> 0).toString(36);
}
function putText(parent, tag, value, className) {
 const node = document.createElement(tag);
 node.textContent = value;
 if (className) node.className = className;
 parent.appendChild(node);
 return node;
}
function safeLink(value) {
 try {
  const url = new URL(value);
  return ["http:", "https:"].includes(url.protocol) ? url.href : null;
 } catch { return null; }
}
async function showArticle() {
 try {
  const response = await fetch("./news/index.json", {cache:"no-store"});
  if (!response.ok) throw new Error("Feed unavailable");
  const data = await response.json();
  const story = (data.articles || []).find(item => hashStory(item) === target);
  if (!story) throw new Error("Story not found");
  root.replaceChildren();
  document.title = story.title + " — AI Pulse";
  putText(root, "div", "AI PULSE / DAILY BRIEFING", "article-category");
  putText(root, "h1", story.title, "article-title");
  const byline = document.createElement("div");
  byline.className = "article-byline";
  putText(byline, "span", story.source || "News publisher");
  putText(byline, "span", story.published || story.date || "");
  root.appendChild(byline);
  const imageUrl = safeLink(story.image);
  if (imageUrl) {
   const frame = document.createElement("div");
   frame.className = "article-cover";
   const img = document.createElement("img");
   img.src = imageUrl;
   img.alt = "Publisher image accompanying this article";
   img.referrerPolicy = "no-referrer";
   img.addEventListener("error", () => frame.remove());
   frame.appendChild(img);
   root.appendChild(frame);
  }
  const body = document.createElement("div");
  body.className = "article-body";
  putText(body, "h2", "Story overview");
  const summary = (story.summary || "").trim();
  putText(body, "p", summary && summary.toLowerCase() !== story.title.toLowerCase() ? summary : "The publisher feed does not provide a detailed summary for this story.");
  putText(body, "p", "This is a feed preview. Read the original publisher for the complete report and context.", "article-disclaimer");
  const sourceUrl = safeLink(story.link);
  if (sourceUrl) {
   const link = putText(body, "a", "Read full article at source ↗", "primary-button");
   link.href = sourceUrl;
   link.target = "_blank";
   link.rel = "noopener noreferrer";
  }
  root.appendChild(body);
 } catch {
  root.replaceChildren();
  putText(root, "h2", "Article unavailable");
  const back = putText(root, "a", "Return to newsroom", "read-link");
  back.href = "./#latest";
 }
}
showArticle();
