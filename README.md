**Cyber News Digest – Automated Cybersecurity Intelligence Feed**



**Overview**
Cyber News Digest is an automated system that collects, processes, and delivers a curated cybersecurity news summary directly to your inbox. It runs entirely in the cloud using GitHub Actions, requiring no local machine or manual intervention once deployed.
This project demonstrates secure automation, workflow orchestration, Python development, and operational reliability — skills relevant to modern security engineering and applied AI safety roles.



**Features**
* Automated Cybersecurity News Collection  
Pulls articles from multiple trusted RSS feeds using Python.

* HTML Email Digest  
Formats news items into a clean, readable HTML email.

* Scheduled Cloud Execution  
Runs automatically via GitHub Actions on a twice‑daily cron schedule.

* Secure Credential Handling  
Uses GitHub Secrets to store email credentials safely.

* Fully Reproducible  
Anyone can fork the repo, add secrets, and run their own automated digest.



**Architecture**
1. Python Script (cyber_news_digest.py)
* Fetches RSS feeds
* Parses and filters articles
* Generates HTML output
* Sends email via SMTP

2. GitHub Actions Workflow (daily-digest.yml)
* Runs on ubuntu-latest
* Installs dependencies
* Executes the script
* Sends digest twice daily

3. Secrets Management
* EMAIL_ADDRESS
* EMAIL_PASSWORD
* RECIPIENT



**Schedule**
The digest runs twice per day using GitHub Actions cron:

Code
5 7 * * *   # 08:05 UK time
5 19 * * *  # 20:05 UK time



**Setup Instructions**
Clone the repository

Add required secrets under
Settings → Secrets and variables → Actions

Review or modify RSS feeds in the script

Push changes — GitHub Actions handles the rest
