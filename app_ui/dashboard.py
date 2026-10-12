# app_ui/dashboard.py
import streamlit as st
import requests
import pandas as pd

from datetime import datetime
import os

# 실행 커맨드 : streamlit run app_ui/dashboard.py

API_BASE = "http://127.0.0.1:8000"

# 로그 디렉토리 및 파일

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
log_file_path  = os.path.join(LOG_DIR, "collect.log")

st.title("FIFA 경기 데이터 대시보드")

# 사이드바 메뉴
st.sidebar.title("📌 메뉴")
menu = st.sidebar.radio("탭 선택", ["개발 환경 구축 매뉴얼", "Architecture Diagram",
                                   "대시보드", "모듈 구조"])

# 매뉴얼
if menu == "개발 환경 구축 매뉴얼":
    st.header("개발환경 구축 매뉴얼")
    st.markdown("""
    1. 가상 환경 생성: 
       ```bash 
       conda create -n fifa python=3.13 # python 3.13.5
       ```  
    2. Oracle 11g 설치 : https://www.notion.so/Window-Oracle-2367eb9760b780c985f0f3d9ebd837b7

    3. 필수 라이브러리 설치: oracledb 사용을 위해서는 oracle_instant_client 필요 
       ```bash
       pip install oracledb fastapi uvicorn streamlit pandas requests
       ```
       
       
    4. 소스코드 가져오기 : https://github.com/sealamen/fifa_tools.git
    
    4. USER 생성 
       ```sql
       CREATE USER FCONLINE IDENTIFIED BY FCONLINE;
       GRANT connect, resource to FCONLINE;
        
       ALTER USER FCONLINE 
       DEFAULT TABLESPACE USERS
       TEMPORARY TABLESPACE TEMP;
        
       ALTER USER FCONLINE QUOTA UNLIMITED ON USERS;
       ```
    
    5. 테이블 생성 : https://github.com/sealamen/fifa_tools/issues/8
    
    6. 매핑용 데이터 추가 
       ```sql
       INSERT INTO TEAMS(TEAM_ID, TEAM_NAME, NICKNAME, SEASON, EMBLEM_URL) VALUES (01, 'ARSENAL', '일품해물탕면', '2025_2', 'arsenal_logo.png');
       INSERT INTO TEAMS(TEAM_ID, TEAM_NAME, NICKNAME, SEASON, EMBLEM_URL) VALUES (02, 'NEWCASTLE Utd', '빱빱디라', '2025_2', 'newcastle_logo.png');
       INSERT INTO TEAMS(TEAM_ID, TEAM_NAME, NICKNAME, SEASON, EMBLEM_URL) VALUES (03, 'BARCELONA', '빱빱디라라', '2025_2', 'barcelona_logo.png');
       INSERT INTO TEAMS(TEAM_ID, TEAM_NAME, NICKNAME, SEASON, EMBLEM_URL) VALUES (04, 'INTER MILAN', '잇다', '2025_2', 'inter_logo.png');
       INSERT INTO TEAMS(TEAM_ID, TEAM_NAME, NICKNAME, SEASON, EMBLEM_URL) VALUES (05, 'PSG', 'bai71739', '2025_2', 'psg_logo.png');
       INSERT INTO TEAMS(TEAM_ID, TEAM_NAME, NICKNAME, SEASON, EMBLEM_URL) VALUES (06, 'MANCHESTER UNITED', 'babysale', '2025_2', 'manutd_logo.png');
       INSERT INTO TEAMS(TEAM_ID, TEAM_NAME, NICKNAME, SEASON, EMBLEM_URL) VALUES (07, 'MANCHESTER CITY', '돗토누리', '2025_2', 'mancity_logo.png');
       INSERT INTO TEAMS(TEAM_ID, TEAM_NAME, NICKNAME, SEASON, EMBLEM_URL) VALUES (08, 'REAL MADRID', '미페만취급', '2025_2', 'real_logo.png');
       INSERT INTO TEAMS(TEAM_ID, TEAM_NAME, NICKNAME, SEASON, EMBLEM_URL) VALUES (09, 'LIVERPOOL', '일품해', '2025_2', 'liverpool_logo.png');
       INSERT INTO TEAMS(TEAM_ID, TEAM_NAME, NICKNAME, SEASON, EMBLEM_URL) VALUES (10, 'BAYERN MUNICH', '울지않기', '2025_2', 'bayern_logo.png');
       ```
    
    5. FastAPI 실행:  
       ```bash
       uvicorn main:app --reload
       ```
    6. Streamlit 실행 : 다른 터미널에서 실행 
       ```bash
       streamlit run dashboard.py
       ```
       
    7. 실행 후 대시보드 -> UPDATE 버튼 클릭  
    """)


