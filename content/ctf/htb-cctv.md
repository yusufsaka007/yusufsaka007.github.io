---
title: "HTB - CCTV"
date: 2026-03-08
draft: false
tags: ["htb", "linux", "zoneminder", "sqli", "sqlmap", "motioneye", "cve", "ligolo-ng", "medium"]
ctf: "Hack The Box"
difficulty: "Medium"
---

**CCTV** is a medium difficulty Linux machine from Hack The Box.

---

## Nmap Scan

As usual, we start with an nmap scan.

```bash
nmap -sT -sV -sC -oA nmap/cctv 10.129.3.52
```

![Nmap scan](/images/ctf/cctv/1nmap_scan.png)

Port 80 is open. The webpage itself is relatively static.

![Webpage](/images/ctf/cctv/2webpage.png)

Following the staff login link we land on a ZoneMinder instance.

![ZoneMinder login page](/images/ctf/cctv/3zoneminder_login.png)

{{< active-machine >}}
