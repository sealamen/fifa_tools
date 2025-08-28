
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

# 시즌 리그 순위 조회
def show_league_table(cur, season):
    cur.execute("""
        WITH team_stats AS (
            SELECT 
                t.TEAM_NAME AS team_name,
                COUNT(*) AS matches_played,
                SUM(CASE WHEN mi1.MATCH_RESULT = '승' THEN 1 ELSE 0 END) AS wins,
                SUM(CASE WHEN mi1.MATCH_RESULT = '무' THEN 1 ELSE 0 END) AS draws,
                SUM(CASE WHEN mi1.MATCH_RESULT = '패' THEN 1 ELSE 0 END) AS losses,
                SUM(CASE 
                        WHEN mi1.MATCH_RESULT = '승' THEN 3
                        WHEN mi1.MATCH_RESULT = '무' THEN 1
                        ELSE 0
                    END
                ) AS points,
                SUM(mi1.GOAL_TOTAL) AS goals_for,
                SUM(mi2.GOAL_TOTAL) AS goals_against,
                LISTAGG(mi1.MATCH_RESULT, '') 
                    WITHIN GROUP (ORDER BY m.MATCH_DATE DESC) AS recent_results_all
            FROM MATCH_INFO mi1
            JOIN MATCH_INFO mi2 
                ON mi1.MATCH_ID = mi2.MATCH_ID 
               AND mi1.MATCH_INFO_ID != mi2.MATCH_INFO_ID
            JOIN MATCHES m
                ON mi1.MATCH_ID = m.MATCH_ID
            JOIN TEAMS t
                ON mi1.NICKNAME = t.NICKNAME   -- 여기서 매핑
               AND mi1.SEASON = t.SEASON       -- 여기서 매핑 
            WHERE mi2.SEASON = :season
            GROUP BY t.TEAM_NAME
        )
        SELECT 
            team_name,
            matches_played,
            wins,
            draws,
            losses,
            points,
            goals_for,
            goals_against,
            (goals_for - goals_against) AS goal_diff,
            SUBSTR(recent_results_all, 1, 5) AS recent_5_results
        FROM team_stats
        ORDER BY points DESC, (goals_for - goals_against) DESC, goals_for DESC
    """, season=season)
    return [dict(zip([d[0] for d in cur.description], row)) for row in cur.fetchall()]

# 시즌 공격포인트 랭킹
def get_attack_point_rank(cur, season):
    cur.execute("""
        SELECT 
            RANK() OVER (ORDER BY SUM(s.GOAL + s.ASSIST) DESC) AS RANKING,
            t.TEAM_NAME AS TEAM,
            p.NAME AS PLAYER,
            SUM(s.GOAL) AS GOAL,
            SUM(s.ASSIST) AS ASSIST,
            (SUM(s.GOAL) + SUM(s.ASSIST)) AS ATTACK_POINT
        FROM MATCH_PLAYER_STATS s
        JOIN MATCH_INFO m 
            ON s.MATCH_INFO_ID = m.MATCH_INFO_ID
        JOIN PLAYERS p 
            ON s.SP_ID = p.SP_ID
        JOIN TEAMS t 
            ON p.TEAM_NAME = t.TEAM_NAME
        WHERE m.SEASON = :season
        GROUP BY t.TEAM_NAME, p.NAME
        ORDER BY RANKING
    """, season=season)
    return [dict(zip([d[0] for d in cur.description], row)) for row in cur.fetchall()]

# 시즌 득점 랭킹
def get_goal_rank(cur, season):
    cur.execute("""
        SELECT 
            RANK() OVER (ORDER BY SUM(s.GOAL) DESC) AS RANKING,
            t.TEAM_NAME AS TEAM,
            p.NAME AS PLAYER,
            SUM(s.GOAL) AS GOAL,
            SUM(s.ASSIST) AS ASSIST,
            (SUM(s.GOAL) + SUM(s.ASSIST)) AS ATTACK_POINT
        FROM MATCH_PLAYER_STATS s
        JOIN MATCH_INFO m ON s.MATCH_INFO_ID = m.MATCH_INFO_ID
        JOIN PLAYERS p ON s.SP_ID = p.SP_ID
        JOIN TEAMS t ON p.TEAM_NAME = t.TEAM_NAME
        WHERE m.SEASON = :season
        GROUP BY t.TEAM_NAME, p.NAME
        ORDER BY RANKING
    """, season=season)
    return [dict(zip([d[0] for d in cur.description], row)) for row in cur.fetchall()]

