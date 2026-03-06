# syntax=docker/dockerfile:1
ARG OLLAMA_VERSION
ARG OLLAMA_SUFFIX=""

FROM ollama/ollama:${OLLAMA_VERSION#v}${OLLAMA_SUFFIX}

RUN mkdir -p /root/.ollama
