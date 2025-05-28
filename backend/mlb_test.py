from pybaseball import statcast_batter, playerid_lookup
import pandas as pd

# Example: Get Aaron Judge's player ID
player_info = playerid_lookup("Judge", "Aaron")
mlb_id = player_info.iloc[0]["key_mlbam"]
print(f"Aaron Judge MLB ID: {mlb_id}")

# Get last 7 days of Statcast data for Judge
data = statcast_batter('2025-05-20', '2025-05-27', player_id=mlb_id)
print(data.head())
