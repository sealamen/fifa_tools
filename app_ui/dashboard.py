# app_ui/dashboard.py
import streamlit as st
import requests
import pandas as pd


API_BASE = "http://127.0.0.1:8000"

st.title("FIFA 경기 데이터 대시보드")



st.sidebar.title("📌 메뉴")
menu = st.sidebar.radio("탭 선택", ["개발 환경 구축 매뉴얼", "Architecture Diagram",
                                   "데이터", "모듈 구조"])


# 매뉴얼
if menu == "개발 환경 구축 매뉴얼":
    st.header("개발환경 구축 매뉴얼")
    st.markdown("""
    1. Python 3.9+ 설치  
    2. 가상환경 생성: `conda create -n fifa python=3.9`  
    3. 필수 라이브러리 설치:  
       ```bash
       pip install fastapi uvicorn streamlit pandas requests matplotlib
       ```
    4. DB 세팅 후 FastAPI 실행:  
       ```bash
       uvicorn main:app --reload
       ```
    5. Streamlit 실행:  
       ```bash
       streamlit run dashboard.py
       ```
    """)


# 아키텍처 다이어그램
elif menu == "Architecture Diagram":
    st.header("Architecture Diagram")
    st.markdown("""
    ```mermaid
    flowchart LR
        User --> Streamlit_UI
        Streamlit_UI --> FastAPI
        FastAPI --> DB[(Database)]
        FastAPI --> ExternalAPI[(Football API)]
    ```
    """)

