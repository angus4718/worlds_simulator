import pandas as pd
import random

# Load data
df_teams = pd.read_excel('settings.xlsx', sheet_name='Teams')
df_teams['Team'] = df_teams['Team'].astype(str)
df_teams.insert(0, 'id', df_teams.iloc[:, 1].astype(str) + df_teams.iloc[:, 2].astype(str))
luck = 0.2
LOOP = 10

# Match class
class Match:
    def __init__(self, team_1, team_2, luck, bo):
        # Normalize team names
        self.team_1 = team_1.strip().upper()
        self.team_2 = team_2.strip().upper()
        self.bo = bo
        self.luck = luck
        print(self.team_1, self.team_2)
        # Validate teams
        filtered_teams_1 = df_teams[df_teams['Team'] == self.team_1]
        filtered_teams_2 = df_teams[df_teams['Team'] == self.team_2]
        if filtered_teams_1.empty or filtered_teams_2.empty:
            raise ValueError(f"Invalid teams: {self.team_1} vs {self.team_2}. Check team names.")

        # Get power levels
        self.power_1 = filtered_teams_1['Power'].iloc[0]
        self.power_2 = filtered_teams_2['Power'].iloc[0]

    def win_prob(self):
        return self.power_1 ** (1 / self.luck) / (self.power_1 ** (1 / self.luck) + self.power_2 ** (1 / self.luck))

    def single_match_winner(self):
        return (self.team_1, self.team_2) if random.uniform(0, 1) < self.win_prob() else (self.team_2, self.team_1)

    def result(self):
        score_1, score_2 = 0, 0
        max_score = self.bo // 2 + 1
        while max(score_1, score_2) < max_score:
            winner, _ = self.single_match_winner()
            if winner == self.team_1:
                score_1 += 1
            else:
                score_2 += 1
        winner = self.team_1 if score_1 == max_score else self.team_2
        loser = self.team_2 if winner == self.team_1 else self.team_1
        print(f'{self.team_1} {score_1}:{score_2} {self.team_2}. {winner} advances!')
        return winner, loser


# Helper functions
def run_matches(matches):
    """Runs a list of matches and returns winners and losers."""
    results = []
    for team_1, team_2, bo in matches:
        match = Match(team_1, team_2, luck, bo)
        results.append(match.result())
    return results


def draw_matches(pool_a, pool_b):
    """Draws matches between two pools."""
    matches = []
    remaining_pool_b = pool_b[:]
    for team_a in pool_a:
        opponent = random.choice(remaining_pool_b)
        matches.append((team_a, opponent))
        remaining_pool_b.remove(opponent)
    return matches


def draw_matches_within_pool(pool):
    """Draws matches within a single pool."""
    random.shuffle(pool)
    return [(pool[i], pool[i + 1]) for i in range(0, len(pool), 2)]


def update_swiss_results(matches, df_swiss_stage):
    """Updates Swiss stage results for winners and losers."""
    for match in matches:
        team_1, team_2 = match
        match_result = Match(team_1, team_2, luck, 1)
        winner, loser = match_result.result()
        df_swiss_stage.loc[df_swiss_stage['Team'] == winner, 'swiss_wins'] += 1
        df_swiss_stage.loc[df_swiss_stage['Team'] == loser, 'swiss_losses'] += 1


# Initialize counters
champion_count = {team: 0 for team in df_teams['Team']}
top_8_count = {team: 0 for team in df_teams['Team']}

