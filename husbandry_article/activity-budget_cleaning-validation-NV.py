# Python script for creating an activity budget for Afruca tangeri, from instantaneous observations of two SWC crabitats (110 tank & tub) throughout 2022-2023.
# Composed by s.titus@ucl.ac.uk 1 October 2024
# Directions to run in SSH (SannaDesk, cmd)
    # ssh -J stitus@ssh.swc.ucl.ac.uk stitus@zoo-db
    # ssh hpc-gw1
    # conda activate crab-activity
    # cd /ceph/zoo/users/stitus/husbandry-article/
    ## if line endings are in windows (CRLF) not linux (LF), can change in VS code or this: tr -d '\r' <activity-budget_cleaning-validation-NV-ssh.sh> activity-budget_cleaning-validation-NV-ssh-linux.sh
    # sbatch activity-budget_cleaning-validation-NV-ssh.sh ##submits the job 
    # squeue -u stitus

import pandas as pd
import os
import datetime
####################################################################
file_path = r'/ceph/zoo/users/stitus/husbandry-article/husbandry-article_selected-data.xlsx'
# df = pd.read_excel(file_path, sheet_name='data')
df = pd.read_excel(file_path, sheet_name='data', engine='openpyxl') # this engine is necessary for the xlsb. the subset is standard xlsx 
####################################################################
## optional sanity check
##df.head()
# DATA CLEANING (fill human visible column, format time, save the order for df integrity, assign high/low A/B tide type for the tub)

# Fill any NaNs in the 'human visible?' column with 'N'
df['human visible?'] = df['human visible?'].fillna('N')

# Function to normalize 'selected observation period start' column
def normalize_observation_period_start(df):
    def format_time(value):
        if isinstance(value, datetime.time):
            return value.strftime("%H:%M:%S")
        if isinstance(value, str):
            return value if len(value) == 8 else value + ":00"
        return value

    df['selected observation period start'] = df['selected observation period start'].apply(format_time)
    return df

# Normalize the 'selected observation period start' column
df = normalize_observation_period_start(df)

# Add a column to store the original row order prior to tide category creation 
df['original_order'] = df.index

# Step 1: Assign Tide Categories and Types
def assign_tide_categories_and_types(df):
    updated_rows = []  # Placeholder for updated rows

    # Group by video file and tide category
    grouped = df.groupby(['video file', 'tide category'])

    for (video_file, tide_category), group in grouped:
        # Check if it's tub data for high/low A and B
        if 'tub' in video_file:
            tide_type = 'high' if 'high' in tide_category else 'low'
            group['tide type'] = tide_type  # Assign tide type
            
            # Sort by observation period start to rank them properly
            group = group.sort_values(by='selected observation period start')

            # Rank the observations within each tide category
            group['tide category rank'] = group.groupby('selected observation period start').ngroup() + 1

            # Assign A or B based on the rank (1 = A, 2 = B)
            group['tide category'] = tide_category + " " + group['tide category rank'].map({1: 'A', 2: 'B'})

        else:  # For tank data, just assign high or low
            tide_type = 'high' if 'high' in tide_category else 'low'
            group['tide type'] = tide_type
            group['tide category'] = tide_category  # Keep the original category

        # Append the updated group to the list
        updated_rows.append(group)

    # Concatenate all the updated rows into a single DataFrame
    updated_df = pd.concat(updated_rows, ignore_index=True)

    # Drop the extra 'tide category rank' column 
    updated_df = updated_df.drop(columns=['tide category rank'], errors='ignore')

    return updated_df

# Apply the function to assign tide categories and types
df_with_tide_categories_and_types = assign_tide_categories_and_types(df)

# Step 2: Identify and Adjust 0-Start Observation Periods
def shift_observation_minutes(df):
    # Group by video file and tide category
    grouped = df.groupby(['video file', 'tide category'])

    for (video_file, tide_category), group in grouped:
        # If an observation window starts with 0, shift the whole group by +1
        if group['observation minute from start'].min() == 0:
            df.loc[group.index, 'observation minute from start'] += 1

    # Check and remove rows with observation minute 31
    df = df[df['observation minute from start'] <= 30]
    
    return df

# Apply the observation minute shifting function
df_with_tide_categories_and_types = shift_observation_minutes(df_with_tide_categories_and_types)

# Step 3: Sort by video file, tide category, and observation minute from start
df_with_tide_categories_and_types = df_with_tide_categories_and_types.sort_values(by=['video file', 'tide category', 'observation minute from start'])

# Step 4: Reorder Columns to place 'tide type' after 'tide category'
columns_order = list(df_with_tide_categories_and_types.columns)
columns_order.remove('tide type')
tide_category_index = columns_order.index('tide category') + 1
columns_order.insert(tide_category_index, 'tide type')

# Reorder the DataFrame
df_with_tide_categories_and_types = df_with_tide_categories_and_types[columns_order]

