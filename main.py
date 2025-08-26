import oracledb
import configparser
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from module import db_utils, data_collector


app = FastAPI(title="FIFA Data Collector")
templates = Jinja2Templates(directory="templates")


@app.get("/collect")
def collect_data():
    """
    특정 유저의 경기 데이터 수집
    TODO : 전체 유저 리스트를 만들어서, 한 번에 모든 경기 데이터를 save 하도록 만들자
    """
    data_collector.collect_and_save_match_data()
    return {"status": "success"}


# 조회용 API
@app.get("/matches")
def get_matches():
    """
    모든 경기 조회
    """
    cur = conn.cursor()
    result = db_utils.query_all_matches(cur)
    cur.close()
    return {"matches": result}


@app.get("/match_info/{match_id}")
def get_match_info(match_id: str):
    """
    특정 경기의 match_info 조회
    """
    cur = conn.cursor()
    result = db_utils.query_match_info(cur, match_id)
    cur.close()
    return {"match_info": result}


@app.get("/player_stats/{match_info_id}")
def get_player_stats(match_info_id: int):
    """
    특정 match_info_id의 선수 통계 조회
    """
    cur = conn.cursor()
    result = db_utils.query_player_stats(cur, match_info_id)
    cur.close()
    return {"player_stats": result}


@app.get("/shoot_detail/{match_info_id}")
def get_shoot_detail(match_info_id: int):
    """
    특정 match_info_id의 슛 상세 조회
    """
    cur = conn.cursor()
    result = db_utils.query_shoot_detail(cur, match_info_id)
    cur.close()
    return {"shoot_detail": result}


@app.get("/")
def root():
    return {"message": "FIFA Data Collector API"}



@app.get("/api/match/{match_id}", response_class=HTMLResponse)
def match_detail_api(request: Request, match_id: str):
    cur = conn.cursor()
    match_info = db_utils.query_match_info(cur, match_id)
    player_stats = []
    shoot_details = []
    for info in match_info:
        stats = db_utils.query_player_stats(cur, info['MATCH_INFO_ID'])
        shoots = db_utils.query_shoot_detail(cur, info['MATCH_INFO_ID'])
        player_stats.append(stats)
        shoot_details.append(shoots)
    cur.close()
    # 작은 HTML fragment 반환
    return templates.TemplateResponse("match_detail_fragment.html", {
        "request": {}, "match_info": match_info,
        "player_stats": player_stats, "shoot_details": shoot_details
    })


if __name__ == "__main__":
    # 설정 파일 로드
    config = configparser.ConfigParser()
    config.read("application.properties", encoding="utf-8")
    db_user = config['DEFAULT']['db.user']
    db_password = config['DEFAULT']['db.password']
    db_dsn = config['DEFAULT']['db.dsn']
    api_key = config['DEFAULT']['api.key']
    oracle_client_location = config['DEFAULT']["oracle_client_location"]

    # Oracle Thick 모드 활성화
    oracledb.init_oracle_client(lib_dir=oracle_client_location)

    # DB 연결
    conn = oracledb.connect(user=db_user, password=db_password, dsn=db_dsn)

    # FastAPI 서버 실행 : reload 가 안되는 단점이 있어서, 제대로 실행하려면 명령어로 실행 필요 (uvicorn main:app --reload)
    uvicorn.run(app, host="127.0.0.1", port=8000)


