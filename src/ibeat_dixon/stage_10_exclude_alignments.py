
import os
import logging
import argparse
import shutil

import dbdicom as db

import utils.data


# This list is built manually 
EXCLUDE = [
    ['1128_030', 'Baseline', 'Dixon_1'], 
    ['2128_040', 'Followup', 'Dixon_1'],
    ['3128_012', 'Followup', 'Dixon_1'],
    ['3128_086', 'Baseline', 'Dixon_1'],
]


def run_ibeat(build):

    dir_input = os.path.join(build, 'dixon', 'stage_8_align_dixon_data')
    dir_png = os.path.join(build, 'dixon', 'stage_9_check_alignment')
    dir_output = os.path.join(build, 'dixon', 'stage_10_exclude_alignments')

    # Patients
    for site in ['Leeds', 'Bari', 'Turku', 'Bordeaux', 'Sheffield', 'Exeter']:
        db_input = os.path.join(dir_input, 'Patients', site)
        dir_png_site = os.path.join(dir_png, 'Patients', site)
        run_db(db_input, dir_png_site, dir_output)

    # Controls
    db_input = os.path.join(db_input, 'Controls') 
    dir_png_site = os.path.join(dir_png, 'Controls')
    run_db(db_input, dir_png_site, dir_output)

    
    

def run_db(db_input, dir_png_input, dir_output):

    db_dcm = os.path.join(dir_output, 'dcm')
    dir_png_output = os.path.join(dir_output, 'png')
    os.makedirs(db_dcm, exist_ok=True)
    os.makedirs(dir_png_output, exist_ok=True)

    all_input_series = db.series(db_input)

    # List of reference dixon series
    src = os.path.dirname(os.path.abspath(__file__))
    record = utils.data.dixon_record(src)
    
    for excl in EXCLUDE:
        try:
            excl_water = [db_input, excl[0], (excl[1], 0), (f'{excl[2]}_water', 0)]
            if excl_water in all_input_series:

                # Exclude pngs
                seq = excl[2]
                png_input = os.path.join(dir_png_input, f"{excl_water[1]}_{excl_water[2][0]}_{seq}.png")
                png_output = os.path.join(dir_png_output, f"{excl_water[1]}_{excl_water[2][0]}_{seq}.png")
                shutil.move(png_input, png_output)

                # Exclude dicoms
                seq_fixed = utils.data.dixon_series_desc(record, excl_water[1], excl_water[2][0])
                for seq in [seq_fixed, excl[2]]:
                    for map in ['water', 'fat', 'out_phase', 'in_phase']:
                        series_input = [db_input, excl_water[1], excl_water[2], (f'{seq}_{map}', 0)]
                        series_output = [db_dcm, excl_water[1], excl_water[2], (f'{seq}_{map}', 0)]
                        db.move(series_input, series_output)

                logging.info(f"Successfully excluded {excl}")
        except:
            logging.exception(f"Error copying {excl}")





if __name__=='__main__':

    BUILD = r'C:\Users\md1spsx\Documents\Data\iBEAt_Build'
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", type=str, default=BUILD, help="Build folder")
    args = parser.parse_args()

    dixon_build = os.path.join(args.build, 'dixon')
    os.makedirs(dixon_build, exist_ok=True)

    logging.basicConfig(
        filename=os.path.join(dixon_build, 'stage_10_exclude_alignments.log'),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    run_ibeat(args.build)
    
    logging.info(f"Finished stage_10_exclude_alignments")