# Simulation loop
for _ in range(LOOP):
    # Play-in groups setup
    # Play-in matches
    play_in_matches = [
        ('MDK', 'VKE', 3),  # Group A Round 1 Match 1
        ('PSG', 'PNG', 3),  # Group A Round 1 Match 2
        ('GAM', 'SHG', 3),  # Group B Round 1 Match 1
        ('100', 'R7', 3),  # Group B Round 1 Match 2
    ]

    # Run play-in matches
    play_in_results = run_matches(play_in_matches)

    # Assign winners and losers
    a11_winner, a11_loser = play_in_results[0]
    a12_winner, a12_loser = play_in_results[1]
    b11_winner, b11_loser = play_in_results[2]
    b12_winner, b12_loser = play_in_results[3]

    # Group A and B Round 2 Matches
    group_a_matches = [
        (a11_winner, a12_winner, 3),  # Group A Round 2 Match 1
        (a11_loser, a12_loser, 3),  # Group A Round 1 Match 3
    ]
    group_a_results = run_matches(group_a_matches)
    a21_winner, a21_loser = group_a_results[0]
    a13_winner, a13_loser = group_a_results[1]

    group_b_matches = [
        (b11_winner, b12_winner, 3),  # Group B Round 2 Match 1
        (b11_loser, b12_loser, 3),  # Group B Round 1 Match 3
    ]
    group_b_results = run_matches(group_b_matches)
    b21_winner, b21_loser = group_b_results[0]
    b13_winner, b13_loser = group_b_results[1]

    # Swiss stage setup
    # Convert IDs to Team names for all pools
    pool1 = ['LCK1', 'LPL1', 'LEC1', 'LCS1']
    pool1 = [df_teams[df_teams['id'] == team]['Team'].iloc[0] for team in pool1]

    pool2 = ['LCK2', 'LPL2', 'LEC2', 'LCS2']
    pool2 = [df_teams[df_teams['id'] == team]['Team'].iloc[0] for team in pool2]

    pool3 = ['LCK3', 'LCK4', 'LPL3', 'LPL4']
    pool3 = [df_teams[df_teams['id'] == team]['Team'].iloc[0] for team in pool3]

    pool4 = [
        df_teams[df_teams['Team'] == a21_winner]['id'].iloc[0],
        df_teams[df_teams['Team'] == b21_winner]['id'].iloc[0],
        df_teams[df_teams['Team'] == a13_winner]['id'].iloc[0],
        df_teams[df_teams['Team'] == b13_winner]['id'].iloc[0]
    ]
    pool4 = [df_teams[df_teams['id'] == team]['Team'].iloc[0] for team in pool4]

    # Debugging
    print(f"Swiss Pools:")
    print(f"Pool1: {pool1}")
    print(f"Pool2: {pool2}")
    print(f"Pool3: {pool3}")
    print(f"Pool4: {pool4}")
    swiss_teams = pool1 + pool2 + pool3 + pool4

    # Initialize Swiss stage
    df_swiss_stage = df_teams[df_teams['Team'].isin(pool1 + pool2 + pool3 + pool4)].copy()
    df_swiss_stage['swiss_wins'] = 0
    df_swiss_stage['swiss_losses'] = 0

    # Round 1: Pool1 vs Pool4 and Pool2 vs Pool3
    print("\nSwiss Round 1: Pool1 vs Pool4 and Pool2 vs Pool3")
    matches_pool1_vs_pool4 = draw_matches(pool1, pool4)
    matches_pool2_vs_pool3 = draw_matches(pool2, pool3)

    # Update results for round 1
    update_swiss_results(matches_pool1_vs_pool4, df_swiss_stage)
    update_swiss_results(matches_pool2_vs_pool3, df_swiss_stage)

    # Debug: Print standings after round 1
    print("\nSwiss Standings After Round 1:")
    print(df_swiss_stage)

    # Subsequent Swiss rounds (2-5)
    for round_num in range(2, 6):  # Rounds 2 to 5
        print(f"\nSwiss Round {round_num}")

        # Create pools based on current win counts
        max_wins = df_swiss_stage['swiss_wins'].max()
        swiss_pools = [
            df_swiss_stage[df_swiss_stage['swiss_wins'] == i]['Team'].tolist()
            for i in range(max_wins + 1)
        ]

        # Debug: Print pools
        print(f"Swiss Pools for Round {round_num}:")
        for i, pool in enumerate(swiss_pools):
            print(f"Pool {i} (Wins = {i}): {pool}")

        # Draw matches within each pool and update results
        for pool in swiss_pools:
            if len(pool) >= 2:  # Only draw matches if there are at least 2 teams
                matches = draw_matches_within_pool(pool)
                update_swiss_results(matches, df_swiss_stage)

        # Debug: Print standings after the round
        print(f"\nSwiss Standings After Round {round_num}:")
        print(df_swiss_stage)

    # Determine top 8 teams
    top_8 = df_swiss_stage[df_swiss_stage['swiss_wins'] >= 3]['Team'].tolist()
    print("\nTop 8 Teams:")
    print(top_8)

    # Ensure exactly 8 teams qualify
    if len(top_8) != 8:
        raise ValueError(
            f"Error: Swiss stage did not produce 8 teams for the top 8. Found: {len(top_8)} teams: {top_8}")

    # Update top 8 count
    for team in top_8:
        top_8_count[team] += 1
    print(top_8)
    # Quarterfinals, Semifinals, Finals
    matches_qf = draw_matches(top_8[:4], top_8[4:])
    print(matches_qf)
    sf_teams = [Match(*match, luck, 5).result()[0] for match in matches_qf]
    print(sf_teams)
    final_match = Match(sf_teams[0], sf_teams[1], luck, 5)
    champion = final_match.result()[0]
    champion_count[champion] += 1

# Display results
print("\nChampion count:")
for team, count in champion_count.items():
    print(f"{team}: {count} times")

print("\nTop 8 count:")
for team, count in top_8_count.items():
    print(f"{team}: {count} times")