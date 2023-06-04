import random

play_list = []

for i in range(10):

    # 팀 초기화
    js_list = ["Arsenal", "Leciester", "Manchester City", "New Castle", "Brighton", "WestHam", "Everton",
               "Cristal Palace", "Legend Manceter United", "Legend Liverpool"]
    hs_list = ["Leeds United", "Burnley", "Aston Vila", "WolverHampton", "Manchester United", "Tottemham Hotsper",
               "Liverpool", "Chelsea", "Legend Arsenal", "Legend Chelsea"]
    temp_play_list = []

    # 1라운드 만들기
    while len(js_list) > 0:

        js_team = random.choice(js_list)
        hs_team = random.choice(hs_list)

        if [js_team, hs_team] in play_list:
            js_list = ["Arsenal", "Leciester", "Manchester City", "New Castle", "Brighton", "WestHam", "Everton",
                       "Cristal Palace", "Legend Manceter United", "Legend Liverpool"]
            hs_list = ["Leeds United", "Burnley", "Aston Vila", "WolverHampton", "Manchester United",
                       "Tottemham Hotsper", "Liverpool", "Chelsea", "Legend Arsenal", "Legend Chelsea"]
            temp_play_list = []
            continue

        js_list.remove(js_team)
        hs_list.remove(hs_team)

        temp_play_list.append([js_team, hs_team])

    play_list.extend(temp_play_list)
    play_list.append(f'{i}END')
    print(play_list)

print(play_list)