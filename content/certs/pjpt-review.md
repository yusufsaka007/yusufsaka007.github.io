---
title: "PJPT Review: My First Pentest Cert"
date: 2025-07-01
draft: false
tags: ["pjpt", "tcm-security", "certifications", "active-directory", "penetration-testing", "review"]
image: "/images/certs/pjpt-cert.png"
---

I passed PJPT. The Practical Junior Penetration Tester certification by TCM Security. In this post I want to give my honest take on the preparation, what the exam is actually like, the report writing phase, and whether the whole thing is worth your time and money.

## What is PJPT?

According to TCM Security, PJPT is an associate-level exam for beginners looking to get into penetration testing and red teaming. You get 2 full days to complete the assessment by exploiting a vulnerable Active Directory environment, and an additional 2 days to write a commercial-grade penetration testing report. The voucher is valid for 12 months and comes with one free retake in case you don't make it on the first try, which is a nice safety net.

When you purchase PJPT you get 12 months of access to the Practical Ethical Hacking (PEH) course. I genuinely believe that course alone is enough to pass the exam, but more on that later.

The course covers:

- A Day in the Life of an Ethical Hacker
- Hacking Methodology
- Reconnaissance and Information Gathering
- Scanning and Enumeration
- Exploitation Basics
- Active Directory Penetration Testing
- Web Application Penetration Testing
- Wireless Attacks
- Legal Documentation and Report Writing

It gives you a solid and well-rounded picture of what actually working as an ethical hacker looks like.

**What I liked:** After grinding through 4 CompTIA exams with a proctor watching my every move, having a fully flexible exam environment was a breath of fresh air. Stuck on something? Get up and take a walk. Tools not cooperating? Go splash some cold water on your face. Report going slower than expected? Do a few pushups. You are completely in control of your time and environment, and that makes a real difference when the pressure starts building up.

The course material is also genuinely one of the best entry-level resources out there. And at $249.12 for the course, the exam voucher, and a free retake included, it's hard to argue with the price. Worth every cent.

**What I didn't like:** My main gripe is that the exam didn't include any web application hacking, even though the course covers its basics. Felt like a missed opportunity. I should also mention that I personally prefer text-based learning over video, but that's entirely on me. The video content itself is very good.

## Preparation

### Course Materials

The PEH course and its labs are more than enough on their own. That said, by the time I sat for PJPT I already had some Python experience, had worked through plenty of CTFs on HackTheBox, and had also gone through HTB Academy's [Active Directory Enumeration and Attacks](https://academy.hackthebox.com/course/preview/active-directory-enumeration--attacks) module since my next goal was CPTS anyway. That AD module is complete overkill for PJPT, but it gives you an extra layer of confidence walking into the exam.

### Note Taking

Take good notes. Seriously. When the exam starts it is just you and your notes. I'd strongly recommend using a hierarchical note-taking app like Notion, Obsidian, or CherryTree. I used Notion and organized everything by course section. That way, when I needed to find something quickly during the exam, I knew exactly where to look.

## Tips for the Exam

You've put in the work, your notes are organized, and the day finally arrives. You launch the exam environment and you're staring at a network for the first time.

The worst thing you can do is let your nerves take over. You've prepared. Be proud of that. Make a cup of coffee, take a breath, and try to actually have fun with it.

Take it slow. 2 days is more than enough for this exam. I learned that the hard way. I missed something critical in the output of a command I ran and it cost me 4 hours. Four hours. I kept going in circles, getting more and more stressed, until I finally ran the same command again and there it was, sitting right in the output the whole time. Read everything carefully, don't rush, and you'll be fine.

One more thing: once you submit, you lose access to the lab. **Take screenshots. Take a lot of them.** You'll be grateful for every single one when you sit down to write the report.

## Writing the Report

The "Legal Documents and Report Writing" section of the PEH course is a solid introduction to writing a commercial-grade report. It covers the structure, the language, everything you need.

TCM Security also provides a [sample report template](https://github.com/hmaverickadams/TCM-Security-Sample-Pentest-Report) that makes the whole process a lot less intimidating.

I used Google Docs to write mine and it was perfectly fine for the scope of this lab. Around the time I'm writing this, I also discovered [SysReptor](https://sysreptor.com/), a really clean report-writing tool with both cloud and self-hosted options. Big fan of it now. As far as I know, TCM Security doesn't have a SysReptor template yet, but it's worth keeping an eye on for future engagements.

## Was it Worth It?

Short answer: yes. I loved both the course and the exam experience.

Looking back though, I think I probably would have gone for PNPT instead. It bundles extra courses on top of PEH (like privilege escalation for Windows and Linux) and it's generally better recognized by companies, which would have made my job search a bit easier at the time. But honestly, no regrets at all. Heath Adams and Alex Olsen put together something genuinely great here.

## Timeline

Because of my prior experience and the time I had available, I got through the course in about 20 days. The exam itself took me 8 hours, and I wrote the report in a day.
