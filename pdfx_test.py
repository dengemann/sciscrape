# Imports
import os
import operator

# Project imports
import sciparse

def read_tables_csv(csv_name):
    
    csv_tables = []
    table = sciparse.Table(None)
    csv_lines = open(csv_name).read().split('\r')

    for csv_line in csv_lines:
        csv_line = csv_line.strip()
        if csv_line != ',,':
            line_split = csv_line.split(',')
            table.add_coord(*line_split)
        else:
            csv_tables.append(table)
            table = sciparse.Table(None)
    if len(table.coords):
        csv_tables.append(table)

    return csv_tables

def compare_table_groups(tref, tcmp):
    
    tref_coords = reduce(operator.add, [t.coords for t in tref])
    tcmp_coords = reduce(operator.add, [t.coords for t in tcmp])

    tref_coords = list(set(tref_coords))
    tcmp_coords = list(set(tcmp_coords))
    
    n_coords = float(len(tref_coords))

    tp = len([t for t in tref_coords if t in tcmp_coords]) / n_coords
    fp = len([t for t in tcmp_coords if t not in tref_coords]) / n_coords
    fn = len([t for t in tref_coords if t not in tcmp_coords]) / n_coords

    return {
        'tp' : tp,
        'fp' : fp,
        'fn' : fn,
    }

pdf_dir = '/Users/jmcarp/Desktop/pdf-parse-sample'
journal = 'jocn'

docs = [
    '10.1162__jocn_a_00094',
    '10.1162__jocn.2007.19.12.1950',
    '10.1162__jocn.2007.19.12.1983',
    '10.1162__jocn.2007.19.12.2035',
    '10.1162__jocn.2008.20044',
    '10.1162__jocn.2008.20053',
    '10.1162__jocn.2008.20055',
    '10.1162__jocn.2009.21274',
    '10.1162__jocn.2009.21287',
]

def run_cmps():
    
    cmps = []

    for doc in docs:

        doc_full = os.path.join(pdf_dir, journal, doc)
        
        pdf_name = '%s.pdf' % (doc_full)
        csv_name = '%s.csv' % (doc_full)

        with open(pdf_name, 'rb') as pdf:
            pdf_tables = sciparse.TableParse().parse(pdf)
        csv_tables = read_tables_csv(csv_name)

        cmps.append(compare_table_groups(csv_tables, pdf_tables))
        
    return cmps
