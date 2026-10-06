"""
Paginates the Medium public API for @lorenzouriel and writes all article
slugs + publish dates to slugs.json.

Run this first, then use the slug list to drive WebFetch in Claude.

Usage:
    python collect_slugs.py                  # all time
    python collect_slugs.py 2024-01-01       # cutoff date
"""

import json
import sys
import urllib.request
from datetime import datetime, timezone

USER_ID = "79192a9d5fcb"
BASE_URL = f"https://medium.com/_/api/users/{USER_ID}/profile/stream"
CUTOFF_DEFAULT = datetime(2024, 1, 1, tzinfo=timezone.utc)
OUTPUT_FILE = "slugs.json"

def fetch_page(cursor=None):
    url = f"{BASE_URL}?limit=25&source=overview"
    if cursor:
        url += f"&to={cursor}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req) as resp:
        raw = resp.read().decode("utf-8")
        # Medium prepends ")]}'\n" as CSRF protection
        if raw.startswith(")]}'\n"):
            raw = raw[5:]
        return json.loads(raw)

def extract_posts(data):
    posts = []
    references = data.get("payload", {}).get("references", {})
    post_refs = references.get("Post", {})
    for post_id, post in post_refs.items():
        slug = post.get("uniqueSlug", "")
        published_at_ms = post.get("firstPublishedAt", 0)
        if slug and published_at_ms:
            posts.append({
                "slug": slug,
                "publishedAt": published_at_ms,
                "date": datetime.fromtimestamp(published_at_ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d"),
            })
    return posts

def main():
    cutoff_str = sys.argv[1] if len(sys.argv) > 1 else None
    cutoff = datetime.fromisoformat(cutoff_str).replace(tzinfo=timezone.utc) if cutoff_str else CUTOFF_DEFAULT

    all_slugs = {}
    cursor = None
    page = 0

    while True:
        page += 1
        print(f"  Fetching page {page}...")
        data = fetch_page(cursor)

        posts = extract_posts(data)
        new = 0
        for p in posts:
            if p["slug"] not in all_slugs:
                all_slugs[p["slug"]] = p
                new += 1

        print(f"    Got {len(posts)} posts, {new} new (total unique: {len(all_slugs)})")

        paging = data.get("payload", {}).get("paging", {})
        cursor = paging.get("to")
        if not cursor:
            break

    # Filter by cutoff
    filtered = [
        v for v in all_slugs.values()
        if datetime.fromtimestamp(v["publishedAt"] / 1000, tz=timezone.utc) >= cutoff
    ]
    filtered.sort(key=lambda x: x["publishedAt"])

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(filtered, f, indent=2, ensure_ascii=False)

    print(f"\nTotal unique slugs:   {len(all_slugs)}")
    print(f"After cutoff filter:  {len(filtered)}")
    print(f"Written to:           {OUTPUT_FILE}")

main()
