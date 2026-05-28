# github_commits

Pulls your GitHub commits across one or more repos and writes them to a JSON file, grouped by date.

## Setup

1. Create a `config.json` next to the script:

   ```json
   {
     "github_token": "ghp_xxx",
     "author_email": "you@example.com"
   }
   ```

   - `github_token` — a personal access token with `repo` scope (read access is enough). Create one at https://github.com/settings/tokens.
   - `author_email` — the email GitHub associates with your commits. Check it with `git config user.email` or on a commit's GitHub page.

2. Python 3.8+ is required. No third-party packages.

## Usage

```bash
# all repos your token can access
python3 github_commits.py

# one repo
python3 github_commits.py https://github.com/owner/repo

# multiple repos, comma-separated (quote it so the shell keeps it as one arg)
python3 github_commits.py "https://github.com/owner/a,https://github.com/owner/b"
```

Output is always written to `my_commits.json` next to the script. Merge commits (more than one parent) are skipped.

## Output format

A JSON object keyed by commit date (`YYYY-MM-DD`, sorted ascending). Each date maps to a list of commits, each with its `repo` (`owner/name`) and the first line of the commit `message`:

```json
{
  "2026-04-10": [
    {
      "repo": "REPO A",
      "message": "commit"
    },
    {
      "repo": "REPO B",
      "message": "commit1"
    }
  ],
  "2026-04-13": [
    {
      "repo": "REPO A",
      "message": "commit2"
    }
  ]
}
```
