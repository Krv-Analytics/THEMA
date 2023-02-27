#!/usr/bin/env bash
# CURVATURE ANALYSIS
    #TODO: automate paths. For now run from same directory as the python file ./scripts/curvature.sh to execute

#TODO (Sid): Set these ranges as you like
K_VALS=(2 3 4 5 6 7 8 9 10)
N_CUBES=(2 3 4 5 6 7 8 9 10)
PERC_OVERLAP=(0.2 0.3 0.4 0.5)
MIN_INTERSECTION=(1 2 3) 

#TODO(Sid): Configure Data Load
    #Added stub here for reference
DATA=../notebooks/coal_mapper.txt

for K_VAL in "${K_VALS[@]}"; do
    for N in "${N_CUBES[@]}"; do
        for P in "${PERC_OVERLAP[@]}"; do
echo "Running curvature analysis on Mapper graphs generated from K = $K_VAL clusters and a cover with $N cubes that overlap by $P %."
    poetry run python curvature_analysis.py --data ${DATA}                                     \
                                    -n ${N}                                                    \
                                    -p ${P}                                                    \
                                    -K ${K_VAL}                                                \
                                    --min_intersection ${MIN_INTERSECTION[@]}                        \
                                   #Using Default min_intersection for now
        done
    done
done

exit 0