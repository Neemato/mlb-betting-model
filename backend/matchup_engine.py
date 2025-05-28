# backend/matchup_engine.py

from pybaseball import playerid_lookup, statcast_batter, statcast_pitcher
from datetime import datetime, timedelta
import statsapi

def get_player_id(first_name, last_name):
    """Return MLBAM player ID from full name."""
    try:
        result = playerid_lookup(last_name, first_name)
        return int(result.iloc[0]['key_mlbam'])
    except:
        return None

def get_recent_batter_data(player_id, days=14):
    """Return Statcast data for a batter over the past X days."""
    end = datetime.today().date()
    start = end - timedelta(days=days)
    return statcast_batter(start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'), player_id=player_id)

def get_recent_pitcher_data(player_id, days=14):
    """Return Statcast data for a pitcher over the past X days."""
    end = datetime.today().date()
    start = end - timedelta(days=days)
    return statcast_pitcher(start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'), player_id=player_id)

from pybaseball import statcast_batter

def get_h2h_matchup(pitcher_id, batter_id):
    """Get all historical pitches between pitcher and batter."""
    start = "2018-01-01"  # Wider range for more matchup history
    end = datetime.today().strftime('%Y-%m-%d')
    data = statcast_batter(start, end, player_id=batter_id)

    # Filter for pitches from specific pitcher
    h2h_data = data[data['pitcher'] == pitcher_id]

    if h2h_data.empty:
        print(f"No historical matchups found between these players.")
        return None

    results = {
    "PA": int(h2h_data["at_bat_number"].nunique()),
    "Pitches Seen": int(len(h2h_data)),
    "Hits": int(h2h_data["events"].isin(["single", "double", "triple", "home_run"]).sum()),
    "HR": int((h2h_data["events"] == "home_run").sum()),
    "K": int((h2h_data["events"] == "strikeout").sum()),
    "BB": int((h2h_data["events"] == "walk").sum()),
    "All Events": {k: int(v) for k, v in h2h_data["events"].dropna().value_counts().items()}
}


    return results

# Example usage
if __name__ == "__main__":
    # Let's test pulling data for Aaron Judge and Gerrit Cole
    batter_id = get_player_id("Aaron", "Judge")
    pitcher_id = get_player_id("Gerrit", "Cole")

    if batter_id:
        batter_data = get_recent_batter_data(batter_id)
        print(f"Aaron Judge last 14 days:\n", batter_data[["game_date", "pitch_type", "events", "launch_speed"]].head())

    if pitcher_id:
        pitcher_data = get_recent_pitcher_data(pitcher_id)
        print(f"\nGerrit Cole last 14 days:\n", pitcher_data[["game_date", "pitch_type", "release_speed", "description"]].head())
            
    if pitcher_id and batter_id:
        print("\n--- H2H Matchup Judge vs Cole ---")
        h2h_stats = get_h2h_matchup(pitcher_id, batter_id)
        print(h2h_stats)

    if pitcher_id and batter_id:
        print("\n--- H2H Matchup Judge vs Cole ---")
        h2h_stats = get_h2h_matchup(pitcher_id, batter_id)
        print(h2h_stats)


def get_h2h_matchup(pitcher_id, batter_id):
    """Get all historical pitches between pitcher and batter."""
    start = "2018-01-01"  # Wider range for more matchup history
    end = datetime.today().strftime('%Y-%m-%d')
    data = statcast_batter(start, end, player_id=batter_id)

    # Filter for pitches from specific pitcher
    h2h_data = data[data['pitcher'] == pitcher_id]

    if h2h_data.empty:
        print(f"No historical matchups found between these players.")
        return None

    results = {
        "PA": h2h_data["at_bat_number"].nunique(),
        "Pitches Seen": len(h2h_data),
        "Hits": h2h_data["events"].isin(["single", "double", "triple", "home_run"]).sum(),
        "HR": (h2h_data["events"] == "home_run").sum(),
        "K": (h2h_data["events"] == "strikeout").sum(),
        "BB": (h2h_data["events"] == "walk").sum(),
        "All Events": h2h_data["events"].dropna().value_counts().to_dict()
    }

    return results
