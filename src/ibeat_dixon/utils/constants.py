IBEAT = {
    "BEAt-DKD-WP4-Leeds": [
        "Leeds_Patients",
        "Leeds_volunteer_repeatability_study",
        "Leeds_setup_scans",
    ],
    "BEAt-DKD-WP4-Bari": [
        "Bari_Patients",
        "Bari_Volunteers_Repeatability",
    ],
    "BEAt-DKD-WP4-Bordeaux": [
        "Bordeaux_Patients_Baseline",
        "Bordeaux_Patients_Followup",
        "Bordeaux_Volunteers_Repeatability_Baseline",
    ],
    "BEAt-DKD-WP4-Exeter": [
        "Exeter_Patients_Baseline",
        "Exeter_Patients_Followup",
        "Exeter_Volunteers_Repeatability",
        "Exeter_setup_scans",
    ],
    "BEAt-DKD-WP4-Turku": [
        "Turku_GE_Setup_Tests",
        "Turku_Patients_GE",
        "Turku_Patients_Philips",
        "Turku_Volunteers_GE_Repeatability",
        "Turku_volunteer_repeatability_study",
    ],
    "BEAt-DKD-WP4-Sheffield": [
        None,
        # one subject per participant - find all
    ],
}

SITE_IDS = {
    'Bari': ['1128'],
    'Leeds': ['4128'],
    'Bordeaux': ['2128', '6128'],
    'Exeter': ['3128'],
    'Leeds': ['4128'],
    'Sheffield': ['7128'],
    'Turku': ['5128', '6128'],
}



pat_id = {

    # Leeds setup
    'Leeds_MR_VOL_006': '4128_C06',
    'Leeds_MR_VOL_007': '4128_C07',
    'Leeds_MR_VOL_008': '4128_C08',
    'Leeds_MR_VOL_009': '4128_C09',
    'Leeds_MR_VOL_012': '4128_C12',
    'Leeds_MR_VOL_013': '4128_C13',
    'Leeds_MR_VOL_014': '4128_C14',
    'Leeds_MR_VOL_016': '4128_C16',
    'Leeds_MR_VOL_019': '4128_C19',
    'Leeds_MR_VOL_020': '4128_C20',

    # Leeds repeatability
    'Leeds_REP_VOL_001': '4128_C21',
    'Leeds_REP_VOL_002': '4128_C22',
    'Leeds_REP_VOL_003': '4128_C23',
    'Leeds_REP_VOL_004': '4128_C24',
    'REP_VOL_004': '4128_C24',
    'Leeds_REP_VOL_005': '4128_C25',
    'Leeds_Rep_Vol_005': '4128_C25',

    # Turku volunteers
    'iBE-5128-251_V1': ('5128_C05', 'Visit1'),
    'iBE-5128-252_V1': ('5128_C05', 'Visit2'),
    'iBE-5128-253_V1': ('5128_C05', 'Visit3'),
    'iBE-5128-251_V2': ('5128_C05', 'Visit4'),
    'iBE-5128-261_V1': ('5128_C06', 'Visit1'),
    'iBE-5128-262_V1': ('5128_C06', 'Visit2'),
    'iBE-5128-263_V1': ('5128_C06', 'Visit3'),
    'iBE-5128-264_V1': ('5128_C06', 'Visit4'),
    'iBE-5128-271_V1': ('5128_C07', 'Visit1'),
    'iBE-5128-281_V1': ('5128_C08', 'Visit1'),
    'iBE-5128-282_V1': ('5128_C08', 'Visit2'),
    'iBE-5128-283_V1': ('5128_C08', 'Visit3'),
    'iBE-5128-281_V2': ('5128_C08', 'Visit4'),
    'iBE-5128-291_V1': ('5128_C09', 'Visit1'),
    'iBE-5128-292_V1': ('5128_C09', 'Visit2'),
    'iBE-5128-293_V1': ('5128_C09', 'Visit3'),
    'iBE-5128-294_V1': ('5128_C09', 'Visit4'),
    'iBE-5128-301_V1': ('5128_C10', 'Visit1'),
    'iBE-5128-301_V2': ('5128_C10', 'Visit2'),
    'iBE-5128-301_V3': ('5128_C10', 'Visit3'),
    'iBE-5128-301_V4': ('5128_C10', 'Visit4'),

    # Turku GE setup
    'subject_1': ('5128_C11', 'Visit1'),
    
}

study_desc = {

    # Bari volunteers
    'bari_volunteer1_20201222': 'Visit1',
    'bari_volunteer1_20210109': 'Visit2',
    'bari_volunteer1_20210123': 'Visit3',
    'bari_volunteer1_20210130': 'Visit4',
}