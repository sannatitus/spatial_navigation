#%% Random selection of husbandry videos for creating an activity budget. Data was collected throughout 2022-2023 in two crabitats. This script selects dates for observation, equal amongst seasons. 
# Composed by Sanna, September 2023 s.titus@ucl.ac.uk
import os
from datetime import datetime, timedelta, time
import random
#%% Find all daily husbandry videos & separate file names into tub and tank crabitats
folder_path = r'X:\raw\CrabLab\CrabitatCam_daily'
file_names = os.listdir(folder_path)
tank_files = [file for file in file_names if 'tank' in file]
tub_files = [file for file in file_names if 'tub' in file]
#%% Extract .avis only
def is_avi(file):
    return file.endswith('.avi')
#%% Extract date and time from the file name
def extract_date_and_time(file_name, tub_tank):
    """
    Args: tub_tank = 'tub' or 'tank'
    """
    # Extract date and time part from the file name
    date_time_str = file_name[len(tub_tank):-4]  # Remove 'tank' or 'tub' and '.avi'
    
    # Split date and time using 'T' as separator
    date_time_parts = date_time_str.split('T')
    
    if len(date_time_parts) == 2:
        date_str, time_str = date_time_parts[0], date_time_parts[1]
        
        # Split time using underscores as separators
        time_parts = time_str.split('_')
        
        if len(time_parts) == 3:
            hour, minute, second_milliseconds = time_parts[0], time_parts[1], time_parts[2].split('.')[0]
            
        # Split date using '-' as separators
            date_parts = date_str.split('-')
            
            if len(date_parts) == 3:
                year, month, day = date_parts[0], date_parts[1], date_parts[2]
                return (year, month, day, hour, minute, second_milliseconds)
    
    return None

## Test date and time extraction for tubs and tank
tub_dates_and_times = []
for tub in tub_files:
    if is_avi(tub):
        date_time = extract_date_and_time(tub, 'tub')  # Use 'tub' as the parameter
        if date_time:
            tub_dates_and_times.append([date_time, tub])
'''print("Tub Dates and Times:")
print(tub_dates_and_times)'''

tank_dates_and_times = []
for tank in tank_files:
    if is_avi(tank):
        date_time = extract_date_and_time(tank, 'tank')  # Use 'tank' as the parameter
        if date_time:
            tank_dates_and_times.append([date_time, tank])
'''print("Tank Dates and Times:")
print(tank_dates_and_times)'''
#%% Organise by season
def categorize_season(month, day):
    if '02-05' <= f'{month}-{day}' <= '05-04':
        return 'Spring'
    elif '05-05' <= f'{month}-{day}' <= '08-04':
        return 'Summer'
    elif '08-05' <= f'{month}-{day}' <= '11-05':
        return 'Fall'
    elif '11-06' <= f'{month}-{day}' and f'{month}-{day}' <= '12-31':
        return 'Winter'
    elif '01-01' <= f'{month}-{day}' <= '02-04':
        return 'Winter'
    else:
        return 'Unknown'

tub_seasons = {'Spring': [], 'Summer': [], 'Fall': [], 'Winter': [], 'Unknown': []}
tank_seasons = {'Spring': [], 'Summer': [], 'Fall': [], 'Winter': [], 'Unknown': []}

for tub_date, tub in tub_dates_and_times:
    year, month, day = tub_date[0], tub_date[1], tub_date[2]
    season = categorize_season(month, day)
    tub_seasons[season].append(tub)
    print(f"File: {tub}, Date: {year}-{month}-{day}, Season: {season}")

for tank_date, tank in tank_dates_and_times:
    year, month, day = tank_date[0], tank_date[1], tank_date[2]
    season = categorize_season(month, day)
    tank_seasons[season].append(tank)
    print(f"File: {tank}, Date: {year}-{month}-{day}, Season: {season}")
    
# Test season categorisation
'''print("Tub Videos by Season:")
for season, videos in tub_seasons.items():
    print(f"{season}: {videos}")

print("\nTank Videos by Season:")
for season, videos in tank_seasons.items():
    print(f"{season}: {videos}")'''
# %% Organise by daytype (i.e., weekend days, no husbandry weekdays, husbandry weekdays)
def categorize_day_of_week(year, month, day):
    date = datetime(int(year), int(month), int(day))
    day_of_week = date.strftime('%A')
    if day_of_week in ['Saturday', 'Sunday']:
        return 'Weekend'
    elif day_of_week in ['Tuesday', 'Thursday']:
        return 'TuesdayThursday'
    else:
        return 'MondayWednesdayFriday'

