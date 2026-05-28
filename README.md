# github_commits

Pulls your GitHub commits across one or more repos and writes them to a text file, grouped by date.

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

Output is always written to `my_commits.txt` next to the script.

## Output format

```
2025-05-26
1. [owner/repo-a] fix login redirect
2. [owner/repo-b] bump dependency

2025-05-27
1. [owner/repo-a] add unit tests for auth
```
