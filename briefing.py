import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import openai  # For Grok API (OpenAI-compatible)
import time

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

Structure — exactly in this order, always the same number of items:

────────────────────────
OVERNIGHT SUMMARY (1 sentence in bold green)
────────────────────────
One razor-sharp TL;DR of global risk tone and the dominant driver.

────────────────────────
MARKETS & FINANCE (exactly 5 stories)
────────────────────────
Exactly 5 of the most important market/finance stories of the last 24 hours.
Bold headline + 3–5 dense sentences + exact numbers.
Insert HTML price table when relevant (S&P 500, Nasdaq 100, Eurostoxx 50, DAX, Nikkei, Gold, Brent, US 10-yr, Bund 10-yr, VIX, DXY, BTC/USD).

────────────────────────
TECH INDUSTRY & MEGACAPS (exactly 5 stories)
────────────────────────
Exactly 5 of the most important tech-sector / megacap / AI / semiconductor stories.
Same format + key numbers (earnings, capex, regulatory, options flow, etc.).

────────────────────────
GEOPOLITICS & POLICY (exactly 5 stories)
────────────────────────
Exactly 5 of the most market-relevant geopolitical, central-bank, regulatory or trade stories.
Same format + quotes/numbers. Bias line only when coverage clearly diverges.

────────────────────────
RATES & FX PRICING SNAPSHOT
────────────────────────
Compact HTML table with:
• Fed Funds (Dec25, Mar26, Jun26) – CME FedWatch %
• ECB Deposit rate expectations (same dates)
• 2y/10y US Treasury spread
• Key FX pairs (EURUSD, USDJPY, GBPUSD, USDCNH) spot + 24h change

────────────────────────
WHAT TO WATCH TOMORROW – MARKETS & DATA
────────────────────────
Bullet list of the 4–6 most important economic releases, earnings, or market events for the next 24–48h (include time zone = Paris).

────────────────────────
WHAT TO WATCH TOMORROW – GEOPOLITICS & POLICY
────────────────────────
Bullet list of the 4–6 most important geopolitical meetings, speeches, deadlines, or risk events for the next 24–48h.

End with this exact line in bold red:
**What actually matters today:** [one single, razor-sharp sentence summarising the dominant risk or trade of the day]

Rules: Bloomberg/Reuters/FT/WSJ/ECB-Fed-BOJ/SEC level sourcing only. Depth required. Never truncate. Use HTML aggressively for beauty.

Start now."""

def generate_briefing():
    for attempt in range(3):  # 3 tentatives max
        try:
            response = client.chat.completions.create(
                model="grok-4",
                messages=[
                    {"role": "system", "content": "You are a world-class macro and tech analyst. Always complete the full briefing."},
                    {"role": "user", "content": PROMPT}
                ],
                temperature=0.25,
                max_tokens=6000,
                timeout=300
            )
            return response.choices[0].message.content
            
        except openai.APITimeoutError:
            print(f"Timeout attempt {attempt+1}/3 – retrying in 10s...")
            time.sleep(10)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)
    
    raise Exception("Failed after 3 attempts")

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
