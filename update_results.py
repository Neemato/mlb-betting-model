
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Authenticate Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Load sheet
sheet = client.open("MLB Positive EV Props").sheet1
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Filter placed bets with results
placed = df[(df["Bet_Placed?"].str.lower() == "yes") & (df["Result"].isin(["Win", "Loss"]))]

# Convert Profit_Loss column to float
placed["Profit_Loss"] = pd.to_numeric(placed["Profit_Loss"], errors="coerce").fillna(0)

# Metrics
total_bets = len(placed)
total_profit = placed["Profit_Loss"].sum()
avg_bet = 100
roi = round((total_profit / (avg_bet * total_bets)) * 100, 2) if total_bets > 0 else 0

# Save bet log with summary
df["Profit_Loss"] = pd.to_numeric(df["Profit_Loss"], errors="coerce").fillna(0)
summary = pd.DataFrame([{
    "Date": "SUMMARY",
    "Player": "",
    "Team": "",
    "Opponent": "",
    "Prop_Type": "",
    "Line": "",
    "Projection": "",
    "Recommended_Bet": "",
    "Odds": "",
    "Model_Prob": "",
    "Implied_Prob": "",
    "Expected_Value": "",
    "Bet_Placed?": f"{total_bets} bets",
    "Result": f"ROI: {roi}%",
    "Profit_Loss": total_profit,
    "Notes": "Summary row"
}])

out = pd.concat([df, summary], ignore_index=True)
out.to_csv("bet_log.csv", index=False)
print("✅ Bet log updated with performance summary.")
