import oracledb
import configparser
import uvicorn
from fastapi import FastAPI, Path
from pydantic import BaseModel
from typing import List, Optional

from module import db_utils, data_collector

# 전역 선언
conn = None

def init_db():
    global conn
    import configparser, oracledb
    config = configparser.ConfigParser()
    config.read("application.properties", encoding="utf-8")
    db_user = config['DEFAULT']['db.user']
    db_password = config['DEFAULT']['db.password']
    db_dsn = config['DEFAULT']['db.dsn']
    oracle_client_location = config['DEFAULT']["oracle_client_location"]
    oracledb.init_oracle_client(lib_dir=oracle_client_location)
    conn = oracledb.connect(user=db_user, password=db_password, dsn=db_dsn)

# FastAPI 실행 전에 DB 초기화
init_db()


# FastAPI 앱 생성
app = FastAPI(
    title="FIFA Data Collector",
    description="FIFA 경기, 선수, 팀 데이터 조회용 API",
    version="1.0"
)

# Pydantic 모델
class PlayerStat(BaseModel):
    team: str
    player: str
    goals: int
    assists: int
    attack_point: int

class PlayerStatsResponse(BaseModel):
    season: str
    stats: List[PlayerStat]

class PlayerInfo(BaseModel):
    team: str
    player: str
    position: str
    image: Optional[str]
    goals: int
    assists: int
    attack_point: int
    dribbles: int
    dribble_success: int
    pass_try: int
    pass_success: int
    tackle_try: int
    tackle_success: int
    average_rating: Optional[float]
    shoot: int
    effective_shoot: int
    defending: int
    block_try: int
    block: int
    yellow_cards: int
    red_cards: int

class TeamInfo(BaseModel):
    team_name: str
    season: str
    matches_played: int
    wins: int
    draws: int
    losses: int
    goals_for: int
    goals_against: int
    goal_diff: int
    own_goals: int
    yellow_cards: int
    red_cards: int

class ShootDetail(BaseModel):
    shoot_id: int
    player_name: str
    shoot_type: str
    result: str
    minute: int

# 루트
@app.get("/", description="API 기본 정보")
def root():
    return {"message": "FIFA Data Collector API"}

# 데이터 수집
@app.put("/collect", description="NEXON API를 통해 최신 경기 데이터를 수집 후 DB에 저장")
def collect_data():
    data_collector.collect_and_save_match_data()
    return {"status": "success"}

# 리그 테이블 조회
@app.get("/league_table/{season}", description="특정 시즌 리그 순위 조회")
def show_league_table(season: str= Path(..., description="조회할 시즌, 예: '2025_1'")):
    cur = conn.cursor()
    result = db_utils.show_league_table(cur, season)
    cur.close()
    return result

# 개인 순위 조회
@app.get("/rank/attack_point/{season}", description="공격 포인트 순위 조회")
def get_attack_point_rank(season: str= Path(..., description="조회할 시즌, 예: '2025_1'")):
    cur = conn.cursor()
    result = db_utils.get_attack_point_rank(cur, season)
    cur.close()
    # return result
    return {"season": season, "stats": result}

@app.get("/rank/goal/{season}", description="득점 순위 조회")
def get_goal_rank(season: str= Path(..., description="조회할 시즌, 예: '2025_1'")):
    cur = conn.cursor()
    result = db_utils.get_goal_rank(cur, season)
    cur.close()
    # return result
    return {"season": season, "stats": result}

@app.get("/rank/assist/{season}", description="어시스트 순위 조회")
def get_assist_rank(season: str= Path(..., description="조회할 시즌, 예: '2025_1'")):
    cur = conn.cursor()
    result = db_utils.get_assist_rank(cur, season)
    cur.close()
    # return result
    return {"season": season, "stats": result}

# 선수 정보 조회
@app.get("/info/player/{season}/{player_name}", description="특정 선수 시즌별 누적 스탯 조회")
def get_player_info(
        season: str = Path(..., description="조회할 시즌, 예: '2025_1'"),
        player_name: str = Path(..., description="조회할 선수 이름")
    ):
    cur = conn.cursor()
    result = db_utils.get_player_info(cur, season, player_name)
    cur.close()
    return result

# 팀 정보 조회
@app.get("/info/teams/{season}/{team_name}", description="특정 팀 시즌별 누적 스탯 조회")
def get_team_info(
        season: str = Path(..., description="조회할 시즌, 예: '2025_1'"),
        team_name: str = Path(..., description="조회할 팀 이름")
    ):
    cur = conn.cursor()
    result = db_utils.get_team_info(cur, season, team_name)
    cur.close()
    return result

# 슛 상세 조회
@app.get("/shoot_detail/{match_info_id}")
def get_shoot_detail(match_info_id: int):
    """
    특정 match_info_id의 슛 상세 조회
    """
    cur = conn.cursor()
    result = db_utils.query_shoot_detail(cur, match_info_id)
    cur.close()
    return {"shoot_detail": result}


if __name__ == "__main__":
    # config = configparser.ConfigParser()
    # config.read("application.properties", encoding="utf-8")
    # db_user = config['DEFAULT']['db.user']
    # db_password = config['DEFAULT']['db.password']
    # db_dsn = config['DEFAULT']['db.dsn']
    # oracle_client_location = config['DEFAULT']["oracle_client_location"]
    #
    # # Oracle Thick 모드 활성화
    # oracledb.init_oracle_client(lib_dir=oracle_client_location)
    #
    # # DB 연결
    # conn = oracledb.connect(user=db_user, password=db_password, dsn=db_dsn)

    # FastAPI 서버 실행 : reload 가 안되는 단점이 있어서, 제대로 실행하려면 명령어로 실행 필요 (uvicorn main:app --reload)
    uvicorn.run(app, host="127.0.0.1", port=8000)


