## Decisions

Sources:
1. Understat - Every player's games, minutes, goals, assists, expected goals (xG) and expected assists (xA), for this season or any season since 2014.

2. Transfermarkt-api - Every squad, with each player's position, age and current market value

Other sources offer either outdated or incomplete data required for this project. For example, I first considered the FPL (Fantasy Premier League) API and API-Football's free plan as sources for player stats. If we chose to use these sources we would greatly limit the app, as the FPL would only provide premier league player stats and API-Football would only cover the 2022 to 2024 seasons. I want a wide variety of players across Europe and up-to-date data so that the app could be used to scout current undervalued players.

Used uv as the installer but kept requirements.txt. I am going with this approach because uv is much faster than pip in general. Though, not everyone has uv installed, so I kept requirements.txt because it works with plain pip, which everyone with Python already has.


## Bugs

## Planned features