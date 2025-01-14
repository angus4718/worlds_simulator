# Tournament Simulation README

This repository contains a Python script for simulating a custom tournament structure. The program uses team data and a Swiss-system format to simulate matches, determine standings, and identify the tournament champion. Below is a detailed explanation of the project, its setup, and usage.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Setup](#setup)
4. [How It Works](#how-it-works)
5. [Configuration](#configuration)
6. [Running the Simulation](#running-the-simulation)
7. [Outputs](#outputs)
8. [Customization](#customization)

---

## Overview

The script simulates a competitive tournament with the following phases:

1. **Play-in Stage**: Matches between teams to determine which advance to the next stage.
2. **Swiss Stage**: Teams are divided into pools and play multiple rounds to determine the top-performing teams.
3. **Knockout Stage**: Top 8 teams from the Swiss stage compete in a single-elimination bracket to determine the tournament champion.

The script uses randomization and team power ratings to simulate match outcomes while allowing for luck as a factor.

---

## Features

- **Team Power Ratings**: Determines the probability of winning a match.
- **Luck Factor**: Adds an element of randomness to the simulations.
- **Swiss-System Tournament**: Implements the Swiss format to rank teams over multiple rounds.
- **Knockout Stage**: Simulates quarterfinals, semifinals, and finals.
- **Repeatable Simulations**: Perform multiple runs to analyze outcomes and trends.
- **Customizable Parameters**: Adjust team data, luck factor, and simulation loops.

---

## Setup

### Prerequisites

Ensure you have the following installed:

- Python 3.7+
- `pandas`
- `openpyxl`

### Installation

1. Clone this repository or copy the script to your local machine.
2. Install the required Python libraries:

   ```bash
   pip install pandas openpyxl
   ```

3. Prepare an Excel file (`settings.xlsx`) with the following structure:

   **Sheet: `Teams`**
   | Team   | Power |
   |--------|-------|
   | LCK1   | 95    |
   | LPL1   | 92    |
   | ...    | ...   |

   - `Team`: The team name (must match the team names used in the script).
   - `Power`: A numerical value representing the team's strength.

---

## How It Works

1. **Match Simulation**: The `Match` class simulates a single match between two teams using their power ratings and the luck factor to determine the winner.
2. **Stages**:
   - **Play-in Stage**: Teams play a series of matches to qualify for the Swiss stage.
   - **Swiss Stage**: Teams are grouped into pools and play several rounds, earning wins and losses.
   - **Knockout Stage**: The top 8 teams from the Swiss stage compete in a bracket to determine the champion.
3. **Repeated Simulations**: The script runs the tournament multiple times (`LOOP` variable) to gather statistics on team performance.
4. **Outputs**: The results include the number of times each team became the champion and how often they reached the top 8.

---

## Configuration

You can customize the following parameters in the script:

1. **Luck Factor** (`luck`): Controls the randomness in match outcomes. Values closer to `0` make match results more random, while higher values favor stronger teams.
   ```python
   luck = 0.2
   ```

2. **Number of Simulations** (`LOOP`): Determines how many times the tournament is simulated.
   ```python
   LOOP = 10
   ```

3. **Team Data**: Modify the `settings.xlsx` file to include your desired teams and their power ratings.

4. **Play-in Matches**: Update the `play_in_matches` list to define the initial matches in the play-in stage.
   ```python
   play_in_matches = [
       ('MDK', 'VKE', 3),  # Group A Round 1 Match 1
       ('PSG', 'PNG', 3),  # Group A Round 1 Match 2
       ...
   ]
   ```

5. **Swiss Pools**: Update the pools in the Swiss stage to include the correct teams.
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
Pool1: ['LCK1', 'LPL1', 'LEC1', 'LCS1']
Pool2: ['LCK2', 'LPL2', 'LEC2', 'LCS2']
...

Swiss Standings After Round 1:
    Team  swiss_wins  swiss_losses
0   LCK1           1             0
1   LPL1           0             1
...

Top 8 Teams:
['LCK1', 'LPL1', 'LEC1', 'LCS1', 'LCK2', 'LPL2', 'LEC2', 'LCS2']

Champion count:
LCK1: 6 times
LPL1: 3 times
...

Top 8 count:
LCK1: 10 times
LPL1: 10 times
...
```

---

## Customization

- **Match Formats**: Adjust the `bo` (best-of) parameter in the match definitions to change the format (e.g., BO1, BO3, BO5).
- **Swiss Rounds**: Modify the Swiss stage to include more or fewer rounds by changing the number of iterations in the loop.
- **Additional Stages**: Add new stages or modify existing ones to fit your tournament structure.

---

## Limitations

- All teams must be included in the `settings.xlsx` file with valid power ratings.
- The Swiss stage requires exactly 16 teams divided into 4 pools.

---

## License

This project is open-source and free to use. Modify it as needed for your tournaments!
