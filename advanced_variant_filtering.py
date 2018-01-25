
##########################################################################################
# UCSF
# Costello Lab
# Run Advanced Variant Filtering protocol as developed for the Costello Lab
# Author: srhilz
# Version: v1 (2018.01.24)

# Input:
#   1. mutfile - *R.mutations file containing processed variant calls for patient
# Output:
#   1. (not returned) mutavffile - *R.mutations.avf file updated with flags and decisions
# Usage:
#   advanced_variant_filtering.py *.R.mutations
#
##########################################################################################

import sys
sys.path.append("/Users/srhilz/Documents/Professional/Positions/UCSF_Costello/Tools/Scripts")
import mutavf_init
import get_repeat_loci
import get_dac_blacklist_loci
import flag_mutavf_by_loci
import decide_mutavf

# Part 0: File paths and
mutfile = sys.argv[1]
mutavffile = mutfile.replace('.mutations','.mutations.avf')
repeat_masker_file = 'UCSC_RepeatMasker_rmsk_hg19.bed.gz'
dac_blacklist_file = 'ENCFF001TDO.bed.gz'

# Part 1: Initializes by setting up a mutation avftated file with placeholder columns
mutavf_init.mutavf_init(mutfile)

# Part 2a: IDs loci in repeat regions
rep_chromosomes, rep_starts, rep_ends, rep_flags = get_repeat_loci.get_repeat_loci(repeat_masker_file)

# Part 2b: Update mutavf file with flags for repeats
flag_mutavf_by_loci.flag_mutavf_by_loci(mutavffile, 'MuTect,Pindel', rep_chromosomes, rep_starts, rep_ends, rep_flags)

# Part 3: IDs loci in ENCODE DAC blacklisted regions
dac_chromosomes, dac_starts, dac_ends, dac_flags = get_dac_blacklist_loci.get_dac_blacklist_loci(dac_blacklist_file)

# Part 3b: Update mutavf file with flags for ENCODE DAC blacklisted regions
flag_mutavf_by_loci.flag_mutavf_by_loci(mutavffile, 'MuTect,Pindel', dac_chromosomes, dac_starts, dac_ends, dac_flags)

# Part N: Make final decisions to retain or discard each variant based on flags
decide_mutavf.decide_mutavf(mutavffile)