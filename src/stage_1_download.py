"""
Automatic download of DIXON data from XNAT.
"""

import os
import logging
import argparse

import miblab_data as data



def leeds_patients(path):
    username, password = data.xnat_credentials()
    data.xnat_download_series(
        xnat_url="https://qib.shef.ac.uk",
        username=username,
        password=password,
        output_dir=path,
        project_id="BEAt-DKD-WP4-Leeds",
        subject_label="Leeds_Patients",
        attr="parameters/sequence",
        value="*fl3d2",
    )

def leeds_volunteers(path):
    username, password = data.xnat_credentials()
    data.xnat_download_series(
        xnat_url="https://qib.shef.ac.uk",
        username=username,
        password=password,
        output_dir=path,
        project_id="BEAt-DKD-WP4-Leeds",
        subject_label="Leeds_volunteer_repeatability_study",
        attr="parameters/sequence",
        value="*fl3d2",
    )

def leeds_setup(path):
    username, password = data.xnat_credentials()
    data.xnat_download_series(
        xnat_url="https://qib.shef.ac.uk",
        username=username,
        password=password,
        output_dir=path,
        project_id="BEAt-DKD-WP4-Leeds",
        subject_label="Leeds_setup_scans",
        attr=("parameters/sequence", "frames"), 
        value=("*fl3d2", 144),
    )

def bari_patients(path):
    username, password = data.xnat_credentials()
    data.xnat_download_series(
        xnat_url="https://qib.shef.ac.uk",
        username=username,
        password=password,
        output_dir=path,
        project_id="BEAt-DKD-WP4-Bari",
        subject_label="Bari_Patients",
        attr="series_description",
        value=[
            "T1w_abdomen_dixon_cor_bh", 
            "T1w_abdomen_post_contrast_dixon_cor_bh"
        ],
    )

def bari_volunteers(path):
    username, password = data.xnat_credentials()
    data.xnat_download_series(
        xnat_url="https://qib.shef.ac.uk",
        username=username,
        password=password,
        output_dir=path,
        project_id="BEAt-DKD-WP4-Bari",
        subject_label="Bari_Volunteers_Repeatability",
        attr="series_description",
        value=[
            "T1w_abdomen_dixon_cor_bh", 
        ],
    )


def sheffield_patients(path):
    username, password = data.xnat_credentials()
    data.xnat_download_series(
        xnat_url="https://qib.shef.ac.uk",
        username=username,
        password=password,
        output_dir=path,
        project_id="BEAt-DKD-WP4-Sheffield",
        #subject_label='IBE7128103', #tmp
        attr="series_description",
        value=[
            # Philips data
            'T1w_abdomen_dixon_cor_bh', 
            'T1w_abdomen_post_contrast_dixon_cor_bh',
            # GE data
            'WATER: T1_abdomen_dixon_cor_bh',
            'FAT: T1_abdomen_dixon_cor_bh',
            'InPhase: T1_abdomen_dixon_cor_bh',
            'OutPhase: T1_abdomen_dixon_cor_bh',
            'WATER: T1_abdomen_post_contrast_dixon_cor_bh',
            'FAT: T1_abdomen_post_contrast_dixon_cor_bh',
            'InPhase: T1_abdomen_post_contrast_dixon_cor_bh',
            'OutPhase: T1_abdomen_post_contrast_dixon_cor_bh',
        ],
    )

def turku_ge_patients(path):
    username, password = data.xnat_credentials()
    data.xnat_download_series(
        xnat_url="https://qib.shef.ac.uk",
        username=username,
        password=password,
        output_dir=path,
        project_id="BEAt-DKD-WP4-Turku",
        subject_label="Turku_Patients_GE",
        attr="series_description",
        value=[
            "WATER: T1_abdomen_dixon_cor_bh", 
            "FAT: T1_abdomen_dixon_cor_bh",
            "InPhase: T1_abdomen_dixon_cor_bh",
            "OutPhase: T1_abdomen_dixon_cor_bh",
            "WATER: T1_abdomen_post_contrast_dixon_cor_bh",
            "FAT: T1_abdomen_post_contrast_dixon_cor_bh",
            "InPhase: T1_abdomen_post_contrast_dixon_cor_bh",
            "OutPhase: T1_abdomen_post_contrast_dixon_cor_bh"
        ],
    )

def turku_ge_repeatability(path):
    username, password = data.xnat_credentials()
    data.xnat_download_series(
        xnat_url="https://qib.shef.ac.uk",
        username=username,
        password=password,
        output_dir=path,
        project_id="BEAt-DKD-WP4-Turku",
        subject_label="Turku_Volunteers_GE_Repeatability",
        attr="series_description",
        value=[
            "WATER: T1_abdomen_dixon_cor_bh", 
            "FAT: T1_abdomen_dixon_cor_bh",
            "InPhase: T1_abdomen_dixon_cor_bh",
            "OutPhase: T1_abdomen_dixon_cor_bh",
            "WATER: T1_abdomen_post_contrast_dixon_cor_bh",
            "FAT: T1_abdomen_post_contrast_dixon_cor_bh",
            "InPhase: T1_abdomen_post_contrast_dixon_cor_bh",
            "OutPhase: T1_abdomen_post_contrast_dixon_cor_bh"
        ],
    )

