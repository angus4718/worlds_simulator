# Tournament Simulation README

This repository contains a Python script, `worlds_simulator.py`, for simulating a custom tournament structure. The program uses team data from a spreadsheet and a Swiss-system format to simulate matches, determine standings, and identify the tournament champion. Below is a detailed explanation of the project, its setup, and usage. The format of the League of Legends 2024 World Championship was used.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Spreadsheet Format](#spreadsheet-format)
4. [Setup](#setup)
5. [How It Works](#how-it-works)
6. [Configuration](#configuration)
7. [Running the Simulation](#running-the-simulation)
8. [Outputs](#outputs)
9. [Customization](#customization)

---

## Overview

The script simulates a competitive tournament with the following phases:

1. **Play-in Stage**: Matches between lower-seeded teams to determine which advance to the next stage.
2. **Swiss Stage**: Teams are divided into pools and play multiple rounds of matches in the Swiss-system format to determine the top-performing teams.
3. **Knockout Stage**: The top 8 teams from the Swiss stage compete in a single-elimination bracket to determine the tournament champion.

The simulation uses team power ratings, randomization, and a configurable luck factor to simulate realistic match outcomes.

---

## Features

- **Team Power Ratings**: Determines the probability of a team winning any given match.
- **Luck Factor**: Adds randomness to the simulation, making results more dynamic.
- **Swiss-System Tournament**: Implements the Swiss-system format to rank teams over multiple rounds.
- **Knockout Stage**: Simulates quarterfinals, semifinals, and finals.
- **Repeatable Simulations**: Perform multiple simulation runs to analyze trends.
- **Customizable Parameters**: Adjust team data, luck factor, simulation loops, and match formats.

---

## Spreadsheet Format

The script requires a spreadsheet file (`settings.xlsx`) with the following structure in the `Teams` sheet:

| Team | Region | Seed | Power |
|------|--------|------|-------|
| HLE  | LCK    | 1    | 95    |
| GEN  | LCK    | 2    | 95    |
| DK   | LCK    | 3    | 85    |
| T1   | LCK    | 4    | 85    |
| BLG  | LPL    | 1    | 95    |
| TES  | LPL    | 2    | 85    |
| LNG  | LPL    | 3    | 75    |
| WBG  | LPL    | 4    | 75    |
| G2   | LEC    | 1    | 75    |
| FNC  | LEC    | 2    | 65    |
| MDK  | LEC    | 3    | 60    |
| FLY  | LCS    | 1    | 75    |
| TL   | LCS    | 2    | 65    |
| 100  | LCS    | 3    | 60    |
| PSG  | PCS    | 1    | 70    |
| SHG  | PCS    | 2    | 60    |
| GAM  | VCS    | 1    | 60    |
| VKE  | VCS    | 2    | 50    |
| PNG  | CBLOL  | 1    | 40    |
| R7   | LATAM  | 1    | 40    |

### Column Descriptions:

- **Team**: The name or abbreviation of the team.
- **Region**: The region the team represents (e.g., LCK, LPL, LEC, etc.).
- **Seed**: The seed of the team in its region.
- **Power**: A numerical value representing the team's strength. Higher values indicate stronger teams.

The script uses the `Power` column to calculate win probabilities for matches.

---

## Setup

### Prerequisites

Ensure you have the following installed:

- Python 3.7+
- Required Python libraries:
  - `pandas`

### Installation

1. Clone this repository or copy the script (`worlds_simulator.py`) to your local machine.
2. Install the required Python library:

   ```bash
   pip install pandas
   ```

3. Prepare the spreadsheet (`settings.xlsx`) using the format described above. Make sure the file is located in the same directory as the script.

---

## How It Works

1. **Match Simulation**: The `Match` class simulates a single match between two teams. The probability of winning is based on the `Power` values of both teams and the configurable `luck` factor.
2. **Tournament Stages**:
   - **Play-in Stage**: Lower-seeded teams play a series of matches to qualify for the next stage.
   - **Swiss Stage**: Teams are grouped into pools and play several rounds. Each round adjusts win/loss records.
   - **Knockout Stage**: The top 8 teams from the Swiss stage compete in a single-elimination bracket to determine the champion.
3. **Repeated Simulations**: The script runs the tournament multiple times (`LOOP` variable) to analyze trends and gather statistics.
4. **Outputs**: Results include team performance statistics such as champion count and top 8 appearances.

---

## Configuration

You can customize the following parameters in the script:

1. **Luck Factor** (`luck`): Controls randomness in match outcomes. Higher values favor stronger teams, while lower values increase randomness.
   ```python
   luck = 0.2
   ```

2. **Number of Simulations** (`LOOP`): Determines how many times the tournament will be simulated.
   ```python
   LOOP = 10
   ```

3. **Play-in Matches**: Update the `play_in_matches` list to define the initial matches in the play-in stage.
   ```python
   play_in_matches = [
       ('MDK', 'VKE', 3),  # Group A Round 1 Match 1
       ('PSG', 'PNG', 3),  # Group A Round 1 Match 2
       ('GAM', 'SHG', 3),  # Group B Round 1 Match 1
       ('100', 'R7', 3),   # Group B Round 1 Match 2
   ]
   ```

4. **Swiss Pools**: Modify the pools of teams for the Swiss stage.
   ```python
   pool1 = ['LCK1', 'LPL1', 'LEC1', 'LCS1']
   ```

---

## Running the Simulation

Run the script using Python:

```bash
python worlds_simulator.py
```

After execution, the simulation results will be displayed in the console.

---

## Outputs

### Console Output

The script prints the following information:

1. **Swiss Pools**: Displays the pools for each round of the Swiss stage.
2. **Match Results**: Reports the outcome of each match.
3. **Swiss Standings**: Displays the win/loss record for all teams after each round of the Swiss stage.
4. **Top 8 Teams**: Lists the teams that qualify for the knockout stage.
5. **Champion Count**: Shows how many times each team became the champion across multiple simulations.
6. **Top 8 Count**: Tracks how many times each team reached the top 8.

### Example Output:

```
Swiss Pools:
Pool1: ['HLE', 'BLG', 'G2', 'FLY']
Pool2: ['GEN', 'TES', 'FNC', 'TL']
...

Swiss Standings After Round 1:
    Team  swiss_wins  swiss_losses
0   HLE           1             0
1   BLG           0             1
...

Top 8 Teams:
['HLE', 'BLG', 'TES', 'GEN', 'G2', 'FLY', 'FNC', 'TL']

Champion count:
HLE: 6 times
BLG: 3 times
...

Top 8 count:
HLE: 10 times
BLG: 10 times
...
```

---

## Customization

- **Match Formats**: Adjust the `bo` (best-of) parameter in the match definitions to change the format (e.g., BO1, BO3, BO5).
- **Swiss Rounds**: Modify the Swiss stage to include more or fewer rounds by adjusting the number of iterations in the loop.
- **Additional Stages**: Add new stages or modify existing ones to fit your tournament structure.

---

## Limitations

- All teams must be included in the `settings.xlsx` file with valid `Team`, `Region`, `Seed`, and `Power` values.
- The Swiss stage supports 16 teams divided into 4 pools. Adjustments may be needed for different team counts.

---

## License

This project is open-source and free to use. Modify it as needed for your tournaments!
