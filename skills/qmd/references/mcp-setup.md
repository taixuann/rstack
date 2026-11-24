# QMD MCP Server Setup

## Install and Update

```bash
npm install -g @tobilu/qmd
npm update -g @tobilu/qmd
qmd collection add /path/to/research-space/wiki --name wiki
qmd collection add /path/to/research-space/projects/res_<name>/docs --name res_<name>
qmd embed
```

Never add `**/data/**` or `analysis/` to any collection.

## Configure MCP Client

**Claude Code** (`~/.claude/settings.json`):
```json
{
  "mcpServers": {
    "qmd": { "command": "qmd", "args": ["mcp"] }
  }
}
```

**Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "qmd": { "command": "qmd", "args": ["mcp"] }
  }
}
```

## HTTP Mode

```bash
qmd mcp --http              # Port 8181
qmd mcp --http --daemon     # Background
qmd mcp stop                # Stop daemon
```

## Tools

- `query`: Search with pre-expanded `lex`, `vec`, `hyde` queries, optional `collections` array, `limit`, and `filter`.
- `get`: Retrieve document by path or `#docid`.
- `multi_get`: Retrieve multiple documents by glob or comma-separated list.
- `status`: Index health and collections.
- `metadata`: Discover metadata keys and value distributions.
