# HyperGSC for Claude

Connect Google Search Console to Claude with HyperGSC's hosted MCP integration.
Review search performance and indexing, plan content, research competitors and backlinks,
and evaluate recorded SEO changes.

![HyperGSC](plugins/hypergsc/assets/logo.png)

## Release status

The Claude package is available from this repository for installation and evaluation. Claude directory review and live installation tests are pending.

## Set up

1. Sign in at https://hypergsc.com and connect Google with read access.
2. Enable the Search Console properties you want your AI client to access.
3. Add the marketplace in your supported client:

```text
/plugin marketplace add hypergsc/claude-code-plugins
/plugin install hypergsc@hypergsc
```

Install HyperGSC using your client's plugin controls and complete browser OAuth.
For ChatGPT public discovery, use the approved directory listing once published.
Publishing this GitHub repository does not establish platform approval.

## Workflows

- **search-review:** compare complete periods and investigate observed traffic changes.
- **ctr-opportunities:** identify pages and queries worth investigating for snippet improvements.
- **indexing-check:** inspect selected URLs and distinguish stored observations from live tests.
- **content-planning:** review query/page opportunities and overlap, draft briefs, and save requested research.
- **competitor-research:** review domain estimates, top pages, and keyword gaps.
- **change-evaluation:** record applied changes and compare complete before/after GSC windows.
- **backlink-gap:** compare bounded referring-domain samples with explicit competitors.

Example: “Use HyperGSC to review my latest complete week of search performance.”
If several properties are enabled, the agent asks which one to use.
These skills do not modify websites or sitemaps or purchase subscriptions.
Availability depends on your current account entitlements and remaining allowances.
Missing data is unknown; results disclose dates, freshness, filters, and coverage.

## Authentication and support

Use browser OAuth. Never paste passwords, API keys, or tokens into chat.
Revoke client access from your HyperGSC dashboard when needed.
Saving or deleting project context, keywords, and SEO change records requires Starter+ and optional
`projects:write` consent alongside `gsc:read`. Existing API keys remain read-only.

- Website: https://hypergsc.com
- Connection documentation: https://hypergsc.com/agent-setup/prompt.md
- Support: https://hypergsc.com/about#support (help@hypergsc.com)
- Privacy: https://hypergsc.com/privacy
- Terms: https://hypergsc.com/tos

Version: 0.2.0. Only public integration files are included here.

## Validate and package

Python 3.9+ is sufficient; there are no third-party dependencies. From the repository root:

```sh
python3 scripts/validate.py
python3 scripts/validate.py --zip dist/hypergsc-claude-0.2.0.zip
```

The ZIP contains the platform manifest, MCP configuration, logo, and seven skills at
the plugin root. Local checks run in GitHub Actions and do not connect to your account.
See [review preparation and live cases](review/README.md) before submitting to a directory.

The hosted HyperGSC application is maintained separately from these integration files.
Report integration issues using this repository's issues or help@hypergsc.com.
