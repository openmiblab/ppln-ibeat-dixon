import os
import argparse
import logging

import dbdicom as db
from utils.db_plot import db_mosaic


def run(build):
    
    run_site(build, 'Controls')
    for site in ['Exeter', 'Leeds', 'Bari', 'Bordeaux', 'Sheffield', 'Turku']:
        run_site(build, 'Patients', site)


def run_site(build, group, site=None):

    resultspath = os.path.join(build, 'stage_6_check')
    os.makedirs(resultspath, exist_ok=True)
    summary = os.path.join(resultspath, 'summary.txt')

    if group == 'Controls':
        datapath = os.path.join(build, 'stage_5_clean_dixon_data', group) 
        csv = os.path.join(resultspath, f'{group}.csv')
        png = os.path.join(resultspath, f'{group}.png')
    else:
        datapath = os.path.join(build, 'stage_5_clean_dixon_data', group, site)
        csv = os.path.join(resultspath, f'{group}_{site}.csv')
        png = os.path.join(resultspath, f'{group}_{site}.png')
    
    # Build csv

    db.to_csv(datapath, csv)

    # Build txt summary

    patients = db.patients(datapath)
    studies = db.studies(datapath)
    series = db.series(datapath)

    nr_studies = {}
    for patient in patients:
        n = len([s for s in studies if s[:2]==patient[:2]])
        if n in nr_studies:
            nr_studies[n] += 1
        else:
            nr_studies[n] = 1

    nr_pre_series = {}
    nr_post_series = {}
    for study in studies:
        series_in_study = [s for s in series if s[:3]==study[:3]]

        pre = [s for s in series_in_study if 'post_contrast' not in s[3][0]]
        n_pre = len(pre)
        if n_pre in nr_pre_series:
            nr_pre_series[n_pre] += 1
        else:
            nr_pre_series[n_pre] = 1

        post = [s for s in series_in_study if 'post_contrast' in s[3][0]]
        n_post = len(post)
        if n_post in nr_post_series:
            nr_post_series[n_post] += 1
        else:
            nr_post_series[n_post] = 1

    with open(summary, 'a') as f:

        f.write('\n')
        f.write(f"{group} ({'all sites' if site is None else site})\n")

        f.write('\n')
        f.write(f"  {len(patients)} patients with {len(studies)} studies\n")
        f.write('\n')
        for n in sorted(nr_studies.keys()):
            f.write(f"    {nr_studies[n]} with {n} studies\n")

        f.write('\n')
        f.write(f"  {len(studies)} studies with {len(series)} series\n")
        f.write('\n')
        for n in sorted(nr_pre_series.keys()):
            f.write(f"    {nr_pre_series[n]} with {n} pre-contrast series\n")
        f.write('\n')
        for n in sorted(nr_post_series.keys()):
            f.write(f"    {nr_post_series[n]} with {n} post-contrast series\n")


    # Build png mosaic

    series_desc = [s[-1][0] for s in series]
    series_fat = [s for i, s in enumerate(series) if series_desc[i][-3:]=='fat']

    if os.path.exists(png):
        return
    
    db_mosaic(series_fat, png, title="Fat maps")


# def run(build):

#     datapath = os.path.join(build, 'stage_5_clean_dixon') 
#     resultspath = os.path.join(build, 'stage_5_check')
#     os.makedirs(resultspath, exist_ok=True)
#     resultsfile = os.path.join(resultspath, 'dixon.csv')
#     db.to_csv(datapath, resultsfile)


if __name__=='__main__':

    BUILD = r'C:\Users\md1spsx\Documents\Data\iBEAt_Build\dixon'
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", type=str, default=BUILD, help="Build folder")
    args = parser.parse_args()

    os.makedirs(args.build, exist_ok=True)

    logging.basicConfig(
        filename=os.path.join(args.build, 'stage_6_check_log.txt'),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    run(args.build)