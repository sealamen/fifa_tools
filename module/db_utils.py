
def save_match(cur, match_id, match_date, match_type):
    cur.execute("""
        MERGE INTO MATCHES M
        USING (SELECT :match_id AS match_id FROM dual) src
        ON (M.MATCH_ID = src.match_id)
        WHEN NOT MATCHED THEN
            INSERT (MATCH_ID, MATCH_DATE, MATCH_TYPE)
            VALUES (:match_id, TO_DATE(:match_date,'YYYY-MM-DD"T"HH24:MI:SS'), :match_type)
    """, match_id=match_id, match_date=match_date, match_type=match_type)

def save_match_info(cur, match_id, info, match_info_id_var):
    cur.execute("""
        INSERT INTO MATCH_INFO
        (MATCH_INFO_ID, MATCH_ID, OUID, NICKNAME, SEASON, MATCH_RESULT,
         POSSESSION, FOUL, INJURY, YELLOW_CARDS, RED_CARDS, AVERAGE_RATING,
         SHOOT_TOTAL, GOAL_TOTAL, PASS_TRY, PASS_SUCCESS,
         SHORT_PASS_TRY, SHORT_PASS_SUCCESS, LONG_PASS_TRY, LONG_PASS_SUCCESS,
         THROUGH_PASS_TRY, THROUGH_PASS_SUCCESS, LOBBED_THROUGH_PASS_TRY, LOBBED_THROUGH_PASS_SUCCESS,
         BOUNCING_LOB_PASS_TRY, BOUNCING_LOB_PASS_SUCCESS, DRIVEN_GROUND_PASS_TRY, DRIVEN_GROUND_PASS_SUCCESS,
         TACKLE_TRY, TACKLE_SUCCESS,
         EFFECTIVE_SHOOT_TOTAL, OWN_GOAL, SHOOT_HEADING, GOAL_HEADING,
         SHOOT_FREEKICK, GOAL_FREEKICK, SHOOT_IN_PENALTY, GOAL_IN_PENALTY,
         SHOOT_OUT_PENALTY, GOAL_OUT_PENALTY, SHOOT_PENALTYKICK, GOAL_PENALTYKICK)
        VALUES (MATCH_INFO_SEQ.NEXTVAL, :match_id, :ouid, :nickname, :season,
                :match_result, :possession, :foul, :injury, :yellow_cards,
                :red_cards, :average_rating, :shoot_total, :goal_total,
                :pass_try, :pass_success,
                :short_pass_try, :short_pass_success, :long_pass_try, :long_pass_success,
                :through_pass_try, :through_pass_success, :lobbed_through_pass_try, :lobbed_through_pass_success,
                :bouncing_lob_pass_try, :bouncing_lob_pass_success, :driven_ground_pass_try, :driven_ground_pass_success,
                :tackle_try, :tackle_success,
                :effective_shoot_total, :own_goal, :shoot_heading, :goal_heading,
                :shoot_freekick, :goal_freekick, :shoot_in_penalty, :goal_in_penalty,
                :shoot_out_penalty, :goal_out_penalty, :shoot_penaltykick, :goal_penaltykick)
        RETURNING MATCH_INFO_ID INTO :match_info_id
    """,
    match_id=match_id,
    ouid=info['ouid'],
    nickname=info['nickname'],
    season=info['matchDetail']['seasonId'],
    match_result=info['matchDetail']['matchResult'],
    possession=info['matchDetail']['possession'],
    foul=info['matchDetail']['foul'],
    injury=info['matchDetail']['injury'],
    yellow_cards=info['matchDetail']['yellowCards'],
    red_cards=info['matchDetail']['redCards'],
    average_rating=info['matchDetail']['averageRating'],
    shoot_total=info['shoot']['shootTotal'],
    goal_total=info['shoot']['goalTotal'],

    pass_try=info['pass']['passTry'],
    pass_success=info['pass']['passSuccess'],
    short_pass_try=info['pass'].get('shortPassTry', 0),
    short_pass_success=info['pass'].get('shortPassSuccess', 0),
    long_pass_try=info['pass'].get('longPassTry', 0),
    long_pass_success=info['pass'].get('longPassSuccess', 0),
    through_pass_try=info['pass'].get('throughPassTry', 0),
    through_pass_success=info['pass'].get('throughPassSuccess', 0),
    lobbed_through_pass_try=info['pass'].get('lobbedThroughPassTry', 0),
    lobbed_through_pass_success=info['pass'].get('lobbedThroughPassSuccess', 0),
    bouncing_lob_pass_try=info['pass'].get('bouncingLobPassTry', 0),
    bouncing_lob_pass_success=info['pass'].get('bouncingLobPassSuccess', 0),
    driven_ground_pass_try=info['pass'].get('drivenGroundPassTry', 0),
    driven_ground_pass_success=info['pass'].get('drivenGroundPassSuccess', 0),

    tackle_try=info['defence']['tackleTry'],
    tackle_success=info['defence']['tackleSuccess'],

    effective_shoot_total=info['shoot'].get('effectiveShootTotal', 0),
    own_goal=info['shoot'].get('ownGoal', 0),
    shoot_heading=info['shoot'].get('shootHeading', 0),
    goal_heading=info['shoot'].get('goalHeading', 0),
    shoot_freekick=info['shoot'].get('shootFreekick', 0),
    goal_freekick=info['shoot'].get('goalFreekick', 0),
    shoot_in_penalty=info['shoot'].get('shootInPenalty', 0),
    goal_in_penalty=info['shoot'].get('goalInPenalty', 0),
    shoot_out_penalty=info['shoot'].get('shootOutPenalty', 0),
    goal_out_penalty=info['shoot'].get('goalOutPenalty', 0),
    shoot_penaltykick=info['shoot'].get('shootPenaltyKick', 0),
    goal_penaltykick=info['shoot'].get('goalPenaltyKick', 0),

    match_info_id=match_info_id_var
    )

