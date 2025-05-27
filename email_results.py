
import smtplib
from email.message import EmailMessage
import pandas as pd

# Load the updated CSV
df = pd.read_csv("bet_log.csv")

# Extract summary row
summary = df[df["Date"] == "SUMMARY"].iloc[0]
subject = f"MLB Model Update - ROI {summary['Result']} | Total Profit ${summary['Profit_Loss']:.2f}"

# Build email body
body = f"""
✅ Daily MLB Model Summary

Total Bets Placed: {summary['Bet_Placed?']}
ROI: {summary['Result']}
Profit/Loss: ${summary['Profit_Loss']:.2f}

Notes: {summary['Notes']}

Full log attached.
"""

# Compose email
msg = EmailMessage()
msg["Subject"] = subject
msg["From"] = "aronklarson@gmail.com"         # Replace with your Gmail
msg["To"] = "aronklarson@gmail.com"           # Replace with your destination email
msg.set_content(body)

# Attach CSV
with open("bet_log.csv", "rb") as f:
    msg.add_attachment(f.read(), maintype="application", subtype="octet-stream", filename="bet_log.csv")

# Send
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login("aronklarson@gmail.com", "rtmf tdtn usmj dxbr")  # Replace with your app password
    smtp.send_message(msg)

print("📧 Summary email sent.")
