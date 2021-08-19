#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Application of Exchangeability Test to 1000 Genomes Data

Created on Fri Aug 6 21:30:17 2021

@author: Alan Aw
"""
# Load libraries
import argparse
import os
from datetime import datetime
import gc
import flintypy
from scipy.spatial.distance import pdist
from bed_reader import open_bed

# Arguments pick up the variables passed from command line
# ARG1 = directory to plink input files
# ARG2 = directory to plink
# ARG3 = number of permutations
# Ex:

# Create parser to parse user-provided arguments
parser = argparse.ArgumentParser()
req_grp = parser.add_argument_group(title="Required arguments")
req_grp.add_argument("--input", "-i", dest="input", help="PLINK input files",
                     type=str, required=True)
req_grp.add_argument("--plink", "-p", dest="plink", help="PLINK location",
                     type=str, required=True)
req_grp.add_argument("--num_perms", "-n", dest="num_perms", help="Number of permutations",
                     type=int, required=True)
args = parser.parse_args()

# Define fixed variables
INPUT_FILE_DIR = args.input
PLINK_DIR = args.plink
NUM_PERMS = args.num_perms

# For each chromosome
print(f"{datetime.now()}: Generating distance matrices for each chromosome...")
dist_list = []
for b in range(1,23):
    print(f"Computing pairwise distances for Chr{b}")
    start = datetime.now()
    # Use PLINK to filter genos to that chrom only
    os.system(PLINK_DIR + " --bfile " + INPUT_FILE_DIR +
              " --chr " + str(b) + " --make-bed --out " +
              INPUT_FILE_DIR + "_" + str(b))

    # Load PLINK file using pybedtools
    bed_file = open_bed(INPUT_FILE_DIR + "_" + str(b) + ".bed")

    # Compute pairwise distances
    pairwise_dists = pdist(bed_file.read(), 'cityblock')

    # Append to dist_list
    dist_list.append(pairwise_dists)

    # Force clear garbage
    gc.collect()

    # Print time elapsed
    print(f"Time elapsed: {(datetime.now() - start).seconds} sec")

# Remove all intermediate files generated (ex: chr-specific bed files and their logs)
print(f"{datetime.now()}: Removing all intermediate files generated...")
os.system("rm -f " + INPUT_FILE_DIR + "_*")

# Compute exchangeability test p-value using 1000 permutations
print(f"{datetime.now()}: Computing exchangeability test p-value...")
start = datetime.now()
p_value = flintypy.v_stat.dist_data_p_value(dist_list, num_perms=NUM_PERMS)
print(f"Exchangeability p-value: {p_value}")
print(f"Time elapsed: {(datetime.now() - start).microseconds} microsec, \
      or {(datetime.now() - start).seconds} sec")
