import random
import openpyxl
import pandas as pd


play_list_on_first_half = []
play_list_on_second_half = []
play_list_on_first_half_for_save = []
play_list_on_second_half_for_save = []

# 이거 입력 해야 함(생성될 파일 이름)
season = "2nd_season"

for i in range(10):

    # 팀 초기화
    js_list = ["Arsenal", "Leicester", "Manchester City", "Juventus", "Dortmund", "WestHam", "Everton",
               "Crystal Palace", "Legend Manchester United", "Legend Liverpool"]
    hs_list = ["Leeds United", "Burnley", "AC Milan", "WolverHampton", "Manchester United", "Tottemham Hotspur",
               "Liverpool", "Chelsea", "Legend Arsenal", "Legend Chelsea"]
    temp_play_list = []

    # 1라운드 만들기
    while len(js_list) > 0:

        js_team = random.choice(js_list)
        hs_team = random.choice(hs_list)

        if [js_team, "", "", hs_team] in play_list_on_first_half:
            js_list = ["Arsenal", "Leicester", "Manchester City", "Juventus", "Dortmund", "WestHam", "Everton",
                       "Crystal Palace", "Legend Manchester United", "Legend Liverpool"]
            hs_list = ["Leeds United", "Burnley", "AC Milan", "WolverHampton", "Manchester United", "Tottemham Hotspur",
                       "Liverpool", "Chelsea", "Legend Arsenal", "Legend Chelsea"]
            temp_play_list = []
            continue

        js_list.remove(js_team)
        hs_list.remove(hs_team)

        temp_play_list.append([js_team, "", "", hs_team])

    play_list_on_first_half.extend(temp_play_list)
    play_list_on_first_half_for_save.extend([temp_play_list])
    # play_list_on_first_half.append(f'{i}END')
    print(play_list_on_first_half)


for k in range(10):

    # 팀 초기화
    js_list = ["Arsenal", "Leicester", "Manchester City", "Juventus", "Dortmund", "WestHam", "Everton",
               "Crystal Palace", "Legend Manchester United", "Legend Liverpool"]
    hs_list = ["Leeds United", "Burnley", "AC Milan", "WolverHampton", "Manchester United", "Tottemham Hotspur",
               "Liverpool", "Chelsea", "Legend Arsenal", "Legend Chelsea"]
    temp_play_list = []

    # 1라운드 만들기
    while len(js_list) > 0:

        js_team = random.choice(js_list)
        hs_team = random.choice(hs_list)

        if [hs_team, "", "", js_team] in play_list_on_second_half:
            js_list = ["Arsenal", "Leicester", "Manchester City", "Juventus", "Dortmund", "WestHam", "Everton",
                       "Crystal Palace", "Legend Manchester United", "Legend Liverpool"]
            hs_list = ["Leeds United", "Burnley", "AC Milan", "WolverHampton", "Manchester United", "Tottemham Hotspur",
                       "Liverpool", "Chelsea", "Legend Arsenal", "Legend Chelsea"]
            temp_play_list = []
            continue

        js_list.remove(js_team)
        hs_list.remove(hs_team)

        temp_play_list.append([hs_team, "", "", js_team])

    play_list_on_second_half.extend(temp_play_list)
    play_list_on_second_half_for_save.extend([temp_play_list])
    # play_list_on_second_half.append(f'{k}END')
    print(play_list_on_second_half)

all_matches = play_list_on_first_half + play_list_on_second_half
all_matches_for_save = play_list_on_first_half_for_save + play_list_on_second_half_for_save

# 중복된 값이 있는 경우 print 출력
for match in all_matches:

    match_count = all_matches.count(match)
    if match_count > 1:
        print(match)

round_count = 1

for this_round in all_matches_for_save:
    print(this_round)

    list_for_index = []
    for j in range(len(all_matches_for_save[0])):
        list_for_index.append(f"{round_count} 라운드 {j+1} 번쨰 매치")

    df = pd.DataFrame(this_round, index=list_for_index, columns=["home", "", "", "away"])
    # df.to_excel('C:\work\develop\python_practice\league_table.xlsx', sheet_name='new_name')

    path = f'C:\\work\\develop\\python_practice\\{season}.xlsx'

    with pd.ExcelWriter(path) as writer:
        if this_round == all_matches_for_save[0]:
            df.to_excel(writer, sheet_name=f'Round {round_count}')
        else:
            writer.book = openpyxl.load_workbook(path)
            df.to_excel(writer, sheet_name=f'Round {round_count}')

    round_count += 1

