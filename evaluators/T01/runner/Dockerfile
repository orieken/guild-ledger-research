FROM node:24.15.0-bookworm-slim@sha256:4e6b70dd6cbfc88c8157ba19aa3d9f9cce6ba4703576d55459e45efcbc9c5f5d
WORKDIR /evaluator
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund && npx playwright install --with-deps chromium && chmod -R a+rX /root/.cache/ms-playwright
ENV PLAYWRIGHT_BROWSERS_PATH=/opt/browsers
RUN mv /root/.cache/ms-playwright /opt/browsers
ARG EVALUATOR_SHA256
LABEL io.guild-ledger.evaluator-sha256=$EVALUATOR_SHA256
COPY acceptance.mjs ./
USER 10001:10001
ENTRYPOINT ["node", "/evaluator/acceptance.mjs"]
