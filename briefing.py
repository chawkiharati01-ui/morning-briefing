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
PROMPT = f"""You are the best macro + tech analyst on the planet writing my private morning briefing for an asset-management firm.

Today is {today} — use this exact date everywhere.

Deliver a beautiful, data-rich, perfectly balanced briefing in **HTML** (Gmail-ready with bold, colors, spacing, tables, emojis).

Structure — exactly in this order, always the same number of items in each section:

────────────────────────
OVERNIGHT SUMMARY (1 sentence in bold green)
────────────────────────
One sharp TL;DR of global risk tone and the dominant driver.

────────────────────────
MARKETS & FINANCE (exactly 5 stories)
────────────────────────
Give exactly 5 of the most important market/finance stories of the last 24 hours.
For each:
• Strong headline in bold
• 3–5 sentences of dense, neutral explanation with exact numbers/quotes
• When relevant, insert a clean HTML table with current levels + 24h change for: S&P 500, Nasdaq 100, Eurostoxx 50, DAX, Nikkei, Gold, Brent, US 10-yr, Bund 10-yr, VIX, DXY, BTC/USD

────────────────────────
TECH INDUSTRY & MEGACAPS (exactly 5 stories)
────────────────────────
Give exactly 5 of the most important tech-sector / megacap / AI / semiconductor stories.
Same format: bold headline + 3–5 sentences + key numbers (revenue moves, capex announcements, regulatory filings, options flow, etc.)

────────────────────────
GEOPOLITICS & POLICY (exactly 5 stories)
────────────────────────
Give exactly 5 of the most market-relevant geopolitical, central-bank, regulatory or trade stories.
Same format: bold headline + 3–5 sentences + quotes or hard numbers.
Add bias distribution only when coverage clearly diverges.

────────────────────────
RATES & FX PRICING SNAPSHOT
────────────────────────
One compact HTML table with:
• Fed Funds (Dec25, Mar26, Jun26) – CME FedWatch %
• ECB Deposit rate expectations (same dates)
• 2y/10y US Treasury spread
• Key FX pairs (EURUSD, USDJPY, GBPUSD, USDCNH) spot + 24h change

End with this exact line in bold red:
**What actually matters today:** [one single, razor-sharp sentence summarising the dominant risk or trade of the day]

Rules:
- Sources only: Bloomberg, Reuters, FT, WSJ, Fed/ECB/BOJ statements, exchange data, SEC/EMA filings.
- Never moralise, speculate or use emotional language.
- Use bold, italics, colors, emojis, spacing and HTML tables aggressively — make it gorgeous and instantly scannable.
- Depth is required — this is for a professional AM desk.
- Never truncate — you have plenty of tokens.

Start now."""

def generate_briefing():
    response = client.chat.completions.create(
        model="grok-4",
        messages=[
            {"role": "system", "content": "You are a world-class macro and tech analyst. Always complete the full briefing."},
            {"role": "user", "content": PROMPT}
        ],
        temperature=0.25,
        max_tokens=4000,          # ← guarantees completion
        timeout=120
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
