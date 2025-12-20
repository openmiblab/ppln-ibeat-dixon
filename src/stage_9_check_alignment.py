import os
import logging
import argparse

import numpy as np
from tqdm import tqdm
import dbdicom as db

from miblab_plot import mosaic_overlay

from utils.total_segmentator_class_maps import class_map


def run(build):
    run_site(build, 'Controls')
    for site in ['Exeter', 'Leeds', 'Bari', 'Bordeaux', 'Sheffield', 'Turku']:
        run_site(build, 'Patients', site=site)


def run_site(build, group, site=None):

    source = 'stage_8_aligned_dixon_data'
    results = 'stage_9_check_alignment'

    if group == 'Controls':
        source_db = os.path.join(build, 'dixon', source, group) 
        results_db = os.path.join(build, 'dixon', results, group)
        kidney_masks_db = os.path.join(build, 'kidneyvol', 'stage_3_edit', group)
        total_masks_db = os.path.join(build, 'totseg', 'stage_1_segment', group)
    else:
        source_db = os.path.join(build, 'dixon', source, group, site)
        results_db = os.path.join(build, 'dixon', results, group, site)
        kidney_masks_db = os.path.join(build, 'kidneyvol', 'stage_3_edit', group, site)
        total_masks_db = os.path.join(build, 'totseg', 'stage_1_segment', group, site)

    os.makedirs(results_db, exist_ok=True)

    kidney_class_map = {1: "kidney_left", 2: "kidney_right"}
    total_class_map = class_map['total_mr']

    # Get all water series in the source database
    all_source_series = db.series(source_db)
    all_water_series = [s for s in all_source_series if s[3][0][-5:]=='water']

    # Loop over the masks
    for water_series in tqdm(all_water_series, 'Displaying masks..'):

        # Patient and study IDs
        patient_id = water_series[1]
        study_desc = water_series[2][0]
        series_desc = water_series[3][0]
        sequence = series_desc[:-len('_water')]

        # Skip if file exists
        png_file = os.path.join(results_db, f'{patient_id}_{study_desc}_{sequence}.png')
        if os.path.exists(png_file):
             continue
        
        # Get mask and fat seriesx
        kidney_mask_series = [kidney_masks_db, patient_id, (study_desc, 0), ('kidney_masks', 0)]
        total_mask_series = [total_masks_db, patient_id, (study_desc, 0), ('total_mr', 0)]
        fat_series = [source_db, patient_id, (study_desc, 0), (f'{sequence}_fat', 0)]
        
        # Read mask volume
        kidney_mask_vol = db.volume(kidney_mask_series)
        total_mask_vol = db.volume(total_mask_series).slice_like(kidney_mask_vol)

        # Get image data - use water fraction so constant scaling can be used
        water = db.volume(water_series).slice_like(kidney_mask_vol).values
        fat = db.volume(fat_series).slice_like(kidney_mask_vol).values
        water_fraction = np.divide(water, fat + water, out=np.zeros_like(water, dtype=float), where=(fat + water) != 0)
    
        # Get masks
        rois = {}
        # for idx, roi in total_class_map.items():
        #     rois[roi] = (total_mask_vol.values==idx).astype(np.int16)
        for idx, roi in kidney_class_map.items():
            rois[roi] = (kidney_mask_vol.values==idx).astype(np.int16)

        # Build mosaic
        try:
            mosaic_overlay(water_fraction, rois, png_file, vmin=0, vmax=1, margin=[16,16,2], opacity=0.2)
            # mosaic_overlay(water, rois, png_file, margin=None, opacity=0.2)
        except:
            logging.exception(f"{patient_id}_{study_desc}_{sequence}: error building mosaic")


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

    run(args.build)
