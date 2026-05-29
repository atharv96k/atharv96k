import urllib.request
import json
import re
import os

token = os.environ.get("GITHUB_TOKEN", "")
username = os.environ.get("USERNAME", "atharv96k")

url = f"https://api.github.com/search/issues?q=is:pr+author:{username}&per_page=100&sort=created&order=desc"
req = urllib.request.Request(url)
req.add_header("Authorization", f"token {token}")
req.add_header("Accept", "application/vnd.github.v3+json")
req.add_header("User-Agent", "readme-updater")

with urllib.request.urlopen(req) as response:
    data = json.loads(response.read())

all_rows = []
for pr in data["items"]:
    title = pr["title"]
    html_url = pr["html_url"]
    repo = pr["repository_url"].replace("https://api.github.com/repos/", "")
    state = pr["state"]
    merged = pr.get("pull_request", {}).get("merged_at")

    if merged:
        status = "✅ Merged"
    elif state == "open":
        status = "🟡 Open"
    else:
        continue

    all_rows.append(f"| [{title}]({html_url}) | `{repo}` | {status} |")

# Show only last 5
preview_rows = all_rows[:5]
total = len(all_rows)

table = "| 🔀 Pull Request | 📦 Repository | 📅 Status |\n"
table += "|---|---|---|\n"
table += "\n".join(preview_rows)

# "See More" link → opens GitHub PR search for this user
see_more_url = f"https://github.com/search?q=is%3Apr+author%3A{username}&type=pullrequests&s=created&o=desc"
table += f"\n\n> Showing **5 of {total}** pull requests. [🔍 See all →]({see_more_url})"

with open("README.md", "r") as f:
    content = f.read()

new_content = re.sub(
    r"(<!-- PR_TABLE_START -->).*?(<!-- PR_TABLE_END -->)",
    f"<!-- PR_TABLE_START -->\n{table}\n<!-- PR_TABLE_END -->",
    content,
    flags=re.DOTALL
)

with open("README.md", "w") as f:
    f.write(new_content)

print(f"README updated: showing 5 of {total} PRs")
