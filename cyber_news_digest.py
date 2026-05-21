#had to add this when i was having email problems
from dotenv import load_dotenv
import os

#print working directory
import os
print("Working directory:", os.getcwd())


env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)


import feedparser
from datetime import datetime, timedelta, UTC
#added UTC here as python didnt know it

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

# Trusted cybersecurity sources (feel free to add more!)
FEEDS = {
    "The Hacker News": "https://feeds.feedburner.com/TheHackersNews",
    "Krebs on Security": "https://krebsonsecurity.com/feed/",
    "BleepingComputer": "https://www.bleepingcomputer.com/feed/",
    "Dark Reading": "https://www.darkreading.com/rss.xml",
    "SecurityWeek": "https://feeds.feedburner.com/securityweek",
    "Civil Eats": "https://feeds.feedburner.com/CivilEats",
    "Billboard": "https://www.billboard.com/feed",
    "BBC World News  ": "https://feeds.bbci.co.uk/news/world/rss.xml",
    "Aljazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "Dow Jones": "https://feeds.content.dowjones.io/public/rss/mw_topstories",
    "Modern Healthcare": "https://www.modernhealthcare.com/section/rss",
    "NHS Cyber Alerts Feed": "https://digital.nhs.uk/feed/cyber-alerts-feed.xml",
    "All NHS Digital Blogs": "https://digital.nhs.uk/feed/all-blog-feed.xml",
    "NHS Statistical Publications Feed": "https://digital.nhs.uk/feed/pubfeed.xml",
}

def get_recent_news(hours=36):
    all_news = []
    cutoff = datetime.now(UTC) - timedelta(hours=hours)

    for source, url in FEEDS.items():
        try:
            feed = feedparser.parse(url)

            for entry in feed.entries:
                pub_time = None

                # Extract published or updated time
                for field in ['published_parsed', 'updated_parsed']:
                    if entry.get(field):
                        # Convert naive → aware UTC
                        pub_time = datetime(*entry[field][:6]).replace(tzinfo=UTC)
                        break

                if not pub_time or pub_time < cutoff:
                    continue

                # Clean HTML from summary
                raw_summary = entry.get('summary', '')
                summary = BeautifulSoup(raw_summary, "html.parser").get_text()[:280]
                if summary:
                    summary += "..."

                all_news.append({
                    "source": source,
                    "title": entry.get('title', 'No title'),
                    "link": entry.get('link', '#'),
                    "summary": summary,
                    "published": pub_time
                })

        except Exception as e:
            print(f"⚠️ Error fetching {source}: {e}")

    # Sort newest first + limit to top 20
    all_news.sort(key=lambda x: x["published"], reverse=True)
    return all_news[:20]


def send_email(news_list):
    if not news_list:
        print("No new articles today.")
        return
    
    today = datetime.now().strftime("%B %d, %Y")
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h1>🛡️ Daily Cybersecurity Digest - {today}</h1>
        <p>Good morning! Here's your curated roundup from trusted sources:</p>
        <ul style="list-style-type: none; padding: 0;">
    """
    for item in news_list:
        html += f"""
        <li style="margin-bottom: 20px; padding: 10px; border-left: 4px solid #0066cc;">
            <strong>{item['source']}</strong><br>
            <a href="{item['link']}" style="font-size: 18px; color: #0066cc;">{item['title']}</a><br>
            <small>{item['summary']}</small>
        </li>
        """
    html += """
        </ul>
        <p><em>🤖 Automation powered by Spitzfm UK Radio • Stay curious and stay safe!</em></p>
    </body>
    </html>
    """
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🛡️ Daily Cyber News Digest - {today}"
    msg["From"] = os.getenv("EMAIL_ADDRESS")
    msg["To"] = os.getenv("RECIPIENT")
    msg.attach(MIMEText(html, "html"))
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
            server.send_message(msg)
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    print("Fetching latest cybersecurity news...")
    news = get_recent_news()
    send_email(news)