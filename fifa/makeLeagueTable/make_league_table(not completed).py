import copy
import random
import openpyxl
import pandas as pd

js_team_list: list = ["Arsenal", "Leicester", "Manchester City", "New Castle", "Brighton", "WestHam",
                      "Everton", "Crystal Palace", "Legend Manchester United", "Legend Liverpool"]
hs_team_list: list = ["Leeds United", "Burnley", "Aston Vila", "WolverHampton", "Manchester United",
                      "Tottemham Hotsper", "Liverpool", "Chelsea", "Legend Arsenal", "Legend Chelsea"]


class LeagueMaker:

    def __init__(self):
        self.team_count: int = 20
        self.season: str = "4rd_season"

    def make_league_schedule(self, first_team_list, second_team_list) -> (list, list):

        every_matches: list = []
        every_matches_for_record: list = []

        for i in range(self.team_count // 2):

            # 팀 초기화
            first_teams: list = copy.deepcopy(first_team_list)
            second_teams: list = copy.deepcopy(second_team_list)
            matches: list = []

            # 1라운드 만들기
            while len(first_teams) > 0:
                first_team: str = random.choice(first_teams)
                second_team: str = random.choice(second_teams)

                if [first_team, "", "", second_team] in every_matches:
                    first_teams = copy.deepcopy(first_team_list)
                    second_teams = copy.deepcopy(second_team_list)
                    matches = []
                    continue

                first_teams.remove(first_team)
                second_teams.remove(second_team)

                matches.append([first_team, "", "", second_team])

            every_matches.extend(matches)
            every_matches_for_record.extend([matches])

        self.check_duplicated_data(every_matches)
        return every_matches_for_record

    def check_duplicated_data(self, games):
        # 중복된 값이 있는 경우 print 출력
        for game in games:
            game_count = games.count(game)
            if game_count > 1:
                print(f'code error(중복된 경기가 있음) : {game}')

    def export_data_to_excel(self, matches):
        round_count = 1

        for this_round in matches:
            print(this_round)

            list_for_index = []
            for j in range(len(matches[0])):
                list_for_index.append(f"{round_count} 라운드 {j + 1} 번쨰 매치")

            df = pd.DataFrame(this_round, index=list_for_index, columns=["home", "", "", "away"])

            path = f'C:\\work\\develop\\python_practice\\{self.season}.xlsx'

            with pd.ExcelWriter(path) as writer:
                if this_round == matches[0]:
                    df.to_excel(writer, sheet_name=f'Round {round_count}')
                else:
                    writer.book = openpyxl.load_workbook(path)
                    df.to_excel(writer, sheet_name=f'Round {round_count}')

            round_count += 1


if __name__ == '__main__':
    league_maker = LeagueMaker()
    first_half_schedules = league_maker.make_league_schedule(js_team_list, hs_team_list)
    second_half_schedules = league_maker.make_league_schedule(hs_team_list, js_team_list)

    total_schedule: list = first_half_schedules + second_half_schedules
    league_maker.export_data_to_excel(total_schedule)
