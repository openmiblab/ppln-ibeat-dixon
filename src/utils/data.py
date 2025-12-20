"""Functions to read and write data in src/data"""

import os
import csv



def dixon_record(src):
    record = os.path.join(src, 'data', 'dixon_data.csv')
    with open(record, 'r') as file:
        reader = csv.reader(file)
        record = [row for row in reader]
    return record


def dixon_series_desc(record, patient, study):
    for row in record:
        if row[1] == patient:
            if row[2]==study:
                return row[5]
    raise ValueError(
        f'Patient {patient}, study {study}: not found in src/data/dixon_data.csv'
    )

def dixon_reference_sequences(src):
    record = os.path.join(src, 'data', 'dixon_data.csv')
    with open(record, 'r') as file:
        reader = csv.reader(file)
        sequences = [
            {'Patient': row[1], 'Study': row[2], 'Sequence': row[5]} 
            for row in reader if row[0] != 'Site'
        ]
    return sequences
