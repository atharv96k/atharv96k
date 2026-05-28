import urllib.request
import json
import re
import os

token = os.environ.get("GITHUB_TOKEN", "")
username = os.environ.get("USERNAME", "atharv96k")

url = f"https://api.github.com/search/issues?q=is:pr+author:{username}&per_page=20&sort=created&order=desc"

req = urllib.request.Request(url)
req.add_header("Authorization", f"token {token}")
req.add_header("Accept", "application/vnd.github.v3+json")
req.add_header("User-Agent", "readme-updater")

with urllib.request.urlopen(req) as response:
    data = json.loads(response.read())

rows = []
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
    continue  # skip closed PRs

rows.append(f"| [{title}]({html_url}) | `{repo}` | {status} |")

table = "| 🔀 Pull Request | 📦 Repository | 📅 Status |\n"
table += "|---|---|---|\n"
table += "\n".join(rows)

with open("README.md", "r") as f:
    content = f.read()

# Replace between markers
new_content = re.sub(
    r"(<!-- PR_TABLE_START -->).*?(<!-- PR_TABLE_END -->)",
    f"<!-- PR_TABLE_START -->\n{table}\n<!-- PR_TABLE_END -->",
    content,
    flags=re.DOTALL
)

with open("README.md", "w") as f:
    f.write(new_content)

print("README updated successfully")
