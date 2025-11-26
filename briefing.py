import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import openai  # For Grok API (OpenAI-compatible)

# === CONFIGURE THESE 4 LINES ONLY (DO NOT PUT REAL KEYS HERE) ===
GROK_API_KEY = os.getenv("GROK_API_KEY")          # Comes from GitHub Secrets
EMAIL_TO = os.getenv("EMAIL_TO")
EMAIL_FROM = os.getenv("EMAIL_FROM")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# Set up OpenAI client for Grok API
client = openai.OpenAI(
    api_key=GROK_API_KEY,
    base_url="https://api.x.ai/v1"
)

# The perfect prompt we built together
today = datetime.now().strftime("%B %d, %Y")  # e.g., "November 26, 2025"
PROMPT = f"""You are the world's best macro analyst writing my private morning briefing. Today is {today} — use this exact date everywhere.

Deliver a clean, beautiful, highly readable daily briefing in **HTML** (so it renders perfectly in Gmail with bold, colors, spacing, tables, emojis).

Strictly separate into two main sections:

────────────────────────
MARKETS & FINANCE
────────────────────────
→ Start with a one-line TL;DR of the overnight price action.
→ Then 3–5 of the most important market/finance stories of the last 24 hours.
→ For each story: one strong headline + 2–3 sentences of neutral, fact-dense explanation + exact numbers.
→ When relevant, insert a clean HTML table with current levels and 24h change for: S&P 500, Nasdaq 100, Eurostoxx 50, DAX, Nikkei, Gold, WTI/Brent, US 10-yr yield, German 10-yr, VIX, DXY, BTC.

────────────────────────
GEOPOLITICS & POLICY
────────────────────────
→ 3–5 of the most market-relevant geopolitical / central-bank / regulatory stories.
→ Same format: strong headline + 2–3 sentences + key quotes or numbers.
→ Bias distribution line only when coverage clearly diverges.

End the entire briefing with this exact final line in bold red:
**What actually matters today:** [one single, sharp sentence summarising the dominant risk/theme of the day]

Rules:
- Use real sources only (Bloomberg, Reuters, FT, WSJ, ECB/Fed statements, exchange data).
- Never moralise, never speculate, never use emotional language.
- Use bold, italics, emojis, spacing and HTML tables liberally to make it beautiful and scannable.
- Maximum total length: whatever is needed — this is for a professional, depth is welcome.

Start now."""

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
    try:
        msg = MIMEText(briefing, 'html')   # ← changed from 'plain' to 'html'
        msg['Subject'] = f"Macro Briefing – {today}"
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_FROM, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("HTML briefing sent successfully!")
    except Exception as e:
        print(f"Email failed: {e}")

# Run it
if __name__ == "__main__":
    briefing = generate_briefing()
    send_email(briefing)
