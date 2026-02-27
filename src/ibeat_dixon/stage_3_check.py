import os
import logging
import csv
from datetime import datetime
import argparse

from tqdm import tqdm
import matplotlib
matplotlib.use('Agg')

import dbdicom as db
import pydicom

from utils.constants import SITE_IDS
from utils.db_plot import db_mosaic





def calculate_age(birth_date_str, current_date_str):
    """
    Calculates age in years based on two dates in YYYYMMDD format.

    Args:
        birth_date_str (str or int): Birth date in YYYYMMDD format.
        current_date_str (str or int): Current/reference date in YYYYMMDD format.

    Returns:
        int: Age in years.
    """
    # Convert to strings if passed as integers
    birth_date_str = str(birth_date_str)
    current_date_str = str(current_date_str)

    # Parse the dates
    birth_date = datetime.strptime(birth_date_str, "%Y%m%d")
    current_date = datetime.strptime(current_date_str, "%Y%m%d")

    # Calculate age
    age = current_date.year - birth_date.year
    # Adjust if current date is before the birthday this year
    if (current_date.month, current_date.day) < (birth_date.month, birth_date.day):
        age -= 1

    return age



def check_fatwater_swap(build, site):

    datapath = os.path.join(build, 'stage_2_data')
    data_qc_path = os.path.join(build, 'stage_3_check')
    os.makedirs(data_qc_path, exist_ok=True)
    
    if site == 'Controls':
        sitedatapath = os.path.join(datapath, "Controls") 
        sitepngpath = os.path.join(data_qc_path, f'controls_fat_water_swap.png')
    else:
        sitedatapath = os.path.join(datapath, "Patients", site) 
        sitepngpath = os.path.join(data_qc_path, f'{site}_fat_water_swap.png')

    # Skip if the site has no data yet.
    if not os.path.exists(sitedatapath):
        return

    # Skip if the file already exists.
    if os.path.exists(sitepngpath):
        print(f'Skipping: file {sitepngpath} already exists..')
        return

    # Get out-phase series
    series = db.series(sitedatapath)
    series_desc = [s[-1][0] for s in series]
    series_fat = [s for i, s in enumerate(series) if series_desc[i][-3:]=='fat']

    # If there are no fat images there is nothing to do
    if series_fat == []:
        return
    
    db_mosaic(series_fat, sitepngpath, title="Fat maps")
    



def fatwater_swap_record_template(build, site):
    """
    Template json file for manual recording of fat water swaps.

    Fat-water swaps should be manually recorded in this template by 
    setting the default value of 0 to 1. 
    
    The completed record should 
    be preserved in the data folder to be used in analyses.
    """

    datapath = os.path.join(build, 'stage_2_data')
    data_qc_path = os.path.join(build, 'stage_3_check')
    os.makedirs(data_qc_path, exist_ok=True)

    if site == 'Controls':
        sitedatapath = os.path.join(datapath, "Controls")
    else:
        sitedatapath = os.path.join(datapath, "Patients", site)

    csv_file = os.path.join(data_qc_path, 'fat_water_swap_record.csv')

    # If the file already exists, don't run it again
    if os.path.exists(csv_file):
        return

    swap_record = [
        ['Site', 'Patient', 'Study', 'Series', 'Swapped']
    ]
     
    if os.path.exists(sitedatapath):
        for series in tqdm(db.series(sitedatapath), desc=f"Building record for {site}"):
            patient_id = series[1]
            study_desc = series[2][0]
            series_desc = series[3][0]
            if series_desc[-3:]=='fat':
                row = [site, patient_id, study_desc, series_desc[:-4], 0]
                swap_record.append(row)

    # Write to CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(swap_record)


def count_dixons(build, site):

    datapath = os.path.join(build, 'stage_2_data')
    data_qc_path = os.path.join(build, 'stage_3_check')
    os.makedirs(data_qc_path, exist_ok=True)

    if site == 'Controls':
        sitedatapath = os.path.join(datapath, "Controls")
    else:
        sitedatapath = os.path.join(datapath, "Patients", site)

    # If the file already exists, don't run it again
    csv_file = os.path.join(data_qc_path, 'dixon_data.csv')
    if os.path.exists(csv_file):
        print('dixon_number_record.csv' + ' already exists. Skipping this step.')
        return
    
    # Build data
    data = [
        ['Site', 'Patient', 'Study', 'Dixon', 'Dixon_post_contrast', 'Use']
    ]
     
    for study in tqdm(db.studies(sitedatapath), desc=f"Counting dixons for {site}"):
        patient_id = study[1]
        study_desc = study[2][0]
        series = db.series(study)
        series_desc = [s[3][0] for s in series] 
        row = [site, patient_id, study_desc, 0, 0, '']
        for desc in ['Dixon', 'Dixon_post_contrast']:
            cnt=0
            while f'{desc}_{cnt+1}_out_phase' in series_desc:
                cnt+=1
            if desc=='Dixon':
                row[3] = f'{cnt}'
            else:
                row[4] = f'{cnt}'
        # Use the last post-contrast if available, else the last precontrast.
        row[5] = f'Dixon_post_contrast_{row[4]}' if cnt>0 else f'Dixon_{row[3]}'
        data.append(row)

    # Save as csv
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def demographics(build, group, site=None):

    datapath = os.path.join(build, 'stage_2_data')
    data_qc_path = os.path.join(build, 'stage_3_check')
    os.makedirs(data_qc_path, exist_ok=True)

    if group == 'Controls':
        sitedatapath = os.path.join(datapath, group)
    else:
        sitedatapath = os.path.join(datapath, group, site)

    # If the file already exists, don't run it again
    csv_file = os.path.join(data_qc_path, 'demographics.csv')
    if os.path.exists(csv_file):
        print('demographics.csv' + ' already exists. Skipping this step.')
        return
    
    # Build data
    data = [
        ['Patient', 'Study', 'StudyDate', 'BirthDate', 'Sex', 'Age', 'Height', 'Weight']
    ]
     
    for study in tqdm(db.studies(sitedatapath), desc=f"Summarising demographics"):
        patient_id = study[1]
        study_desc = study[2][0]
        if site is not None:
            if patient_id[:4] not in SITE_IDS[site]:
                continue
        first_file = db.files(study)[0]
        ds = pydicom.dcmread(first_file)
        row = [patient_id, study_desc]
        for field in ['StudyDate', 'PatientBirthDate', 'PatientSex', 'PatientAge', 'PatientSize', 'PatientWeight']:
            if field in ds:
                row.append(ds[field].value)
            # If Age is empty, try to derive it from the dates
            elif field == 'PatientAge':
                if ('PatientBirthDate' in ds) and ('StudyDate' in ds):
                    try:
                        age = calculate_age(ds['PatientBirthDate'].value, ds['StudyDate'].value)
                        row.append(age)
                    except:
                        row.append('Unknown')
                else:
                    row.append('Unknown')
            else:
                row.append('Unknown')
        data.append(row)

    # Save as csv
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)




    # Save as csv
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def run(build):
    
    count_dixons(build, 'Exeter')
    fatwater_swap_record_template(build, 'Controls')
    check_fatwater_swap(build, 'Controls')
    count_dixons(build, 'Controls')
    demographics(build, 'Controls')


if __name__=='__main__':

    BUILD = r'C:\Users\md1spsx\Documents\Data\iBEAt_Build\dixon'
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", type=str, default=BUILD, help="Build folder")
    args = parser.parse_args()

    logging.basicConfig(
        filename=os.path.join(args.build, 'stage_3_check.log'),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    run(args.build)
   
