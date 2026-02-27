
import os
import logging
import argparse

from tqdm import tqdm
import dbdicom as db
import numpy as np


def run(build):
    
    edit_turku_philips(build, 'Controls')
    edit_turku_philips(build, 'Patients')


def edit_turku_philips(build, group):

    # Define site paths
    dir = 'stage_5_clean_dixon_data'

    if group == 'Controls':
        database = os.path.join(build, dir, group)
    else:
        database = os.path.join(build, dir, group, 'Turku')

    # Get all source out_phase series
    source_series = db.series(database)
    source_series_op = [s for s in source_series if s[3][0][-9:]=='out_phase']

    # Loop over the out_phase series
    for source_op in tqdm(source_series_op, desc='Editing DICOM header'):
    
        # Define in-phase series
        sequence = source_op[3][0][:-10] # Remove _out_phase suffix
        source_ip = source_op[:3] + [(f'{sequence}_in_phase', 0)]

        # Edit echo times for Turku Philips data
        vars = ['Manufacturer', 'InstitutionName', 'StationName']
        vals = db.unique(vars, source_ip)

        if ((vals['Manufacturer'][0] == 'Philips Medical Systems') and \
            (vals['InstitutionName'][0] == 'TURKU PET centre') and \
            (vals['StationName'][0] == 'PETMR')):

            # Read TE and TR from private tags
            te, tr = db.values(source_ip, (0x2001, 0x1025), (0x2005, 0x1030))
            te_vals = [
                float(te[0].split('/')[0]),
                float(te[0].split('/')[1]),
            ]
            te_op = min(te_vals)  # Opposed phase
            te_ip = max(te_vals)  # In phase

            # Write TE and TR to standard tag
            try:
                db.edit(source_op, {'EchoTime': np.full(te.shape, te_op), 'RepetitionTime': np.full(tr.shape, tr[0])})
                db.edit(source_ip, {'EchoTime': np.full(te.shape, te_ip), 'RepetitionTime': np.full(tr.shape, tr[0])})
            except:
                logging.exception(f"Patient {source_ip[1]} - error editing EchoTime for {sequence}")




if __name__=='__main__':

    BUILD = r'C:\Users\md1spsx\Documents\Data\iBEAt_Build\dixon'
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", type=str, default=BUILD, help="Build folder")
    args = parser.parse_args()

    os.makedirs(args.build, exist_ok=True)

    logging.basicConfig(
        filename=os.path.join(args.build, 'stage_7_edit_header.log'),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    run(args.build)