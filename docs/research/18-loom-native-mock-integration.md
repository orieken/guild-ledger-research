# Loom native/mock integration decision

22 October 2026. [Container build and usage](../../containers/loom/README.md), [verification receipt](../../containers/loom/verification.json), [profile registry](../../harness-packages.json).

## What is now verified

A local tracked-source export of Loom commit `3f2817818c68f42520229aab9342ce91533cef2f` was built with Go 1.26.5 and executed in an offline non-root container. This supersedes the older source snapshot for this mock profile only. Historical discovery reports remain unchanged. The original source checkout and global installation state were not modified.

The native `deliver-feature` plan has 16 stages. The default mock route completed nine and skipped seven after three explicit synthetic fixture approvals. Default execution without those fixture approvals halted at `confirm-design` with no approval recorded. Approval gates and router decisions were preserved; no new plan was substituted to make the test pass.

Ten test cases verify the default gate, full fixture-gated completion, interruption/checkpoint/resume, original task preservation, manifest/spec integrity, real-provider rejection, incompatible image rejection, source/profile binding and non-mock resume rejection. Native artifact hashes matched exported files. No model was called, and absent model usage/cost was kept null. A native mock has no measured code-quality result.

The executor reported posture violations and post-review edits in mock-generated files. We retained these diagnostics. An isolated Git baseline was needed to enable native posture checking; it lives only in the disposable workspace and does not introduce host Git configuration or commit changes to a user repository.

## Experimental placement

This is **H3-native-mock**, an integration profile for the native-workflow track. It is not H3-context, a full model-backed Loom run, or a fourth admitted controlled condition. Loom embeds framework instructions, but the mock provider does not demonstrate their effective model exposure, retrieval behavior or actual Claude invocation.

Future autonomous analysis must treat an unapproved native gate as `needs-human`. Fixture-approved completion is a mechanics test with synthetic gate decisions; it is never entered as autonomous benchmark success or a human-assisted product result. Actual human gate time and decisions must be captured separately in native-workflow experiments.

The native source revision advanced since our earlier review and requires a newer compiler. It still selects Claude or mock, and the inspected real-provider launcher still lacks explicit model/effort selection and leaves project-context isolation false by default. Those are unchanged admission questions; this task did not execute or patch that provider.

## Next decisions

Keep the clean H0/H1/H2 container path separate from native Loom output directories. Freeze this H3 package/export and resulting image before any scheduled campaign. Add real-runtime model/auth/context/tool policy, durable aggregate usage and spend enforcement, native child-call accounting, genuine human-gate capture and independent evaluation only in a separately authorized phase. A reduced H3-context package remains undefined.
