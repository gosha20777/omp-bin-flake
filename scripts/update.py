#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import urllib.request

REPO = "can1357/oh-my-pi"
SOURCES_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sources.json")

def main():
    headers = {"User-Agent": "omp-bin-flake-updater"}
    github_token = os.environ.get("GITHUB_TOKEN")
    if github_token:
        headers["Authorization"] = f"token {github_token}"

    req = urllib.request.Request(f"https://api.github.com/repos/{REPO}/releases/latest", headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"Error fetching latest release: {e}", file=sys.stderr)
        sys.exit(1)

    tag = data["tag_name"]
    latest_version = tag.lstrip("v")

    with open(SOURCES_FILE, "r") as f:
        current_sources = json.load(f)

    current_version = current_sources.get("version")
    print(f"Current version: {current_version}")
    print(f"Latest version:  {latest_version}")

    if current_version == latest_version and "--force" not in sys.argv:
        print("Already up to date.")
        return

    assets = {
        "x86_64-linux": f"https://github.com/{REPO}/releases/download/{tag}/omp-linux-x64",
        "aarch64-linux": f"https://github.com/{REPO}/releases/download/{tag}/omp-linux-arm64",
        "aarch64-darwin": f"https://github.com/{REPO}/releases/download/{tag}/omp-darwin-arm64",
    }

    new_sources = {"version": latest_version}

    for sys_name, url in assets.items():
        print(f"Prefetching {sys_name} from {url}...")
        res = subprocess.run(
            ["nix", "store", "prefetch-file", url, "--json"],
            capture_output=True,
            text=True,
            check=True
        )
        info = json.loads(res.stdout)
        new_sources[sys_name] = {
            "url": url,
            "hash": info["hash"]
        }

    with open(SOURCES_FILE, "w") as f:
        json.dump(new_sources, f, indent=2)
        f.write("\n")

    print(f"Successfully updated sources.json to {latest_version}")

if __name__ == "__main__":
    main()
