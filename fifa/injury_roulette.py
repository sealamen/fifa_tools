from random import randrange
import random

# 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

one_injury_list: list = ["Liverpool", "Tottenham", "Legend Arsenal"]
two_injury_list: list = ["Juventus", "Manchester Cith", "Westham United", "Crystal Palace", "Leichester City", "Legend Chelsea"]
three_injury_list: list = ["Wolverhampton", "Leeds United", "Dortmund", "Legend Liverpool"]

injury_duration_list = [3, 3, 5, 5, 5, 7, 7, 10, 10, 20]

for team_name in one_injury_list:

    # 1. 선수 고르기 (1 ~ 11 랜덤 번호)
    player_number = randrange(11)

    # 2. 부상 일수 출력
    injury_duration = random.choice(injury_duration_list)

    print(f'{team_name} 부상 룰렛 결과 : {player_number + 1}번 선수 {injury_duration}경기 결장')

for team_name in two_injury_list:
    # 1. 선수 고르기 (1 ~ 11 랜덤 번호)
    player_number_1 = randrange(11)
    player_number_2 = randrange(11)

    while player_number_1 == player_number_2:
        player_number_2 = randrange(11)

        if player_number_1 != player_number_2:
            break

    # 2. 부상 일수 출력
    injury_duration_1 = random.choice(injury_duration_list)
    injury_duration_2 = random.choice(injury_duration_list)

    print(f'{team_name} 부상 룰렛 결과 : {player_number_1 + 1}번 선수 {injury_duration_1}경기 결장')
    print(f'{team_name} 부상 룰렛 결과 : {player_number_2 + 1}번 선수 {injury_duration_2}경기 결장')

for team_name in three_injury_list:
    # 1. 선수 고르기 (1 ~ 11 랜덤 번호)
    player_number_1 = randrange(11)
    player_number_2 = randrange(11)
    player_number_3 = randrange(11)

    while player_number_1 == player_number_2 or player_number_1 == player_number_3 or player_number_2 == player_number_3:
        player_number_1 = randrange(11)
        player_number_2 = randrange(11)
        player_number_3 = randrange(11)

        if player_number_1 != player_number_2 and player_number_1 != player_number_3 and player_number_2 != player_number_3:
            break

    # 2. 부상 일수 출력
    injury_duration_1 = random.choice(injury_duration_list)
    injury_duration_2 = random.choice(injury_duration_list)
    injury_duration_3 = random.choice(injury_duration_list)

    print(f'{team_name} 부상 룰렛 결과 : {player_number_1 + 1}번 선수 {injury_duration_1}경기 결장')
    print(f'{team_name} 부상 룰렛 결과 : {player_number_2 + 1}번 선수 {injury_duration_2}경기 결장')
    print(f'{team_name} 부상 룰렛 결과 : {player_number_3 + 1}번 선수 {injury_duration_3}경기 결장')
