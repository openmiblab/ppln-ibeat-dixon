import os
import logging
import argparse

import numpy as np
from tqdm import tqdm
import dbdicom as db
from miblab_plot import mosaic_checkerboard

import utils.data



def run_ibeat(build):

    dir_coreg = os.path.join(build, 'dixon', 'stage_8_align_dixon_data')
    dir_mosaics = os.path.join(build, 'dixon', 'stage_9_check_alignment')

    db_coreg = os.path.join(dir_coreg, 'Controls')
    run_db(db_coreg, dir_mosaics)

    for site in ['Exeter', 'Leeds', 'Bari', 'Bordeaux', 'Sheffield', 'Turku']:
        db_coreg = os.path.join(dir_coreg, 'Patients', site)
        dir_mosaics = os.path.join(dir_mosaics, 'Patients', site)
        run_db(db_coreg, dir_mosaics)



def run_db(db_coreg, dir_mosaics):

    os.makedirs(dir_mosaics, exist_ok=True)

    # List of reference dixon series
    src = os.path.dirname(os.path.abspath(__file__))
    record = utils.data.dixon_record(src)

    # Get all coregistered water series
    all_coreg_series = db.series(db_coreg)
    all_coreg_water_series = [s for s in all_coreg_series if s[3][0][-5:]=='water']

    # Loop over the coregistered water series
    for series_coreg_water in tqdm(all_coreg_water_series, 'Displaying masks..'):

        # Patient and study IDs
        patient_id = series_coreg_water[1]
        study_desc = series_coreg_water[2][0]
        series_desc = series_coreg_water[3][0]
        sequence = series_desc[:-len('_water')]

        try:

            # Skip if it is the refence sequence
            sequence_fixed = utils.data.dixon_series_desc(record, patient_id, study_desc)
            if sequence == sequence_fixed:
                continue

            # Skip if file exists
            png_file = os.path.join(dir_mosaics, f'{patient_id}_{study_desc}_{sequence}.png')
            if os.path.exists(png_file):
                continue
            
            # Defined fixed and coregistered series
            study_coreg = [db_coreg, patient_id, (study_desc, 0)]
            series_fixed_water = study_coreg + [(f'{sequence_fixed}_water', 0)]
            series_coreg_water = study_coreg + [(f'{sequence}_water', 0)]       

            # Load the data
            val_fixed_water = db.volume(series_fixed_water, verbose=0).values
            val_coreg_water = db.volume(series_coreg_water, verbose=0).values

            # Build mosaics
            mosaic_checkerboard(val_fixed_water, val_coreg_water, png_file, normalize=True)

            logging.info(f'Successfully saved checkerboard for {patient_id}, {study_desc}, {sequence}')

        except:

            logging.exception(f'Error building checkerboard for {patient_id}, {study_desc}, {sequence}')



if __name__=='__main__':

    BUILD = r'C:\Users\md1spsx\Documents\Data\iBEAt_Build'
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", type=str, default=BUILD, help="Build folder")
    args = parser.parse_args()

    dixon_build = os.path.join(args.build, 'dixon')
    os.makedirs(dixon_build, exist_ok=True)

    logging.basicConfig(
        filename=os.path.join(dixon_build, 'stage_9_check_alignment.log'),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    run_ibeat(args.build)
