#!/usr/bin/env python3
"""Fetch GitHub commits by author across one or more repos."""

import argparse
import json
import urllib.error
import urllib.request
from collections import defaultdict
from urllib.parse import urlparse

GITHUB_API = "https://api.github.com"
OUTPUT_FILE = "my_commits.json"

with open("config.json") as f:
    CONFIG = json.load(f)
TOKEN = CONFIG["github_token"]
AUTHOR = CONFIG["author_email"]


def github_get(url):
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {TOKEN}",
    })
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read()), resp.headers


def paginate(url):
    while url:
        page, headers = github_get(url)
        yield from page
        url = None
        for part in (headers.get("Link") or "").split(","):
            if 'rel="next"' in part:
                url = part[part.index("<") + 1 : part.index(">")]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repos", nargs="?", help="comma-separated GitHub repo URLs (default: all accessible)")
    args = parser.parse_args()

    if args.repos:
        repos = [urlparse(u).path.strip("/") for u in args.repos.split(",") if u.strip()]
    else:
        repos = [r["full_name"] for r in paginate(f"{GITHUB_API}/user/repos?per_page=100")]

    grouped = defaultdict(list)
    for repo in repos:
        url = f"{GITHUB_API}/repos/{repo}/commits?author={AUTHOR}&per_page=100"
        try:
            commits = list(paginate(url))
        except urllib.error.HTTPError:
            continue
        for c in commits:
            if len(c["parents"]) > 1:
                continue
            date = c["commit"]["author"]["date"][:10]
            message = c["commit"]["message"].splitlines()[0]
            grouped[date].append({"repo": repo, "message": message})

    output = {date: grouped[date] for date in sorted(grouped)}
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    total = sum(len(v) for v in grouped.values())
    print(f"Wrote {total} commits across {len(grouped)} dates -> {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