# 시즌 도움 랭킹
def get_assist_rank(cur, season):
    cur.execute("""
        SELECT 
            RANK() OVER (ORDER BY SUM(s.ASSIST) DESC) AS RANKING,
            t.TEAM_NAME AS TEAM,
            p.NAME AS PLAYER,
            SUM(s.GOAL) AS GOAL,
            SUM(s.ASSIST) AS ASSIST,
            (SUM(s.GOAL) + SUM(s.ASSIST)) AS ATTACK_POINT
        FROM MATCH_PLAYER_STATS s
        JOIN MATCH_INFO m ON s.MATCH_INFO_ID = m.MATCH_INFO_ID
        JOIN PLAYERS p ON s.SP_ID = p.SP_ID
        JOIN TEAMS t ON p.TEAM_NAME = t.TEAM_NAME
        WHERE m.SEASON = :season
        GROUP BY t.TEAM_NAME, p.NAME
        ORDER BY RANKING
    """, season=season)
    return [dict(zip([d[0] for d in cur.description], row)) for row in cur.fetchall()]

# 특정 선수 정보 조회
def get_player_info(cur, season, player_name):
    cur.execute("""
        SELECT 
            MAX(t.TEAM_NAME) AS TEAM,        -- 여러 행 중 하나만 가져오기
            p.NAME AS PLAYER,
            MAX(p.SP_ID) AS PLAYER_ID,
            MAX(p.POSITION) AS POSITION,
            MAX(p.IMAGE_URL) AS IMAGE,
            SUM(s.GOAL) AS GOALS,
            SUM(s.ASSIST) AS ASSISTS,
            SUM(s.GOAL + s.ASSIST) AS ATTACK_POINT,
            SUM(s.DRIBBLE_TRY) AS DRIBBLES,
            SUM(s.DRIBBLE_SUCCESS) AS DRIBBLE_SUCCESS,
            SUM(s.PASS_TRY) AS PASS_TRY,
            SUM(s.PASS_SUCCESS) AS PASS_SUCCESS,
            SUM(s.THROUGH_PASS_TRY) AS THROUGH_PASS_TRY,
            SUM(s.THROUGH_PASS_SUCCESS) AS THROUGH_PASS_SUCCESS,
            SUM(s.LONG_PASS_TRY) AS LONG_PASS_TRY,
            SUM(s.LONG_PASS_SUCCESS) AS LONG_PASS_SUCCESS,
            SUM(s.SHORT_PASS_TRY) AS SHORT_PASS_TRY,
            SUM(s.SHORT_PASS_SUCCESS) AS SHORT_PASS_SUCCESS,
            SUM(s.TACKLE_TRY) AS TACKLE_TRY,
            SUM(s.TACKLE_SUCCESS) AS TACKLE_SUCCESS,
            AVG(s.SP_RATING) AS AVERAGE_RATING,
            SUM(s.SHOOT) AS SHOOT, 
            SUM(s.EFFECTIVE_SHOOT) AS EFFECTIVE_SHOOT,
            SUM(s.DEFENDING) AS DEFENDING,
            SUM(s.INTERCEPT) AS INTERCEPT,
            SUM(s.BLOCK_TRY) AS BLOCK_TRY,
            SUM(s.BLOCK) AS BLOCK,
            SUM(s.YELLOW_CARDS) AS YELLOW_CARDS,
            SUM(s.RED_CARDS) AS RED_CARDS
        FROM MATCH_PLAYER_STATS s
        JOIN MATCH_INFO m ON s.MATCH_INFO_ID = m.MATCH_INFO_ID
        JOIN PLAYERS p ON s.SP_ID = p.SP_ID
        JOIN TEAMS t ON p.TEAM_NAME = t.TEAM_NAME
        WHERE p.NAME = :player_name
          AND m.SEASON = :season
        GROUP BY p.NAME
    """, season=season, player_name=player_name)
    return [dict(zip([d[0] for d in cur.description], row)) for row in cur.fetchall()]


