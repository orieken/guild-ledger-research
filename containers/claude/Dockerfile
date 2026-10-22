# Build from this directory only; personal/research files never enter the context.
FROM golang:1.26.0-bookworm@sha256:2a0ba12e116687098780d3ce700f9ce3cb340783779646aafbabed748fa6677c AS go
FROM node:24.10.0-bookworm-slim@sha256:b8d2197aff9129d16c801a3e3e1b2a873c4946480f5a310f38056df2268c38d9 AS base
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-venv python3-pip make gcc g++ git curl ca-certificates \
    ripgrep jq procps tini gnupg postgresql-client \
    && rm -rf /var/lib/apt/lists/*
COPY --from=go /usr/local/go /usr/local/go
ENV PATH=/usr/local/go/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    HOME=/home/runner CLAUDE_CONFIG_DIR=/home/runner/.claude \
    DISABLE_AUTOUPDATER=1 DISABLE_TELEMETRY=1 \
    DISABLE_ERROR_REPORTING=1 CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 \
    PYTHONDONTWRITEBYTECODE=1
RUN useradd --uid 10001 --create-home --shell /bin/bash runner \
    && mkdir /workspace /inputs /opt/runner && chown runner:runner /workspace
COPY entrypoint.py fake-claude.py /opt/runner/
WORKDIR /workspace
USER 10001:10001
ENTRYPOINT ["/usr/bin/tini", "--", "python3", "/opt/runner/entrypoint.py"]
CMD ["preflight"]

FROM base AS smoke
ENV RUNNER_KIND=synthetic

FROM base AS claude
USER root
ARG CLAUDE_VERSION=2.1.304
# Verify the signed release manifest before trusting its binary checksum.
RUN set -eu; case "$(dpkg --print-architecture)" in arm64) platform=linux-arm64;; amd64) platform=linux-x64;; *) exit 1;; esac; \
    mkdir -p /tmp/claude-release /opt/runner/release; \
    cd /tmp/claude-release; \
    curl --connect-timeout 20 --max-time 300 --retry 2 -fsSL https://downloads.claude.ai/keys/claude-code.asc -o key.asc; \
    gpg --batch --import key.asc; \
    gpg --batch --with-colons --fingerprint security@anthropic.com | grep -q '^fpr:::::::::31DDDE24DDFAB679F42D7BD2BAA929FF1A7ECACE:'; \
    base="https://downloads.claude.ai/claude-code-releases/$CLAUDE_VERSION"; \
    curl --connect-timeout 20 --max-time 300 --retry 2 -fsSL "$base/manifest.json" -o manifest.json; \
    curl --connect-timeout 20 --max-time 300 --retry 2 -fsSL "$base/manifest.json.sig" -o manifest.json.sig; \
    gpg --batch --verify manifest.json.sig manifest.json; \
    curl --connect-timeout 20 --max-time 300 --retry 2 -fsSL "$base/$platform/claude" -o claude; \
    checksum="$(jq -er --arg p "$platform" '.platforms[$p].checksum' manifest.json)"; \
    printf '%s  claude\n' "$checksum" | sha256sum -c -; \
    install -m 0755 claude /usr/local/bin/claude; \
    cp manifest.json manifest.json.sig key.asc /opt/runner/release/; \
    printf '%s\n' "$CLAUDE_VERSION" > /opt/runner/release/version; \
    sha256sum /usr/local/bin/claude > /opt/runner/release/binary.sha256; \
    rm -rf /tmp/claude-release /root/.gnupg /home/runner/.gnupg
ENV RUNNER_KIND=claude
USER 10001:10001
