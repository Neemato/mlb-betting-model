import subprocess
from email_notify import send_email
import sys
import os

print("🟢 Running daily MLB model...")

python_exe = os.path.join(sys.prefix, "Scripts", "python.exe")

try:
    subprocess.run([python_exe, "sync_google_sheets.py"], check=True)
    send_email(
        subject="✅ MLB Props Synced",
        body="Your positive EV props have been synced to Google Sheets successfully.",
        to_email="aronklarson@gmail.com"  # Replace with your actual email
    )
    print("✅ Daily run and email complete.")

except Exception as e:
    send_email(
        subject="❌ MLB Sync Failed",
        body=f"There was an error during your MLB model sync:\n\n{str(e)}",
        to_email="aronklarson@gmail.com"
    )
    print("❌ Sync failed. Email alert sent.")
