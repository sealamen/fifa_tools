import oracledb
import configparser

from module import fconline_api
from module import db_utils


def main():

    # 환경 설정 읽기
    config = configparser.ConfigParser()
    config.read("application.properties", encoding="utf-8")

    db_user = config['DEFAULT']['db.user']
    db_password = config['DEFAULT']['db.password']
    db_dsn = config['DEFAULT']['db.dsn']
    oracle_client_location = config['DEFAULT']["oracle_client_location"]

    user_name = "일품해물탕면"
    api_key = config['DEFAULT']['api.key']


    print("=== 환경 설정 로드 완료 ===")
    print(f"DB: {db_user}@{db_dsn}, API_KEY: {api_key[:6]}***\n")

    # Oracle Thick 모드 활성화 및 연결
    oracledb.init_oracle_client(lib_dir=oracle_client_location)
    conn = oracledb.connect(user=db_user, password=db_password, dsn=db_dsn)
    cur = conn.cursor()
    print("=== DB 연결 완료 ===\n")

    # NEXON API 데이터 불러오기
    all_players = fconline_api.get_all_players(api_key)
    match_types = fconline_api.get_match_type(api_key)
    friendly_match_type = match_types[1]["matchtype"]
    user_access_id = fconline_api.get_user_access_id(api_key, user_name)
    user_match_ids = fconline_api.get_user_match_ids(api_key, user_access_id, friendly_match_type)
    print("=== NEXON API 불러오기 완료 ===")
    print(f"총 경기 수 조회: {len(user_match_ids)}\n")


    def get_player_name(player_id):
        for player_info in all_players:
            if player_info['id'] == player_id:
                return player_info["name"]
        return None

    # 경기 데이터 저장
    print("=== 데이터 저장 시작 ===\n")
    for match_id in user_match_ids:
        print(f">>> Match_ID: {match_id} 처리 시작")
        match_results = fconline_api.get_match_detail(api_key, match_id)
        print(f">>> Match Date: {match_results['matchDate']}")

        db_utils.save_match(cur, match_id, match_results['matchDate'], match_results['matchType'])
        conn.commit()
        print(">>> [DONE] MATCHES 테이블 저장 완료")

        for match_info in match_results['matchInfo']:

            # 중복 체크
            if db_utils.is_match_info_exists(cur, match_id, match_info['ouid']):
                print(f">>> [SKIP] 중복 데이터 존재: match_id={match_id}, ouid={match_info['ouid']}")
                continue

            match_info_id_var = cur.var(int)
            db_utils.save_match_info(cur, match_id, match_info, match_info_id_var)
            match_info_id = match_info_id_var.getvalue()[0]
            print(f">>> [DONE] MATCH_INFO 저장 완료: match_info_id={match_info_id}, ouid={match_info['ouid']}")

            for player in match_info['player']:
                name = get_player_name(player['spId'])
                db_utils.save_player(cur, player, match_info, name)
                db_utils.save_player_stats(cur, player, match_info_id)
                print(f">>> [DONE] PLAYER & PLAYER_STATS 저장 완료: sp_id={player['spId']}, name={name}")

            for shoot in match_info.get('shootDetail', []):
                db_utils.save_shoot_detail(cur, shoot, match_info_id)
                print(f">>> [DONE] SHOOT_DETAIL 저장 완료: shoot_id={shoot.get('shootId', 'N/A')}")

        conn.commit()
        print(f">>> Match_ID {match_id} 처리 완료\n")

    cur.close()
    conn.close()
    print("=== DB 연결 종료 ===")


if __name__ == "__main__":
    main()
