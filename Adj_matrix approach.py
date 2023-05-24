from pandas import DataFrame
from datetime import datetime
import csv
################ - Classes - #####################
class Team:
    def __init__(self, name: str, matches_played: int = 0, wins: int = 0, draws: int = 0, losses: int = 0, points: int = 0, goals_scored: int = 0, goals_conceded: int = 0) -> None:
        self.name = name
        self.matches_played = matches_played
        self.wins = wins
        self.draws = draws
        self.losses = losses
        self.points = points
        self.goals_scored = goals_scored
        self.goals_conceded = goals_conceded
        self.goals_diff = self.goals_scored - self.goals_conceded

    def __setattr__(self, attr: str, value) -> None:
        if attr == 'name' and (isinstance(value, str)):
            super().__setattr__(attr, value)
        elif isinstance(value, int):
            if attr == 'matches_played':
                super().__setattr__(attr, value)
            elif attr == 'wins':
                super().__setattr__(attr, value)
            elif attr == 'draws':
                super().__setattr__(attr, value)
            elif attr == 'losses':
                super().__setattr__(attr, value)
            elif attr == 'points':
                super().__setattr__(attr, value)
            elif attr == 'goals_scored':
                super().__setattr__(attr, value)
            elif attr == 'goals_conceded':
                super().__setattr__(attr, value)
            elif attr == 'goals_diff':
                super().__setattr__(attr, value)
        else:
            raise ValueError(
                "All attributes must be of type int except for attribute name must be a string")

    def display(self, tabular: bool = False) -> None:
        if tabular:
            data = {
                'Name': [self.name],
                'PL': [self.matches_played],
                'W': [self.wins],
                'D': [self.draws],
                'L': [self.losses],
                'Pts': [self.points],
                'GF': [self.goals_scored],
                'GA': [self.goals_conceded],
                'GD': [self.goals_diff]
            }
            df = DataFrame(data)
            print(df.to_string(index=False))
        else:
            print(f"{self.name}\t{self.matches_played}\t{self.wins}\t{self.draws}\t{self.losses}\t{self.points}\t{self.goals_scored}\t{self.goals_conceded}\t{self.goals_diff}")

    def add_win(self, goals_scored: int, goals_conceded: int) -> None:
        if goals_scored > goals_conceded:
            self.matches_played += 1
            self.wins += 1
            self.points += 3
            self.goals_scored += goals_scored
            self.goals_conceded += goals_conceded
            self.goals_diff += (goals_scored - goals_conceded)
        else:
            raise ValueError(
                "To add a win, goals scored must be > goals conceded")

    def add_draw(self, goals: int) -> None:
        self.matches_played += 1
        self.draws += 1
        self.points += 1
        self.goals_scored += goals
        self.goals_conceded += goals

    def add_loss(self, goals_scored: int, goals_conceded: int) -> None:
        if goals_scored < goals_conceded:
            self.matches_played += 1
            self.losses += 1
            self.goals_scored += goals_scored
            self.goals_conceded += goals_conceded
            self.goals_diff += (goals_scored - goals_conceded)
        else:
            raise ValueError(
                "To add a loss, goals scored must be < goals conceded")


class Match:
    def __init__(self, week: int, date: datetime, home_team: Team, away_team: Team, home_goals: int, away_goals: int) -> None:
        self.week = week
        self.date = date
        self.home_team = home_team
        self.away_team = away_team
        self.home_goals = home_goals
        self.away_goals = away_goals
        self.played = 0

    def play(self) -> None:
        if self.played == 0:
            if self.home_goals > self.away_goals:
                self.home_team.add_win(self.home_goals, self.away_goals)
                self.away_team.add_loss(self.away_goals, self.home_goals)
            elif self.away_goals > self.home_goals:
                self.away_team.add_win(self.away_goals, self.home_goals)
                self.home_team.add_loss(self.home_goals, self.away_goals)  
            else:
                self.home_team.add_draw(self.home_goals)
                self.away_team.add_draw(self.away_goals)
            self.played = 1

    def display_match(self):
        print(f"{self.week} - {self.date} - {self.home_team.name} - {self.away_team.name} - {self.home_goals} - {self.away_goals}", sep=" ")