def save_player(cur, player, info, name, team_name):
    cur.execute("""
        MERGE INTO PLAYERS P
        USING (SELECT :sp_id AS sp_id FROM dual) src
        ON (P.SP_ID = src.sp_id)
        WHEN NOT MATCHED THEN
            INSERT (SP_ID, NAME, SEASON, POSITION, TEAM_NAME)
            VALUES (:sp_id, :name, :season, :position, :team_name)
    """,
    sp_id=player['spId'],
    name=name,
    team_name=team_name,
    season=info['matchDetail']['seasonId'],
    position=player['spPosition'])

def save_player_stats(cur, player, match_info_id):
    cur.execute("""
        INSERT INTO MATCH_PLAYER_STATS
        (PLAYER_STATS_ID, MATCH_INFO_ID, SP_ID, SP_POSITION, SP_GRADE, SP_RATING,
         SHOOT, EFFECTIVE_SHOOT, GOAL, ASSIST, DRIBBLE, DRIBBLE_TRY, DRIBBLE_SUCCESS,
         PASS_TRY, PASS_SUCCESS, BALL_POSSESSION_TRY, BALL_POSSESSION_SUCCESS,
         TACKLE_TRY, TACKLE_SUCCESS, INTERCEPT, DEFENDING, BLOCK_TRY, BLOCK, AERIAL_TRY, AERIAL_SUCCESS,
         YELLOW_CARDS, RED_CARDS)
        VALUES (MATCH_PLAYER_STATS_SEQ.NEXTVAL, :match_info_id, :sp_id, :sp_position, :sp_grade, :sp_rating,
                :shoot, :effective_shoot, :goal, :assist, :dribble, :dribble_try, :dribble_success,
                :pass_try, :pass_success, :ball_possession_try, :ball_possession_success,
                :tackle_try, :tackle_success, :intercept, :defending, :block_try, :block,
                :aerial_try, :aerial_success, :yellow_cards, :red_cards)
    """,
    match_info_id=match_info_id,
    sp_id=player['spId'],
    sp_position=player['spPosition'],
    sp_grade=player['spGrade'],
    sp_rating=player['status']['spRating'],

    shoot=player['status']['shoot'],
    effective_shoot=player['status']['effectiveShoot'],
    goal=player['status']['goal'],
    assist=player['status']['assist'],
    dribble=player['status']['dribble'],
    dribble_try=player['status']['dribbleTry'],
    dribble_success=player['status']['dribbleSuccess'],

    pass_try=player['status']['passTry'],
    pass_success=player['status']['passSuccess'],
    ball_possession_try=player['status']['ballPossesionTry'],
    ball_possession_success=player['status']['ballPossesionSuccess'],
    tackle_try=player['status']['tackleTry'],
    tackle_success=player['status']['tackle'],
    block_try=player['status']['blockTry'],
    block=player['status']['block'],
    intercept=player['status']['intercept'],
    defending=player['status']['defending'],
    aerial_try=player['status']['aerialTry'],
    aerial_success=player['status']['aerialSuccess'],

    yellow_cards=player['status']['yellowCards'],
    red_cards=player['status']['redCards']
    )

