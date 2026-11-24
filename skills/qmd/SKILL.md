---
name: qmd
description: Search local markdown knowledge bases, notes, docs, and wikis with QMD. Use when users ask to find notes, retrieve documents, inspect a wiki, answer from indexed markdown, or set up QMD access.
license: MIT
upstream: https://github.com/tobi/qmd
compatibility: Requires external qmd CLI or MCP server. Install/update via `npm install -g @tobilu/qmd` / `npm update -g @tobilu/qmd`.
metadata:
  author: tobi
  version: "2.3.0"
allowed-tools: Bash(qmd:*), mcp__qmd__*
---

# QMD - Query Markdown Documents

## Research-space scoping and data protection

- **External binary:** `rstack` bundles only this skill; install and update `qmd` externally (`npm install -g @tobilu/qmd`, `npm update -g @tobilu/qmd`).
- **One collection per project + `wiki`:** Register each project root (`projects/res_<name>`) as its own collection with `ignore: ["**/data/**"]` in `~/.config/qmd/index.yml`, and `research-space/wiki` as `wiki`. Never index `**/data/**` (especially `data/raw/`).
- **Always scope queries:** Pass `-c <project>` (and `-c wiki` when consulting lab experience) so results never leak across projects.

## How search works

QMD searches local markdown collections: notes, docs, wikis, transcripts, and
project knowledge bases. Use it before web search when the answer may already be
in indexed local files.

The workflow is always:

1. Search for candidate documents.
2. Retrieve the full source with `qmd get` or `qmd multi-get`.
3. Answer from retrieved text, citing paths or docids.

Do not answer from snippets alone when the user needs facts, decisions, quotes,
or nuance. Snippets are only leads.

Typical loop:

```bash
qmd search "four-probe sheet resistance" -c res_wearable-ecg-devices -n 5
# leads: #abc123 reports/hall-effects-thin-film-measurement/README.md
qmd multi-get "#abc123" --format md
```

**Default to structured `qmd query` with `intent:`, `lex:`, `vec:`, and `hyde:`
fields that you write yourself.** You are a better query expander than the
built-in model: you know the user's actual goal, the domain vocabulary, and the
nearby-but-wrong concepts to avoid. Do not just paste the user's words into
`qmd query "..."` and hope the expansion model guesses right — supply the
`intent:` and craft the lexical and semantic terms deliberately.

## Pick the right search mode

Use **BM25 lexical search** when you know exact words, titles, names, code
symbols, or rare phrases:

```bash
qmd search "van der Pauw" -c res_wearable-ecg-devices -n 10
qmd search "evaporated carbon" -c wiki -n 5
```

Use **`qmd query` with structured fields** when the user describes an idea
indirectly, uses different wording than the source, or needs conceptual recall:

```bash
qmd query -c res_wearable-ecg-devices -c wiki $'intent: Find prior fabrication notes for evaporated carbon films.\nlex: evaporated carbon sheet resistance four-probe\nvec: thin film deposition contact resistance measurement\nhyde: Lab note describing how evaporated carbon thin films are prepared and measured with a four-probe setup.'
```

Structured query fields:

- `intent:` states what you are trying to find **and what to avoid**.
- `lex:` exact terms, aliases, titles, symbols, and rare words expected in the source.
- `vec:` paraphrases the idea in natural language, in source-like wording.
- `hyde:` describes the document or answer that would satisfy the request.

If `qmd query` is slow or model/GPU setup fails, fall back to `qmd search` with
better lexical terms.

## Retrieve sources

Search results include docids like `#abc123` and `qmd://...` paths. Fetch them:

```bash
qmd get "#abc123"
qmd get qmd://res_wearable-ecg-devices/README.md
qmd multi-get "#abc123,#def432" --format md
```

`get` and `multi-get` are **line-numbered by default** and always print `#docid`
and the `qmd://` path. Use `:from:count` (e.g., `qmd get "#abc123:120:40"`)
instead of piping through `sed`/`head`/`tail`. Pass `--full-path` when you need
an on-disk path.

## Discover what is indexed

```bash
qmd collection list
qmd ls res_wearable-ecg-devices
qmd status
```

## Setup and maintenance

Only mutate indexes when the user asks for setup or maintenance:

```bash
npm install -g @tobilu/qmd
qmd collection add /path/to/research-space/wiki --name wiki
qmd collection add /path/to/research-space/projects/res_<name> --name res_<name>
# Then add `ignore: ["**/data/**"]` under that collection in ~/.config/qmd/index.yml
qmd update
qmd embed
```

Health and diagnostics:

```bash
qmd doctor
qmd status
qmd pull
```

## MCP setup

See `references/mcp-setup.md` for Claude Code, Claude Desktop, OpenClaw, and HTTP
server configuration.

## Pitfalls

- **Never add `**/data/**`:** Only index `docs/` and `wiki/`.
- **Do not stop at snippets:** Fetch documents with `qmd get`/`qmd multi-get` before making claims.
- **Do not slice with `sed`/`head`/`tail`:** Use `path:from:count` or `--from`/`-l`.
- **Do not lean on bare `qmd query`:** Write `intent:`/`lex:`/`vec:`/`hyde:` yourself.
- **Always pass `-c`:** Scope to the active project collection (and `-c wiki` when needed).