# 아키텍처 다이어그램
elif menu == "Architecture Diagram":
    st.markdown("### Architecture Diagram")

    from PIL import Image
    architecture_image = Image.open("assets/architecture.png")  # 로컬 경로
    st.image(architecture_image, caption="아키텍처 다이어그램")

    st.markdown("""
    - 백엔드 서버 구축 이유
    1. 한 달 이내의 데이터만 외부 API 조회 가능 ⇒ 데이터 누적 시, 경기 예측 서비스 개발 가능 
    2. 추후 작업 스케쥴러 or cron 을 통한 자동화 예정
    """)

    st.markdown("### ")
    st.markdown("### DB Modeling")
    db_modeling_image = Image.open("assets/db_modeling.png")  # 로컬 경로
    st.image(db_modeling_image, caption="DB Modeling")

    st.markdown("""
    - 테이블 설명
        - MATCHES : MATCH 목록을 관리하는 테이블
        - MATCH_INFO : MATCH 의 경기 점수, 승패, 점유율, 총 패스 횟수 등 경기 전반의 데이터를 저장
        - MATCH_PLAYER_STATS : MATCH 에 출전한 선수의 평점, 슛, 득점, 패스 수 등 개인 기록을 저장
        - MATCH_SHOOT_DETAIL : 득점 장면에 대한 세부 지표 (사용 X)
        - PLAYERS : 선수 전체 목록 관리
        - TEAMS : 팀 전체 목록 관리
        
    
    - 역할 단위로 나눈 테이블 목록
    - MATCH_INFO, MATCH_PLAYER_STAST 는 각각 30개가 넘는 세부 지표들이 있지만, 조회용 테이블이기 때문에, 정규화 진행 X
    - 미사용 컬럼 및 미사용 테이블에 대한 추가 기능 개발 및 정리 필요
    """)

