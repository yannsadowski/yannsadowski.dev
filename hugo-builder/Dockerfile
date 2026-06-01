FROM hugomods/hugo:exts AS builder

RUN apk add --no-cache git

WORKDIR /site

ARG REPO_URL
ENV REPO_URL=${REPO_URL}

CMD git clone --recurse-submodules --depth 1 "$REPO_URL" /site && \
    hugo --minify --destination /html-output