# 특정 팀 정보 조회
def get_team_info(cur, season, team_name):
    cur.execute("""
        WITH team_stats AS (
            SELECT 
                t.TEAM_NAME AS TEAM,
                t.EMBLEM_URL,
                COUNT(*) AS MATCHES_PLAYED,
                SUM(CASE WHEN mi1.MATCH_RESULT = '승' THEN 1 ELSE 0 END) AS WINS,
                SUM(CASE WHEN mi1.MATCH_RESULT = '무' THEN 1 ELSE 0 END) AS DRAWS,
                SUM(CASE WHEN mi1.MATCH_RESULT = '패' THEN 1 ELSE 0 END) AS LOSSES,
                SUM(CASE WHEN mi1.MATCH_RESULT = '승' THEN 3
                         WHEN mi1.MATCH_RESULT = '무' THEN 1
                         ELSE 0 END) AS POINTS,
                SUM(mi1.GOAL_TOTAL) AS GOALS_FOR,
                SUM(mi2.GOAL_TOTAL) AS GOALS_AGAINST,
                SUM(mi1.OWN_GOAL) AS OWN_GOALS,
                SUM(mi1.SHOOT_TOTAL) AS SHOOTS,
                SUM(mi1.EFFECTIVE_SHOOT_TOTAL) AS EFFECTIVE_SHOOTS,
                SUM(mi1.TACKLE_TRY) AS TACKLE_TRIES,
                SUM(mi1.TACKLE_SUCCESS) AS TACKLE_SUCCESSES,
                SUM(mi1.YELLOW_CARDS) AS YELLOW_CARDS,
                SUM(mi1.RED_CARDS) AS RED_CARDS,
                LISTAGG(mi1.MATCH_RESULT, '') WITHIN GROUP (ORDER BY m.MATCH_DATE DESC) AS RECENT_RESULTS_ALL
            FROM MATCH_INFO mi1
            JOIN MATCH_INFO mi2
                ON mi1.MATCH_ID = mi2.MATCH_ID
               AND mi1.MATCH_INFO_ID != mi2.MATCH_INFO_ID
            JOIN MATCHES m
                ON mi1.MATCH_ID = m.MATCH_ID
            JOIN TEAMS t
                ON mi1.NICKNAME = t.NICKNAME
               AND mi1.SEASON = t.SEASON
            WHERE mi1.SEASON = :season
              AND t.TEAM_NAME = :team_name
            GROUP BY t.TEAM_NAME, t.EMBLEM_URL
        )
        SELECT
            TEAM,
            EMBLEM_URL,
            MATCHES_PLAYED,
            WINS,
            DRAWS,
            LOSSES,
            POINTS,
            GOALS_FOR,
            GOALS_AGAINST,
            (GOALS_FOR - GOALS_AGAINST) AS GOAL_DIFF,
            SHOOTS,
            EFFECTIVE_SHOOTS,
            TACKLE_TRIES,
            TACKLE_SUCCESSES,
            OWN_GOALS,
            YELLOW_CARDS,
            RED_CARDS,
            SUBSTR(RECENT_RESULTS_ALL, 1, 5) AS RECENT_5_RESULTS
        FROM team_stats
    """, season=season, team_name=team_name)
    return [dict(zip([d[0] for d in cur.description], row)) for row in cur.fetchall()]


def get_team_list(cur, season):
    cur.execute("""
        SELECT TEAM_NAME
        FROM TEAMS
        WHERE SEASON = :season
        ORDER BY TEAM_NAME
    """, season=season)
    return [dict(zip([d[0] for d in cur.description], row)) for row in cur.fetchall()]
