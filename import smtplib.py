import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
        print("Login successful!")
except Exception as e:
    print("Login failed:", e)

print("Email:", os.getenv("EMAIL_ADDRESS"))
print("Password:", os.getenv("EMAIL_PASSWORD"))
