## Decisions

Sources:
1. Understat - Every player's games, minutes, goals, assists, expected goals (xG) and expected assists (xA), for this season or any season since 2014.

2. Transfermarkt-api - Every squad, with each player's position, age and current market value

Other sources offer either outdated or incomplete data required for this project. For example, I first considered the FPL (Fantasy Premier League) API and API-Football's free plan as sources for player stats. If we chose to use these sources we would greatly limit the app, as the FPL would only provide premier league player stats and API-Football would only cover the 2022 to 2024 seasons. I want a wide variety of players across Europe and up-to-date data so that the app could be used to scout current undervalued players.

Used uv as the installer but kept requirements.txt. I am going with this approach because uv is much faster than pip in general. Though, not everyone has uv installed, so I kept requirements.txt because it works with plain pip, which everyone with Python already has.

Tweaks:
base value: 15mil -> 16.5mil
age factors: (21: 1.3 -> 1.35), (25: 1.2 -> 1.4), (28: 1.0 -> 1.5),  (30: 0.7 -> 0.9), added (34, 0.7), (99: 0.4 -> 0.3)
typical output: (fwd: 0.45 -> 0.4), (mid: 0.22 -> 0.2)
xA weight: 0.8 -> 0.85
output factor: 0.5 -> 1.0
output limits: min(0.4 -> 0.3), max(2.5 -> 3.0)
position factors: (fwd: 1.2 -> 1.3), (mid: 1.0 -> 1.1)
leauge factors: (EPL: 1.5 -> 1.75), (La_Liga: 1.1 -> 1.2), (Bundaesliga: 1.0 -> 1.1)

the leauge and season are hardcoded in right now


## Bugs

## Planned features