#!/bin/bash

API_URL="https://api.github.com"

# # GitHub username and personal access token
USERNAME="$USERNAME"
TOKEN="$TOKEN"

# User and Repository information
REPO_OWNER="$1"
REPO_NAME="$2"

# Function to make a GET request to the GitHub API
github_api_get() {
	local endpoint="$1"
	local url="${API_URL}/${endpoint}"
	curl -s -u "${USERNAME}:${TOKEN}" "$url"
}


list_pull_requests() {
	echo "=== PULL REQUEST ==="
	github_api_get "repos/${REPO_OWNER}/${REPO_NAME}/pulls" |
		jq -r '.[] | "PR #\(.number): \(.title)"'
}

list_commits() {
	echo "=== Commits ==="
	github_api_get "repos/${REPO_OWNER}/${REPO_NAME}/commits" |
		jq -r '.[] | "Commit #\(.sha): \(.commit.message)"'
}

list_pull_requests
list_commits
