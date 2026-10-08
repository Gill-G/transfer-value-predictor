"""My own market value formula: a starting value, scaled up or down by factors I choose."""

import requests
import pandas as pd


# ---------------- The dials: tweak these ----------------

BASE_VALUE = 16_500_000        # what an average player is worth before any factor is applied

AGE_FACTORS = [(21, 1.35), (25, 1.4), (28, 1.5), (30, 0.9), (34, 0.7), (99, 0.3)]  # (oldest age in band, factor): younger = worth more

TYPICAL_OUTPUT = {"FWD": 0.4, "MID": 0.2, "DEF": 0.08}  # normal xG + xA per 90 for each position
XA_WEIGHT = 0.85                 # how much one expected assist counts compared with one expected goal
OUTPUT_POWER = 1.0               # 0 = output doesn't matter, 1 = twice the output means twice the value
OUTPUT_LIMITS = (0.3, 3.0)       # the smallest and biggest the output factor is allowed to be

MINUTES_FLOOR = 0.6            # factor for a player with almost no minutes (2,500+ minutes gets 1.0)

POSITION_FACTORS = {"FWD": 1.3, "MID": 1.1, "DEF": 0.85}  # forwards cost more, defenders less
LEAGUE_FACTORS = {"EPL": 1.75, "La_Liga": 1.2, "Bundesliga": 1.1, "Serie_A": 0.95, "Ligue_1": 0.85}  # Premier League costs the most

LEAGUE = "EPL"      # which league to download (must be one of the keys)
SEASON = "2025"      # season start year will be 2025 = the 2025/26 season


# ---------------- The formula ----------------

def age_factor(age):
    for oldest, factor in AGE_FACTORS:          # check each age band, youngest first
        if age <= oldest:                    # the first band the player fits into
            return factor


def output_factor(player):
    output = player["xg_per90"] + XA_WEIGHT * player["xa_per90"]
    ratio = output / TYPICAL_OUTPUT[player["position"]]
    factor = ratio ** OUTPUT_POWER
    low, high = OUTPUT_LIMITS
    return max(low, min(high, factor))


def minutes_factor(minutes):
    share = min(minutes, 2500) / 2500                  
    return MINUTES_FLOOR + (1 - MINUTES_FLOOR) * share  


def my_value(player):
    value = BASE_VALUE
    value *= age_factor(player["age"])
    value *= output_factor(player)
    value *= minutes_factor(player["minutes"])
    value *= POSITION_FACTORS[player["position"]]
    value *= LEAGUE_FACTORS[player["league"]]
    return value                                     # the final estimate in euros


def short_position(understat_position):
    first_letter = understat_position[0]        # Understat gives ex: "F M S" -> we only need "F"
    if first_letter == "F":
        return "FWD"
    if first_letter == "M":
        return "MID"
    if first_letter == "D":
        return "DEF"
    return None                           # no goalkeepers ("GK")


# ---------------- Scoring: how close is my formula? ----------------

# # def score(name, players, median):
# #     actual = players["market_value"]
# #     median_guess = [median] * len(players)
# #     print(f"{name}: my formula is off by €{mean_absolute_error(actual, players['estimate']) / 1e6:.1f}m on average, "
# #           f"guessing the median is off by €{mean_absolute_error(actual, median_guess) / 1e6:.1f}m")


# df = pd.read_csv(PLAYERS_FILE)
# df["xg_per90"] = df["xg"] / df["minutes"] * 90
# df["xa_per90"] = df["xa"] / df["minutes"] * 90
# df["estimate"] = df.apply(my_value, axis=1)

# # The same split as train.py, so the two can be compared fairly
# train, test = train_test_split(df, test_size=0.2, random_state=42)

# median = train["market_value"].median()
# # score("Training players (tune on these)", train, median)
# # score("Test players (check once, at the end)", test, median)

# print("\nBiggest misses among training players:")
# train = train.assign(miss=train["estimate"] - train["market_value"])
# biggest = train.reindex(train["miss"].abs().sort_values(ascending=False).index).head(10)
# for _, p in biggest.iterrows():
#     print(f"  {p['name']:<22} {p['age']:>2} {p['position']} {p['league']:<10} {p['minutes']:>5.0f} min  "
#           f"value €{p['market_value'] / 1e6:5.1f}m  mine €{p['estimate'] / 1e6:5.1f}m")


# ---------------- getting datra ----------------

url = f"https://understat.com/getLeagueData/{LEAGUE}/{SEASON}"  # tryin out variables
# url = "https://understat.com/getLeagueData/EPL/2025"
headers = {"X-Requested-With": "XMLHttpRequest"}

response = requests.get(url, headers=headers)
response.raise_for_status()                      # stop with an error if the download failed
print("Status Code:", response.status_code, "\n")

data = response.json()              # parse JSON into a python dictionary
df = pd.DataFrame(data["players"])  # store the players in a table: this is our variable

df["name"] = df["player_name"]              # renaming Understat's columns to the names the formula uses
df["minutes"] = df["time"].astype(float)        # understat sends numbers as strings so turn i them into numbers
df["xg"] = df["xG"].astype(float)
df["xa"] = df["xA"].astype(float)
df["position"] = df["position"].apply(short_position)  # renaming postion names to match key names in POSITION_FACTORS
df["league"] = LEAGUE

df = df[df["position"].notna()]          # drop goalkeepers cuz they not a key
df = df[df["minutes"] > 0]        # drop players with no minutes (was having divide by 0 eror)

df["xg_per90"] = df["xg"] / df["minutes"] * 90 
df["xa_per90"] = df["xa"] / df["minutes"] * 90 

print("Players loaded:", len(df), "\n")


# ---------------- predicting a player's value witht he formula ----------------

name = input("Player name: ")
matches = df[df["name"].str.contains(name, case=False)]

if len(matches) == 0:
    print("No player found with that name.")
else:
    player = matches.iloc[0].copy()     # take the first match as one row
    player["age"] = int(input(f"Age of {player['name']}: "))   # understat has no ages

    print()
    print(f"{player['name']} ({player['position']}, {player['team_title']})")
    print(f" Minutes: {player['minutes']:.0f}")
    print(f" xG per 90: {player['xg_per90']:.2f}   xA per 90: {player['xa_per90']:.2f}")
    print(f" Age factor: {age_factor(player['age'])}") 
    print(f" Output factor: {output_factor(player):.2f}")
    print(f" Minutes factor: {minutes_factor(player['minutes']):.2f}")
    print(f" My value: €{my_value(player) / 1e6:.1f}m")