def turku_ge_setup(path):
    username, password = data.xnat_credentials()
    data.xnat_download_series(
        xnat_url="https://qib.shef.ac.uk",
        username=username,
        password=password,
        output_dir=path,
        project_id="BEAt-DKD-WP4-Turku",
        subject_label="Turku_GE_Setup_Tests",
        attr="series_description",
        value=[
            "WATER: T1_abdomen_dixon_cor_bh_iso", 
            "FAT: T1_abdomen_dixon_cor_bh_iso",
            "InPhase: T1_abdomen_dixon_cor_bh_iso",
            "OutPhase: T1_abdomen_dixon_cor_bh_iso",
            "WATER: T1_abdomen_dixon_cor_bh_npw_fip512",
            "FAT: T1_abdomen_dixon_cor_bh_npw_fip512",
            "InPhase: T1_abdomen_dixon_cor_bh_npw_fip512",
            "OutPhase: T1_abdomen_dixon_cor_bh_npw_fip512"
        ],
    )

def turku_philips_patients(path):
    username, password = data.xnat_credentials()
    data.xnat_download_series(
        xnat_url="https://qib.shef.ac.uk",
        username=username,
        password=password,
        output_dir=path,
        project_id="BEAt-DKD-WP4-Turku",
        subject_label="Turku_Patients_Philips",
        attr="series_description",
        value=[
            'T1W-abdomen-Dixon-coronal-BH', 
            'T1W-abdomen-Dixon-post-coronal-BH',
        ],
    )

def turku_philips_repeatability(path):
    username, password = data.xnat_credentials()
    data.xnat_download_series(
        xnat_url="https://qib.shef.ac.uk",
        username=username,
        password=password,
        output_dir=path,
        project_id="BEAt-DKD-WP4-Turku",
        subject_label="Turku_volunteer_repeatability_study",
        attr="series_description",
        value=[
            'T1W-abdomen-Dixon-coronal-BH', 
            'T1W-abdomen-Dixon-post-coronal-BH',
        ],
    )

def bordeaux_patients_baseline(path):
    username, password = data.xnat_credentials()
    data.xnat_download_series(
        xnat_url="https://qib.shef.ac.uk",
        username=username,
        password=password,
        output_dir=path,
        project_id="BEAt-DKD-WP4-Bordeaux",
        subject_label="Bordeaux_Patients_Baseline",
        # experiment_label='iBE-6128-005_baseline', # tmp
        attr="series_description",
        value=[
            "T1w_abdomen_dixon_cor_bh_opp", 
            "T1w_abdomen_dixon_cor_bh_in",
            "T1w_abdomen_dixon_cor_bh_F",
            "T1w_abdomen_dixon_cor_bh_W",
            "T1w_abdomen_post_contrast_dixon_cor_bh_opp",
            "T1w_abdomen_post_contrast_dixon_cor_bh_in",
            "T1w_abdomen_post_contrast_dixon_cor_bh_F",
            "T1w_abdomen_post_contrast_dixon_cor_bh_W"
        ],
    )

def bordeaux_volunteers(path):
    username, password = data.xnat_credentials()
    data.xnat_download_series(
        xnat_url="https://qib.shef.ac.uk",
        username=username,
        password=password,
        output_dir=path,
        project_id="BEAt-DKD-WP4-Bordeaux",
        subject_label="Bordeaux_Volunteers_Repeatability_Baseline",
        attr="series_description",
        value=[
            "T1w_abdomen_dixon_cor_bh_opp", 
            "T1w_abdomen_dixon_cor_bh_in",
            "T1w_abdomen_dixon_cor_bh_F",
            "T1w_abdomen_dixon_cor_bh_W",
            "T1w_abdomen_post_contrast_dixon_cor_bh_opp",
            "T1w_abdomen_post_contrast_dixon_cor_bh_in",
            "T1w_abdomen_post_contrast_dixon_cor_bh_F",
            "T1w_abdomen_post_contrast_dixon_cor_bh_W"
        ],
    )

def bordeaux_patients_followup(path):
    username, password = data.xnat_credentials()
    data.xnat_download_series(
        xnat_url="https://qib.shef.ac.uk",
        username=username,
        password=password,
        output_dir=path,
        project_id="BEAt-DKD-WP4-Bordeaux",
        subject_label="Bordeaux_Patients_Followup",
        attr="series_description",
        value=[
            "T1w_abdomen_dixon_cor_bh_opp", 
            "T1w_abdomen_dixon_cor_bh_in",
            "T1w_abdomen_dixon_cor_bh_F",
            "T1w_abdomen_dixon_cor_bh_W",
            "T1w_abdomen_post_contrast_dixon_cor_bh_opp",
            "T1w_abdomen_post_contrast_dixon_cor_bh_in",
            "T1w_abdomen_post_contrast_dixon_cor_bh_F",
            "T1w_abdomen_post_contrast_dixon_cor_bh_W"
        ],
    )

