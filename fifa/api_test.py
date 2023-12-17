import requests
from urllib.parse import urlparse

def get_Player_info(playerID, ID_data):

    # 선수 이름 저장
    for info in ID_data:
        if info['id'] == playerID:
            return info["name"]


key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJYLUFwcC1SYXRlLUxpbWl0IjoiNTAwOjEwIiwiYWNjb3VudF9pZCI6IjE0MDk0MTEzOTIiLCJhdXRoX2lkIjoiMiIsImV4cCI6MTcxNjYzNDE3MCwiaWF0IjoxNzAxMDgyMTcwLCJuYmYiOjE3MDEwODIxNzAsInNlcnZpY2VfaWQiOiI0MzAwMTE0ODEiLCJ0b2tlbl90eXBlIjoiQWNjZXNzVG9rZW4ifQ.ZMTQ1lkYqrGJvADBtNlawic8sgPv51jMF_f969VYdnE"

get_all_players_url = "https://static.api.nexon.co.kr/fconline/latest/spid.json"
all_players = requests.get(urlparse(get_all_players_url).geturl(), headers = {"Authorization" : key}).json()

user_name = "빱빱디라"




# 1. Match Type 구하기 (친선 경기 만)
get_match_type_url = "https://static.api.nexon.co.kr/fconline/latest/matchtype.json"
match_types = requests.get(urlparse(get_match_type_url).geturl(), headers = {"Authorization" : key}).json()
friendly_match_type = match_types[1]["matchtype"]

# 2. User access ID 구하기
get_user_access_id_url = "https://public.api.nexon.com/openapi/fconline/v1.0/users?nickname=" + user_name
user_access_id = requests.get(urlparse(get_user_access_id_url).geturl(), headers = {"Authorization" : key}).json()["accessId"]

# 3. User Match ID 구하기
get_user_match_id_url = "https://public.api.nexon.com/openapi/fconline/v1.0/users/" + user_access_id + "/matches?matchtype=" + str(friendly_match_type)
user_match_ids = requests.get(urlparse(get_user_match_id_url).geturl(), headers = {"Authorization" : key}).json()

# 4. 해당 match ID 의 세부 정보 가져오기

for user_match_id in user_match_ids:
    get_match_info_url = "https://public.api.nexon.com/openapi/fconline/v1.0/matches/" + user_match_id
    match_info = requests.get(urlparse(get_match_info_url).geturl(), headers = {"Authorization" : key}).json()
    match_date = match_info["matchDate"]
    match_teams = match_info["matchInfo"]

    team1_info = match_teams[0]
    team2_info = match_teams[1]

    team1_nickname = team1_info["nickname"]
    team1_match_result = team1_info["matchDetail"]["matchResult"]
    team1_match_score = team1_info["shoot"]["goalTotal"]
    team1_players = team1_info["player"]

    team_1_score_details = team1_info["shootDetail"]
    team_1_score_specifics = []

    if team_1_score_details:
        for score_specific in team_1_score_details:

            goalTime = score_specific["goalTime"]
            scorer_id = score_specific["spId"]
            scorer = get_Player_info(scorer_id, all_players)


            if score_specific["assist"]:
                assist_id = score_specific["assistSpId"]
                assist = get_Player_info(assist_id, all_players)

                team_1_score_specifics.append(f"{goalTime} : {scorer}({assist})")


            else:
                team_1_score_specifics.append(f"{goalTime} : {scorer}")
    # team1_scored_players = []
    # team1_assist_players = []
    #
    # for player_info in team1_players:
    #
    #     if player_info["status"]["goal"] > 0:
    #         player_id = player_info["spId"]
    #         player_name = get_Player_info(player_id, all_players)
    #
    #         for i in range(player_info["status"]["goal"]):
    #             team1_scored_players.append(player_name)
    #
    #     if player_info["status"]["assist"] > 0:
    #         player_id = player_info["spId"]
    #         player_name = get_Player_info(player_id, all_players)
    #
    #         for i in range(player_info["status"]["assist"]):
    #             team1_assist_players.append(player_name)


    team2_nickname = team2_info["nickname"]
    team2_match_result = team2_info["matchDetail"]["matchResult"]
    team2_match_score = team2_info["shoot"]["goalTotal"]
    team2_players = team2_info["player"]

    # team2_scored_players = []
    # team2_assist_players = []
    #
    # for player_info in team2_players:
    #
    #     if player_info["status"]["goal"] > 0:
    #         player_id = player_info["spId"]
    #         player_name = get_Player_info(player_id, all_players)
    #
    #         for i in range(player_info["status"]["goal"]):
    #             team2_scored_players.append(player_name)
    #
    #     if player_info["status"]["assist"] > 0:
    #         player_id = player_info["spId"]
    #         player_name = get_Player_info(player_id, all_players)
    #
    #         for i in range(player_info["status"]["assist"]):
    #             team2_assist_players.append(player_name)

    team_2_score_details = team2_info["shootDetail"]
    team_2_score_specifics = []

    if team_2_score_details:
        for score_specific in team_2_score_details:

            goalTime = score_specific["goalTime"]
            scorer_id = score_specific["spId"]
            scorer = get_Player_info(scorer_id, all_players)

            if score_specific["assist"]:
                assist_id = score_specific["assistSpId"]
                assist = get_Player_info(assist_id, all_players)

                team_2_score_specifics.append(f"{goalTime} : {scorer}({assist})")

            else:
                team_2_score_specifics.append(f"{goalTime} : {scorer}")

    print(f"======== {team1_nickname} vs {team2_nickname} 경기 결과 ({match_date}) ====== ")
    print(f"{team1_nickname} ({team1_match_result}) {team1_match_score} : {team2_match_score} ({team2_match_result}) {team2_nickname}")
    # print(f" {team1_nickname} 득점자 : {team1_scored_players}\n {team1_nickname} 어시스트 : {team1_assist_players}\n")
    # print(f" {team2_nickname} 득점자 : {team2_scored_players}\n {team2_nickname} 어시스트 : {team2_assist_players}\n")
    print (f"{team_1_score_specifics}\n{team_2_score_specifics}")




    # print(user_match_id)
    # print(team1_info)
    # print(team2_info)


# get_all_match_id_url = "https://public.api.nexon.com/openapi/fconline/v1.0/matches?matchtype=" + str(friendly_match_type) + "&orderby=desc"
# all_match_id = requests.get(urlparse(get_all_match_id_url).geturl(), headers = {"Authorization" : key}).json()
# print(all_match_id)