class EPLGraph:
    def __init__(self) -> None:
        self.adj_matrix = [[0 for _ in range(20)] for _ in range(20)]
        self.coordinates = []

    def add_edge(self,home_team: int, away_team: int, match: Match) -> None:
        self.adj_matrix[home_team][away_team] = match
    
    def construct_graph(self, matches: list[Match], teams: dict[Team:int]) -> None:
        for match in matches:
            self.add_edge(teams[match.home_team], teams[match.away_team], match)
            self.coordinates.append((teams[match.home_team], teams[match.away_team]))

    def display_graph(self) -> None:
        count = 0
        for row in self.adj_matrix:
            for match in row:
                if isinstance(match,Match):
                    count += 1
        print(count)

    def traverse_graph_by_week(self, week=30):
        
        '''print("Old traversing")                                     #O(T^2)   where T = teams
        for row in self.adj_matrix:
            for match in row:
                if isinstance(match,Match) and match.week <= week:
                    match.play()'''
        
        '''print("New Traversing")                                     #O(T)     where T = teams
        for home_team,away_team in self.coordinates:
            match = self.adj_matrix[home_team][away_team]
            if match.week <= week:
                match.play()'''

        print("Very new traversing")                                  #O(T^2)    where T = teams
        queue = [0]
        visited = set()
        while queue:
            home_team = queue.pop(0)
            visited.add(home_team)
            for away_team in range(20):
                match = self.adj_matrix[home_team][away_team]
                if isinstance(match, Match):
                    if away_team not in visited and away_team not in queue:
                        queue.append(away_team)
                    if match.week <= week:
                        match.play()
      
    def traverse_graph_by_date(self, date='9-4-2023'):
        date = datetime.strptime(date,'%d-%m-%Y').date()
        queue = [0]
        visited = set()
        while queue:
            home_team = queue.pop(0)
            visited.add(home_team)
            for away_team in range(20):
                match = self.adj_matrix[home_team][away_team]
                if isinstance(match, Match):
                    if away_team not in visited and away_team not in queue:
                        queue.append(away_team)
                    if match.date <= date:
                        match.play()

                
    def construct_table(self,teams):
        sorted_teams = dict(sorted(teams.items(), key=lambda x: (x[1].points, x[1].goals_diff, x[1].goals_scored), reverse=True))
        data = {
        'Name': [team.name for team in sorted_teams.values()],
        'PL': [team.matches_played for team in sorted_teams.values()],
        'W': [team.wins for team in sorted_teams.values()],
        'D': [team.draws for team in sorted_teams.values()],
        'L': [team.losses for team in sorted_teams.values()],
        'Pts': [team.points for team in sorted_teams.values()],
        'GF': [team.goals_scored for team in sorted_teams.values()],
        'GA': [team.goals_conceded for team in sorted_teams.values()],
        'GD': [team.goals_diff for team in sorted_teams.values()]
            }
        df = DataFrame(data)
        print(df.to_string(index=False))


    def get_match_result(self,home_team: str, away_team: str, teams_int: dict[str:int]) -> None:
        if self.adj_matrix[teams_int[home_team]][teams_int[away_team]]:
            match = self.adj_matrix[teams_int[home_team]][teams_int[away_team]]
            print(f"The match ended with the result: {home_team} {match.home_goals} - {match.away_goals} {away_team} ")
        else:
            print('match has not been played yet')


############## - functions - ###################

def read_csv_file(file_path: str) -> DataFrame:

    # Create an empty list to hold the data
    data = []

    # Read the CSV file and append the data to the list
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader) # skip header
        for row in reader:
            data.append(row)

    # Convert the date strings to date objects and remove the results column
    for row in data:
        row[1] = datetime.strptime(row[1], '%d/%m/%Y').date()
        del row[6]

    # Convert the list of lists to a pandas DataFrame
    df = DataFrame(data, columns=['week', 'date', 'home_team', 'away_team', 'home_goals', 'away_goals'])

    return df


def create_matches(df: DataFrame, teams: dict[str:Team]) -> list[Match]:
    #df.sort_values(['week','date'],ascending=[True,True],inplace=True)
    matches = []
    for i in range(len(df)):
        week = int(df.loc[i,'week'])
        date = df.loc[i,'date']
        home_team_name = df.loc[i,'home_team']
        away_team_name = df.loc[i,'away_team']
        home_goals = int(df.loc[i,'home_goals'])
        away_goals = int(df.loc[i,'away_goals'])

        home_team = teams[home_team_name]
        away_team = teams[away_team_name]
        match = Match(week,date,home_team,away_team,home_goals,away_goals)
        matches.append(match)
    return matches


def create_teams_dict_for_matrix(df: DataFrame):
    teams_dict_for_matrix = {}
    teams = {}
    teams_int = {}
    teams_names = df['home_team'].unique()
    for i in range(len(teams_names)):
        team = Team(teams_names[i])
        teams_dict_for_matrix[team] = i #Assigning every team object to a number based on their first occurance in the home_team column in the csv file
        teams[teams_names[i]] = team    #Assigning every team name to an object of this team
        teams_int[teams_names[i]] = i

    return teams_dict_for_matrix, teams, teams_int


############### - Main - ####################
if __name__ == '__main__':
    df = read_csv_file('epl_results.csv')
    teams_dict_for_matrix , teams , teams_int = create_teams_dict_for_matrix(df)
    matches = create_matches(df,teams)
    my_graph = EPLGraph()
    my_graph.construct_graph(matches,teams_dict_for_matrix)
    my_graph.traverse_graph_by_week(5)
    #my_graph.traverse_graph_by_date('24-10-2022')
    #my_graph.get_match_result('Tottenham','Tottenham',teams_int)
    my_graph.construct_table(teams)