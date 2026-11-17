![Codebreaker Challenge Stats (Unofficial)](assets/readme-banner.png)

<p align="center">
  <a href="#get-started"><img alt="Python: 3.9+" src="assets/badges/python.svg"></a>
  <a href="https://github.com/XSS3cut10n3r/CBC_Scraper-Rebuilt/actions/workflows/tests.yml"><img alt="CI status" src="https://github.com/XSS3cut10n3r/CBC_Scraper-Rebuilt/actions/workflows/tests.yml/badge.svg?branch=main"></a>
  <a href="pyproject.toml"><img alt="Project version: 0.2.0" src="assets/badges/version.svg"></a>
  <a href="COPYING"><img alt="License: GPL-3.0-or-later" src="assets/badges/license.svg"></a>
</p>

Based on [code-zm/cbc_scraper](https://github.com/code-zm/cbc_scraper). Thank you to [code-zm](https://github.com/code-zm) for creating the original project.

School leaderboards, fastest first solves, and your personal task times in the terminal.

## Fork changes

This fork adds one command and one helper script for exporting your own submission attempts. Everything else works as described in the original project below.

### `dump` command

Writes every submission attempt to a single file, grouped by task and sorted oldest first. Each entry has the timestamp, the submitted text, and the API response.

```sh
cbc-scraper dump                                  # fetch, then write data/all_attempts.txt
cbc-scraper dump --display                        # use saved data, no network
cbc-scraper dump --format json                    # raw rows, data/all_attempts.json
cbc-scraper dump --output ~/attempts.txt          # choose the file location
cbc-scraper dump --display --format json --output attempts.json
```

| Option | Effect |
|--------|--------|
| `--display` | Read `data/submission_stats.json` instead of contacting the site. Run `dump` or `submissions` once without it first. |
| `--format json` | Write the raw rows (including the original hex data) instead of text. |
| `--output PATH` | Write to PATH instead of the default under the data folder. |
| `--data-dir DIR` | Use a different data folder (default `data`). |

A normal `dump` run also refreshes the saved `data/submission_stats.json`, the same as `submissions`. `dump` is not in the interactive menu; run it from the command line. `--format csv` and `--all-years` are rejected.

Text output looks like this (sample data):

```text
Total submissions: 3

========================================================================
task1: 2 submissions
========================================================================

--- task1 #1 | 2026-10-01 12:00:00 UTC ---
Submission:
first try
API response:
wrong
```

The text format removes terminal control characters from submissions, as the existing history viewer does. Use `--format json` if you need the exact bytes.

### `extract_attempts.py`

Reads a text file made by `dump` and keeps only the submitted attempts: one per line, under a `# taskN` heading, with a blank line between tasks. It uses only the Python standard library. <!-- TODO: verify the script's location in this fork -->

```sh
python3 extract_attempts.py data/all_attempts.txt                  # print to screen
python3 extract_attempts.py data/all_attempts.txt -o attempts.txt  # write a file
python3 extract_attempts.py data/all_attempts.txt --unique         # drop repeats within a task
python3 extract_attempts.py data/all_attempts.txt --no-headers     # bare lines only
```

Output (sample data):

```text
# task1
first try
second try
```

If a submission contains a line break, it is written as a literal `\n` so each attempt stays on one line.

### Limitations

- `extract_attempts.py` reads the text format that `dump` writes, so changing that format would break the extractor.
- No automated tests cover `dump` or the extractor.

## Get started

```sh
python -m venv .venv
source .venv/bin/activate
pip install -e .
cbc-scraper
```

Choose **6. Set up / refresh browser login** from the menu. This creates `edit_this_request.txt` for you.

Open `edit_this_request.txt` and follow its comments to copy your browser's **Cookie** header. Paste it where indicated and save. The scraper finds it automatically. This file is ignored by Git. You can also paste a full **Copy as cURL** request there, replacing the Cookie line.

To refresh an expired login, choose **6** again and replace the cookies in the same file. Existing contents are preserved.

## Shortcuts

```sh
cbc-scraper submissions                       # Your attempts and times
cbc-scraper leaderboard --task 'Task 8'       # Earliest school solves
cbc-scraper leaderboard --school 'Georgia'   # Filter schools
cbc-scraper graphs                            # Overall, personal, and school graphs
cbc-scraper offline                           # All saved results, offline
cbc-scraper history                           # Browse submission text by task
```

**View progress and solve-time graphs** is option 4. Personal graphs include an `s` toggle for linear/logarithmic scales. School graphs compare registered participants’ solve rates with overall rates. Use `cbc-scraper graphs --display` for saved data.

Submission history shows the submitted content and API response, earliest first, in pages of 20. Select an entry number to read long text in full. Use `cbc-scraper history --display` to browse saved submissions offline.

**Solve Time** runs from the previous task's last submission to the current task's last submission. **Total** starts at your first task0 submission. Times include breaks; submissions are approximate completion markers.

More options: `cbc-scraper --help`. Login files and results stay local and are excluded from Git.

[GPL-3.0-or-later](COPYING).

## Non-affiliation notice

CBC Scraper Rebuilt is an independent, unofficial project. Neither this project nor its maintainers are affiliated with, sponsored by, endorsed by, or acting on behalf of the United States National Security Agency (NSA). This software and its accompanying documentation are not authored, published, distributed, approved, or supported by the NSA. References to the NSA, the Codebreaker Challenge, and associated names, logos, or imagery identify the challenge this tool supports and do not imply official status, authorization, or endorsement.
