# exomeAdvancedVariantFiltering
A post-mutation calling pipeline for additional variant filtering.

To use, clone repository to the desired directory, then run with:

   `python advanced_variant_filtering.py mutfile`
   
   
### Details on input and output:

#### Input:
   1. mutfile - *R.mutations file containing processed variant calls for patient
   2. (not directly input with run command but required in same directory as mutfile) quality stats file - *.qualitystats.txt file generated by the running my exomeQualityPlots; see start of advanced_variant_filtering.py for more info on how it is used
   
#### Output:
   1. (not returned) mutavffile - *R.mutations.avf file updated with flags and decisions
   
