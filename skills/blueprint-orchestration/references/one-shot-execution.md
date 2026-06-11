# One-Shot Execution: Practical Gotchas

Real-world lessons from running the one-shot pattern (`hermes -z` and `claude -p`).

## Prompt Delivery

### Problem: Shell quoting breaks complex prompts

On Windows (git-bash/MSYS), embedding multi-line JSON, model definitions, or special
characters inside `hermes -z "..."` causes shell parse errors — unmatched quotes,
backslash escapes, and variable expansion conflicts.

### Fix: Write prompt to a file, then pipe or cat

```bash
# Good — write prompt to temp file
cat > task-prompt.txt << 'PROMPT'
TASK N: Description
... multi-line content with "quotes", $vars, and special chars ...
PROMPT

# Then deliver via cat
hermes -z "$(cat task-prompt.txt)"

# Clean up
rm task-prompt.txt
```

The heredoc with single-quoted delimiter `'PROMPT'` prevents variable expansion and
backslash interpretation.

### Alternative: Pass via stdin (Linux/macOS)

```bash
cat task-prompt.txt | hermes -z
# Or
hermes -z < task-prompt.txt
```

## Timeout Handling

### Problem: `hermes -z` can exceed default timeout

For large tasks (project scaffold, multi-file refactors), the local model may need
5+ minutes. Hermes `-z` mode runs the full agent loop including tool calls.

### Fix: Set generous timeout

```bash
# terminal(timeout=300) — 5-minute ceiling for scaffold/init tasks
output=$(timeout 300 hermes -z "$(cat task-prompt.txt)" 2>&1)
```

If timeout still fires, the task may be too large — decompose into smaller one-shots.

### What 300s buys you

| Task type | Typical time | Notes |
|-----------|-------------|-------|
| Scaffold + npm install | 120-300s | npm install is the bottleneck |
| Single-file CRUD API | 30-90s | Fast on local models |
| Prisma schema + validate | 30-60s | Schema writing is fast |
| Migration + DB setup | 30-60s | Depends on Docker start |
| Full build (`next build`) | 30-120s | Separate from one-shot |

## Partial Completion

### Problem: The one-shot times out but the model made progress

`hermes -z` does real work during its run — writes files, runs commands. If it
times out, check what was already done before retrying:

```bash
# Check what was created during the timed-out one-shot
find . -name "*.ts" -type f -newer <start-marker-file> 2>/dev/null
ls -la <expected-output-dir>
```

Often the model created most of the files before the timeout. You can then:
1. Run `npm install` / `npm run build` to catch up on any missed steps
2. Hand-write the few missing files yourself
3. Re-run with a smaller, more focused prompt for just the remaining items

## Handoff Between Architect and Executor

### Problem: The one-shot executor has zero context

Each `hermes -z` session starts fresh — no memory of the blueprint, prior tasks,
or project structure. Every prompt must be fully self-contained.

### The minimum viable one-shot prompt template

```
TASK [N]: [short name]

Project: [2-3 lines: framework, key patterns, repo path]
Input files: [paths for the executor to read]
Output: [exact output contract — file names, schemas, commands]
Verify: [one command to confirm success — script, curl, ls]

Use ONLY what is provided below — invent nothing, escalate instead.
```

Test: if you paste the prompt into a fresh terminal with `hermes -z`, does the
executor have everything it needs? If not, add context.

## Post-One-Shot Verification

Always verify after every one-shot:

1. **Exit code** — non-zero means something failed mid-task
2. **Files on disk** — `ls` or `stat` expected output files
3. **Content quality** — read a few key files, check for placeholder stubs
4. **Run the Verify command** — the prompt should include this
5. **If partial** — salvage what was done, prompt again with only remaining items
6. **If empty/no output** — the model may have printed code instead of writing files
   (common with local models). Run `write_file` manually with the printed output.