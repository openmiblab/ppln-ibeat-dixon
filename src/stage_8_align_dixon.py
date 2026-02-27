
import os
import logging
import argparse

from tqdm import tqdm
import numpy as np
import dbdicom as db
# from mdreg.ants import coreg, transform
from mdreg.elastix import coreg, transform
#from mdreg.skimage import coreg, transform

import utils.data


def run_ibeat(build):

    dir_moving = os.path.join(build, 'dixon', 'stage_5_clean_dixon_data')
    dir_coreg = os.path.join(build, 'dixon', 'stage_8_align_dixon_data')

    # Patients
    for site in ['Leeds', 'Bari', 'Turku', 'Bordeaux', 'Sheffield', 'Exeter']:
        db_moving = os.path.join(dir_moving, 'Patients', site)
        db_coreg = os.path.join(dir_coreg, 'Patients', site)
        run_db(db_moving, db_coreg)

    # Controls
    db_moving = os.path.join(dir_moving, 'Controls') 
    db_coreg = os.path.join(dir_coreg, 'Controls')
    run_db(db_moving, db_coreg)
    

def run_db(db_moving, db_coreg):

    os.makedirs(db_coreg, exist_ok=True)

    # Get all fat series in the source database
    all_moving_series = db.series(db_moving)
    all_water_series = [s for s in all_moving_series if s[3][0][-len('water'):]=='water']

    # List existing series so they can be skipped in the loop
    existing_result_series = db.series(db_coreg)

    # List of reference dixon series
    src = os.path.dirname(os.path.abspath(__file__))
    record = utils.data.dixon_record(src)

    # Loop over the fat series in the source database
    for series_moving_water in tqdm(all_water_series, desc='Aligning dixons'):

        # Patient and study IDs
        patient_id = series_moving_water[1]
        study_desc = series_moving_water[2][0]
        series_desc = series_moving_water[3][0]
        sequence = series_desc[:-len('_water')]

        # Get the other source series of the same sequence
        study_moving = [db_moving, patient_id, (study_desc, 0)]
        series_moving_ip = study_moving + [(f'{sequence}_in_phase', 0)]
        series_moving_op = study_moving + [(f'{sequence}_out_phase', 0)]
        series_moving_fat = study_moving + [(f'{sequence}_fat', 0)]

        # Define corresponding results series
        study_coreg = [db_coreg, patient_id, (study_desc, 0)]
        series_coreg_ip = study_coreg + [(f'{sequence}_in_phase', 0)]
        series_coreg_op = study_coreg + [(f'{sequence}_out_phase', 0)]
        series_coreg_water = study_coreg + [(f'{sequence}_water', 0)]
        series_coreg_fat = study_coreg + [(f'{sequence}_fat', 0)]

        # Skip computation if the results are already there
        if series_coreg_ip in existing_result_series:
            continue

        # Get the refence sequence and reference water series
        sequence_fixed = utils.data.dixon_series_desc(record, patient_id, study_desc)
        series_water_fixed = study_moving + [(f'{sequence_fixed}_water', 0)]

        try:

            # The fixed sequence does not need coregistering
            if sequence == sequence_fixed:
                db.copy(series_moving_ip, series_coreg_ip)
                db.copy(series_moving_op, series_coreg_op)
                db.copy(series_moving_fat, series_coreg_fat)
                db.copy(series_moving_water, series_coreg_water)
                continue
            
            # Read the volumes and reslice on fixed volume
            vol_fixed_water = db.volume(series_water_fixed, verbose=0)
            vol_moving_fat = db.volume(series_moving_fat, verbose=0).slice_like(vol_fixed_water)
            vol_moving_water = db.volume(series_moving_water, verbose=0).slice_like(vol_fixed_water)
            vol_moving_ip = db.volume(series_moving_ip, verbose=0).slice_like(vol_fixed_water)
            vol_moving_op = db.volume(series_moving_op, verbose=0).slice_like(vol_fixed_water)
            
            # Coregister water series with the reference
            spacing = vol_fixed_water.spacing.tolist()
            values_coreg_water, transfo = coreg(
                vol_moving_water.values.astype(float), 
                vol_fixed_water.values.astype(float), 
                # Elastix options
                spacing=spacing,
                FinalGridSpacingInPhysicalUnits="16",
                # skimage options
                # attachment=30,
            )

            # Apply the same transformation to the other series
            values_coreg_fat = transform(vol_moving_fat.values, transfo, spacing=spacing)
            values_coreg_ip = transform(vol_moving_ip.values, transfo, spacing=spacing)
            values_coreg_op = transform(vol_moving_op.values, transfo, spacing=spacing)

            # # Ensure positive (not used)
            # values_coreg_water[values_coreg_water < 0] = 0
            # values_coreg_fat[values_coreg_fat < 0] = 0
            # values_coreg_ip[values_coreg_ip < 0] = 0
            # values_coreg_op[values_coreg_op < 0] = 0

            # Save results 
            db.write_volume((values_coreg_fat, vol_fixed_water.affine), series_coreg_fat, ref=series_moving_fat)
            db.write_volume((values_coreg_water, vol_fixed_water.affine), series_coreg_water, ref=series_moving_water)
            db.write_volume((values_coreg_ip, vol_fixed_water.affine), series_coreg_ip, ref=series_moving_ip)
            db.write_volume((values_coreg_op, vol_fixed_water.affine), series_coreg_op, ref=series_moving_op)

            logging.info(f"Successfully aligned {series_moving_water[1:]}")

        except:

            logging.exception(f"Error aligning {series_moving_water[1:]}")





if __name__=='__main__':

    BUILD = r'C:\Users\md1spsx\Documents\Data\iBEAt_Build'
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", type=str, default=BUILD, help="Build folder")
    args = parser.parse_args()

    dixon_build = os.path.join(args.build, 'dixon')
    os.makedirs(dixon_build, exist_ok=True)

    logging.basicConfig(
        filename=os.path.join(dixon_build, 'stage_8_align_dixon.log'),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    run_ibeat(args.build)