# 데이터 (선수/팀 조회)
elif menu == "대시보드":

    st.sidebar.markdown("---")
    st.sidebar.subheader("데이터 업데이트")
    if st.sidebar.button("UPDATE"):
        with st.spinner("데이터 수집 중..."):
            try:
                resp = requests.put(f"{API_BASE}/collect")
                if resp.status_code == 200:
                    log_text = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 수집 완료: {resp.text}\n"
                    with open(log_file_path, "a", encoding="utf-8") as f:
                        f.write(log_text)
                    st.success("데이터 수집 완료!")
                else:
                    st.error(f"수집 실패: {resp.status_code}")
            except Exception as e:
                st.error(f"예외 발생: {e}")

    # 마지막 동기화 날짜 표시
    if os.path.exists(log_file_path):
        with open(log_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if lines:
            last_sync = lines[-1].split("]")[0].replace("[", "")
            st.sidebar.caption(f"마지막 동기화: {last_sync}")

    # 로그 다운로드 버튼
    if os.path.exists(log_file_path):
        with open(log_file_path, "r", encoding="utf-8") as f:
            logs = f.read()
        st.sidebar.download_button("로그 파일 다운로드", logs, file_name="collect.log", mime="text/plain")

    # 시즌 선택
    season = st.selectbox("시즌 선택", ["2025_1", "2025_2", "2025_3", "2025_4", "2025_5", "2025_6", "2025_7", "2025_8",
                                    "2025_9", "2025_10", "2025_11", "2026_1"], index=11)

    # 탭 구성
    tabs = st.tabs(["리그 테이블", "개인 순위", "선수 정보", "팀 정보", "슛 상세", "경기 일정"])

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
        sub_tabs = st.tabs(["득점", "어시스트", "공격 포인트"])

        # ⚡ 공격 포인트 순위
        with sub_tabs[2]:
            resp = requests.get(f"{API_BASE}/rank/attack_point/{season}")
            if resp.status_code == 200:
                df_attack = pd.DataFrame(resp.json()['stats'])
                # st.dataframe(df_attack)
                st.dataframe(df_attack, use_container_width=True, hide_index=True)  # <- hide_index=True
            else:
                st.error("공격 포인트 순위 조회 실패")

        # ⚡ 득점 순위
        with sub_tabs[0]:
            resp = requests.get(f"{API_BASE}/rank/goal/{season}")
            if resp.status_code == 200:
                df_goal = pd.DataFrame(resp.json()['stats'])
                # st.dataframe(df_goal)
                st.dataframe(df_goal, use_container_width=True, hide_index=True)

            else:
                st.error("득점 순위 조회 실패")

        # ⚡ 어시스트 순위
        with sub_tabs[1]:
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
                    sorted_league = sorted(league_data, key=lambda x: x['승점'], reverse=True)
                    for i, t in enumerate(sorted_league):
                        if t['팀이름'] == team_name:
                            team_rank = i + 1
                            recent_5_results = t.get('최근 5경기', None)
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

    # 6️⃣ 경기 일정 탭
    with tabs[5]:
        st.header(f"{season} 시즌 경기 일정")
        resp = requests.get(f"{API_BASE}/schedule/{season}")
        if resp.status_code == 200:
            df_fixture = pd.DataFrame(resp.json()['fixtures'])
            # 이번 라운드만 필터링
            current_round = df_fixture['ROUND'].max()
            st.subheader(f"📅 이번 라운드: {current_round}R")
            st.dataframe(df_fixture[df_fixture['ROUND'] == current_round], use_container_width=True, hide_index=True)

            # 전체 일정 조회
            with st.expander("전체 일정 보기"):
                st.dataframe(df_fixture, use_container_width=True, hide_index=True)
        else:
            st.error("경기 일정 조회 실패")


# 모듈 구조
elif menu == "모듈 구조":
    st.markdown("### 모듈 구조")
    st.code("""
    📂 fifa_tools/
     ├─ module/
     │   ├─ fconline_api.py       # 외부 API 실행 
     │   ├─ data_collector.py     # 데이터 수집/저장 로직
     │   └─ db_utils.py           # SQL 모음 
     │
     ├─ app_ui/
     │   └─ dashboard.py          # Streamlit 대시보드
     │
     ├─ assets/
     │   ├─ arsenal_logo.png      # 팀 엠블럼 이미지파일
     │   ├─ barcelona_logo.png  
     │   └─ ...        
     │
     ├─ logs/
     │   └─ collect.log           # 데이터 가져오기에 대한 log 기록 
     │
     ├─ main.py                   # FastAPI API 서버
     └─ application.properties    # 보안 요소가 포함된 환경 설정 값  
    """)

    st.markdown("### 모듈 Flow Chart")

    from PIL import Image
    flowchart_image = Image.open("assets/flowchart.png")  # 로컬 경로
    st.image(flowchart_image, caption="모듈 Flow chart")

    st.markdown("""
    ### 기타 내용
    
    추후 개발 내용 
    
    - 작업 스케쥴러 or Crontab 등을 통한 경기 정보 저장 자동화 설정
    - 데이터 UI 추가 개발 및, 데이터 활용(경기 결과 예측, 득점 지표 등)
    """)