tub_seasons = {'Spring': {'Weekend': [], 'TuesdayThursday': [], 'MondayWednesdayFriday': []},
               'Summer': {'Weekend': [], 'TuesdayThursday': [], 'MondayWednesdayFriday': []},
               'Fall': {'Weekend': [], 'TuesdayThursday': [], 'MondayWednesdayFriday': []},
               'Winter': {'Weekend': [], 'TuesdayThursday': [], 'MondayWednesdayFriday': []},
               'Unknown': {'Weekend': [], 'TuesdayThursday': [], 'MondayWednesdayFriday': []}}

tank_seasons = {'Spring': {'Weekend': [], 'TuesdayThursday': [], 'MondayWednesdayFriday': []},
                'Summer': {'Weekend': [], 'TuesdayThursday': [], 'MondayWednesdayFriday': []},
                'Fall': {'Weekend': [], 'TuesdayThursday': [], 'MondayWednesdayFriday': []},
                'Winter': {'Weekend': [], 'TuesdayThursday': [], 'MondayWednesdayFriday': []},
                'Unknown': {'Weekend': [], 'TuesdayThursday': [], 'MondayWednesdayFriday': []}}

for tub_date, tub in tub_dates_and_times:
    year, month, day = tub_date[0], tub_date[1], tub_date[2]
    season = categorize_season(month, day)
    day_of_week = categorize_day_of_week(year, month, day)
    tub_seasons[season][day_of_week].append(tub)

for tank_date, tank in tank_dates_and_times:
    year, month, day = tank_date[0], tank_date[1], tank_date[2]
    season = categorize_season(month, day)
    day_of_week = categorize_day_of_week(year, month, day)
    tank_seasons[season][day_of_week].append(tank)
#%% Randomly select files 
# For each season and crabitat, grab 3 videos from the weekend, 2 videos from non-husbandry weekdays (tuesday & Thursday), and 5 videos from husbandry weekdays
def random_select_files(file_list, num_files_to_select):
    if num_files_to_select >= len(file_list):
        return file_list
    return random.sample(file_list, num_files_to_select)

# Randomly select 3 files from the Weekend list for each season
selected_weekend_tub = {season: random_select_files(tub_seasons[season]['Weekend'], 3) for season in tub_seasons}
selected_weekend_tank = {season: random_select_files(tank_seasons[season]['Weekend'], 3) for season in tank_seasons}

# Randomly select 2 files from the TuesdayThursday (non-husbandry weekday) list for each season
selected_tue_thu_tub = {season: random_select_files(tub_seasons[season]['TuesdayThursday'], 2) for season in tub_seasons}
selected_tue_thu_tank = {season: random_select_files(tank_seasons[season]['TuesdayThursday'], 2) for season in tank_seasons}

# Randomly select 3 files from the MondayWednesdayFriday (husbandry weekday) list for each season
selected_mon_wed_fri_tub = {season: random_select_files(tub_seasons[season]['MondayWednesdayFriday'], 5) for season in tub_seasons}
selected_mon_wed_fri_tank = {season: random_select_files(tank_seasons[season]['MondayWednesdayFriday'], 5) for season in tank_seasons}

# Print randomly selected files
'''print("Randomly Selected Weekend Videos for Tubs:")
for season, files in selected_weekend_tub.items():
    print(f"{season}: {files}")

print("\nRandomly Selected Weekend Videos for Tanks:")
for season, files in selected_weekend_tank.items():
    print(f"{season}: {files}")

print("\nRandomly Selected TuesdayThursday Videos for Tubs:")
for season, files in selected_tue_thu_tub.items():
    print(f"{season}: {files}")

print("\nRandomly Selected TuesdayThursday Videos for Tanks:")
for season, files in selected_tue_thu_tank.items():
    print(f"{season}: {files}")

print("\nRandomly Selected MondayWednesdayFriday Videos for Tubs:")
for season, files in selected_mon_wed_fri_tub.items():
    print(f"{season}: {files}")

print("\nRandomly Selected MondayWednesdayFriday Videos for Tanks:")
for season, files in selected_mon_wed_fri_tank.items():
    print(f"{season}: {files}")'''
#%% Randomly select 4x 30-minute windows, within a range of tidal scenarios, for each randomly selected file^ 
# For the tank, select 4x 30-minute windows for the flow high, ebb high, ebb low, and flow low tides for each randomly selected file^
tank_time_ranges = {
    'flow high': [('17', '20')],
    'ebb high': [('08', '11'), ('20', '22')],
    'ebb low': [('11', '14')],
    'flow low': [('14', '17')],
}

