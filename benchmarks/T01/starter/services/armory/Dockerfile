FROM golang:1.26.0-bookworm@sha256:2a0ba12e116687098780d3ce700f9ce3cb340783779646aafbabed748fa6677c AS build
WORKDIR /src
COPY go.mod main.go ./
RUN CGO_ENABLED=0 go build -trimpath -o /armory .
FROM gcr.io/distroless/static-debian12:nonroot@sha256:afa5c872c891853ca7fcf1f12c3edb23f7eeef36189728842dd51042ff57f7ab
COPY --from=build /armory /armory
USER nonroot:nonroot
ENTRYPOINT ["/armory"]