def exeter_patients_baseline(path):
    username, password = data.xnat_credentials()
    data.xnat_download_series(
        xnat_url="https://qib.shef.ac.uk",
        username=username,
        password=password,
        output_dir=path,
        project_id="BEAt-DKD-WP4-Exeter",
        subject_label="Exeter_Patients_Baseline",
        attr="series_description",
        value=[
            "T1w_abdomen_dixon_cor_bh", 
            "T1w_abdomen_dixon_cor_bh_opp", 
            "T1w_abdomen_dixon_cor_bh_in",
            "T1w_abdomen_dixon_cor_bh_F",
            "T1w_abdomen_dixon_cor_bh_W",
            "T1w_abdomen_post_contrast_dixon_cor_bh",
            "T1w_abdomen_post_contrast_dixon_cor_bh_opp",
            "T1w_abdomen_post_contrast_dixon_cor_bh_in",
            "T1w_abdomen_post_contrast_dixon_cor_bh_F",
            "T1w_abdomen_post_contrast_dixon_cor_bh_W"
        ],
    )

def exeter_patients_followup(path):
    username, password = data.xnat_credentials()
    data.xnat_download_series(
        xnat_url="https://qib.shef.ac.uk",
        username=username,
        password=password,
        output_dir=path,
        project_id="BEAt-DKD-WP4-Exeter",
        subject_label="Exeter_Patients_Followup",
        attr="series_description",
        value=[
            "T1w_abdomen_dixon_cor_bh_opp", 
            "T1w_abdomen_dixon_cor_bh_in",
            "T1w_abdomen_dixon_cor_bh_F",
            "T1w_abdomen_dixon_cor_bh_W",
            "T1w_abdomen_post_contrast_dixon_cor_bh_opp",
            "T1w_abdomen_post_contrast_dixon_cor_bh_in",
            "T1w_abdomen_post_contrast_dixon_cor_bh_F",
            "T1w_abdomen_post_contrast_dixon_cor_bh_W"
        ],
    )

def exeter_volunteers(path):
    username, password = data.xnat_credentials()
    data.xnat_download_series(
        xnat_url="https://qib.shef.ac.uk",
        username=username,
        password=password,
        output_dir=path,
        project_id="BEAt-DKD-WP4-Exeter",
        subject_label="Exeter_Volunteer",
        attr="series_description",
        value=[
            "T1w_abdomen_dixon_cor_bh", 
            "T1w_abdomen_dixon_cor_bh_opp", 
            "T1w_abdomen_dixon_cor_bh_in",
            "T1w_abdomen_dixon_cor_bh_F",
            "T1w_abdomen_dixon_cor_bh_W",
            "T1w_abdomen_post_contrast_dixon_cor_bh",
            "T1w_abdomen_post_contrast_dixon_cor_bh_opp",
            "T1w_abdomen_post_contrast_dixon_cor_bh_in",
            "T1w_abdomen_post_contrast_dixon_cor_bh_F",
            "T1w_abdomen_post_contrast_dixon_cor_bh_W"
        ],
    )

def exeter_setup(path):
    username, password = data.xnat_credentials()
    data.xnat_download_series(
        xnat_url="https://qib.shef.ac.uk",
        username=username,
        password=password,
        output_dir=path,
        project_id="BEAt-DKD-WP4-Exeter",
        subject_label="Exeter_setup_scans",
        attr="series_description",
        value=[
            "T1w_abdomen_dixon_cor_bh", 
            "T1w_abdomen_dixon_cor_bh_opp", 
            "T1w_abdomen_dixon_cor_bh_in",
            "T1w_abdomen_dixon_cor_bh_F",
            "T1w_abdomen_dixon_cor_bh_W",
            "T1w_abdomen_post_contrast_dixon_cor_bh",
            "T1w_abdomen_post_contrast_dixon_cor_bh_opp",
            "T1w_abdomen_post_contrast_dixon_cor_bh_in",
            "T1w_abdomen_post_contrast_dixon_cor_bh_F",
            "T1w_abdomen_post_contrast_dixon_cor_bh_W"
        ],
    )

def run(path):
    leeds_patients(path)
    bari_patients(path)
    sheffield_patients(path)
    turku_philips_patients(path)
    bordeaux_patients_baseline(path)
    bordeaux_patients_followup(path)
    exeter_patients_baseline(path)
    exeter_patients_followup(path)

    bari_volunteers(path)
    leeds_setup(path)
    leeds_volunteers(path)
    bordeaux_volunteers(path)
    exeter_volunteers(path)
    exeter_setup(path)
    turku_philips_repeatability(path)
    turku_ge_repeatability(path)
    turku_ge_setup(path)


if __name__=='__main__':

    BUILD = r'C:\Users\md1spsx\Documents\Data\iBEAt_Build\dixon'
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", type=str, default=BUILD, help="Build folder")
    args = parser.parse_args()

    path = os.path.join(args.build, 'stage_1_download')
    os.makedirs(path, exist_ok=True)

    logging.basicConfig(
        filename=os.path.join(args.build, 'stage_1_download.log'),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
   
    run(path)


