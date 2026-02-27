"""
Compute water-dominance masks from data that have fat and water maps
"""

import os
import logging
import argparse
import subprocess
import time

from tqdm import tqdm
import numpy as np
import dbdicom as db
from miblab_dl import fatwater


def run(build, cache=None):
    compute(build, 'Controls', cache=cache)
    for site in ['Exeter', 'Leeds', 'Bari', 'Bordeaux', 'Sheffield', 'Turku']:
        compute(build, 'Patients', site=site, cache=cache)

def compute(build, group, site=None, cache=None):

    # Define site paths
    if group == 'Controls':
        datapath = os.path.join(build, 'stage_2_data', group) 
        resultspath = os.path.join(build, 'stage_4_compute_fatwater', group)
    else:
        datapath = os.path.join(build, 'stage_2_data', group, site)
        resultspath = os.path.join(build, 'stage_4_compute_fatwater', group, site)
    os.makedirs(resultspath, exist_ok=True)

    # Get all out_phase series
    series = db.series(datapath)
    series_out_phase = [s for s in series if s[3][0][-9:]=='out_phase']

    # List existing series so they can be skipped in the loop
    existing_series = db.series(resultspath)

    # Loop over the out_phase series
    for series_op in tqdm(series_out_phase, desc='Computing fat-water maps'):

        # Patient and study IDs
        patient = series_op[1]
        study = series_op[2][0]

        # Remove '_out_phase' suffix from series description
        sequence = series_op[3][0][:-10] 

        # Skip if the source series has a computed fat map already
        fat_series = series_op[:3] + [(f'{sequence}_fat', 0)]
        if fat_series in series:
            continue

        # Define output series
        fat_series = [resultspath, patient, (study, 0), (f'{sequence}_fat', 0)]
        water_series = [resultspath, patient, (study, 0), (f'{sequence}_water', 0)]

        # Skip if the output already exists
        if fat_series in existing_series:
            continue

        # Get in_phase series
        series_ip = series_op[:3] + [(f'{sequence}_in_phase', 0)]

        # Read the in-phase and opposed-phase data
        try:
            op = db.volume(series_op)
            ip = db.volume(series_ip)
        except Exception as e:
            logging.error(f"Patient {patient} - error reading I-O {sequence}: {e}")
            continue

        if op.shape != ip.shape:
            logging.error(f"Patient {patient} - shape mismatch I-O {sequence}: {op.shape} vs {ip.shape}")
            continue

        # Compute fat and water images
        try:
            fat, water = fatwater(op.values, ip.values, cache=cache)
        except Exception as e:
            logging.error(f"Error predicting fat-water maps for {patient} {sequence}: {e}")
            continue
        
        # Save results in DICOM
        db.write_volume((fat, op.affine), fat_series, ref=series_op, Manufacturer='miblab')
        db.write_volume((water, op.affine), water_series, ref=series_op, Manufacturer='miblab')




if __name__=='__main__':

    BUILD = r'C:\Users\md1spsx\Documents\Data\iBEAt_Build\dixon'
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", type=str, default=BUILD, help="Build folder")
    parser.add_argument("--cache", type=str, default=None, help="Cache folder")
    args = parser.parse_args()

    os.makedirs(args.build, exist_ok=True)

    logging.basicConfig(
        filename=os.path.join(args.build, 'stage_4_compute_fatwater.log'),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    run(args.build, args.cache)


