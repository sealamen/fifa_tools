import requests
from urllib.parse import urlparse

def get_all_players(api_key):
    url = "https://open.api.nexon.com/static/fconline/meta/spid.json"
    return requests.get(urlparse(url).geturl(), headers={"Authorization": api_key}).json()

def get_match_type(api_key):
    url = "https://open.api.nexon.com/static/fconline/meta/matchtype.json"
    return requests.get(urlparse(url).geturl(), headers={"Auth  orization": api_key}).json()

def get_user_access_id(api_key, nickname):
    url = f"https://open.api.nexon.com/fconline/v1/id?nickname={nickname}"
    return requests.get(urlparse(url).geturl(), headers={"x-nxopen-api-key": api_key}).json()["ouid"]

def get_user_match_ids(api_key, ouid, match_type):
    url = f"https://open.api.nexon.com/fconline/v1/user/match?ouid={ouid}&matchtype={match_type}"
    return requests.get(urlparse(url).geturl(), headers={"x-nxopen-api-key": api_key }).json()

def get_match_detail(api_key, match_id):
    url = f"https://open.api.nexon.com/fconline/v1/match-detail?matchid={match_id}"
    return requests.get(urlparse(url).geturl(), headers={"x-nxopen-api-key": api_key}).json()
