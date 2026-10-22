# Tested Loom source snapshot

Published with user authorization on 22 October 2026 for reproducible offline CI. This is the exact tracked-source archive used in the H3 native/mock tests, not a new source revision.

- Origin: [Oscar Rieken's Loom](https://github.com/orieken/loom).
- Commit: `3f2817818c68f42520229aab9342ce91533cef2f` (local-only at snapshot publication).
- SHA-256: `99a12e8c129457b3c291d6efbc07e5998a18be098f416e1a595ccc189a555d63`.
- Archive: `loom-3f2817818c68.tar.gz`; no untracked/personal working-tree files included.

See [provenance.json](provenance.json) for identity, size, archive audit and license hashes. Code is MIT; instructional content is CC BY 4.0 with attribution to Oscar Rieken. Exact upstream [LICENSE](LICENSE) and [LICENSE-CONTENT.md](LICENSE-CONTENT.md) are copied here and retained inside the archive and runtime image.

CI verifies the archive against the existing H3 profile before copying it into the build context. It does not need the unpublished commit from the upstream remote. Other pending upstream commits are not pushed by this publication. Do not edit or silently regenerate this archive; a new snapshot requires explicit provenance and a reviewed profile revision.
