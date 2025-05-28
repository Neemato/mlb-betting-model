from utils.data_fetching import (
    get_player_id,
    get_h2h_matchup,
)

import statsapi


def extract_starting_pitcher(info_list):
    """Safely extract the starting pitcher from the boxscore info list."""
    for item in info_list:
        if item.get('title') == 'Starting Pitcher':
            try:
                return item['fieldList'][0]['value']
            except (IndexError, KeyError, TypeError):
                return None
    return None


def analyze_game(home, away):
    print(f"\n🔍 Analyzing {away} @ {home}")

    # Get today’s schedule and locate this specific game
    games = statsapi.schedule(sportId=1)
    game = next((g for g in games if g['home_name'] == home and g['away_name'] == away), None)

    if not game:
        print(f"❌ Could not find game for {away} @ {home}")
        return

    game_id = game.get('game_id') or game.get('gamePk')
    if not game_id:
        print(f"❌ No game ID for {away} @ {home}")
        return

    # First try to get boxscore starting pitchers
    home_pitcher = None
    away_pitcher = None
    try:
        box = statsapi.boxscore_data(game_id)
        home_pitcher = extract_starting_pitcher(box.get('home', {}).get('info', []))
        away_pitcher = extract_starting_pitcher(box.get('away', {}).get('info', []))
    except Exception:
        pass

    # If boxscore data fails, fall back to probable starters
    if not home_pitcher:
        home_pitcher = game.get('home_probable_pitcher')
    if not away_pitcher:
        away_pitcher = game.get('away_probable_pitcher')

    if not home_pitcher or not away_pitcher:
        print("⚠️ No probable or listed starting pitchers.")
        return

    print(f"\n🧢 Home Pitcher: {home_pitcher}")
    print(f"🧢 Away Pitcher: {away_pitcher}")

    # Placeholder lineups
    home_lineup = ["Aaron Judge", "Giancarlo Stanton"]
    away_lineup = ["Mookie Betts", "Freddie Freeman"]

    # Analyze away hitters vs home pitcher
    pitcher_id = get_player_id(home_pitcher)
    for batter in away_lineup:
        batter_id = get_player_id(batter)
        if batter_id and pitcher_id:
            print(f"\n⚔️ {batter} vs {home_pitcher}")
            h2h = get_h2h_matchup(pitcher_id, batter_id)
            print(h2h)

    # Analyze home hitters vs away pitcher
    pitcher_id = get_player_id(away_pitcher)
    for batter in home_lineup:
        batter_id = get_player_id(batter)
        if batter_id and pitcher_id:
            print(f"\n⚔️ {batter} vs {away_pitcher}")
            h2h = get_h2h_matchup(pitcher_id, batter_id)
            print(h2h)



def main():
    games = statsapi.schedule(sportId=1)
    matchups = [(g['home_name'], g['away_name']) for g in games]
    for home, away in matchups:
        analyze_game(home, away)


if __name__ == "__main__":
    main()
