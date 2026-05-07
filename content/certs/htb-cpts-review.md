---
title: "CPTS Review: How to Pass the Hack The Box Certified Penetration Testing Specialist"
date: 2026-05-07
draft: false
tags: ["cpts", "hack-the-box", "certifications", "active-directory", "penetration-testing", "review"]
image: "/images/certs/cpts-cert.png"
---

# Intro
After all the patience and work, I finally got that email. I passed the Certified Penetration Testing Specialist (CPTS) exam by Hack The Box. It has been a very long and challenging journey but at the same time a rewarding one. In this blog post I will provide you with some tips and thoughts about the preparation process and the exam itself. While I believe I will be sharing a lot of things in common with other blogs like [Bruno Chamoura's posts](https://www.brunorochamoura.com/posts/cpts-tips/), I still believe I have some additional tips and hints for the folks working their journey of becoming Hack The Box certified. I hope you enjoy.

![CPTS Certificate](/images/certs/cpts-cert.png)

# What is CPTS
For those who don't know, CPTS is a penetration testing certificate created by Hack The Box. It is highly hands-on and verifies advanced skills in red teaming, reconnaissance, web exploitation, Active Directory attacks and privilege escalation. For willing candidates, the requirements are completing the 28 modules in the "Penetration Tester" job-role path on the [HTB Academy](https://academy.hackthebox.com/) and then one can start their exam environment.
The exam itself is a 10 day fierce, practical, hands-on environment that involves exploiting a complete network and submitting a **commercial-grade** penetration testing report within that time frame.
Unlike many certificates out there, CPTS does not expire and stays valid for a lifetime.

Another thing worth noting is that you get 2 retakes for a single voucher. I failed my first attempt. Not because I couldn't get all the flags, no. I got all of the 14 flags within the first 5 days. I failed because I was too lazy to write a better report. Well, now looking back, I feel very grateful I had the chance to redeem it on my second try.

# CPTS vs OSCP
## Price
Well you might think, why not go for Offensive Security Certified Professional (OSCP) by Offsec then? It has been an industry standard for years and many HR people still drool when they hear about it like it's the holy grail of pentesting.

Well of course the price was a thing to consider...
![OSCP price comparison](/images/certs/cpts-oscp-price.png)

But it was certainly not the only factor. Looking at the exam format of OSCP and its reviews, I just think it is too hacky an exam compressed in such a short window.

Having some prior experience on Hack The Box Machines (more on that later) and listening to other experienced pentesters, I could see that Hack The Box's certificates were slowly becoming the people's favourites. Also, they are more reasonably priced and you don't have to sacrifice one of your kidneys during the process.
![HTB certificates pricing](/images/certs/cpts-htb-price.png)

## Recognition
I also started seeing CPTS more and more in the job postings, meaning it is gaining recognition at a fast pace.

For those who don't know there is a very prestigious CTF event in Belgium called Cyber Security Challenge Belgium. Being top 16 in the whole country in the senior division, I was lucky enough to be able to attend this year's challenge. After completing the event you are asked to come into a room to network and get to know the leading tech companies all around Belgium. One of the companies specifically asked whether I had a certificate like CPTS. Of course at that time I didn't have it, but now looking back I feel more happy that I got it.

# Experience with the study process
As I mentioned, in order to be able to buy the voucher, one needs to complete all 28 modules for the Penetration Tester job-role path. I was at the time someone who could be considered a beginner in the field of Penetration Testing when I first started out.

Extremely curious, just got my PJPT by TCM Security (more on that on this [blog post](https://yusufsaka007.github.io/certs/pjpt-review/)). At that time, I had also done some Hack The Box and TryHackMe CTFs. So overall one can say I was indeed a beginner at that time.

## Academy Modules Structure
Hack The Box Academy is a learning platform for people who want to improve in the field of cyber security. However I must mention that the course material is fully text based. I personally am someone that learns better by reading. If you prefer audio based content it might not be the best learning platform for you. However, being a bug bounty hunter, reading is a skill that helps a lot since you constantly need to read the documentations of the web technologies you face.

I am pretty sure reading is a skill that will help you along your journey of cyber security no matter what your field is. So the CPTS and Academy modules can be the cause for you to improve your reading skills.
![HTB Academy modules overview](/images/certs/cpts-academy-modules.png)

After almost every section, you are also expected to answer certain questions. In order to find the answers, you are usually expected to solve interactive challenges through the labs you spawn, helping you actually practice and get better prepared.

Sometimes the questions or skills assessments might get overwhelming for some, or it was for me at least. Do not start looking for a leak after spending some time on them for an hour. This mentality will not help during your CPTS exam. Everything you need is in the modules. Take good notes and be patient and you will see that they are actually solvable.

Do not get me wrong. I do not say that you should never look up for hints, no. What I am trying to imply is, when you get stuck on a specific lab, the first thing you do should not be looking for hints. Depending on the assessment, set yourself specific time limits. If you still can't find the answer by yourself within that time limit, feel free to look for help.

## Note taking
![Note taking setup](/images/certs/cpts-notes.png)
TAKE NOTES! I can't stress enough how important a good note structure is and how handy it will become in the future. Pick a good note taking application that you like, find aesthetic and efficient. At that time I was using Notion (not anymore) but there are so many options like Obsidian, CherryTree and so on. If it is hierarchical it will be easier for you to find your way around when you need them.

For my note structure I used Hack The Box's own structure in their academy modules. However I am not sure if I would do the same, now looking back. It is not as black and white as you might think. Some sections from the Active Directory module might overlap with some sections in password attacks or Windows privilege escalation (spoiler alert: it does)

Instead try to make it more methodological.

```
Are you facing a web app => web recon todo list
Did you find credentials of an AD user => SMB shares, AD privileges, Remote connection checks, local directory checks etc.
Did you get a shell on a Linux machine => Run sudo -l, history commands ...
```

I am sure my exam process would have been much easier if I had these note structures instead.

## Thoughts on Hack The Box machines
How about Hack The Box machines or pro labs? I had this question a lot regarding whether one should solve [IppSec's Unofficial CPTS Prep](https://www.youtube.com/playlist?list=PLidcsTyj9JXItWpbRtTg6aDEj10_F17x5) or Pro Labs like *Zephyr*.

![IppSec's unofficial CPTS prep playlist](/images/certs/cpts-htb-machines.png)

Short answer **no**. Long answer **it depends**. Let me explain. At that time I solved close to *50 Hack The Box machines* and finished *Zephyr Pro Lab*.
![Zephyr Pro Lab completion](/images/certs/cpts-zephyr.png)

Me coming and saying they did not help me at all would not be the truth, because they did help during my exam a lot, but not the way you think.

Though the labs were very realistic and fun to do, most of the techniques that were used solving these labs are not included in the Academy module. You will not have to use any of these techniques unless they were mentioned in the *Penetration Tester Job Role Path*.

However, and I say however, they will still help in other ways. They, in a way, make you mentally prepared for facing such situations, new technologies, new AD environments. Basically, in a way, you train your mindset to be ready and not give up when you are unable to find the solution.

However do not get me wrong. Solving those labs requires extra subscriptions other than your already existing Academy subscription, and most importantly, it requires extra time. *Zephyr* alone took me 5 focused days just to root every single machine. Not everybody has the privileges I had. You might not have the time, or the financial requirements to do those additional preparations. But don't worry. CPTS is still passable if your notes are in place and you did the labs provided in the Hack The Box Academy.

If you however still decide to do extra labs, I would recommend the ones in [IppSec's Unofficial CPTS Prep](https://www.youtube.com/playlist?list=PLidcsTyj9JXItWpbRtTg6aDEj10_F17x5) since they are the closest to your real target and you won't find yourself in a rabbit hole.

If you want to go even further than that, I would recommend the *Pro Lab Zephyr*. It is almost fully active directory focused, and has multiple machines, thus you can practice your tunneling and lateral movement skills even further.

## Gearing up for the exam
Okay you studied for the exam, took good notes, grasped the theory part. In order to execute the task, the next step is crucial, which is collecting the right tools.

### Tools and Scripts
Throughout the academy modules Hack The Box suggests you to use certain tools for automation of certain tasks and detection of vulnerabilities. I mean there are literally modules dedicated to the usage of certain open source tools like *SQLmap, Metasploit, NMAP etc.*. Just like your notes it is crucial to organize your tools and scripts in a way that you will be able to find them easily when you are in need, and you won't spend too much time running `find` or `locate` desperately.
![Tool organization setup](/images/certs/cpts-tools.png)

I do, however, have additional suggestions for you. Note that none of these were mentioned in the *Academy Modules* in depth. However I must admit that I saw great help from these tools during my exam.

- NetExec
    - NetExec (a.k.a nxc) is the all in one swiss knife for Pentesting Active-Directory environments. It has built-in recon features and exploits for `LDAP`, `SMB`, `RDP`, `WinRM` and so on. You get the idea. It is fairly easy to learn to use and very modular. It supports authentication mechanisms like `Kerberos` or `NTLM` and the best part is, it is fully remote.
- Screenshot Taker
    - You need a good, efficient, working screenshot tool. Yes there are many. I personally use a combination of `grim` and `swappy` but it doesn't matter what you use. As we saw in the *Reporting Module* you will have to redact a lot of sensitive information in your screenshots, like the hashes, passwords etc. So make sure your screenshot application has a built-in editing feature, so that you won't have to waste hours in Canva trying to hide a field in your screenshot.
![Screenshot tool with editing](/images/certs/cpts-screenshot-tool.png)
- Clipboard History Saver
     - Hear me out, it sounds simple but it is a lifesaver. Not every shell you will get during the exam will be flawless and have an up-button to view older commands, not every change in Active Directory will last, there are cleanup scripts and so on and so on. Trust me it causes great headache when you are trying to remember the command that worked but just can't find it anymore. Have a good, reliable clipboard manager. I use [clipse](https://github.com/savedra1/clipse) and it works without any problem. I can pin the entries that I don't want to disappear after I hit the maximum threshold. Give it a shot, and thank me later.
    ![Clipse clipboard manager](/images/certs/cpts-clipboard.png)
- SysReptor
    - I saw this tool being mentioned in every blog post I read related to CPTS so I will not talk about it too much. [SysReptor](https://sysreptor.com/), an amazing application for pentesters to write their reports. I personally hosted it on my other *Ubuntu* laptop so that I didn't have to pay any fees for cloud hosting. The best part? There are free templates for Hack The Box exams which will make your life so much easier. You can easily set it up by reading this [blog post](https://www.hackthebox.com/blog/certification-templates)
- Notes
    - During your testing you will be taking a lot of notes and to be honest you should. This is not only for proof when writing your report but also a way of organizing your thoughts, and strategies that you want to execute. Maybe there are people with over 180 IQ, memorizing all the information like they know their name. I certainly was not, and there is a chance that you will not either. To be honest we don't have to anyways. Take good notes, type your brainstorming ideas, credentials you found. Again as always there are so many options. I use neovim. I like having the efficiency of not needing to use my mouse.
    ![Neovim for note taking during exam](/images/certs/cpts-neovim.png)

### Operating system
I won't be writing too much about this part. Just pick one where you feel comfortable and efficient with navigating. Some hackers I've met use Windows as their main host and they usually have a Linux VM with all their tools installed.

They are very skilled and great hackers, however with all due respect to them, I don't like having Windows as my main host at all. I don't like having a bloated system, nor do I like the feeling that I don't actually own my computer. Yes you guessed it, I use Arch btw!
![I use Arch btw](/images/certs/cpts-arch.png)

Jokes aside, it is not that I am bragging about it by any means. It just suits my understanding of productivity. I like being able to find my way around with **hyprland** and the efficiency it brings. As pentesters, a majority of our time will be spent in front of our screens. So it is just better to make the most out of it. Again all personal preference. **One tip I would give is though**, have both! A Linux machine with all your tools installed, a Windows machine with Visual Studio installed where you can build **Windows-specific** tools from source when you are testing Windows applications. There are also some files which cause a lot of headache when you try to view them on Linux, so overall having a Windows machine, even if it is a VM, will be handy when you want to improve as a penetration tester.

# The Exam
You studied, got the required tools, now it is time to finally pass it. This part of the blog post explains what to do and what not to do during this 10 day long exam whether it is about the hacking part or writing the report.

## Penetration testing part
### Timing of the exam
I highly recommend doing the exam where your mind can almost completely focus on it. It is a tough and mentally exhausting exam. I personally started mine after the break we had upon finishing my school exams. It might feel like you can actually do both and to be honest you can maybe actually do both your exam and work or school stuff. However I am not sure if it is worth the risk.
### Reconnaissance
Recon will save you. When the exam starts, the only thing you will have is a single IP. Recon, recon and recon until no stone is unturned. If you don't see a path forward, you probably missed an endpoint, a domain, a machine. Be careful of the false positives and false negatives. The exam is designed to put you into rabbit holes. However it is still your job to know when something is a dead end, and it is maybe the time to change your perspective.

### Rest
**You will get stuck**. Yes you heard me right. There will be a point where you will feel like you've tried everything but still nothing seems to work. I had that moment. My ego was so crushed over a single specific flag I thought it was an error on their side. Restarted the environment thinking it would allow me to proceed, but still nothing :(

![Grinding at 3am](/images/certs/cpts-stuck.png)

I sat in front of my computer for 16 hours straight just to get that single flag. Most of you will understand which one that is when you start doing the exam. It got late, I am still in front of my screen frustrated and feeling like a fraud. My girlfriend told me to have a rest and sleep.

Unwillingly I listened to her, and when I woke up a new idea popped up in my mind. I thought why not try that as well. And it worked! From there on it was pretty straightforward. I got all the flags in about 5 to 6 days and the report took me an additional 2 days which I will be talking about now.

It is true you still need to spend a lot of time doing the exam, however do not skip the rest. Take a walk, train, splash some cold water to your face, pause and you will see the ideas coming up.

## Writing the report
I failed my first attempt. Not because I couldn't get enough flags, no. But because I failed to meet the standards when it comes to writing a commercial grade report. I got lazy and complacent in short. I don't want you to experience the same, so don't do what I did. Put enough time, energy, and effort so that all your time studying and the effort you put into getting the flags during the exam won't be a waste.

### Read the CPTS mock report
Since you finished all 28 modules, I am assuming you read the **Reporting Module** as well. In one of those pages you will find a report created by Hack The Box themselves. Read it carefully. A good report consists of the right balance between being too detailed where it is just long and messy and being too vague where the IT team reading your report can't even replicate the results. That is why you should read that report. See which fields you should take screenshots of, which fields to note, the PoCs and so on.

During my second attempt, thanks to the examiners' feedback, I knew what I had to change and I didn't have to redo the whole exam from the beginning (Thank God)! I fixed my errors, restarted the lab environment and put myself into the shoes of the company's technical dudes reading the report and see if I could replicate it. Even though I rewrote the whole thing, I saw there were still some serious logic errors and typos.

Finish the report and try to replicate it just by reading your walkthrough.

### Write while doing the exam
Another mistake I made was I didn't take detailed enough notes whilst I was doing the exam and capturing the flags. I still took the screenshots and brief notes, however I realized at the end it was too overwhelming and difficult to bring all that mess into a structured report.

Write while you are doing the exam. You get an initial foothold? Make sure your shell is stable and then start writing what you had so far. You escalated your privileges? Again, start writing. Do not let them all pile up at the end.


# Summary
CPTS is a good, well thought and prepared exam. The course material is incredibly high quality, covering from old techniques to get the foundations, then the more modern techniques which are actually useful to even build up on top of the basics you acquired.

Do not stress it out. I love hacking and since you are taking this exam, you probably do as well. Enjoy it. It is a one time experience in your life.

I did my job. I had a lot of tips from the community while I was preparing for my exam, so it is my responsibility to give back the help I got to people. Study hard, crush the exam and get those stickers on the back of your laptop.
![CPTS badge](/images/certs/cpts-badge.jpg)

I hope you enjoyed my blog. If you have any questions you can send me a text on **LinkedIn**, I would be happy to help. Keep learning, keep hacking! See you on the next one.