# Drop the 'original_order' column after sorting
df_with_tide_categories_and_types = df_with_tide_categories_and_types.drop(columns=['original_order'])

# Save the cleaned DataFrame to Excel
file_name, file_extension = os.path.splitext(file_path)
output_path_1 = f"{file_name}_cleaned{file_extension}" 
df_with_tide_categories_and_types.to_excel(output_path_1, index=False)
print(f"Cleaned dataset saved to: {output_path_1}")
# DATA VALIDATION (_cleaned) (30obs/crabID)

# Check that each crab ID has exactly 30 rows in each observation window
def validate_crab_id_rows(df):
    # Group by video file, tide category, and crab ID
    grouped = df.groupby(['video file', 'tide category', 'crab ID'])

    # Create a list to hold any validation issues
    validation_issues = []

    # Iterate through the groups and check row counts
    for (video_file, tide_category, crab_id), group in grouped:
        count = len(group)
        if count != 30:
            validation_issues.append({
                'video file': video_file,
                'tide category': tide_category,
                'crab ID': crab_id,
                'row count': count
            })

    return validation_issues

# Perform validation
validation_results = validate_crab_id_rows(df_with_tide_categories_and_types)

# Output the validation results
if validation_results:
    print("Validation issues found:")
    for issue in validation_results:
        print(f"Crab ID: {issue['crab ID']} in {issue['video file']} - {issue['tide category']} has {issue['row count']} rows.")
else:
    print("All crab IDs have the correct number of rows (30) in each observation window.")

# Save validation summary to Excel
if validation_results:
    # Convert validation issues into a DataFrame
    validation_summary_df = pd.DataFrame(validation_results)
    
    # Specify the path for saving
    validation_summary_path = f"{file_name}_cleaned_validation.xlsx"
    
    # Save the DataFrame to Excel
    validation_summary_df.to_excel(validation_summary_path, index=False)
    print(f"Validation summary saved to: {validation_summary_path}")
else:
    no_issues_df = pd.DataFrame({'Message': ['No validation issues found.']})
    no_issues_df.to_excel(f"{file_name}_cleaned_validation.xlsx", index=False)
    print("All crab IDs have the correct number of rows (30) in each observation window.")


# CALCULATE NV PRESENCE (assign correct sexes, and maintain column/row order with 30 rows per NV crab (i.e., full obs window)) 
def calculate_nv_crabs_with_debugging(df):
    complete_data = pd.DataFrame()  # Final DataFrame to accumulate validated data

    # Group by video file, tide category, and observation start period
    grouped = df.groupby(['video file', 'tide category', 'selected observation period start'])

    for (video_file, tide_category, obs_start), group in grouped:
        present_population = group['present population'].iloc[0]
        present_males = group['present males'].iloc[0]
        present_females = group['present females'].iloc[0]

        observed_males = group.loc[group['sex'] == 'm', 'crab ID'].nunique()
        observed_females = group.loc[group['sex'] == 'f', 'crab ID'].nunique()

        num_nv_males = max(0, present_males - observed_males)
        num_nv_females = max(0, present_females - observed_females)

        print(f"Processing: {video_file}, {tide_category}, {obs_start}")
        print(f"Expected NV males: {num_nv_males}, Expected NV females: {num_nv_females}")

        # Check if adding the NV data will result in the expected row count
        nv_rows = pd.DataFrame()  # Temp DataFrame for current NV rows

        for i in range(1, num_nv_males + 1):
            for minute in range(1, 31):
                nv_male_row = {
                    'video file': video_file,
                    'crabitat': group['crabitat'].iloc[0],
                    'season': group['season'].iloc[0],
                    'day type': group['day type'].iloc[0],
                    'tide category': tide_category,
                    'tide type': group['tide type'].iloc[0],
                    'present population': present_population,
                    'present sex ratio': group['present sex ratio'].iloc[0],
                    'present males': present_males,
                    'present females': present_females,
                    'selected observation period start': obs_start,
                    'real time': group['real time'].iloc[0],
                    'observation minute from start': minute,
                    'crab ID': f'NV_m{i}',
                    'sex': 'm',
                    'instantaneous behaviour': 'NV',
                    'human visible?': 'N'
                }
                nv_rows = pd.concat([nv_rows, pd.DataFrame([nv_male_row])], ignore_index=True)

        for i in range(1, num_nv_females + 1):
            for minute in range(1, 31):
                nv_female_row = {
                    'video file': video_file,
                    'crabitat': group['crabitat'].iloc[0],
                    'season': group['season'].iloc[0],
                    'day type': group['day type'].iloc[0],
                    'tide category': tide_category,
                    'tide type': group['tide type'].iloc[0],
                    'present population': present_population,
                    'present sex ratio': group['present sex ratio'].iloc[0],
                    'present males': present_males,
                    'present females': present_females,
                    'selected observation period start': obs_start,
                    'real time': group['real time'].iloc[0],
                    'observation minute from start': minute,
                    'crab ID': f'NV_f{i}',
                    'sex': 'f',
                    'instantaneous behaviour': 'NV',
                    'human visible?': 'N'
                }
                nv_rows = pd.concat([nv_rows, pd.DataFrame([nv_female_row])], ignore_index=True)

        # Concatenate observed data and NV rows
        full_group_data = pd.concat([group, nv_rows], ignore_index=True)
        expected_rows = present_population * 30
        actual_rows = full_group_data.shape[0]

        print(f"Expected total rows for {video_file} {tide_category}: {expected_rows}, Actual: {actual_rows}")

        # Append to final DataFrame only if row count matches expectation
        if actual_rows == expected_rows:
            complete_data = pd.concat([complete_data, full_group_data], ignore_index=True)
        else:
            print(f"Skipping {video_file} {tide_category} due to row mismatch.")

    # Sort and reorder columns
    column_order = ['video file', 'crabitat', 'season', 'day type', 'tide category', 'tide type', 'present population',
                    'present sex ratio', 'present males', 'present females', 'selected observation period start',
                    'real time', 'observation minute from start', 'crab ID', 'sex', 'instantaneous behaviour', 'human visible?']

    complete_data = complete_data[column_order]
    return complete_data

