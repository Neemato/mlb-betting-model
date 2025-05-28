from pybaseball import cache
cache.enable()


import statsapi
from pybaseball import statcast_batter, statcast_pitcher
import pandas as pd

def get_player_id(name):
    people = statsapi.lookup_player(name)
    return people[0]['id'] if people else None

def get_recent_batter_data(player_id, days=14):
    return statcast_batter(start_dt=pd.Timestamp.today() - pd.Timedelta(days=days), 
                           end_dt=pd.Timestamp.today(), player_id=player_id)

def get_recent_pitcher_data(player_id, days=14):
    return statcast_pitcher(start_dt=pd.Timestamp.today() - pd.Timedelta(days=days), 
                            end_dt=pd.Timestamp.today(), player_id=player_id)

import pandas as pd
from pybaseball import statcast

def get_h2h_matchup(pitcher_id, batter_id, days=730):
    start = (pd.Timestamp.today() - pd.Timedelta(days=days)).strftime('%Y-%m-%d')
    end = pd.Timestamp.today().strftime('%Y-%m-%d')

    df = statcast(start_dt=start, end_dt=end)
    matchup = df[(df['batter'] == batter_id) & (df['pitcher'] == pitcher_id)]

    if matchup.empty:
        return {"H2H": "No matchup history found"}

    summary = {
        "PA": len(matchup),
        "Hits": matchup['events'].isin(['single', 'double', 'triple', 'home_run']).sum(),
        "HR": matchup['events'].eq('home_run').sum(),
        "K": matchup['events'].eq('strikeout').sum(),
        "BB": matchup['events'].eq('walk').sum(),
        "AVG Exit Velo": round(matchup['launch_speed'].dropna().mean(), 1)
    }
    return summary


