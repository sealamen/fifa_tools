import random
import openpyxl
import pandas as pd


play_list = []
play_list_for_save = []

for i in range(10):

    # 팀 초기화
    js_list = ["Arsenal", "Leicester", "Manchester City", "New Castle", "Brighton", "WestHam", "Everton",
               "Crystal Palace", "Legend Manchester United", "Legend Liverpool"]
    hs_list = ["Leeds United", "Burnley", "Aston Vila", "WolverHampton", "Manchester United", "Tottemham Hotsper",
               "Liverpool", "Chelsea", "Legend Arsenal", "Legend Chelsea"]
    temp_play_list = []

    # 1라운드 만들기
    while len(js_list) > 0:

        js_team = random.choice(js_list)
        hs_team = random.choice(hs_list)

        if [hs_team, "", "", js_team] in play_list:
            js_list = ["Arsenal", "Leicester", "Manchester City", "New Castle", "Brighton", "WestHam", "Everton",
                       "Crystal Palace", "Legend Manchester United", "Legend Liverpool"]
            hs_list = ["Leeds United", "Burnley", "Aston Vila", "WolverHampton", "Manchester United",
                       "Tottemham Hotsper", "Liverpool", "Chelsea", "Legend Arsenal", "Legend Chelsea"]
            temp_play_list = []
            continue

        js_list.remove(js_team)
        hs_list.remove(hs_team)

        temp_play_list.append([hs_team, "", "", js_team])

    play_list.extend(temp_play_list)
    play_list_for_save.extend([temp_play_list])
    print(play_list)

# 중복된 값이 있는 경우 print 출력
for i in play_list:

    match_count = play_list.count(i)
    if match_count > 1:
        print(i)

round = 11
for i in play_list_for_save:
    print(i)

    list_for_index = []
    for j in range(len(play_list_for_save[0])):
        list_for_index.append(f"{round} 라운드 {j+1} 번쨰 매치")

    df = pd.DataFrame(i, index=list_for_index, columns=["home", "", "", "away"])
    # df.to_excel('C:\work\develop\python_practice\league_table.xlsx', sheet_name='new_name')

    path = "C:\work\develop\python_practice\\2nd_league_table.xlsx"

    with pd.ExcelWriter(path) as writer:
        if i == play_list_for_save[0]:
            df.to_excel(writer, sheet_name=f'Round {round}')
        else:
            writer.book = openpyxl.load_workbook(path)
            df.to_excel(writer, sheet_name=f'Round {round}')

    round += 1

