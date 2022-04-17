import pandas as pd
import json
import requests
import nba_api
import pprint

from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail

def get_shot_data(pid, year):
    shots = shotchartdetail.ShotChartDetail(
        team_id=0,
        player_id=pid,
        season_nullable=year,
        context_measure_simple= 'FGA',
        season_type_all_star='Regular Season'
    )
    dict_load = json.loads(shots.get_json())
    return pd.DataFrame(dict_load['resultSets'][0]['rowSet'], columns=dict_load['resultSets'][0]['headers'])


jordan = get_shot_data(893, '1996-97')
james = get_shot_data(2544, '2018-19')

df = jordan.append(james)

columns_to_drop = ['GRID_TYPE', 'GAME_ID', 'GAME_EVENT_ID', 'PLAYER_ID', 'TEAM_ID', 'TEAM_NAME', 'GAME_DATE',
                   'HTM', 'VTM', 'EVENT_TYPE']

df = df.drop(columns=columns_to_drop)

print(df.describe())
df.to_csv('dataset.csv', index=False)
