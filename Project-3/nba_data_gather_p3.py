import pandas as pd
import json
import requests
import nba_api
import pprint

from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail

from nba_api.stats.static import players

# Find players by full name.
# players.find_players_by_full_name('james')

# Find players by first name.
# players.find_players_by_first_name('lebron')

# Find players by last name.
# players.find_players_by_last_name('^(james|love)$')

# Get all players.
player_list = players.get_players()
# print(player_list, len(player_list))

from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import playerprofilev2
rodman = commonplayerinfo.CommonPlayerInfo(player_id=23).available_seasons.get_data_frame()
rodman2 = playerprofilev2.PlayerProfileV2(player_id=23).season_totals_regular_season.get_data_frame()
# print(rodman2)

'''
If I were able to extract all player id's, then I could run a loop that would get the regular season totals into a df.
From there, I could combine all the player df's into one large data frame.  This would be my dataset.
'''

print(player_list[1])
print(player_list[1]['id'])
print(len(player_list))

df = pd.DataFrame()
for i, num in enumerate(player_list):
    print(player_list[i]['last_name'])
    player_profile = playerprofilev2.PlayerProfileV2(player_id=player_list[i]['id']).season_totals_regular_season.get_data_frame()
    df = df.append(player_profile)

print(df.describe())
df.to_csv('nba_player_dataset.csv', index=False)