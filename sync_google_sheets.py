import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Load the data
df = pd.read_csv("sample_player_props.csv")

# Calculate implied probability
def american_to_prob(odds):
    return round(100 / (odds + 100), 4) if odds > 0 else round(abs(odds) / (abs(odds) + 100), 4)

# Apply EV logic
ev_rows = []
for _, row in df.iterrows():
    proj = row["Model_Projection"]
    line = row["Prop_Line"]
    
    if proj > line:
        bet = "Over"
        odds = row["Odds_Over"]
        model_prob = 0.55 if proj - line > 1 else 0.52
    else:
        bet = "Under"
        odds = row["Odds_Under"]
        model_prob = 0.55 if line - proj > 1 else 0.52
    
    implied = american_to_prob(odds)
    ev = round((model_prob * abs(odds) / 100) - (1 - model_prob), 4)

    if ev > 0:
        ev_rows.append({
            "Player": row["Player"],
            "Team": row["Team"],
            "Opponent": row["Opponent"],
            "Prop_Type": row["Prop_Type"],
            "Line": line,
            "Projection": proj,
            "Recommended_Bet": bet,
            "Odds": odds,
            "Model_Prob": model_prob,
            "Implied_Prob": implied,
            "Expected_Value": ev
        })

filtered_df = pd.DataFrame(ev_rows)

# Authenticate Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Connect to the sheet
sheet = client.open("MLB Positive EV Props").sheet1
sheet.clear()
sheet.update([filtered_df.columns.values.tolist()] + filtered_df.values.tolist())

print("✅ Synced positive EV props to Google Sheets.")
