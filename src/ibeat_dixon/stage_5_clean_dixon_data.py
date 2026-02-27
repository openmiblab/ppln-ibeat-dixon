
import os
import logging
import argparse

from tqdm import tqdm
import dbdicom as db


def run(build):
    run_site(build, 'Controls')
    for site in ['Exeter', 'Leeds', 'Bari', 'Bordeaux', 'Sheffield', 'Turku']:
        run_site(build, 'Patients', site=site)


def run_site(build, group, site=None):

    # Define site paths
    if group == 'Controls':
        source_db = os.path.join(build, 'stage_2_data', group) 
        computed_db = os.path.join(build, 'stage_4_compute_fatwater', group)
        clean_db = os.path.join(build, 'stage_5_clean_dixon_data', group)
    else:
        source_db = os.path.join(build, 'stage_2_data', group, site)
        computed_db = os.path.join(build, 'stage_4_compute_fatwater', group, site)
        clean_db = os.path.join(build, 'stage_5_clean_dixon_data', group, site)
    os.makedirs(clean_db, exist_ok=True)

    # Get all source out_phase series
    source_series = db.series(source_db)
    source_series_op = [s for s in source_series if s[3][0][-9:]=='out_phase']

    # Get all exisiting clean data series
    dest_series = db.series(clean_db)

    # Loop over the out_phase series
    for source_op in tqdm(source_series_op, desc='Creating clean dixon database'):

        # Get source study and sequence name
        patient = source_op[1]
        study_desc = source_op[2][0]
        sequence = source_op[3][0][:-10] # Remove _out_phase suffix

        # Define other source series
        study = source_op[:3]
        source_ip = study + [(f'{sequence}_in_phase', 0)]
        source_fat = study + [(f'{sequence}_fat', 0)]
        source_water = study + [(f'{sequence}_water', 0)]

        # Exceptions: in two cases, the fat series
        # has a different study UID than water/in phase/opposed phase
        # Not clear why - fixing manually here.
        if patient=='6128_005':
            source_fat = [source_db, patient, (study_desc, 0), (f'{sequence}_fat', 0)]
        elif (patient=='7128_103') and (sequence=='Dixon_post_contrast_1'):
            source_fat = [source_db, patient, (study_desc, 0), (f'{sequence}_fat', 0)]
        # For one patient the fat water swap had not been executed.
        elif (patient=='2128_040') and (study_desc=='Baseline'):
            source_fat = study + [(f'{sequence}_water', 0)]
            source_water = study + [(f'{sequence}_fat', 0)]

        # If fat and water are not in the source, they are computed
        if source_water not in source_series:
            study = [computed_db, patient, (study_desc, 0)]
            source_fat = study + [(f'{sequence}_fat', 0)]
            source_water = study + [(f'{sequence}_water', 0)]           

        # Define destinations
        study = [clean_db, patient, (study_desc, 0)]
        dest_ip = study + [(f'{sequence}_in_phase', 0)]
        dest_op = study + [(f'{sequence}_out_phase', 0)]
        dest_water = study + [(f'{sequence}_water', 0)]
        dest_fat = study + [(f'{sequence}_fat', 0)]

        # If the destination series already exist, skip
        if dest_op in dest_series:
            continue

        # Copy all sources to destinations
        try:
            db.copy(source_op, dest_op)
            db.copy(source_ip, dest_ip)
            db.copy(source_fat, dest_fat)
            db.copy(source_water, dest_water)
        except Exception as e:
            logging.error(f"Patient {study[1]} - error copying {sequence}: {e}")



if __name__=='__main__':

    BUILD = r'C:\Users\md1spsx\Documents\Data\iBEAt_Build\dixon'
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", type=str, default=BUILD, help="Build folder")
    args = parser.parse_args()

    os.makedirs(args.build, exist_ok=True)

    logging.basicConfig(
        filename=os.path.join(args.build, 'stage_5_clean_dixon_data_log.txt'),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    run(args.build)


