import pandas as pd
import openpyxl
import random

df_teams = pd.read_excel('settings.xlsx', sheet_name='Teams')
df_teams['Team'] = df_teams['Team'].astype(str)
df_teams.insert(0, 'id', df_teams.iloc[:, 1].astype(str) + df_teams.iloc[:, 2].astype(str))
luck = 0.2

class Match:
    def __init__(self, team_1, team_2, luck, bo):
        self.bo = bo
        self.team_1 = team_1
        self.team_2 = team_2
        self.power_1 = df_teams[df_teams['Team'] == team_1]['Power'].iloc[0]
        self.power_2 = df_teams[df_teams['Team'] == team_2]['Power'].iloc[0]
        self.luck = luck

    def win_prob(self):
        p1 = self.power_1 ** (1 / self.luck) / (self.power_1 ** (1 / self.luck) + self.power_2 ** (1 / self.luck))
        return p1

    def single_match_winner(self):
        random_number = random.uniform(0, 1)
        if random_number < self.win_prob():
            return self.team_1, self.team_2
        return self.team_2, self.team_1

    def result(self):
        score_1 = 0
        score_2 = 0
        max_score = self.bo // 2 + 1
        while max(score_1, score_2) < max_score:
            winner, _ = self.single_match_winner()
            if winner == self.team_1:
                score_1 += 1
            else:
                score_2 += 1

        if score_1 == max_score:
            print(f'{self.team_1} {score_1}:{score_2} {self.team_2}. {self.team_1} advances!')
            return self.team_1, self.team_2
        else:
            print(f'{self.team_1} {score_1}:{score_2} {self.team_2}. {self.team_2} advances!')
            return self.team_2, self.team_1

