import random
import os
import time
import pandas as pd

def try_remove_file(path, retries=5, delay=5):
    for attempt in range(retries):
        try:
            if os.path.exists(path):
                os.remove(path)
                print(f"{path} 파일 삭제 성공")
                return True
            else:
                print(f"{path} 파일이 존재하지 않습니다.")
                return True
        except PermissionError:
            print(f"파일이 열려있어 삭제 실패했습니다. {delay}초 후 다시 시도합니다... (시도 {attempt + 1}/{retries})")
            time.sleep(delay)
    print("파일을 삭제할 수 없습니다. 파일을 닫고 다시 실행해 주세요.")
    return False


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

    list_for_index = []
    for j in range(len(all_matches_for_save[0])):
        list_for_index.append(f"{round_count} 라운드 {j+1} 번쨰 매치")

    df = pd.DataFrame(this_round, index=list_for_index, columns=["home", "", "", "away"])

    path = f'C:\\playground\\seasons\\{season}.xlsx'

    if not os.path.exists(path):
        # 파일 없으면 새로 생성
        with pd.ExcelWriter(path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=f'Round {round_count}')
    else:
        # 파일이 있지만 깨졌거나 문제 있을 수도 있으니 예외 처리 권장
        try:
            with pd.ExcelWriter(path, mode='a', engine='openpyxl', if_sheet_exists='new') as writer:
                df.to_excel(writer, sheet_name=f'Round {round_count}')
        except Exception as e:
            print(f"기존 파일 열기 실패: {e}")
            print("파일 삭제 시도 중...")
            if try_remove_file(path):
                with pd.ExcelWriter(path, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name=f'Round {round_count}')
            else:
                print("프로그램을 종료합니다.")
                break

    round_count += 1

