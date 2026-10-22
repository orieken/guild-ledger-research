FROM python:3.12-slim-bookworm@sha256:6a0e06f5ba0b373d051aabd3fffb9b873f27f9a2a3a14bcbe37dee6f0e3bbc70
ARG PROFILE_SHA256=98ea2f392df4140dd18cceeecc6b09c442aafa090b50ef62ceba43b5f71f0af0
LABEL io.guild-ledger.profile-sha256=$PROFILE_SHA256
COPY build/source.tar.gz /tmp/source.tar.gz
COPY build/manifest.json /opt/profile.json
RUN printf '%s  /opt/profile.json\n' "$PROFILE_SHA256" | sha256sum -c - \
    && python -c 'import hashlib,json; p=json.load(open("/opt/profile.json")); assert hashlib.sha256(open("/tmp/source.tar.gz","rb").read()).hexdigest()==p["source"]["archive_sha256"]' \
    && mkdir -p /opt/harness2 /workspace /home/runner \
    && tar -xzf /tmp/source.tar.gz -C /opt/harness2 && rm /tmp/source.tar.gz \
    && chown 10001:10001 /workspace /home/runner
ENV PYTHONPATH=/opt/harness2 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    HOME=/home/runner RUNNER_KIND=harness2-deterministic
COPY entrypoint.py /opt/entrypoint.py
WORKDIR /workspace
USER 10001:10001
ENTRYPOINT ["python", "/opt/entrypoint.py"]
