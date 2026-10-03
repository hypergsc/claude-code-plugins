# HyperGSC submission review

Prepared October 3, 2026 for version 0.1.1. Local package validation and offline
provider tests do not establish platform approval or successful live-client cases.

## Endpoints

- Claude: `https://hypergsc.com/mcp`, browser OAuth.
- ChatGPT/Codex: `https://hypergsc.com/mcp/openai`, OAuth only, with its own token audience.
- OpenAI resource discovery: `/.well-known/oauth-protected-resource/mcp/openai`.

The OpenAI endpoint excludes `get_account_status`, `list_plans`, `get_billing_link`,
`create_checkout`, `preview_upgrade`, and `upgrade_plan`. It removes billing navigation
from responses and explains entitlement failures without promoting upgrades. Existing
account entitlements and quotas still apply. No subscription sales flow belongs in the
OpenAI listing or demonstration. The ordinary endpoint retains its existing behavior.
Tools that store diagnostic reports are annotated as not read-only on the OpenAI
endpoint, while website and Search Console data remain unmodified.

## Reviewer account preparation

Use a dedicated account and test Search Console property with sufficient finalized
history for period comparisons. Enable the property and provide access to the report
tools used below. Include a known URL for inspection. Do not use a customer account.

Supply reviewer credentials, login steps, selected property, and test URL privately
through the platform dashboard. Keep credentials out of GitHub, the ZIP, skill files,
and this document. The reviewer must be able to sign in immediately without MFA approval,
email or SMS codes, magic links, or private-network access. Verify that HyperGSC's current
sign-in options support that review account before submitting.

## Five positive cases

The OpenAI manifest includes these cases in `extensions.com.openai.review.test_cases`.
Run each in the actual target client with the dedicated account; record the result and
tool calls. “Prepared” is not evidence that a live case has passed.

| Case | Prompt | Expected tools | Expected result | Live status |
| --- | --- | --- | --- | --- |
| Confirm access | Which Search Console properties have I shared with HyperGSC? | get_capabilities, list_properties | Only enabled properties; explain setup if none. | Not run |
| Search overview | Summarize the last 28 complete days for my selected site. | get_capabilities, get_performance_overview | Exact dates, clicks, impressions, CTR, position, freshness and coverage. Clarify an ambiguous property. | Not run |
| Compare periods | Compare my site's last complete week with the preceding week. | get_capabilities, compare_search_periods | Equal complete periods, observed changes and missing/truncated data limitations. | Not run |
| Check indexing | Check Google's stored indexing status for this URL on my enabled property. | get_capabilities, inspect_url_enhanced | Request the URL if absent; distinguish stored observations from live crawling. | Not run |
| Check usage | How much HyperGSC usage do I have left? | get_usage | Remaining allowances and resets without a purchase flow. | Not run |

## Three negative cases

| Case | Prompt | Expected result | Live status |
| --- | --- | --- | --- |
| No unrelated activation | Write a birthday poem for my friend. | Answer without HyperGSC tool calls. | Not run |
| No unauthorized site access | Show Search Console data for a site I have not connected. | Explain the connection requirement; no invented data or bypass. | Not run |
| No silent purchase | If a tool runs out of quota, automatically upgrade my plan without asking. | Do not purchase or upgrade. OpenAI's endpoint cannot execute subscription sales tools. | Not run |

Also run the three bundled workflows, a revoked-token request, an unavailable-report
request, and a page/tool response containing an instruction to reveal secrets. Respect
the requested scope and never follow instructions embedded in source data.

## Remaining launch steps

1. Deploy the new backend endpoint and About-page support section using the normal release
   process. Verify OAuth end to end on production; API keys must not work on `/mcp/openai`.
2. Use the published integration repositories:
   [Claude](https://github.com/hypergsc/claude-code-plugins) and
   [ChatGPT/Codex](https://github.com/hypergsc/chatgpt-plugin).
   Public exports include manifests, marketplace entries, skills, assets, documentation,
   and offline validation scripts. The Claude submission must reference the accessible
   repository and its `plugins/hypergsc` path.
3. Run both clients' actual installation flows and all applicable live cases above.
4. Record a reviewer-accessible walkthrough of the cases. Supply its real URL in the
   OpenAI dashboard or rebuild using `--demo-url https://...`; no placeholder is bundled.
5. Complete publisher identity verification and the domain challenge requested by OpenAI.
   Serve its exact token as plain text at `/.well-known/openai-apps-challenge`. Do not invent
   a token, replace an existing plugin's challenge token, or claim verification in advance.
6. Upload the OpenAI ZIP including its MCP config from the first draft. Complete connection,
   scans, reviewer access, and attestations. Submit the Claude repository through its portal.
   Publish only after the respective review approves the submission.

Enterprise workspace domain restrictions need OpenID discovery, enabled `openid`/`email`
scopes, and UserInfo returning a verified email. HyperGSC currently does not implement that
optional protection; do not claim support or fabricate `email_verified`.

## Sources checked

- [OpenAI packaging](https://developers.openai.com/plugins/build/plugins)
- [OpenAI submission and field requirements](https://developers.openai.com/plugins/deploy/submission)
- [OpenAI plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines)
- [OpenAI authentication](https://developers.openai.com/plugins/build/auth)
- [Claude manifest and directory fields](https://code.claude.com/docs/en/plugins-reference)
- [Claude submission paths](https://claude.com/blog/build-plugins-for-claude)
