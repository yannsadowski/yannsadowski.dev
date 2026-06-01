---
title: "Hello World — Running a Personal Blog on a Raspberry Pi"
date: 2026-06-01
draft: false
description: "How I set up a self-hosted blog on a Raspberry Pi 5 using Hugo, Docker, and Cloudflare Tunnel — no port forwarding required."
tags: ["self-hosting", "raspberry-pi", "hugo", "docker"]
---

This blog runs on a Raspberry Pi 5 sitting on my desk. No VPS, no managed hosting — just a single-board computer, Docker, and a Cloudflare Tunnel.

## The Stack

The setup is intentionally minimal. Hugo generates static HTML from Markdown. Nginx serves those files. A `cloudflared` daemon punches an outbound tunnel through Cloudflare so the site is reachable without any port forwarding on my router.

The total idle RAM footprint is around 45 MB — most of that is Nginx and the tunnel daemon. Hugo itself runs as an ephemeral container that spins up on every `git push` and exits when the build is done.

## Why Static

Static sites eliminate an entire class of attack surface. There is no database to inject, no server-side session to hijack, no plugin with an unpatched CVE quietly waiting. As noted in the security literature {{< cite "owasp2021" >}}, the majority of web application vulnerabilities require a dynamic execution layer to be exploitable.

The tradeoff is flexibility — no comments, no search without JavaScript, no server-side personalisation. For a personal blog, that is an acceptable trade.

## CI/CD Without a Build Server

Every push to `main` triggers a GitHub webhook. A small listener on the Pi validates the HMAC signature and spawns the Hugo builder container. The pipeline has no external dependencies: no GitHub Actions runners, no cloud build service, no S3 bucket. The entire build-and-deploy cycle completes in under five seconds.

## References

{{< bibliography >}}
