import argparse
import os
import logging


import stage_1_download
import stage_2_data_harmonization
import stage_3_check
import stage_4_compute_fatwater
import stage_5_clean_dixon_data
import stage_6_check
import stage_7_edit_header
import stage_8_align_dixon
import stage_9_check_alignment


if __name__=='__main__':

    BUILD = r'C:\Users\md1spsx\Documents\Data\iBEAt_Build'
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", type=str, default=BUILD, help="Build folder")
    args = parser.parse_args()

    dixon_build = os.path.join(args.build, 'dixon')
    os.makedirs(dixon_build, exist_ok=True)

    logging.basicConfig(
        filename=os.path.join(dixon_build, 'pipeline.log'),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    stage_1_download.run(args.build)
    stage_2_data_harmonization.run(args.build)
    stage_3_check.run(args.build)
    stage_4_compute_fatwater.run(args.build)
    stage_5_clean_dixon_data.run(args.build)
    stage_6_check.run(args.build)
    stage_7_edit_header.run(args.build)
    stage_8_align_dixon.run(args.build)
    stage_9_check_alignment.run(args.build)