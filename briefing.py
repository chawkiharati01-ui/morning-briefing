import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import openai  # For Grok API (OpenAI-compatible)

# === CONFIGURE THESE 4 LINES ONLY ===
GROK_API_KEY = "xai-thvtrBeBMMTbJqjZ4n2GOsETavsZmJyJn43XBnFeh01TxVAZFGKCrv1AVjeGL17SYebVfhG9X8m6DNP9"  # Get from https://console.x.ai/api-keys
EMAIL_TO = "chawki.harati01@gmail.com"      # Where to send the briefing
EMAIL_FROM = "chawki.harati01@gmail.com"    # Your sending email (same as TO if testing)
SMTP_PASSWORD = "ygsl timj axcl flhz"      # Gmail app password (see Step 2 below)

# Set up OpenAI client for Grok API
client = openai.OpenAI(
    api_key=GROK_API_KEY,
    base_url="https://api.x.ai/v1"
)

# The perfect prompt we built together
today = datetime.now().strftime("%B %d, %Y")  # e.g., "November 26, 2025"
PROMPT = f"""You are an impartial senior analyst. Today is {today} (use this exact date everywhere).

Deliver a strict Ground News-style daily briefing covering ONLY financial markets and geopolitics from the last 24 hours.

Sources priority: Bloomberg, Reuters, FT, WSJ, AP, AFP, official statements, exchange filings. Never use Wikipedia, X threads, or opinion pieces as facts.

For each major story:
• One completely neutral single-sentence summary
• Today’s bias distribution (e.g. “Covered by 34 left, 19 center, 28 right-leaning outlets” or “Right-leaning blindspot”)
• Only verifiable facts (prices, %, quotes, data)
• One example source from L|C|R only when coverage diverges

End with exactly these two sections:
• What the market is currently pricing in (CME FedWatch, yields, VIX, FX, etc.)
• What to watch tomorrow (events & times)

Structure in clean markdown. Maximum 600 words total.

**Top Stories – {today}**

1. …

**What the market is currently pricing in**

**What to watch tomorrow**"""

def generate_briefing():
    response = client.chat.completions.create(
        model="grok-4",
        messages=[
            {"role": "system", "content": "You are an impartial senior analyst. Never moralize, speculate, or use emotional language."},
            {"role": "user", "content": PROMPT}
        ],
        temperature=0.2,
        max_tokens=1400
    )
    return response.choices[0].message.content

def send_email(briefing):
    msg = MIMEText(briefing, 'plain')
    msg['Subject'] = f"Daily Markets & Geopolitics Briefing – {today}"
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO

    # Gmail SMTP (change server/port if using Outlook/etc.)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_FROM, SMTP_PASSWORD)
    server.send_message(msg)
    server.quit()
    print("Briefing sent successfully!")

# Run it
if __name__ == "__main__":
    briefing = generate_briefing()
    send_email(briefing)