# Run the debugging function
df_with_nv_debugged = calculate_nv_crabs_with_debugging(df_with_tide_categories_and_types)

# Save the output to a new file
output_path_2 = f"{file_name}_cleaned+NV{file_extension}"
df_with_nv_debugged.to_excel(output_path_2, index=False)
print(f"Cleaned dataframe including NVs saved to: {output_path_2}")

def validate_data(df_with_nv_debugged):
    # Create a list to store validation results
    validation_results = []
    # Keep track of duplicates
    duplicates_list = []

    # Group by video file and tide category
    grouped = df_with_nv_debugged.groupby(['video file', 'tide category'])

    for (video_file, tide_category), group in grouped:
        # Calculate expected number of rows
        present_population = group['present population'].iloc[0]
        expected_rows = present_population * 30
        
        # Calculate actual rows directly from the group size
        actual_rows = group.shape[0]

        missing_rows = expected_rows - actual_rows

        # Append validation result to the list
        validation_results.append({
            'video file': video_file,
            'tide category': tide_category,
            'expected rows': expected_rows,
            'actual rows': actual_rows,
            'missing rows': missing_rows
        })

        # Check for duplicates based on relevant columns
        duplicate_columns = ['selected observation period start', 'observation minute from start', 'crab ID']
        duplicates = group[group.duplicated(subset=duplicate_columns, keep=False)]  # Get all duplicate rows

        # If duplicates exist, append to duplicates list
        if not duplicates.empty:
            duplicates_list.append({
                'video file': video_file,
                'tide category': tide_category,
                'duplicates': duplicates.to_dict(orient='records')  # Store duplicate rows
            })

        # Check for NaN values in critical columns
        for column in ['video file', 'tide category', 'present population']:
            if group[column].isnull().any():
                print(f"NaN values found in column '{column}' for video file {video_file}, tide category {tide_category}.")

        # Check observation minute range
        if not ((group['observation minute from start'] >= 1).all() and (group['observation minute from start'] <= 30).all()):
            print(f"Observation minutes out of expected range (1-30) for video file {video_file}, tide category {tide_category}.")

    # Create a DataFrame from the results list
    validation_results_df_with_nv = pd.DataFrame(validation_results)

    # Filter out results with 0 missing rows
    validation_results_df_with_nv = validation_results_df_with_nv[validation_results_df_with_nv['missing rows'] != 0]

    # Save duplicates if any
    duplicates_df_with_nv = pd.DataFrame(duplicates_list)

    # Display the validation summary
    print(validation_results_df_with_nv)
    print("Duplicates found:")
    print(duplicates_df_with_nv)

    if validation_results_df_with_nv:
        validation_summary_df.to_excel(f"{file_name}_cleaned+NV_validation.xlsx", index=False)
        print(f"Validation summary saved to: {validation_summary_path}")
    else:
        no_issues_df = pd.DataFrame({'Message': ['No validation issues found.']})
        no_issues_df.to_excel(f"{file_name}_cleaned+NV_validation.xlsx", index=False)
        print("All crab IDs have the correct number of rows (30) in each observation window.")

    if duplicates_df_with_nv:
        duplicates_list.to_excel(f"{file_name}_cleaned+NV_duplication.xlsx", index=False)
        print(f"Duplication summary saved to: {validation_summary_path}")
    else:
        no_issues_df = pd.DataFrame({'Message': ['No duplicates found.']})
        no_issues_df.to_excel(f"{file_name}_cleaned+NV_duplicates.xlsx", index=False)
        print("No crab IDs possess duplicates.")

    return validation_results_df_with_nv, duplicates_df_with_nv
