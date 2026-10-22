ARG RUNNER_IMAGE=guild-ledger-claude-smoke:local
FROM golang:1.26.5-bookworm@sha256:53eeac89074db483fdf0ab3be1df32bf6e47562263d2d0d6baa7f26acb4957dd AS compiler
WORKDIR /src
COPY build/loom-source.tar.gz /tmp/loom-source.tar.gz
COPY build/source-lock.json /tmp/source-lock.json
RUN expected="$(sed -n 's/.*"archive_sha256": "\([a-f0-9]*\)".*/\1/p' /tmp/source-lock.json)" \
    && printf '%s  /tmp/loom-source.tar.gz\n' "$expected" | sha256sum -c - \
    && tar -xzf /tmp/loom-source.tar.gz -C /src
ENV GOTOOLCHAIN=local CGO_ENABLED=0
RUN go build -mod=readonly -trimpath -buildvcs=false -o /out/loom ./cmd/loom

FROM ${RUNNER_IMAGE}
USER root
COPY --from=compiler /out/loom /usr/local/bin/loom
COPY --from=compiler /src/LICENSE /src/LICENSE-CONTENT.md /opt/loom/
COPY build/source-lock.json /opt/loom/source-lock.json
COPY entrypoint.py /opt/loom/entrypoint.py
RUN ! command -v claude && sha256sum /usr/local/bin/loom > /opt/loom/binary.sha256
ENV RUNNER_KIND=loom-mock
USER 10001:10001
ENTRYPOINT ["/usr/bin/tini", "--", "python3", "/opt/loom/entrypoint.py"]
CMD []