# 데이터 (선수/팀 조회)
elif menu == "데이터":

    # 시즌 선택
    season = st.selectbox("시즌 선택", ["2025_1", "2024_2"])

    # 탭 구성
    tabs = st.tabs(["리그 테이블", "개인 순위", "선수 정보", "팀 정보", "슛 상세"])

    # 1️⃣ 리그 테이블 탭
    with tabs[0]:
        st.header(f"{season} 시즌 리그 테이블")
        resp = requests.get(f"{API_BASE}/league_table/{season}")
        if resp.status_code == 200:
            df_league = pd.DataFrame(resp.json())
            df_league.index = df_league.index + 1
            st.dataframe(df_league)
        else:
            st.error("리그 테이블 조회 실패")

    # 2️⃣ 개인 순위 탭 (서브탭: 공격/득점/어시스트)
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

    # 3️⃣ 선수 정보 탭
    with tabs[2]:
        st.header("선수 정보 조회")
        player_name = st.text_input("선수 이름 입력 (예: 레반도프스키)")
        if player_name:
            resp = requests.get(f"{API_BASE}/info/player/{season}/{player_name}")
            if resp.status_code == 200 and resp.json():
                player_data = resp.json()

                # 리스트라면 첫 번째 요소만 사용
                if isinstance(player_data, list):
                    player_info = player_data[0]
                else:
                    player_info = player_data

                spid = player_info['PLAYER_ID']
                image_url = f"https://fo4.dn.nexoncdn.co.kr/live/externalAssets/common/playersAction/p{spid}.png"

                with st.container():
                    col1, col2 = st.columns([2, 2])  # 좌측: 이미지 / 우측: 정보
                    with col1:
                        st.image(image_url, width=180)  # 선수 이미지
                    with col2:

                        st.subheader(f"{player_info['PLAYER']} ({player_info['TEAM']})")
                        cap_col1, cap_col2, cap_col3 = st.columns([3, 1, 1])

                        with cap_col1:
                            st.caption(f"평균 평점: {player_info['AVERAGE_RATING']:.2f}")
                        with cap_col2:
                            st.caption(f"🟨 {player_info.get('YELLOW_CARDS', 0)}")
                        with cap_col3:
                            st.caption(f"🟥 {player_info.get('RED_CARDS', 0)}")

                        # 메트릭들 한 줄에 정렬
                        mcol1, mcol2, mcol3 = st.columns(3)
                        mcol1.metric("GOALS", player_info.get("GOALS", 0))
                        mcol2.metric("ASSISTS", player_info.get("ASSISTS", 0))
                        mcol3.metric("공격P", player_info.get("ATTACK_POINT", 0))

                # 나머지 스탯 DataFrame으로 표시
                stats_to_show = {k: v for k, v in player_info.items()}
                # df_player = pd.DataFrame([stats_to_show])
                # st.dataframe(df_player)

                # 공격 스탯
                attack_keys = ["GOALS", "ASSISTS", "ATTACK_POINT", "SHOOT", "EFFECTIVE_SHOOT", "DRIBBLES", "DRIBBLE_SUCCESS"]
                stats_to_show_for_attack = {k: stats_to_show[k] for k in attack_keys if k in stats_to_show}
                df_player_attack = pd.DataFrame([stats_to_show_for_attack])
                st.caption("공격 지표")
                st.dataframe(df_player_attack, use_container_width=True, hide_index=True)

                # 패스 스탯
                pass_keys = ["PASS_TRY", "PASS_SUCCESS", "THROUGH_PASS_TRY", "THROUGH_PASS_SUCCESS", "LONG_PASS_TRY", "LONG_PASS_SUCCESS", "SHORT_PASS_TRY", "SHORT_PASS_SUCCESS"]
                stats_to_show_for_pass = {k: stats_to_show[k] for k in pass_keys if k in stats_to_show}
                df_player_pass = pd.DataFrame([stats_to_show_for_pass])
                st.caption("패스 지표")
                st.dataframe(df_player_pass, use_container_width=True, hide_index=True)

                # 수비 스탯
                defense_keys = ["TACKLE_TRY", "TACKLE_SUCCESS", "BLOCK_TRY", "BLOCK", "DEFENDING", "INTERCEPT"]
                stats_to_show_for_defense = {k: stats_to_show[k] for k in defense_keys if k in stats_to_show}
                df_player_defense = pd.DataFrame([stats_to_show_for_defense])
                st.caption("수비 지표")
                st.dataframe(df_player_defense, use_container_width=True, hide_index=True)

            else:
                st.warning("선수 정보가 존재하지 않거나 조회 실패")

    # 4️⃣ 팀 정보 탭
    with tabs[3]:
        st.header("팀 정보 조회")

        # 팀 리스트 조회
        resp = requests.get(f"{API_BASE}/info/team_list/{season}")
        if resp.status_code == 200:
            json_data = resp.json()
            teams = [t["TEAM_NAME"] for t in json_data]
        else:
            st.error("팀 리스트 조회 실패")
            teams = []

        team_name = st.selectbox("팀 선택", ['선택하세요'] + teams)

        if team_name != '선택하세요':
            # 팀 정보 가져오기
            resp_team = requests.get(f"{API_BASE}/info/teams/{season}/{team_name}")
            resp_rank = requests.get(f"{API_BASE}/league_table/{season}")

            if resp_team.status_code == 200 and resp_team.json():
                team_info = resp_team.json()[0]

                # 현재 순위 계산
                team_rank = None
                recent_5_results = None
                if resp_rank.status_code == 200:
                    league_data = resp_rank.json()
                    sorted_league = sorted(league_data, key=lambda x: x['POINTS'], reverse=True)
                    for i, t in enumerate(sorted_league):
                        if t['TEAM_NAME'] == team_name:
                            team_rank = i + 1
                            recent_5_results = t.get('RECENT_5_RESULTS', None)
                            break

                # 팀 헤더 + 로고
                with st.container():
                    col_logo, col_title = st.columns([1, 3])
                    with col_logo:
                        try:
                            logo_path = f"assets/{team_info['EMBLEM_URL']}"
                            st.image(logo_path, width=100)
                        except:
                            st.image("assets/logo.png", width=100)

                    with col_title:
                        st.subheader(f"{team_info['TEAM']} ({season} 순위 : {team_rank}위)")
                        st.markdown(
                            f"**총 경기:** {team_info['MATCHES_PLAYED']} | "
                            f"**승:** {team_info['WINS']} | "
                            f"**무:** {team_info['DRAWS']} | "
                            f"**패:** {team_info['LOSSES']} | "
                            f"**득점:** {team_info['GOALS_FOR']} | "
                            f"**실점:** {team_info['GOALS_AGAINST']}"
                        )

                # 추가 스탯 DataFrame
                stats_to_show = {k: v for k, v in team_info.items() if
                                 k not in ["TEAM", "SEASON", "MATCHES_PLAYED", "WINS", "DRAWS", "LOSSES",
                                           "GOALS_FOR", "GOALS_AGAINST", "EMBLEM_URL", "RANK", "RECENT_5_RESULTS"]}
                if stats_to_show:
                    st.caption("기타 스탯")
                    df_team = pd.DataFrame([stats_to_show])
                    st.dataframe(df_team, use_container_width=True, hide_index=True)

                # 최근 5경기 컬러 블록
                st.caption("최근 5경기 결과")
                recent_results = team_info.get("RECENT_5_RESULTS", "")
                recent_list = list(recent_results)

                html_blocks = ""
                for r in recent_list:
                    if r == '승':
                        color = "#4CAF50"
                    elif r == '무':
                        color = "#FFC107"
                    elif r == '패':
                        color = "#F44336"
                    else:
                        color = "#B0BEC5"
                    html_blocks += f"""
                        <div style='display:inline-block; width:40px; height:40px; background-color:{color};
                                    color:white; text-align:center; line-height:40px; margin-right:5px; border-radius:5px;'>
                            {r}
                        </div>
                    """
                st.markdown(html_blocks, unsafe_allow_html=True)

            else:
                st.warning("팀 정보가 존재하지 않거나 조회 실패")

    # 5️⃣ 슛 상세 탭
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


# 모듈 구조
elif menu == "모듈 구조":
    st.header("모듈 구조")
    st.code("""
    📂 fifa_tools/
    ├── app_ui/
    │   ├── dashboard.py      # Streamlit 대시보드
    ├── api/
    │   ├── main.py           # FastAPI 엔트리포인트
    │   ├── routers/          # 라우터들
    │   └── schemas.py        # Pydantic 모델
    ├── db/
    │   ├── models.py         # SQLAlchemy 모델
    │   ├── crud.py           # DB 쿼리
    │   └── database.py       # DB 연결
    └── scripts/
        └── fetch_data.py     # API/크롤링 자동 수집
    """)