# For the tub, select 4x 30-minute windows for the high (2x) and low (2x) tide periods
tub_time_ranges = {
    'high': [('08', '14'), ('20', '22')],
    'low': [('14', '20')]
}

def get_mins_hours(minutes):
    return (minutes//60,minutes%60)

def random_time_from_range(start, end):
    """
    Args: start (list) e.g. [hours, seconds] [7, 0] 
    Args: emd (list) e.g. [hours, seconds] [9, 30] 
    """
    start_time = (start[0] * 60)+start[1]
    end_time = (end[0] * 60)+end[1]
    v_length = end_time - start_time
    if v_length >= 0:
        start_mins = random.randint(0, v_length)
        return get_mins_hours(start_time+start_mins)
    else:
        return 'null'



def calculate_valid_time_periods(video_start_time, crabitat_type):
    if crabitat_type == 'tank':
        time_categories = tank_time_ranges
    elif crabitat_type == 'tub':
        time_categories = tub_time_ranges    
    else:
        raise ValueError("Invalid crabitat type")

    valid_time_periods = {}
    for time_category, time_ranges in time_categories.items():
        valid_time_periods[time_category] = []
        for start_hour, end_hour in time_ranges:
            if int(start_hour) < int(video_start_time):
                valid_start_hour = int(video_start_time)
            else:
                valid_start_hour = int(start_hour)

            if int(end_hour) > int(video_start_time) + 24:  # Handle the case when the end hour goes beyond midnight
                valid_end_hour = int(video_start_time) + 24
            else:
                valid_end_hour = int(end_hour)

            valid_time_periods[time_category].append((valid_start_hour, valid_end_hour))
    
    return valid_time_periods

def get_time_period(valid_time_periods, high_low):
    time_periods = valid_time_periods[high_low]
    random_range_iterator = random.randint(0, len(time_periods)-1)
    random_range = time_periods[random_range_iterator]
    selected_time_period = random_time_from_range([random_range[0], 0], [random_range[1]-1, 30])
    return selected_time_period

''' Original script without time limit for identifiying a selected period (time limit, functional script, below)
# Loop through each season, daytype, video, and time category for tub videos
for season, daytypes in tub_seasons.items():
    for day_type, files in daytypes.items():
        if day_type in ['Weekend', 'TuesdayThursday', 'MondayWednesdayFriday']:
            for file in files:
                if file in selected_weekend_tub[season] or file in selected_tue_thu_tub[season] or file in selected_mon_wed_fri_tub[season]:
                    video_start_time = extract_date_and_time(file, 'tub')[-3]  # Extract video start hour
                    valid_time_periods = calculate_valid_time_periods(video_start_time, 'tub')

                    # Randomly select 2 "high" time periods
                    for time_category in ['high'] * 2:
                        selected_time_period = get_time_period(valid_time_periods, 'high')
                        while selected_time_period == 'null':
                            selected_time_period = get_time_period(valid_time_periods, 'high')
                        
                        print(f"Season: {season}, Day Type: {day_type}, Video: {file}, Time Category: {time_category}, Selected Period: {selected_time_period[0]:02d}:{selected_time_period[1]:02d}")

                    # Randomly select 2 "low" time periods
                    for time_category in ['low'] * 2:
                        selected_time_period = get_time_period(valid_time_periods, 'low')
                        while selected_time_period == 'null':
                            selected_time_period = get_time_period(valid_time_periods, 'low')
                        
                        print(f"Season: {season}, Day Type: {day_type}, Video: {file}, Time Category: {time_category}, Selected Period: {selected_time_period[0]:02d}:{selected_time_period[1]:02d}")



# Loop through each season, daytype, video, and time category for tank videos
for season, daytypes in tank_seasons.items():
    for day_type, files in daytypes.items():
        if day_type in ['Weekend', 'TuesdayThursday', 'MondayWednesdayFriday']:
            for file in files: 
                    if file in selected_weekend_tank[season] or file in selected_tue_thu_tank[season] or file in selected_mon_wed_fri_tank[season]:
                        video_start_time = extract_date_and_time(file, 'tank')[-3] # Extract video start hour 
                        valid_time_periods = calculate_valid_time_periods(video_start_time, 'tank')

                        # Randomly select flow high time period
                        for time_category in ['flow high']:
                            selected_time_period=get_time_period(valid_time_periods, 'flow high')
                            while selected_time_period == 'null':
                                selected_time_period=get_time_period(valid_time_periods, 'flow high')
                            
                            print(f"Season: {season}, Day Type: {day_type}, Video: {file}, Time Category: {time_category}, Selected Period: {selected_time_period[0]:02d}:{selected_time_period[1]:02d}")

                        # Randomly select flow low time period 
                        for time_category in ['flow low']:
                            selected_time_period = get_time_period(valid_time_periods, 'flow low')
                            while selected_time_period == 'null':
                                selected_time_period = get_time_period(valid_time_periods, 'flow low')
                            
                            print(f"Season: {season}, Day Type: {day_type}, Video: {file}, Time Category: {time_category}, Selected Period: {selected_time_period[0]:02d}:{selected_time_period[1]:02d}")
                            
                        # Randomly select ebb high time period
                        for time_category in ['ebb high']:
                            selected_time_period=get_time_period(valid_time_periods, 'ebb high')
                            while selected_time_period == 'null':
                                selected_time_period=get_time_period(valid_time_periods, 'ebb high')
                            
                            print(f"Season: {season}, Day Type: {day_type}, Video: {file}, Time Category: {time_category}, Selected Period: {selected_time_period[0]:02d}:{selected_time_period[1]:02d}")

                        # Randomly select ebb low time period 
                        for time_category in ['ebb low']:
                            selected_time_period = get_time_period(valid_time_periods, 'ebb low')
                            while selected_time_period == 'null':
                                selected_time_period = get_time_period(valid_time_periods, 'ebb low')

                            print(f"Season: {season}, Day Type: {day_type}, Video: {file}, Time Category: {time_category}, Selected Period: {selected_time_period[0]:02d}:{selected_time_period[1]:02d}")
'''
time_limit = 360
collected_data = []

# Loop through each season, daytype, video, and time category for tub videos
for season, daytypes in tub_seasons.items():
    for day_type, files in daytypes.items():
        if day_type in ['Weekend', 'TuesdayThursday', 'MondayWednesdayFriday']:
            for file in files:
                if file in selected_weekend_tub[season] or file in selected_tue_thu_tub[season] or file in selected_mon_wed_fri_tub[season]:
                    video_start_time = extract_date_and_time(
                        file, 'tub')[-3]  # Extract video start hour
                    valid_time_periods = calculate_valid_time_periods(
                        video_start_time, 'tub')

                    # Randomly select 2 "high" time periods
                    for time_category in ['high'] * 2:
                        start_time = datetime.now()
                        selected_time_period = get_time_period(
                            valid_time_periods, 'high')

                        while selected_time_period == 'null':
                            current_time = datetime.now()
                            elapsed_time = current_time - start_time
                            if elapsed_time.total_seconds() >= time_limit:
                                print(
                                    "Time limit exceeded. No valid selection found.")
                                break  # Break out of the retry loop if time limit is exceeded

                            selected_time_period = get_time_period(
                                valid_time_periods, 'high')

                        if selected_time_period != 'null':
                            '''print(f"Season: {season}, Day Type: {day_type}, Video: {file}, Time Category: {time_category}, Selected Period: {selected_time_period[0]:02d}:{selected_time_period[1]:02d}")'''
                            collected_data.append(
                                [file, season, day_type, time_category, f"{selected_time_period[0]:02d}:{selected_time_period[1]:02d}"])

                    # Randomly select 2 "low" time periods
                    for time_category in ['low'] * 2:
                        start_time = datetime.now()
                        selected_time_period = get_time_period(
                            valid_time_periods, 'low')

                        while selected_time_period == 'null':
                            current_time = datetime.now()
                            elapsed_time = current_time - start_time
                            if elapsed_time.total_seconds() >= time_limit:
                                print(
                                    "Time limit exceeded. No valid selection found.")
                                break  # Break out of the retry loop if time limit is exceeded

                            selected_time_period = get_time_period(
                                valid_time_periods, 'low')

                        if selected_time_period != 'null':
                            '''print(f"Season: {season}, Day Type: {day_type}, Video: {file}, Time Category: {time_category}, Selected Period: {selected_time_period[0]:02d}:{selected_time_period[1]:02d}")'''
                            collected_data.append(
                                [file, season, day_type, time_category, f"{selected_time_period[0]:02d}:{selected_time_period[1]:02d}"])

# Loop through each season, daytype, video, and time category for tank videos
for season, daytypes in tank_seasons.items():
    for day_type, files in daytypes.items():
        if day_type in ['Weekend', 'TuesdayThursday', 'MondayWednesdayFriday']:
            for file in files:
                if file in selected_weekend_tank[season] or file in selected_tue_thu_tank[season] or file in selected_mon_wed_fri_tank[season]:
                     video_start_time = extract_date_and_time(
                         file, 'tank')[-3]  # Extract video start hour
                      valid_time_periods = calculate_valid_time_periods(
                           video_start_time, 'tank')

                       # Randomly select flow high time period
                       for time_category in ['flow high']:
                            start_time = datetime.now()
                            selected_time_period = get_time_period(
                                valid_time_periods, 'flow high')

                            while selected_time_period == 'null':
                                current_time = datetime.now()
                                elapsed_time = current_time - start_time
                                if elapsed_time.total_seconds() >= time_limit:
                                    print(
                                        "Time limit exceeded. No valid selection found.")
                                    break  # Break out of the retry loop if time limit is exceeded

                            selected_time_period = get_time_period(
                                valid_time_periods, 'flow high')

                        if selected_time_period != 'null':
                            '''print(f"Season: {season}, Day Type: {day_type}, Video: {file}, Time Category: {time_category}, Selected Period: {selected_time_period[0]:02d}:{selected_time_period[1]:02d}")'''
                            collected_data.append(
                                [file, season, day_type, time_category, f"{selected_time_period[0]:02d}:{selected_time_period[1]:02d}"])

                        # Randomly select flow low time period
                        for time_category in ['flow low']:
                            start_time = datetime.now()
                            selected_time_period = get_time_period(
                                valid_time_periods, 'flow low')

                            while selected_time_period == 'null':
                                current_time = datetime.now()
                                elapsed_time = current_time - start_time
                                if elapsed_time.total_seconds() >= time_limit:
                                    print(
                                        "Time limit exceeded. No valid selection found.")
                                    break  # Break out of the retry loop if time limit is exceeded

                            selected_time_period = get_time_period(
                                valid_time_periods, 'flow low')

                        if selected_time_period != 'null':
                            '''print(f"Season: {season}, Day Type: {day_type}, Video: {file}, Time Category: {time_category}, Selected Period: {selected_time_period[0]:02d}:{selected_time_period[1]:02d}")'''
                            collected_data.append(
                                [file, season, day_type, time_category, f"{selected_time_period[0]:02d}:{selected_time_period[1]:02d}"])

                        # Randomly select ebb high time period
                        for time_category in ['ebb high']:
                            start_time = datetime.now()
                            selected_time_period = get_time_period(
                                valid_time_periods, 'ebb high')

                            while selected_time_period == 'null':
                                current_time = datetime.now()
                                elapsed_time = current_time - start_time
                                if elapsed_time.total_seconds() >= time_limit:
                                    print(
                                        "Time limit exceeded. No valid selection found.")
                                    break  # Break out of the retry loop if time limit is exceeded

                            selected_time_period = get_time_period(
                                valid_time_periods, 'ebb high')

                        if selected_time_period != 'null':
                            '''print(f"Season: {season}, Day Type: {day_type}, Video: {file}, Time Category: {time_category}, Selected Period: {selected_time_period[0]:02d}:{selected_time_period[1]:02d}")'''
                            collected_data.append(
                                [file, season, day_type, time_category, f"{selected_time_period[0]:02d}:{selected_time_period[1]:02d}"])

                        # Randomly select ebb low time period
                        for time_category in ['ebb low']:
                            start_time = datetime.now()
                            selected_time_period = get_time_period(
                                valid_time_periods, 'ebb low')

                            while selected_time_period == 'null':
                                current_time = datetime.now()
                                elapsed_time = current_time - start_time
                                if elapsed_time.total_seconds() >= time_limit:
                                    print(
                                        "Time limit exceeded. No valid selection found.")
                                    break  # Break out of the retry loop if time limit is exceeded

                            selected_time_period = get_time_period(
                                valid_time_periods, 'ebb low')

                        if selected_time_period != 'null':
                            '''print(f"Season: {season}, Day Type: {day_type}, Video: {file}, Time Category: {time_category}, Selected Period: {selected_time_period[0]:02d}:{selected_time_period[1]:02d}")'''
                            collected_data.append(
                                [file, season, day_type, time_category, f"{selected_time_period[0]:02d}:{selected_time_period[1]:02d}"])
#%%
# Get organised into a csv
## If Errno 13 permission denied is thrown, delete the existing "selected_data.xlsx" file
df = pd.DataFrame(collected_data, columns=[
                  "video file", "season", "day type", "tide category", "selected observation period start"])

excel_file = r'C:/Users/Sanna/Desktop/selected_data.xlsx'
df.to_excel(excel_file, index=False)
print(f"Data saved to {excel_file}.")
#%%
# %%