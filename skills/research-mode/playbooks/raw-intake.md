### Raw intake

State: progressing. Output: correctly named raw files in `data/raw/YYYY-MM-DD/`, each finished folder sealed by `.intake.log`. This is the only step allowed to change `data/raw/`, and only by renaming, moving, and quarantining. File contents never change.

Filename: `DDMMYY-HHMMSS_instrument.mode_[device-id]_library.study[_r.[remarks]][_f.[flags]][_NNN].ext`. The date folder only keeps a day's files together.

Rules the script follows (`scripts/raw_intake.py`):

- Date and time come from the file's own header, read through `raw-viewer files inspect` (instrument profiles belong to raw-viewer; this step only reads them). Without raw-viewer, or for a file no profile matches, the filename's `DDMMYY-HHMMSS` stays. A missing `HHMMSS` becomes `000000`. A missing `DDMMYY` comes from the folder name. A filename time is never overwritten by a missing header.
- `r.x` and `f.x` get brackets. The file moves to the folder of its final date.
- Files matching a glob in `data/profiles/intake.json` (`{"skip": ["*.ibw", "*_keysight-b1500a.*"]}`) are left exactly as they are, with no checks. The file is optional.
- `backup*`, `*.tmp`, `~*` and empty (0-byte) files go to `.quarantine/`, untouched, with no log inside.
- A date more than 31 days from its folder, an unreadable name, a name collision, or a sealed destination: the file stays and is listed for the user.
- A folder with `.intake.log` is sealed and skipped. Delete the log to re-open a folder.

1. **Explore.** `python3 scripts/raw_intake.py data/raw/<YYYY-MM-DD>` (or `data/raw` for every unsealed folder). Without `--apply` it changes nothing.
2. **Show your work.** Report counts per kind and 1 or 2 typical old → new names per change, plus every file left for the user and every date the header changed. Do not paste the full list.
3. **Wait for the user's approval** of that folder. A new instrument or a new kind of change needs a fresh approval.
4. **Apply.** Same command with `--apply`. Each move is hash-checked before and after; any mismatch rolls every move back. `.intake.log` is written last.
5. **Verify.** Check the line `raw-viewer header date/time read for N of M files`: N far below M means the profile is missing. Re-run without `--apply`: it should report the folder sealed. Count `.quarantine/` and moved files against the log.
6. **Record.** One row in `docs/rstack/decisions.tsv`: folder, counts, anything left for the user, and the log path.

**Reply:** folder, counts (renamed, moved, quarantined, left for you), and what needs the user.