champion_count = {team: 0 for team in df_teams['Team']}
top_8_count = {team: 0 for team in df_teams['Team']}
for _ in range(1000):
    # Play-in

    # Group A Round 1 Match 1 - LEC3 vs VCS2
    matcha11 = Match('MDK', 'VKE', luck, 3)
    a11_winner, a11_loser = matcha11.result()

    # Group A Round 1 Match 2 - PCS1 vs CBLOL1
    matcha12 = Match('PSG', 'PNG', luck, 3)
    a12_winner, a12_loser = matcha12.result()

    # Group B Round 1 Match 1 - LEC3 vs VCS2
    matchb11 = Match('GAM', 'SHG', luck, 3)
    b11_winner, b11_loser = matchb11.result()

    # Group B Round 1 Match 2 - PCS1 vs CBLOL1
    matchb12 = Match('100', 'R7', luck, 3)
    b12_winner, b12_loser = matchb12.result()

    # Group A Round 2 Match 1 - a11_winner vs a12_winner
    matcha21 = Match(a11_winner, a12_winner, luck, 3)
    a21_winner, a21_loser = matcha21.result()

    # Group B Round 2 Match 1 - b11_winner vs b12_winner
    matchb21 = Match(b11_winner, b12_winner, luck, 3)
    b21_winner, b21_loser = matchb21.result()

    # Group A Round 1 Match 3 - a11_loser vs a12_loser
    matcha13 = Match(a11_loser, a12_loser, luck, 3)
    a13_winner, a13_loser = matcha13.result()

    # Group B Round 1 Match 3 - b11_loser vs b12_loser
    matchb13 = Match(b11_loser, b12_loser, luck, 3)
    b13_winner, b13_loser = matchb13.result()

    # Group A Round 2 Match 2 - a13_winner vs b21_loser
    matcha22 = Match(a13_winner, b21_loser, luck, 3)
    a22_winner, a22_loser = matcha22.result()

    # Group B Round 2 Match 2 - b13_winner vs a21_loser
    matchb22 = Match(b13_winner, a21_loser, luck, 3)
    b22_winner, b22_loser = matchb22.result()

    print(a21_winner, b21_winner, a22_winner, b22_winner)

    # Swiss
    pool1 = ['LCK1', 'LPL1', 'LEC1', 'LCS1']
    pool2 = ['LCK2', 'LPL2', 'LEC2', 'LCS2']
    pool3 = ['LCK3', 'LCK4', 'LPL3', 'LPL4']
    pool4 = [df_teams[df_teams['Team'] == a21_winner]['id'].iloc[0], df_teams[df_teams['Team'] == b21_winner]['id'].iloc[0], df_teams[df_teams['Team'] == a22_winner]['id'].iloc[0], df_teams[df_teams['Team'] == b22_winner]['id'].iloc[0]]

    swiss_teams = pool1 + pool2 + pool3 + pool4

    df_swiss_stage = df_teams[df_teams['id'].isin(swiss_teams)]
    df_swiss_stage = df_swiss_stage.copy()
    df_swiss_stage.loc[:, 'swiss_wins'] = 0
    df_swiss_stage.loc[:, 'swiss_losses'] = 0

    def draw_matches(pool_a, pool_b):
        matches = []
        remaining_pool_b = pool_b[:]
        for team_a in pool_a:
            opponent = random.choice(remaining_pool_b)
            matches.append((team_a, opponent))
            remaining_pool_b.remove(opponent)
        return matches

    # Draw matches
    matches_pool1_vs_pool4 = draw_matches(pool1, pool4)
    matches_pool2_vs_pool3 = draw_matches(pool2, pool3)

    print("\nResults for Matches Pool 1 vs Pool 4:")
    for match in matches_pool1_vs_pool4:
        team_1 = df_teams[df_teams['id'] == match[0]]['Team'].iloc[0]
        team_2 = df_teams[df_teams['id'] == match[1]]['Team'].iloc[0]
        match_result = Match(team_1, team_2, luck, 1)
        winner, loser = match_result.result()
        df_swiss_stage.loc[df_swiss_stage['Team'] == winner, 'swiss_wins'] += 1
        df_swiss_stage.loc[df_swiss_stage['Team'] == loser, 'swiss_losses'] += 1

    print("\nResults for Matches Pool 2 vs Pool 3:")
    for match in matches_pool2_vs_pool3:
        team_1 = df_teams[df_teams['id'] == match[0]]['Team'].iloc[0]
        team_2 = df_teams[df_teams['id'] == match[1]]['Team'].iloc[0]
        match_result = Match(team_1, team_2, luck, 1)
        winner, loser = match_result.result()
        df_swiss_stage.loc[df_swiss_stage['Team'] == winner, 'swiss_wins'] += 1
        df_swiss_stage.loc[df_swiss_stage['Team'] == loser, 'swiss_losses'] += 1

    # Swiss Round 2
    pool10 = df_swiss_stage[df_swiss_stage['swiss_wins'] == 1]['Team'].tolist()
    pool01 = df_swiss_stage[df_swiss_stage['swiss_wins'] == 0]['Team'].tolist()

    def draw_matches_within_pool(pool):
        matches = []
        remaining_teams = pool[:]
        random.shuffle(remaining_teams)

        while len(remaining_teams) > 1:
            team_a = remaining_teams.pop()
            team_b = remaining_teams.pop()
            matches.append((team_a, team_b))

        return matches

    matches_10 = draw_matches_within_pool(pool10)
    matches_01 = draw_matches_within_pool(pool01)

    print("\nResults for Group 1-0:")
    for match in matches_10:
        team_1 = match[0]
        team_2 = match[1]
        match_result = Match(team_1, team_2, luck, 1)
        winner, loser = match_result.result()
        df_swiss_stage.loc[df_swiss_stage['Team'] == winner, 'swiss_wins'] += 1
        df_swiss_stage.loc[df_swiss_stage['Team'] == loser, 'swiss_losses'] += 1

    print("\nResults for Group 0-1:")
    for match in matches_01:
        team_1 = match[0]
        team_2 = match[1]
        match_result = Match(team_1, team_2, luck, 1)
        winner, loser = match_result.result()
        df_swiss_stage.loc[df_swiss_stage['Team'] == winner, 'swiss_wins'] += 1
        df_swiss_stage.loc[df_swiss_stage['Team'] == loser, 'swiss_losses'] += 1

    # Swiss Round 3
    pool20 = df_swiss_stage[df_swiss_stage['swiss_wins'] == 2]['Team'].tolist()
    pool11 = df_swiss_stage[df_swiss_stage['swiss_wins'] == 1]['Team'].tolist()
    pool02 = df_swiss_stage[df_swiss_stage['swiss_wins'] == 0]['Team'].tolist()

    matches_20 = draw_matches_within_pool(pool20)
    matches_11 = draw_matches_within_pool(pool11)
    matches_02 = draw_matches_within_pool(pool02)

    print("\nResults for Group 2-0:")
    pool_qf1 = []
    for match in matches_20:
        team_1 = match[0]
        team_2 = match[1]
        match_result = Match(team_1, team_2, luck, 3)
        winner, loser = match_result.result()
        df_swiss_stage.loc[df_swiss_stage['Team'] == winner, 'swiss_wins'] += 1
        df_swiss_stage.loc[df_swiss_stage['Team'] == loser, 'swiss_losses'] += 1
        print(f'{winner} advances to the Quarterfinals!')
        pool_qf1.append(winner)


    print("\nResults for Group 1-1:")
    for match in matches_11:
        team_1 = match[0]
        team_2 = match[1]
        match_result = Match(team_1, team_2, luck, 1)
        winner, loser = match_result.result()
        df_swiss_stage.loc[df_swiss_stage['Team'] == winner, 'swiss_wins'] += 1
        df_swiss_stage.loc[df_swiss_stage['Team'] == loser, 'swiss_losses'] += 1

    print("\nResults for Group 0-2:")
    for match in matches_02:
        team_1 = match[0]
        team_2 = match[1]
        match_result = Match(team_1, team_2, luck, 3)
        winner, loser = match_result.result()
        df_swiss_stage.loc[df_swiss_stage['Team'] == winner, 'swiss_wins'] += 1
        df_swiss_stage.loc[df_swiss_stage['Team'] == loser, 'swiss_losses'] += 1
        print(f'{loser} is eliminated.')

    # Swiss Round 4
    pool21 = df_swiss_stage[(df_swiss_stage['swiss_wins'] == 2) & (df_swiss_stage['swiss_losses'] == 1)]['Team'].tolist()
    pool12 = df_swiss_stage[(df_swiss_stage['swiss_wins'] == 1) & (df_swiss_stage['swiss_losses'] == 2)]['Team'].tolist()

    matches_21 = draw_matches_within_pool(pool21)
    matches_12 = draw_matches_within_pool(pool12)

    print("\nResults for Group 2-1:")
    pool_qf2 = []
    for match in matches_21:
        team_1 = match[0]
        team_2 = match[1]
        match_result = Match(team_1, team_2, luck, 3)
        winner, loser = match_result.result()
        df_swiss_stage.loc[df_swiss_stage['Team'] == winner, 'swiss_wins'] += 1
        df_swiss_stage.loc[df_swiss_stage['Team'] == loser, 'swiss_losses'] += 1
        print(f'{winner} advances to the Quarterfinals!')
        pool_qf2.append(winner)

    print("\nResults for Group 1-2:")
    for match in matches_12:
        team_1 = match[0]
        team_2 = match[1]
        match_result = Match(team_1, team_2, luck, 3)
        winner, loser = match_result.result()
        df_swiss_stage.loc[df_swiss_stage['Team'] == winner, 'swiss_wins'] += 1
        df_swiss_stage.loc[df_swiss_stage['Team'] == loser, 'swiss_losses'] += 1
        print(f'{loser} is eliminated.')

    # Swiss Round 5
    pool22 = df_swiss_stage[(df_swiss_stage['swiss_wins'] == 2) & (df_swiss_stage['swiss_losses'] == 2)]['Team'].tolist()

    matches_22 = draw_matches_within_pool(pool22)

    print("\nResults for Group 2-2:")
    pool_qf3 = []
    for match in matches_22:
        team_1 = match[0]
        team_2 = match[1]
        match_result = Match(team_1, team_2, luck, 3)
        winner, loser = match_result.result()
        df_swiss_stage.loc[df_swiss_stage['Team'] == winner, 'swiss_wins'] += 1
        df_swiss_stage.loc[df_swiss_stage['Team'] == loser, 'swiss_losses'] += 1
        print(f'{winner} advances to the Quarterfinals!')
        print(f'{loser} is eliminated.')
        pool_qf3.append(winner)

    teams_qf = pool_qf1 + pool_qf2 + pool_qf3
    for team in teams_qf:
        top_8_count[team] += 1
    pool_qf1_id = [df_teams[df_teams['Team'] == x]['id'].iloc[0] for x in pool_qf1]
    pool_qf2_id = [df_teams[df_teams['Team'] == x]['id'].iloc[0] for x in pool_qf2]
    pool_qf3_id = [df_teams[df_teams['Team'] == x]['id'].iloc[0] for x in pool_qf3]

    def draw_matches_qf(pool_qf1_id, pool_qf2_id, pool_qf3_id):
        matches = []
        remaining_pool_qf3_id = pool_qf3_id[:]
        while len(matches) < 2:
            for team_1 in pool_qf1_id:
                team_2 = random.choice(remaining_pool_qf3_id)
                remaining_pool_qf3_id.remove(team_2)
                matches.append((team_1, team_2))

        remaining_teams = pool_qf2_id + remaining_pool_qf3_id

        random.shuffle(remaining_teams)
        while len(matches) < 4:
            team_1 = remaining_teams.pop()
            team_2 = remaining_teams.pop()
            matches.append((team_1, team_2))

        return matches

    matches_qf = draw_matches_qf(pool_qf1_id, pool_qf2_id, pool_qf3_id)
    sf_teams = []
    print("\nResults for Quarterfinals:")
    for match in matches_qf:
        team_1 = df_teams[df_teams['id'] == match[0]]['Team'].iloc[0]
        team_2 = df_teams[df_teams['id'] == match[1]]['Team'].iloc[0]
        match_result = Match(team_1, team_2, luck, 5)
        winner, loser = match_result.result()
        sf_teams.append(winner)

    print("\nResults for Semifinals:")
    matches_sf = [(sf_teams[0], sf_teams[3]), (sf_teams[1], sf_teams[2])]
    f_teams = []
    for match in matches_sf:
        team_1 = match[0]
        team_2 = match[1]
        match_result = Match(team_1, team_2, luck, 5)
        winner, loser = match_result.result()
        f_teams.append(winner)

    print("\nResults for Finals:")
    finals = Match(f_teams[0], f_teams[1], luck, 5)
    winner, _ = finals.result()
    champion_count[winner] += 1

print("\nChampion count:")
for team, count in champion_count.items():
    print(f"{team}: {count} times")

print("\nTop 8 count:")
for team, count in top_8_count.items():
    print(f"{team}: {count} times")