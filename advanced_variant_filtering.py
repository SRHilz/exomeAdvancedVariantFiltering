
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
import get_whitelist_loci
import get_lowqual_loci

# Part 0: File paths - will have to be edited once moved onto server
mutfile = sys.argv[1]
mutavffile = mutfile.replace('.mutations','.mutations.avf')
hotspot_file = 'hotspot-list-union-v1-v2.txt'
repeat_masker_file = 'UCSC_RepeatMasker_rmsk_hg19.bed.gz'
dac_blacklist_file = 'ENCFF001TDO.bed.gz'
qualitystats_file = mutfile.replace('.R.mutations','.qualitystats.txt')

# Part 1: Initialize by setting up a mutation avftated file with placeholder columns
mutavf_init.mutavf_init(mutfile)

# Part 2: ID loci in whitelist
white_chromosomes, white_starts, white_ends, white_flags = get_whitelist_loci.get_whitelist_loci(hotspot_file)

# Part 2b: Update mutavf file with flags for whitelist regions
flag_mutavf_by_loci.flag_mutavf_by_loci(mutavffile, 'MuTect,Pindel', white_chromosomes, white_starts, white_ends, white_flags)

# Part 3a: ID loci in repeat regions
rep_chromosomes, rep_starts, rep_ends, rep_flags = get_repeat_loci.get_repeat_loci(repeat_masker_file)

# Part 3b: Update mutavf file with flags for repeats
flag_mutavf_by_loci.flag_mutavf_by_loci(mutavffile, 'MuTect,Pindel', rep_chromosomes, rep_starts, rep_ends, rep_flags)

# Part 4: ID loci in ENCODE DAC blacklisted regions
dac_chromosomes, dac_starts, dac_ends, dac_flags = get_dac_blacklist_loci.get_dac_blacklist_loci(dac_blacklist_file)

# Part 4b: Update mutavf file with flags for ENCODE DAC blacklisted regions
flag_mutavf_by_loci.flag_mutavf_by_loci(mutavffile, 'MuTect,Pindel', dac_chromosomes, dac_starts, dac_ends, dac_flags)

# Part 5: ID low quality loci
low_chromosomes, low_starts, low_ends, low_flags = get_lowqual_loci.get_lowqual_loci(qualitystats_file)

# Part 5b: Update mutavf file with flags for ENCODE DAC blacklisted regions
flag_mutavf_by_loci.flag_mutavf_by_loci(mutavffile, 'MuTect', low_chromosomes, low_starts, low_ends, low_flags)

# Part N: Make final decisions to retain or discard each variant based on flags
decide_mutavf.decide_mutavf(mutavffile)
