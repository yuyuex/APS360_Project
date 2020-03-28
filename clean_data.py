
def remove_non_nba():
    # regular season match ids start with 2
    # Filter all those starting with 2


def separate_season():
    # The data contains 2 seasons
    # Separate 2017 and 2018 season
    # Look at season_id attribute



def bool_home_away():
    # Use the players dataset
    #Compare team_id with hometeam_id
    # Then use match_ids in the two datasets to take home/away boolean
    # from players dataset to team dataset


def pts_scored_received():
    # distinguish between  points scored and points received
    # look at final_hscore (final home score) and final_vscore
    # Do bool_home_away frist. That will help you filter out 
    #home and away scores


# adds 2 columns to player dataset, 
# ['start_datetime'] is the time the match took place
# ['rest_hours'] is the time between the current match and their last match in hours
def add_rest_time(team_dataset, player_dataset):
  import numpy as np

  #group and sort based on team_id
  team_dataset['start_datetime'] = pd.to_datetime(team_dataset.start_datetime)
  team_dataset = team_dataset.groupby('team_id').apply(pd.DataFrame.sort_values, ['start_datetime'], ascending=True)
  #rest period for each team is in hours
  team_dataset['rest_hours'] = team_dataset.start_datetime.diff().astype('timedelta64[h]')
  #fix the first entry of each team
  mask = team_dataset.team_id != team_dataset.team_id.shift(1)
  team_dataset['rest_hours'][mask] = np.nan

  #revert index
  team_dataset.reset_index(level=0, inplace=True,drop=True)

  player_dataset = player_dataset.merge(team_dataset[['match_id', 'team_id', 'start_datetime','rest_hours']], on=['match_id', 'team_id'], how = 'left')

  return team_dataset.dropna(subset=['rest_hours']), player_dataset.dropna(subset=['rest_hours'])
