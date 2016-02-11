#!/usr/bin/env sh

echo "\nTest 1: Calculate log kw and S from the LSS theory\n"
# Calculate Log Kw and S parameters
python ../bin/lssgen.py test_caculation_lss_parameter.txt output_test_lss_parameter.txt

echo "\nTest 2: Build and plot a simple chromatogram from retention times\n"
# Build a simple chromatogram
python ../bin/MakeCromatogram.py testchromatogram.txt 25 0.02 output_testchromatogram.txt


echo "Done!"

