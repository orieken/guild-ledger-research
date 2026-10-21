# Collecting GitHub-hosted Copilot discovery reports

The manually dispatched **Collect Copilot discovery report** workflow copies three report files from an existing, same-repository PR at its exact head commit. It saves a 90-day Actions artifact with SHA-256 hashes and collection provenance. It does not launch Copilot, retrieve private session telemetry, merge a PR, or write reports into Git history. Agent-authored claims still need review. No model credentials are needed; repository contents and pull-request read permissions suffice.

## Use

1. Push the workflow commit to the repository's default branch so manual dispatch becomes available.
2. Run the discovery prompt in **GitHub-hosted Copilot cloud agent**, asking it to open a PR containing `report.md`, `capabilities.json`, and `evidence.md` under `docs/runtime-discovery/github-copilot-coding-agent/<UTC-timestamp>/`. This separate agent task consumes the account's normal Copilot allocation; this collector does not start it.
3. In Actions, select **Collect Copilot discovery report**, then **Run workflow**. Enter its PR number and folder timestamp, such as `20261021T065724Z`.
4. Download the `copilot-discovery-<PR>-<timestamp>` artifact and review it. Archive approved evidence durably before expiration. If the PR receives new commits, dispatch again; each run records the source SHA.

Missing files, malformed JSON/schema version, invalid inputs, fork PRs, and inaccessible files fail collection. These checks do not validate every capability record or establish that the author really ran in the hosted surface. Report data is never executed. Run this collector from a trusted workflow revision. Do not include credentials, private reasoning, or unrelated personal logs in report files.

The existing local VS Code report is not proof of GitHub-hosted execution. This workflow transports report files; it does not supply missing token or billing measurements.

GitHub API references: [PR metadata](https://docs.github.com/en/rest/pulls/pulls#get-a-pull-request), [contents at a commit ref](https://docs.github.com/en/rest/repos/contents#get-repository-content). Session review is separate: [Managing agent sessions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/manage-and-track-agents).
