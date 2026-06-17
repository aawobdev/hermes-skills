#!/usr/bin/env bash
set -euo pipefail

# Sync local Hermes memory → shared/learnings.md in hermes-skills repo
# Designed to run as a Hermes cron job. Uses hermes -z for LLM curation.
#
# Flow: git pull → read local memory → LLM curates into learnings.md → git commit + push
# Safe to run repeatedly — idempotent (only commits if content changes).

REPO_DIR="${HERMES_SKILLS_DIR:-$HOME/projects/hermes-skills}"
LEARNINGS_FILE="$REPO_DIR/shared/learnings.md"
MEMORY_FILE="$HOME/.hermes/memories/MEMORY.md"
USER_FILE="$HOME/.hermes/memories/USER.md"
HOST=$(hostname -s)

# --- Check prerequisites ---
if [[ ! -d "$REPO_DIR/.git" ]]; then
  echo "ERROR: $REPO_DIR is not a git repo. Set HERMES_SKILLS_DIR env var."
  exit 1
fi

if [[ ! -f "$MEMORY_FILE" ]]; then
  echo "No local memory file found at $MEMORY_FILE. Nothing to sync."
  exit 0
fi

# --- Git pull (best effort — fail silently if offline) ---
cd "$REPO_DIR"
git pull --ff-only --quiet 2>/dev/null || true

# --- Build the LLM prompt ---
LOCAL_MEMORY=$(cat "$MEMORY_FILE" 2>/dev/null)
LOCAL_USER=$(cat "$USER_FILE" 2>/dev/null)
EXISTING_LEARNINGS=$(cat "$LEARNINGS_FILE" 2>/dev/null || echo "(empty — first sync)")

PROMPT="You are curating a shared learnings file for AI coding agents.

Read the local Hermes memory and the existing shared learnings file below.
Produce an updated shared/learnings.md that:

1. Merges any new durable facts from local memory into the existing file
2. Keeps only facts useful to ANY AI coding agent (project ports, known issues, user preferences, environment facts, conventions)
3. Removes Hermes-specific operational details (delegation command syntax, tool-specific quirks)
4. Removes task progress, session outcomes, commit SHAs, PR numbers — anything stale in a week
5. Groups by section: User, Projects, Conventions
6. Maximum 2500 chars total. One fact per line. Concise.

Do NOT remove facts from the existing file unless they are clearly stale/contradicted.
Do NOT add commentary or explanations — just the curated facts.

--- LOCAL HERMES MEMORY (MEMORY.md) ---
$LOCAL_MEMORY

--- LOCAL USER PROFILE (USER.md) ---
$LOCAL_USER

--- EXISTING SHARED LEARNINGS ---
$EXISTING_LEARNINGS

Write the complete updated learnings.md to stdout. No preamble, no code fences."

# --- Run LLM curation ---
UPDATED_LEARNINGS=$(hermes -z "$PROMPT" 2>/dev/null)

if [[ -z "$UPDATED_LEARNINGS" ]]; then
  echo "LLM returned empty output. Skipping sync."
  exit 0
fi

# --- Strip any leading/trailing whitespace ---
UPDATED_LEARNINGS=$(echo "$UPDATED_LEARNINGS" | sed -e '/^```/d' | head -c 3000)

# --- Check if anything actually changed ---
if [[ "$UPDATED_LEARNINGS" == "$EXISTING_LEARNINGS" ]]; then
  echo "No changes. Learnings file already up to date."
  exit 0
fi

# --- Write, commit, push ---
echo "$UPDATED_LEARNINGS" > "$LEARNINGS_FILE"

git add shared/learnings.md
git commit --quiet -m "sync: memory → shared/learnings.md from $HOST" || {
  echo "Nothing to commit (no changes)."
  exit 0
}
git push --quiet 2>/dev/null || {
  echo "Push failed (offline or conflict). Changes committed locally — will push next run."
  exit 0
}

echo "Synced learnings from $HOST. Pushed to remote."
