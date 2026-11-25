---
title: "BSCP Review: How to Pass Your Burp Suite Certified Practitioner Exam"
date: 2026-11-25
draft: false
tags: ["bscp", "portswigger", "certifications", "web-security", "burp-suite", "review"]
image: "/images/certs/bscp-cert.png"
---

# How to pass your BSCP exam

## Intro
![alt text](/images/certs/bscp-cert.png)

> For a while, I had been studying for PortSwigger's BSCP (Burp Suite Certified Practitioner) exam, and I recently passed it on my second attempt. In this blog, I will briefly explain what the BSCP exam is, what it includes, who it is for, and how you can actually pass it. I will write about the mistakes I made while preparing as well as while taking the exam, so that you won't have to repeat the same mistakes. I hope you enjoy it.

## What is BSCP
The Burp Suite Certified Practitioner (BSCP) is the official certificate created and evaluated by **PortSwigger**, the creators of Burp Suite. If you have been in the AppSec field for a while, you have probably heard of Burp Suite and even used it during your testing.

The exam includes different vulnerability classes, from server-side vulnerabilities like SQLi to client-side vulnerabilities like XSS, as well as advanced vulnerability classes like HTTP smuggling. All of these vulnerability classes can be found in the completely free and interactive courses created by PortSwigger, [Web Security Academy](https://portswigger.net/web-security/all-topics).

## Exam format and pricing
The exam format is pretty straightforward. When you launch your exam, you will be provided with two different applications, each having 3 different stages. In order to **pass** the exam, you need to complete all 3 stages in both applications.

- Stage 1: You have to get an initial foothold in `carlos'` account.
- Stage 2: You have to elevate your privileges to get access to admin functionality.
- Stage 3: Using your admin privileges, you need to read the flag located in `/home/carlos/secret` and submit it.

The following is an amazing graph that shows possible attack vectors per stage (kudos to https://github.com/botesjuan/).

![](https://user-images.githubusercontent.com/58632878/225064808-72de66b7-ef3a-4915-a9bf-d253d7f981f6.png)

At the time of writing this, the exam voucher itself costs $99 (without VAT). However, it is mandatory to have a Burp Suite Professional license when taking your exam, since they might have to check your Burp project file. A Burp Suite Professional license costs around 500 dollars. Since I use Burp Suite in my day-to-day life, I already had a Pro license. However, it **might** be possible to request a one-month free trial [here](https://portswigger.net/burp/pro/trial).


## How to prepare for your exam
PortSwigger recommends that you be able to solve every Practitioner-level lab in Web Security Academy on your own.

It is a good starting point, but not enough in my opinion. During the exam, you not only have to find the vulnerability, you also have to exploit it in a meaningful way to get access to the next stage. Thus, understanding web application basics like cookies, sessions, browser behaviour, and backend and proxy behaviour is crucial.

Also, in most cases, you will encounter some sort of WAF behaviour. Therefore, it is highly recommended that you know different kinds of URL whitelist bypasses, as well as different obfuscation techniques and encodings to bypass WAFs. I highly recommend the [Hackvertor](https://portswigger.net/bappstore/65033cbd2c344fbabe57ac060b5dd100) Burp Suite extension for finding WAF bypasses and carefully reading the [Essential Skills](https://portswigger.net/web-security/essential-skills) section in Web Academy.

Note-taking is crucial. The main problem you will face in this exam is the limited time. That is why it is recommended to have well-structured notes and payloads that you can easily access.

I used Obsidian to create my notes, but you can use anything you prefer. For every vulnerability class, I separated the notes into Theory and Lab Solutions. This way, if I encounter a situation similar to one in a lab I have solved, I can quickly visit that section in my notes and find the payload I used when solving that lab. Below, you can see an example for SSTI vulnerabilities.

![alt text](/images/certs/bscp-notes.png)

Taking the official [practice exams](https://portswigger.net/web-security/certification/practice-exam) by PortSwigger is recommended. They will give you a clear picture of the exam format and what you can expect. However, they won't guarantee that you will pass. If you are a beginner or intermediate in this field, it is still highly recommended that you solve [mystery lab challenges](https://portswigger.net/web-security/mystery-lab-challenge) until you get comfortable exploiting the vulnerabilities.

## What not to do during your exam
As I mentioned before, I passed my exam on my second attempt. During my first attempt, I had finished all 5 stages. For the final stage, I just had to read the flag using the admin panel. When I first looked at the admin panel, it seemed to point to a very specific vulnerability class. Too specific, even.

I tried many attack types related to that vulnerability class, but nothing seemed to work, and in the end, my time ran out. It was disappointing, as expected. Failing when you are so close to getting the final flag is frustrating. However, after reading the official [page](https://portswigger.net/web-security/certification/exam-hints-and-guidance/retaking-your-exam) on retaking the exam, I bought another voucher and decided to take my chances again.

Somehow, I got the same app that I got stuck on during my first attempt. Worried, I tried the same techniques, hoping that the first exam environment had been broken during my first attempt. But I received the same error message again.

However, I tried another technique that was completely different from what I had assumed, and it worked. I was just experiencing tunnel vision.

I want you to learn from my mistakes, so that you won't have to spend your money on another voucher. It is good to have assumptions and hypotheses. You need to try every technique you have learnt in Web Academy to prove whether your hypotheses are right or wrong. However, if you have taken good notes and your payloads are not working, maybe it is time to come up with another theory. There is also another side to this. During my second attempt, I came up with a theory and tried many payloads, but they failed. In the end, however, it turned out to be a simple typo, and my assumption was correct. So do not have tunnel vision, but do not give up on your theories that easily either.

## What to do during your exam
Probably the biggest issue during your exam will be time. You only have 4 hours to complete it. The good news, however, is that most vulnerabilities can be identified using automated scanners and extensions.

1) Learn how to use targeted scanning (use insertion points to speed up your scans)
2) Learn how to use the `Hackvertor` extension for WAF bypasses
3) Use the [HTTP Smuggler](https://portswigger.net/bappstore/aaaa60ef945341e8a450217a54a11646) extension to detect HTTP smuggling vulnerabilities
4) Use DOM Invader to detect certain client-side issues

Most vulnerabilities can be identified with these tools. But again, please do not fully rely on them, since even if they identify vulnerabilities, they can't give you context-specific payloads, and sometimes they can't even identify the vulnerabilities. The app that caused me to fail my first attempt was an example of this. No scanner was able to detect it.

## Summary
In this blog, I have shared some tips and tricks on how you can pass your BSCP exam. I shared some of the mistakes I made, so that you won't have to repeat them. I hope you enjoyed reading it, and see you on the next one.
