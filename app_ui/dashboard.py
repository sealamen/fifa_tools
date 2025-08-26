# app_ui/dashboard.py
import streamlit as st
import requests
import pandas as pd

API_BASE = "http://127.0.0.1:8000"

st.title("FIFA 경기 데이터 대시보드")

# 시즌 선택
season = st.selectbox("시즌 선택", ["2025_1", "2024_2"])

# 탭 구성
tabs = st.tabs(["리그 테이블", "개인 순위", "선수 정보", "팀 정보", "슛 상세"])

# =========================
# 1️⃣ 리그 테이블 탭
# =========================
with tabs[0]:
    st.header(f"{season} 시즌 리그 테이블")
    resp = requests.get(f"{API_BASE}/league_table/{season}")
    if resp.status_code == 200:
        df_league = pd.DataFrame(resp.json())
        st.dataframe(df_league)
    else:
        st.error("리그 테이블 조회 실패")

# =========================
# 2️⃣ 개인 순위 탭 (서브탭: 공격/득점/어시스트)
# =========================
with tabs[1]:
    st.header(f"{season} 시즌 개인 순위")
    sub_tabs = st.tabs(["공격 포인트", "득점", "어시스트"])

    # ⚡ 공격 포인트 순위
    with sub_tabs[0]:
        resp = requests.get(f"{API_BASE}/rank/attack_point/{season}")
        if resp.status_code == 200:
            df_attack = pd.DataFrame(resp.json()['stats'])
            # st.dataframe(df_attack)
            st.dataframe(df_attack, use_container_width=True, hide_index=True)  # <- hide_index=True
        else:
            st.error("공격 포인트 순위 조회 실패")

    # ⚡ 득점 순위
    with sub_tabs[1]:
        resp = requests.get(f"{API_BASE}/rank/goal/{season}")
        if resp.status_code == 200:
            df_goal = pd.DataFrame(resp.json()['stats'])
            # st.dataframe(df_goal)
            st.dataframe(df_goal, use_container_width=True, hide_index=True)

        else:
            st.error("득점 순위 조회 실패")

    # ⚡ 어시스트 순위
    with sub_tabs[2]:
        resp = requests.get(f"{API_BASE}/rank/assist/{season}")
        if resp.status_code == 200:
            df_assist = pd.DataFrame(resp.json()['stats'])
            st.dataframe(df_assist, use_container_width=True, hide_index=True)

            # st.dataframe(df_assist)
        else:
            st.error("어시스트 순위 조회 실패")

# =========================
# 3️⃣ 선수 정보 탭
# =========================
with tabs[2]:
    st.header("선수 정보 조회")
    player_name = st.text_input("선수 이름 입력 (예: 부카요 사카)")
    if player_name:
        resp = requests.get(f"{API_BASE}/info/player/{season}/{player_name}")
        if resp.status_code == 200 and resp.json():
            player_data = resp.json()

            # 리스트라면 첫 번째 요소만 사용
            if isinstance(player_data, list):
                player_info = player_data[0]
            else:
                player_info = player_data

            # 핵심 스탯 강조
            st.subheader(f"{player_info['PLAYER']} ({player_info['TEAM']})")
            col1, col2, col3 = st.columns(3)
            col1.metric("GOALS", player_info.get("GOALS", 0))
            col2.metric("ASSISTS", player_info.get("ASSISTS", 0))
            col3.metric("ATTACK_POINT", player_info.get("ATTACK_POINT", 0))

            # 나머지 스탯 DataFrame으로 표시
            stats_to_show = {k: v for k, v in player_info.items() if
                             k not in ["PLAYER", "TEAM", "GOALS", "ASSISTS", "ATTACK_POINT"]}
            df_player = pd.DataFrame([stats_to_show])
            st.dataframe(df_player)
        else:
            st.warning("선수 정보가 존재하지 않거나 조회 실패")

# =========================
# 4️⃣ 팀 정보 탭
# =========================
with tabs[3]:
    st.header("팀 정보 조회")
    team_name = st.text_input("팀 이름 입력 (예: 아스날)")
    if team_name:
        resp = requests.get(f"{API_BASE}/info/teams/{season}/{team_name}")
        if resp.status_code == 200 and resp.json():
            team_info = resp.json()[0]  # API에서 리스트로 넘어올 경우 첫 번째 데이터 사용

            # 핵심 스탯 강조
            st.subheader(f"{team_info['TEAM']}")
            col1, col2, col3 = st.columns(3)
            col1.metric("MATCHES_PLAYED", team_info["MATCHES_PLAYED"])
            col2.metric("WINS", team_info["WINS"])
            col3.metric("LOSSES", team_info["LOSSES"])

            # 나머지 스탯 DataFrame으로 표시
            stats_to_show = {k: v for k, v in team_info.items() if
                             k not in ["TEAM", "SEASON", "MATCHES_PLAYED", "WINS", "LOSSES"]}
            df_team = pd.DataFrame([stats_to_show])
            st.dataframe(df_team)
        else:
            st.warning("팀 정보가 존재하지 않거나 조회 실패")

# =========================
# 5️⃣ 슛 상세 탭
# =========================
with tabs[4]:
    st.header("슛 상세 조회")
    match_info_id = st.text_input("MATCH_INFO_ID 입력")
    if match_info_id:
        resp = requests.get(f"{API_BASE}/shoot_detail/{match_info_id}")
        if resp.status_code == 200 and resp.json():
            df_shoot = pd.DataFrame(resp.json()['shoot_detail'])
            st.dataframe(df_shoot)
        else:
            st.warning("슛 상세 정보 조회 실패")
