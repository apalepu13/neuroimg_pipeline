import argparse
import os
import sys
import pandas as pd
import numpy as np
import nibabel as nb



def read_wm_stats(wm_stats_file):
    wm_df = pd.read_csv(wm_stats_file, delim_whitespace=True)

def read_subcort_stats(subcort_stats_file):
    pass

def read_cort_stats(lh_cortical_stats_file, rh_cortical_stats_file):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('lh_atlas_stats', help="The stats file produced for this atlas.")
    parser.add_argument('rh_atlas_stats', help="The stats file produced for this atlas.")
    parser.add_argument('wm_stats', help="The stats file produced for the white matter detected.")

    parser.add_argument('fsl_lut', help="Brain parcellation look up table to map the correct labels.")
    parser.add_argument('outdir', help="Output data directory to save results.")
    args = parser.parse_args()

    # extract arguments from parser
    lh_atlas_stats_file = args.lh_atlas_stats
    rh_atlas_stats_file = args.rh_atlas_stats
    wm_stats_file = args.wm_stats

    lutfile = args.fsl_lut
    outdir = args.outdir

    # perform registration
