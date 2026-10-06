"""
Paginates the Substack public API for a publication and writes all post
slugs + metadata to posts.json.

Run this first, then use the slug list to drive WebFetch in Claude.

Usage:
    python collect_posts.py                  # all time, default publication
    python collect_posts.py 2024-01-01       # cutoff date
"""

import json
import sys
import urllib.request
from datetime import datetime, timezone

PUBLICATION_URL = "https://lorenzouriel.substack.com"
CUTOFF_DEFAULT = datetime(2024, 1, 1, tzinfo=timezone.utc)
OUTPUT_FILE = "posts.json"
PAGE_SIZE = 12

def fetch_page(offset):
    url = f"{PUBLICATION_URL}/api/v1/archive?sort=new&offset={offset}&limit={PAGE_SIZE}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def main():
    cutoff_str = sys.argv[1] if len(sys.argv) > 1 else None
    cutoff = datetime.fromisoformat(cutoff_str).replace(tzinfo=timezone.utc) if cutoff_str else CUTOFF_DEFAULT

    all_posts = {}
    offset = 0
    page = 0

    while True:
        page += 1
        print(f"  Fetching page {page} (offset {offset})...")
        posts = fetch_page(offset)

        if not posts:
            print("  Empty response — done.")
            break

        new = 0
        for post in posts:
            slug = post.get("slug", "")
            post_type = post.get("type", "newsletter")
            if not slug or post_type not in ("newsletter", "post"):
                continue
            if slug not in all_posts:
                post_date_raw = post.get("post_date", "")
                all_posts[slug] = {
                    "slug": slug,
                    "title": post.get("title", ""),
                    "post_date": post_date_raw,
                    "canonical_url": post.get("canonical_url", f"{PUBLICATION_URL}/p/{slug}"),
                    "audience": post.get("audience", "everyone"),
                }
                new += 1

        print(f"    Got {len(posts)} posts, {new} new (total unique: {len(all_posts)})")
        offset += PAGE_SIZE

    # Filter by cutoff
    def parse_date(s):
        try:
            dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except Exception:
            return datetime.min.replace(tzinfo=timezone.utc)

    filtered = [
        v for v in all_posts.values()
        if parse_date(v["post_date"]) >= cutoff
    ]
    filtered.sort(key=lambda x: x["post_date"])

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(filtered, f, indent=2, ensure_ascii=False)

    print(f"\nTotal unique posts:   {len(all_posts)}")
    print(f"After cutoff filter:  {len(filtered)}")
    print(f"Written to:           {OUTPUT_FILE}")

main()