def save_shoot_detail(cur, shoot, match_info_id):
    cur.execute("""
        INSERT INTO MATCH_SHOOT_DETAIL
        (SHOOT_ID, MATCH_INFO_ID, SP_ID, GOAL_TIME, X, Y, TYPE, RESULT,
         ASSIST, ASSIST_SP_ID, HIT_POST, IN_PENALTY)
        VALUES (MATCH_SHOOT_DETAIL_SEQ.NEXTVAL, :match_info_id, :sp_id, :goal_time,
                :x, :y, :type, :result, :assist, :assist_sp_id, :hit_post, :in_penalty)
    """,
    match_info_id=match_info_id,
    sp_id=shoot['spId'],
    goal_time=shoot['goalTime'],
    x=shoot['x'],
    y=shoot['y'],
    type=shoot['type'],
    result=shoot['result'],
    assist=1 if shoot.get('assist', False) else 0,
    assist_sp_id=shoot.get('assistSpI', None),
    hit_post=1 if shoot.get('hitPost', False) else 0,
    in_penalty=1 if shoot.get('inPenalty', False) else 0
    )

def is_match_info_exists(cur, match_id, ouid):
    """
    MATCH_INFO 테이블에서 match_id + ouid 조합이 존재하는지 확인
    :param cur: DB 커서
    :param match_id: 경기 ID
    :param ouid: 유저 ID
    :return: 존재하면 True, 아니면 False
    """
    cur.execute("""
        SELECT COUNT(*) FROM MATCH_INFO
        WHERE MATCH_ID = :match_id AND OUID = :ouid
    """, match_id=match_id, ouid=ouid)
    return cur.fetchone()[0] > 0


# 기존 저장 함수들은 그대로 두고, 아래 조회 함수 추가

def query_all_matches(cur):
    cur.execute("SELECT MATCH_ID, MATCH_DATE, MATCH_TYPE FROM MATCHES ORDER BY MATCH_DATE DESC")
    return [dict(zip([d[0] for d in cur.description], row)) for row in cur.fetchall()]


def query_match_info(cur, match_id):
    cur.execute("""
        SELECT * 
        FROM MATCH_INFO 
        WHERE MATCH_ID = :match_id
        ORDER BY MATCH_INFO_ID
    """, match_id=match_id)
    return [dict(zip([d[0] for d in cur.description], row)) for row in cur.fetchall()]


def query_player_stats(cur, match_info_id):
    cur.execute("""
        SELECT * 
        FROM MATCH_PLAYER_STATS 
        WHERE MATCH_INFO_ID = :match_info_id
        ORDER BY PLAYER_STATS_ID
    """, match_info_id=match_info_id)
    return [dict(zip([d[0] for d in cur.description], row)) for row in cur.fetchall()]


def query_shoot_detail(cur, match_info_id):
    cur.execute("""
        SELECT * 
        FROM MATCH_SHOOT_DETAIL 
        WHERE MATCH_INFO_ID = :match_info_id
        ORDER BY SHOOT_ID
    """, match_info_id=match_info_id)
    return [dict(zip([d[0] for d in cur.description], row)) for row in cur.fetchall()]
