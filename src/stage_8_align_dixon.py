
import os
import logging
import argparse

from tqdm import tqdm
import numpy as np
import dbdicom as db
# from mdreg.ants import coreg, transform
from mdreg.elastix import coreg, transform
# from mdreg.skimage import coreg, transform

import utils.data


def run(build):
    run_site(build, 'Controls')
    for site in ['Leeds', 'Bari', 'Turku', 'Bordeaux', 'Sheffield', 'Exeter']:
        run_site(build, 'Patients', site=site)
    

def run_site(build, group, site=None):

    # Define database paths
    source = 'test_stage_5_clean_dixon_data'
    results = 'stage_8_aligned_dixon_data'

    if group == 'Controls':
        source_db = os.path.join(build, 'dixon', source, group) 
        results_db = os.path.join(build, 'dixon', results, group)
    else:
        source_db = os.path.join(build, 'dixon', source, group, site)
        results_db = os.path.join(build, 'dixon', results, group, site)

    os.makedirs(results_db, exist_ok=True)

    # Get all fat series in the source database
    all_source_series = db.series(source_db)
    all_fat_series = [s for s in all_source_series if s[3][0][-3:]=='fat']

    # List existing series so they can be skipped in the loop
    existing_result_series = db.series(results_db)

    # List of reference dixon series
    src = os.path.dirname(os.path.abspath(__file__))
    record = utils.data.dixon_record(src)

    # Loop over the fat series in the source database
    for source_series_fat in tqdm(all_fat_series, desc='Aligning dixons'):

        # Patient and study IDs
        patient_id = source_series_fat[1]
        study_desc = source_series_fat[2][0]
        series_desc = source_series_fat[3][0]
        sequence = series_desc[:-4]

        # Get the other source series of the same sequence
        source_study = [source_db, patient_id, (study_desc, 0)]
        source_series_ip = source_study + [(f'{sequence}_in_phase', 0)]
        source_series_op = source_study + [(f'{sequence}_out_phase', 0)]
        source_series_water = source_study + [(f'{sequence}_water', 0)]

        # Define corresponding results series
        result_study = [results_db, patient_id, (study_desc, 0)]
        result_series_ip = result_study + [(f'{sequence}_in_phase', 0)]
        result_series_op = result_study + [(f'{sequence}_out_phase', 0)]
        result_series_water = result_study + [(f'{sequence}_water', 0)]
        result_series_fat = result_study + [(f'{sequence}_fat', 0)]

        # Skip computation if the results are already there
        if result_series_ip in existing_result_series:
            continue

        # Get the refence sequence and reference fat series
        fixed_sequence = utils.data.dixon_series_desc(record, patient_id, study_desc)
        fixed_series_water = source_study + [(f'{fixed_sequence}_water', 0)]

        # Any error happens in the computations, log and move on to the next
        try:

            # The fixed sequence does not need coregistering
            if sequence == fixed_sequence:
                db.copy(source_series_ip, result_series_ip)
                db.copy(source_series_op, result_series_op)
                db.copy(source_series_fat, result_series_fat)
                db.copy(source_series_water, result_series_water)
                continue

            # Read the fixed fat volume
            fixed_vol = db.volume(fixed_series_water)

            # Read the other volumes and reslice (in case geometries are not matched)
            moving_vol_fat = db.volume(source_series_fat).slice_like(fixed_vol)
            moving_vol_water = db.volume(source_series_water).slice_like(fixed_vol)
            moving_vol_ip = db.volume(source_series_ip).slice_like(fixed_vol)
            moving_vol_op = db.volume(source_series_op).slice_like(fixed_vol)
            
            # Coregister fat series with the reference
            spacing = fixed_vol.spacing.tolist()
            coreg_values_water, transfo = coreg(
                moving_vol_water.values.astype(float), 
                fixed_vol.values.astype(float), 
                # Elastix options
                spacing=spacing,
                FinalGridSpacingInPhysicalUnits="16",
                # skimage options
                # attachment=30,
            )

            # Apply the same transformation to the other series
            coreg_values_fat = transform(moving_vol_fat.values, transfo, spacing=spacing)
            coreg_values_ip = transform(moving_vol_ip.values, transfo, spacing=spacing)
            coreg_values_op = transform(moving_vol_op.values, transfo, spacing=spacing)

            # Save results 
            db.write_volume((coreg_values_fat, fixed_vol.affine), result_series_fat, ref=source_series_fat)
            db.write_volume((coreg_values_water, fixed_vol.affine), result_series_water, ref=source_series_water)
            db.write_volume((coreg_values_ip, fixed_vol.affine), result_series_ip, ref=source_series_ip)
            db.write_volume((coreg_values_op, fixed_vol.affine), result_series_op, ref=source_series_op)

        except:

            logging.exception(f"Error aligning {source_series_fat}")





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

    run(args.build)


