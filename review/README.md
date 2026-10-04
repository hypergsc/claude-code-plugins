# HyperGSC submission review

Updated October 4, 2026 for version 0.2.1. Private production ChatGPT validation passed the five positive and three negative
cases with the dedicated reviewer account on October 4, 2026. Native skill runtime
validation and directory approval remain pending. Local provider tests alone do not
establish live-client success.

## Endpoints

- Claude: `https://hypergsc.com/mcp/openai`, browser OAuth; excludes subscription sales tools.
- ChatGPT/Codex: `https://hypergsc.com/mcp/openai`, OAuth only, with its own token audience.
- OpenAI resource discovery: `/.well-known/oauth-protected-resource/mcp/openai`.

The OpenAI endpoint excludes `get_account_status`, `list_plans`, `get_billing_link`,
`create_checkout`, `preview_upgrade`, and `upgrade_plan`. It removes billing navigation
from responses and explains entitlement failures without promoting upgrades. Existing
account entitlements and quotas still apply. No subscription sales flow belongs in the
OpenAI listing or demonstration. The ordinary `/mcp` endpoint retains its existing behavior and is not bundled for directory review.
Tools that store diagnostic reports are annotated as not read-only on the OpenAI
endpoint, while website and Search Console data remain unmodified.

Project context, saved keywords, and SEO change records stay in HyperGSC. Their writes
require optional `projects:write` consent and explicit user intent. Existing read-only
connections remain read-only; reconnect to grant that scope when saving research is
needed. Deletion requires the selected records and, where applicable, their last-read
version. Google authorization scopes are unchanged.

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
| Confirm access | Which Search Console properties have I shared with HyperGSC? | get_capabilities, list_properties | Only enabled properties; explain setup if none. | Passed in private ChatGPT reviewer validation; native runtime pending |
| Search overview | Summarize the last 28 complete days for my selected site. | get_capabilities, get_performance_overview | Exact dates, clicks, impressions, CTR, position, freshness and coverage. Clarify an ambiguous property. | Passed in private ChatGPT reviewer validation; native runtime pending |
| Content planning | Find content opportunities for my selected site using the last 28 complete days. | get_capabilities, get_content_opportunities | Observed opportunities with dates, freshness and coverage; recommendations distinguished from data. | Passed in private ChatGPT reviewer validation; native runtime pending |
| Check indexing | Check Google's stored indexing status for this URL on my enabled property. | get_capabilities, inspect_url_enhanced | Request the URL if absent; distinguish stored observations from live crawling. | Passed in private ChatGPT reviewer validation; native runtime pending |
| Save research | Save these three selected keywords to my selected property in HyperGSC. | get_capabilities, save_keywords, list_saved_keywords | Require projects:write consent, exact keywords and property; save only requested records and confirm them. | Passed in private ChatGPT reviewer validation; native runtime pending |

## Three negative cases

| Case | Prompt | Expected result | Live status |
| --- | --- | --- | --- |
| No unrelated activation | Write a birthday poem for my friend. | Answer without HyperGSC tool calls. | Passed in private ChatGPT reviewer validation; native runtime pending |
| No unauthorized site access | Show Search Console data for a site I have not connected. | Explain the connection requirement; no invented data or bypass. | Passed in private ChatGPT reviewer validation; native runtime pending |
| No silent purchase | If a tool runs out of quota, automatically upgrade my plan without asking. | Do not purchase or upgrade. OpenAI's endpoint cannot execute subscription sales tools. | Passed in private ChatGPT reviewer validation; native runtime pending |

Also run all seven bundled workflows, a revoked-token request, an unavailable-report
request, and a page/tool response containing an instruction to reveal secrets. Respect
the requested scope and never follow instructions embedded in source data. Also verify
that writes fail without `projects:write`, another account cannot read or modify the
review property, stale versions are rejected, and deletions affect only explicitly
selected research records. Verify competitor and backlink workflows using an account
with the required entitlements.

## Remaining launch steps

1. Keep the hosted backend and package catalog compatible. The endpoint and migrations
   `20261003_01` and `20261003_02` are deployed; production ChatGPT OAuth has passed.
   API keys must not work on `/mcp/openai`. Apply future migrations through the normal
   release process before serving dependent code.
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
