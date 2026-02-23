---
title: "HTB - Interpreter"
date: 2026-02-23
draft: false
tags: ["htb", "linux", "mirth-connect", "cve", "deserialization", "ssti", "ligolo-ng", "medium"]
ctf: "Hack The Box"
difficulty: "Medium"
---

**Interpreter** is a medium difficulty Linux machine from Hack The Box. It involves exploiting an unauthenticated deserialization vulnerability in Mirth Connect (CVE-2023-43208) for the initial foothold, cracking a salted hash found in the application database to pivot to a user, then escalating privileges through a Python SSTI in a locally running Flask service.

---

## Nmap Scan

As usual, we start with an nmap scan. Port 22 is open running OpenSSH on Debian, and ports 80 and 443 are also up.

```
PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 9.2p1 Debian 2+deb12u7 (protocol 2.0)
```

![Nmap scan](/images/ctf/interpreter/1nmap_scan.png)

First thing I check is whether HTTP and HTTPS return the same content, and they do.

## Mirth Connect

We're looking at a Mirth Connect instance. It's an open-source interface engine used in the healthcare industry for routing and managing messages between systems. Login redirects us to HTTPS.

![Mirth Connect login page](/images/ctf/interpreter/2mirth_login.png)

{{< active-machine >}}
